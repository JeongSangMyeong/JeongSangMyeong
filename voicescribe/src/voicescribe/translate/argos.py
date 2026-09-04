"""Argos Translate 기반 번역기 — 완전 무료·오프라인.

한 번 언어팩을 내려받으면 인터넷 없이 동작한다. 품질은 상용 번역기보다는
떨어지지만 회의록 요약 용도로는 충분하고, 라이선스 제약이 없다(MIT).
"""

from __future__ import annotations

from collections.abc import Sequence

from .base import Translator, TranslatorNotAvailableError


class ArgosTranslator(Translator):
    """argostranslate 래퍼."""

    name = "argos"
    description = "무료·오프라인 번역(언어팩 최초 1회 다운로드). 상업적 이용 제약 없음."
    needs_download = True

    def __init__(self) -> None:
        self._installed_pairs: set[tuple[str, str]] = set()
        self._index_updated = False

    def is_available(self) -> bool:
        try:
            import argostranslate.translate  # noqa: F401
        except ImportError:
            return False
        return True

    def install_hint(self) -> str:
        return (
            "설치 방법:\n"
            '  pip install "voicescribe[translate]"\n'
            "  (또는 직접: pip install argostranslate)"
        )

    def _ensure_pair(self, source: str, target: str) -> None:
        """해당 언어쌍 패키지를 설치한다(이미 있으면 그냥 통과)."""
        import argostranslate.package
        import argostranslate.translate

        if (source, target) in self._installed_pairs:
            return

        installed = {
            (lang.code, dest.code)
            for lang in argostranslate.translate.get_installed_languages()
            for dest in lang.translations_from_this_language()
            if hasattr(dest, "code")
        }
        # 구버전 API 호환: 설치된 언어 코드만으로 확인한다.
        codes = {lang.code for lang in argostranslate.translate.get_installed_languages()}
        if (source, target) in installed or {source, target} <= codes:
            self._installed_pairs.add((source, target))
            return

        if not self._index_updated:
            argostranslate.package.update_package_index()
            self._index_updated = True

        available = argostranslate.package.get_available_packages()
        match = next(
            (p for p in available if p.from_code == source and p.to_code == target), None
        )
        if match is None:
            raise TranslatorNotAvailableError(
                f"Argos 에 '{source} → {target}' 언어팩이 없습니다.\n"
                "영어를 경유하는 방법을 쓰거나 다른 번역기(--translator hf)를 사용하세요."
            )
        argostranslate.package.install_from_path(match.download())
        self._installed_pairs.add((source, target))

    def translate_batch(self, texts: Sequence[str], source: str, target: str) -> list[str]:
        self.ensure_available()
        import argostranslate.translate

        if source == target:
            return list(texts)
        self._ensure_pair(source, target)
        out: list[str] = []
        for text in texts:
            stripped = text.strip()
            out.append("" if not stripped else argostranslate.translate.translate(stripped, source, target))
        return out
