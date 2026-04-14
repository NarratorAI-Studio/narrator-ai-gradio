"""Tests for static data integrity."""

from __future__ import annotations

from data import (
    BGM_LIST,
    DUBBING_LANGUAGES,
    DUBBING_LIST,
    NARRATION_STYLES,
    STYLE_GENRES,
    TASK_ENDPOINTS,
)


class TestListCounts:
    def test_bgm_list_count(self) -> None:
        assert len(BGM_LIST) == 30

    def test_dubbing_list_count(self) -> None:
        assert len(DUBBING_LIST) == 35

    def test_narration_styles_count(self) -> None:
        assert len(NARRATION_STYLES) == 90

    def test_style_genres_count(self) -> None:
        assert len(STYLE_GENRES) == 12

    def test_dubbing_languages_count(self) -> None:
        assert len(DUBBING_LANGUAGES) == 11

    def test_task_endpoints_count(self) -> None:
        assert len(TASK_ENDPOINTS) == 9


class TestNoDuplicateIds:
    def test_bgm_no_duplicate_ids(self) -> None:
        ids = [b["id"] for b in BGM_LIST]
        assert len(ids) == len(set(ids))

    def test_dubbing_no_duplicate_ids(self) -> None:
        ids = [d["id"] for d in DUBBING_LIST]
        assert len(ids) == len(set(ids))

    def test_narration_styles_no_duplicate_ids(self) -> None:
        ids = [s["id"] for s in NARRATION_STYLES]
        assert len(ids) == len(set(ids))


class TestItemKeys:
    def test_bgm_items_have_required_keys(self) -> None:
        for item in BGM_LIST:
            assert "name" in item
            assert "id" in item

    def test_dubbing_items_have_required_keys(self) -> None:
        for item in DUBBING_LIST:
            assert "name" in item
            assert "id" in item
            assert "type" in item
            assert "tag" in item

    def test_narration_styles_have_required_keys(self) -> None:
        for item in NARRATION_STYLES:
            assert "genre" in item
            assert "name" in item
            assert "id" in item

    def test_task_endpoints_values_start_with_v2(self) -> None:
        for value in TASK_ENDPOINTS.values():
            assert value.startswith("/v2/")
