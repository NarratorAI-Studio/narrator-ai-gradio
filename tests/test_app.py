"""Tests for the Gradio application module."""

from __future__ import annotations

import pytest


class TestAppImport:
    def test_module_imports_without_error(self) -> None:
        import app  # noqa: F401


class TestTranslation:
    def test_t_returns_chinese_by_default(self) -> None:
        from app import t

        result = t("api_key_label")
        assert result == "API \u5bc6\u94a5"

    def test_t_with_kwargs_substitution(self) -> None:
        from app import t

        result = t("step1", movie="Test Movie")
        assert "Test Movie" in result


class TestHelpers:
    def test_find_voice_id_known(self) -> None:
        from app import find_voice_id

        voice_id, voice_type = find_voice_id("蜡笔小新")
        assert voice_id == "MiniMaxVoiceId14640"
        assert voice_type == "普通话"

    def test_find_bgm_id_known(self) -> None:
        from app import find_bgm_id

        bgm_id = find_bgm_id("River Flows in You")
        assert bgm_id == "065b0fbb-16f3-4b5e-a326-e05279eb7fc3"

    def test_find_style_id_known(self) -> None:
        from app import find_style_id

        style_id = find_style_id("热血动作-困兽之斗解说 (热血动作)")
        assert style_id == "narrator-20250916152104-DYsban"

    def test_filter_voices_empty_language(self) -> None:
        from app import filter_voices
        from data import DUBBING_LIST

        result = filter_voices("")
        # gr.update returns a dict with 'choices' key
        assert len(result["choices"]) == len(DUBBING_LIST)

    def test_filter_styles_empty_genre(self) -> None:
        from app import filter_styles
        from data import NARRATION_STYLES

        result = filter_styles("")
        assert len(result["choices"]) == len(NARRATION_STYLES)


class TestGetClient:
    def test_raises_on_empty_key(self) -> None:
        import gradio as gr

        from app import get_client

        with pytest.raises(gr.Error):
            get_client("")

    def test_raises_on_whitespace_key(self) -> None:
        import gradio as gr

        from app import get_client

        with pytest.raises(gr.Error):
            get_client("   ")


class TestLangDicts:
    def test_zh_and_en_have_same_keys(self) -> None:
        from app import LANG_EN, LANG_ZH

        assert set(LANG_ZH.keys()) == set(LANG_EN.keys())
