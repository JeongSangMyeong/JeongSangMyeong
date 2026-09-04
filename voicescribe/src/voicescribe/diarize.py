"""화자 분리(누가 언제 말했는지).

두 가지 방법을 지원한다.

1. **pyannote.audio** — 정확하지만 Hugging Face 무료 토큰이 필요하고,
   모델 페이지에서 이용약관에 동의해야 한다. 설치·설정이 번거롭다.
2. **간이 방식(기본값)** — 추가 설치·다운로드 없이 numpy 만으로 동작한다.
   각 발화 구간에서 MFCC 특징을 뽑아 목소리가 비슷한 구간끼리 묶는다.
   정확도는 pyannote 보다 떨어지지만 "2~3명이 번갈아 말하는 회의록" 정도는 잘 나눈다.

정확도가 중요하면 pyannote 를, 바로 쓰고 싶으면 간이 방식을 쓰면 된다.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np

    from .audio import AudioBuffer
    from .types import TranscriptionResult

#: 화자 수를 자동으로 정할 때 시도할 최대 인원.
_DEFAULT_MAX_SPEAKERS = 6
#: 특징 추출 설정.
_FRAME_LENGTH = 0.025  # 25ms
_FRAME_HOP = 0.010  # 10ms
_N_MELS = 26
_N_MFCC = 13


class DiarizationError(RuntimeError):
    """화자 분리에 실패했을 때."""


# --------------------------------------------------------------------------- #
# 특징 추출 (numpy 만 사용)
# --------------------------------------------------------------------------- #


def _hz_to_mel(hz: np.ndarray | float) -> np.ndarray | float:
    import numpy as np

    return 2595.0 * np.log10(1.0 + np.asarray(hz) / 700.0)


def _mel_to_hz(mel: np.ndarray | float) -> np.ndarray | float:
    import numpy as np

    return 700.0 * (10.0 ** (np.asarray(mel) / 2595.0) - 1.0)


def _mel_filterbank(n_filters: int, n_fft: int, sample_rate: int) -> np.ndarray:
    """삼각형 멜 필터뱅크를 만든다."""
    import numpy as np

    low_mel = _hz_to_mel(0.0)
    high_mel = _hz_to_mel(sample_rate / 2.0)
    mel_points = np.linspace(low_mel, high_mel, n_filters + 2)
    hz_points = _mel_to_hz(mel_points)
    bins = np.floor((n_fft + 1) * hz_points / sample_rate).astype(int)
    bins = np.clip(bins, 0, n_fft // 2)

    fbank = np.zeros((n_filters, n_fft // 2 + 1), dtype=np.float32)
    for i in range(1, n_filters + 1):
        left, center, right = bins[i - 1], bins[i], bins[i + 1]
        if center == left:
            center = min(left + 1, n_fft // 2)
        if right == center:
            right = min(center + 1, n_fft // 2)
        for k in range(left, center):
            fbank[i - 1, k] = (k - left) / max(1, center - left)
        for k in range(center, right):
            fbank[i - 1, k] = (right - k) / max(1, right - center)
    return fbank


def _mfcc(samples: np.ndarray, sample_rate: int) -> np.ndarray:
    """MFCC 특징을 (프레임 수, _N_MFCC) 모양으로 계산한다."""
    import numpy as np

    frame_len = max(1, int(sample_rate * _FRAME_LENGTH))
    hop = max(1, int(sample_rate * _FRAME_HOP))
    if samples.size < frame_len:
        samples = np.pad(samples, (0, frame_len - samples.size))

    n_frames = 1 + (samples.size - frame_len) // hop
    if n_frames <= 0:
        return np.zeros((1, _N_MFCC), dtype=np.float32)

    indices = np.arange(frame_len)[None, :] + hop * np.arange(n_frames)[:, None]
    frames = samples[indices] * np.hamming(frame_len).astype(np.float32)

    n_fft = 1
    while n_fft < frame_len:
        n_fft *= 2
    spectrum = np.abs(np.fft.rfft(frames, n=n_fft)) ** 2 / n_fft

    fbank = _mel_filterbank(_N_MELS, n_fft, sample_rate)
    mel_energy = np.maximum(spectrum @ fbank.T, 1e-10)
    log_mel = np.log(mel_energy)

    # DCT-II 로 MFCC 를 만든다(scipy 없이 직접 계산).
    n = np.arange(_N_MELS)
    k = np.arange(_N_MFCC)[:, None]
    dct_matrix = np.cos(np.pi * k * (2 * n + 1) / (2 * _N_MELS)).astype(np.float32)
    return (log_mel @ dct_matrix.T).astype(np.float32)


def _segment_embedding(samples: np.ndarray, sample_rate: int) -> np.ndarray:
    """한 발화 구간을 고정 길이 벡터로 요약한다(평균 + 표준편차)."""
    import numpy as np

    mfcc = _mfcc(samples, sample_rate)
    embedding = np.concatenate([mfcc.mean(axis=0), mfcc.std(axis=0)])
    norm = float(np.linalg.norm(embedding))
    return embedding / norm if norm > 0 else embedding


# --------------------------------------------------------------------------- #
# 군집화
# --------------------------------------------------------------------------- #


def _cosine_distance_matrix(embeddings: np.ndarray) -> np.ndarray:
    import numpy as np

    similarity = embeddings @ embeddings.T
    return np.clip(1.0 - similarity, 0.0, 2.0)


def _agglomerative(distances: np.ndarray, n_clusters: int) -> list[int]:
    """평균 연결(average linkage) 병합 군집화. 라벨 리스트를 돌려준다."""
    import numpy as np

    n = distances.shape[0]
    clusters: list[list[int]] = [[i] for i in range(n)]
    while len(clusters) > max(1, n_clusters):
        best = (float("inf"), 0, 1)
        for a in range(len(clusters)):
            for b in range(a + 1, len(clusters)):
                block = distances[np.ix_(clusters[a], clusters[b])]
                dist = float(block.mean())
                if dist < best[0]:
                    best = (dist, a, b)
        _, a, b = best
        clusters[a] = clusters[a] + clusters[b]
        clusters.pop(b)

    labels = [0] * n
    for label, members in enumerate(clusters):
        for idx in members:
            labels[idx] = label
    return labels


def _silhouette(distances: np.ndarray, labels: list[int]) -> float:
    """군집 품질 점수(-1~1, 클수록 좋음). 화자 수를 자동으로 고를 때 쓴다."""
    import numpy as np

    unique = sorted(set(labels))
    if len(unique) < 2 or len(labels) <= len(unique):
        return -1.0

    label_array = np.array(labels)
    scores: list[float] = []
    for i in range(len(labels)):
        same = (label_array == label_array[i]) & (np.arange(len(labels)) != i)
        if not same.any():
            continue
        a = float(distances[i, same].mean())
        b = min(
            float(distances[i, label_array == other].mean())
            for other in unique
            if other != label_array[i]
        )
        denominator = max(a, b)
        if denominator > 0:
            scores.append((b - a) / denominator)
    return float(np.mean(scores)) if scores else -1.0


# --------------------------------------------------------------------------- #
# 공개 API
# --------------------------------------------------------------------------- #


def diarize_simple(
    audio: AudioBuffer,
    result: TranscriptionResult,
    *,
    min_speakers: int | None = None,
    max_speakers: int | None = None,
) -> list[str]:
    """추가 설치 없이 동작하는 간이 화자 분리. 구간별 화자 라벨을 돌려준다."""
    import numpy as np

    segments = result.segments
    if len(segments) < 2:
        return ["화자1"] * len(segments)

    rate = audio.sample_rate
    embeddings = []
    for seg in segments:
        start = max(0, int(seg.start * rate))
        end = min(len(audio.samples), int(seg.end * rate))
        chunk = audio.samples[start:end]
        if chunk.size < int(0.1 * rate):  # 0.1초 미만은 특징이 불안정하다.
            chunk = np.pad(chunk, (0, max(0, int(0.1 * rate) - chunk.size)))
        embeddings.append(_segment_embedding(chunk, rate))

    matrix = np.vstack(embeddings)
    distances = _cosine_distance_matrix(matrix)

    lower = max(1, min_speakers or 1)
    upper = min(max_speakers or _DEFAULT_MAX_SPEAKERS, len(segments))
    if min_speakers and max_speakers and min_speakers == max_speakers:
        best_labels = _agglomerative(distances, min_speakers)
    else:
        # k 후보별 점수를 모두 구한 뒤, 점수가 비슷하면 '사람이 더 적은 쪽'을 고른다.
        # (실루엣 점수만 보면 같은 사람을 둘로 쪼개는 경향이 있다.)
        scored: list[tuple[int, float, list[int]]] = []
        for k in range(max(2, lower), max(2, upper) + 1):
            labels = _agglomerative(distances, k)
            scored.append((k, _silhouette(distances, labels), labels))

        if not scored:
            best_labels = [0] * len(segments)
        else:
            best_score = max(score for _, score, _ in scored)
            # 최고점의 92% 이상(또는 0.03 이내)이면 동급으로 보고 가장 적은 화자 수를 택한다.
            threshold = min(best_score * 0.92, best_score - 0.03) if best_score > 0 else best_score
            eligible = [item for item in scored if item[1] >= threshold]
            best_labels = min(eligible, key=lambda item: item[0])[2]
            # 군집이 뚜렷하지 않으면 전부 한 사람으로 본다.
            if best_score < 0.05 and not min_speakers:
                best_labels = [0] * len(segments)

    # 처음 말한 사람이 화자1 이 되도록 번호를 다시 매긴다.
    order: dict[int, int] = {}
    for label in best_labels:
        if label not in order:
            order[label] = len(order) + 1
    return [f"화자{order[label]}" for label in best_labels]


def diarize_pyannote(
    audio: AudioBuffer,
    result: TranscriptionResult,
    *,
    min_speakers: int | None = None,
    max_speakers: int | None = None,
    token: str | None = None,
) -> list[str]:
    """pyannote.audio 로 정확한 화자 분리를 수행한다.

    Hugging Face 무료 토큰(``HF_TOKEN`` 환경변수)과 모델 약관 동의가 필요하다.
    """
    try:
        import torch
        from pyannote.audio import Pipeline
    except ImportError as exc:
        raise DiarizationError(
            "pyannote.audio 가 설치되지 않았습니다.\n"
            '설치: pip install "voicescribe[diarize]"\n'
            "그리고 https://huggingface.co/pyannote/speaker-diarization-3.1 에서 약관에 동의한 뒤\n"
            "HF_TOKEN 환경변수에 무료 토큰을 넣어 주세요."
        ) from exc

    hf_token = token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if not hf_token:
        raise DiarizationError(
            "HF_TOKEN 환경변수가 없습니다. huggingface.co 에서 무료 토큰을 만들어 설정하세요."
        )

    try:
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=hf_token)
    except Exception as exc:
        raise DiarizationError(f"pyannote 모델을 불러오지 못했습니다: {exc}") from exc

    waveform = torch.from_numpy(audio.samples).unsqueeze(0)
    kwargs: dict[str, int] = {}
    if min_speakers:
        kwargs["min_speakers"] = min_speakers
    if max_speakers:
        kwargs["max_speakers"] = max_speakers
    annotation = pipeline({"waveform": waveform, "sample_rate": audio.sample_rate}, **kwargs)

    # 각 받아쓰기 구간과 가장 많이 겹치는 화자를 고른다.
    turns = [(turn.start, turn.end, speaker) for turn, _, speaker in annotation.itertracks(yield_label=True)]
    mapping: dict[str, str] = {}
    labels: list[str] = []
    for seg in result.segments:
        overlaps: dict[str, float] = {}
        for start, end, speaker in turns:
            overlap = min(seg.end, end) - max(seg.start, start)
            if overlap > 0:
                overlaps[speaker] = overlaps.get(speaker, 0.0) + overlap
        raw = max(overlaps, key=overlaps.get) if overlaps else "SPEAKER_00"  # type: ignore[arg-type]
        if raw not in mapping:
            mapping[raw] = f"화자{len(mapping) + 1}"
        labels.append(mapping[raw])
    return labels


def apply_diarization(
    audio: AudioBuffer,
    result: TranscriptionResult,
    *,
    method: str = "auto",
    min_speakers: int | None = None,
    max_speakers: int | None = None,
) -> TranscriptionResult:
    """화자 라벨을 결과에 채워 넣는다(제자리 수정).

    Args:
        method: ``"auto"``(pyannote 가 있으면 그것을, 없으면 간이 방식),
            ``"pyannote"``, ``"simple"`` 중 하나.
    """
    labels: list[str]
    if method in ("auto", "pyannote"):
        try:
            labels = diarize_pyannote(
                audio, result, min_speakers=min_speakers, max_speakers=max_speakers
            )
        except DiarizationError:
            if method == "pyannote":
                raise
            labels = diarize_simple(
                audio, result, min_speakers=min_speakers, max_speakers=max_speakers
            )
    else:
        labels = diarize_simple(audio, result, min_speakers=min_speakers, max_speakers=max_speakers)

    for seg, label in zip(result.segments, labels, strict=False):
        seg.speaker = label
    result.speakers = sorted(set(labels), key=lambda s: (len(s), s))
    return result
