"""Narrator AI — Gradio Web UI (bilingual: Chinese / English)."""

from __future__ import annotations

import json
import time
from collections.abc import Generator
from typing import Any

import gradio as gr

from client import NarratorAPIError, NarratorClient
from data import (
    BGM_LIST,
    DUBBING_LANGUAGES,
    DUBBING_LIST,
    NARRATION_STYLES,
    STYLE_GENRES,
    TASK_ENDPOINTS,
)

# ---------------------------------------------------------------------------
# i18n
# ---------------------------------------------------------------------------

LANG_ZH: dict[str, str] = {
    "title": "# AI 解说大师\nAI 驱动的视频解说生成平台",
    "api_key_label": "API 密钥",
    "api_key_placeholder": "输入你的 Narrator AI API 密钥",
    "api_key_missing": "请先输入 API 密钥。",
    "tab_wizard": "一键生成",
    "tab_tasks": "任务管理",
    "tab_library": "素材库",
    "tab_account": "账户",
    "wizard_desc": "选择电影、解说风格、配音和背景音乐 — 一键生成解说视频。",
    "load_movies": "加载电影列表",
    "movie": "电影",
    "genre_filter": "类型筛选",
    "narration_style": "解说风格",
    "language": "语言",
    "voice": "配音",
    "bgm": "背景音乐",
    "generate": "生成视频",
    "progress": "进度",
    "query_task": "查询任务",
    "task_id": "任务 ID",
    "task_id_placeholder": "输入任务 UUID",
    "query": "查询",
    "result": "结果",
    "list_tasks": "任务列表",
    "page": "页码",
    "limit": "每页数量",
    "list": "查询",
    "create_task": "创建任务（高级）",
    "create_task_desc": "面向高级用户。粘贴完整的 JSON 请求体来创建任意类型的任务。",
    "task_type": "任务类型",
    "request_body": "请求体 (JSON)",
    "stream": "流式输出 (SSE)",
    "create": "创建任务",
    "styles": "解说风格模板",
    "voices": "配音角色",
    "bgm_tracks": "背景音乐",
    "genre": "类型",
    "name": "名称",
    "template_id": "模板 ID",
    "dubbing_id": "配音 ID",
    "tag": "标签",
    "bgm_name": "BGM 名称",
    "bgm_id": "BGM ID",
    "check_balance": "查询余额",
    "account_info": "账户信息",
    "user": "用户",
    "balance": "余额",
    "company": "公司",
    "login": "登录",
    "username": "用户名",
    "password": "密码",
    "login_btn": "登录",
    "login_result": "登录结果",
    "api_keys": "API 密钥列表",
    "list_keys": "查询密钥",
    "key_result": "密钥信息",
    "create_key": "创建密钥",
    "key_remark": "备注",
    "key_quota": "配额",
    "create_key_btn": "创建",
    "create_key_result": "创建结果",
    "files_tab": "文件管理",
    "upload_file": "上传文件",
    "upload_btn": "上传",
    "upload_result": "上传结果",
    "transfer_link": "远程转存",
    "link_url": "链接地址",
    "transfer_btn": "转存",
    "transfer_result": "转存结果",
    "file_list": "文件列表",
    "list_files_btn": "查询文件",
    "file_list_result": "文件列表",
    "download_file": "下载文件",
    "file_id_input": "文件 ID",
    "download_btn": "获取下载链接",
    "download_result": "下载链接",
    "storage": "存储用量",
    "storage_btn": "查询用量",
    "storage_result": "用量信息",
    "search_movie": "搜索电影",
    "search_placeholder": "输入电影名称搜索",
    "search_btn": "搜索",
    "search_result": "搜索结果",
    "or_search": "或搜索未收录的电影：",
    "video_url": "视频下载链接",
    "no_video_url": "视频生成中或暂无下载链接，请稍后用任务 ID 查询。",
    "no_tasks": "未找到任务。",
    "step1": "步骤 1/3：正在为 [{movie}] 生成解说文案...",
    "task_created": "  任务已创建：{task_id}",
    "waiting_script": "  正在等待文案生成...",
    "script_ready": "  文案已完成。file_id: {file_id}",
    "step2": "步骤 2/3：正在生成剪辑数据...",
    "waiting_clip": "  正在等待剪辑数据...",
    "clip_ready": "  剪辑数据已完成。order_num: {order_num}",
    "step3": "步骤 3/3：正在合成视频...",
    "waiting_video": "  正在等待视频...",
    "done": "  完成！",
    "movie_not_found": "未在素材库中找到该电影。",
    "load_first": "请先加载并选择一部电影。",
    "voice_not_found": "未找到配音：{name}",
    "bgm_not_found": "未找到 BGM：{name}",
    "style_not_found": "未找到风格：{name}",
    "task_failed": "任务失败：{status}",
    "task_timeout": "任务超时（{seconds}秒）",
    "prog_script": "正在生成文案...",
    "prog_wait_script": "等待文案...",
    "prog_clip": "正在生成剪辑数据...",
    "prog_wait_clip": "等待剪辑数据...",
    "prog_video": "正在合成视频...",
    "prog_wait_video": "等待视频...",
    "prog_done": "完成！",
    "preview_voice": "试听配音",
    "preview_btn": "试听",
    "lang_switch": "English",
}

LANG_EN: dict[str, str] = {
    "title": "# Narrator AI\nAI-powered video narration generation platform",
    "api_key_label": "API Key",
    "api_key_placeholder": "Enter your Narrator AI API key",
    "api_key_missing": "Please enter your API Key first.",
    "tab_wizard": "One-Click Generate",
    "tab_tasks": "Tasks",
    "tab_library": "Library",
    "tab_account": "Account",
    "wizard_desc": "Select a movie, style, voice, and BGM — one click to generate a narration video.",
    "load_movies": "Load Movies",
    "movie": "Movie",
    "genre_filter": "Genre Filter",
    "narration_style": "Narration Style",
    "language": "Language",
    "voice": "Voice",
    "bgm": "Background Music",
    "generate": "Generate Video",
    "progress": "Progress",
    "query_task": "Query Task",
    "task_id": "Task ID",
    "task_id_placeholder": "Enter task UUID",
    "query": "Query",
    "result": "Result",
    "list_tasks": "List Tasks",
    "page": "Page",
    "limit": "Limit",
    "list": "List",
    "create_task": "Create Task (Advanced)",
    "create_task_desc": "For advanced users. Paste the full JSON body for any task type.",
    "task_type": "Task Type",
    "request_body": "Request Body (JSON)",
    "stream": "Stream (SSE)",
    "create": "Create Task",
    "styles": "Narration Styles",
    "voices": "Voices",
    "bgm_tracks": "BGM Tracks",
    "genre": "Genre",
    "name": "Name",
    "template_id": "Template ID",
    "dubbing_id": "Dubbing ID",
    "tag": "Tag",
    "bgm_name": "BGM Name",
    "bgm_id": "BGM ID",
    "check_balance": "Check Balance",
    "account_info": "Account Info",
    "user": "User",
    "balance": "Balance",
    "company": "Company",
    "login": "Login",
    "username": "Username",
    "password": "Password",
    "login_btn": "Login",
    "login_result": "Login Result",
    "api_keys": "API Keys",
    "list_keys": "List Keys",
    "key_result": "Key Info",
    "create_key": "Create Key",
    "key_remark": "Remark",
    "key_quota": "Quota",
    "create_key_btn": "Create",
    "create_key_result": "Create Result",
    "files_tab": "Files",
    "upload_file": "Upload File",
    "upload_btn": "Upload",
    "upload_result": "Upload Result",
    "transfer_link": "Transfer from Link",
    "link_url": "Link URL",
    "transfer_btn": "Transfer",
    "transfer_result": "Transfer Result",
    "file_list": "File List",
    "list_files_btn": "List Files",
    "file_list_result": "File List",
    "download_file": "Download File",
    "file_id_input": "File ID",
    "download_btn": "Get Download Link",
    "download_result": "Download Link",
    "storage": "Storage",
    "storage_btn": "Check Usage",
    "storage_result": "Storage Info",
    "search_movie": "Search Movie",
    "search_placeholder": "Enter movie name to search",
    "search_btn": "Search",
    "search_result": "Search Results",
    "or_search": "Or search for unlisted movies:",
    "video_url": "Video Download Link",
    "no_video_url": "Video is being generated or not yet available. Query the task ID later.",
    "no_tasks": "No tasks found.",
    "step1": "Step 1/3: Generating narration script for [{movie}]...",
    "task_created": "  Task created: {task_id}",
    "waiting_script": "  Waiting for script generation...",
    "script_ready": "  Script ready. file_id: {file_id}",
    "step2": "Step 2/3: Generating clip/editing data...",
    "waiting_clip": "  Waiting for clip data...",
    "clip_ready": "  Clip data ready. order_num: {order_num}",
    "step3": "Step 3/3: Composing final video...",
    "waiting_video": "  Waiting for video...",
    "done": "  Done!",
    "movie_not_found": "Movie not found in materials.",
    "load_first": "Please load and select a movie first.",
    "voice_not_found": "Voice not found: {name}",
    "bgm_not_found": "BGM not found: {name}",
    "style_not_found": "Style not found: {name}",
    "task_failed": "Task failed: {status}",
    "task_timeout": "Task timed out after {seconds}s",
    "prog_script": "Generating script...",
    "prog_wait_script": "Waiting for script...",
    "prog_clip": "Generating clip data...",
    "prog_wait_clip": "Waiting for clip data...",
    "prog_video": "Composing video...",
    "prog_wait_video": "Waiting for video...",
    "prog_done": "Done!",
    "preview_voice": "Preview Voice",
    "preview_btn": "Preview",
    "lang_switch": "中文",
}

# Current language state — default Chinese
_current_lang: dict[str, str] = LANG_ZH


def t(key: str, **kwargs) -> str:
    return _current_lang.get(key, key).format(**kwargs) if kwargs else _current_lang.get(key, key)


def get_client(app_key: str) -> NarratorClient:
    if not app_key.strip():
        raise gr.Error(t("api_key_missing"))
    return NarratorClient(app_key=app_key.strip())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_materials(app_key: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    client = get_client(app_key)
    try:
        data = client.get("/v2/res/movie-sucai", params={"page": 1, "size": 100})
    except NarratorAPIError as e:
        raise gr.Error(f"API Error [{e.code}]: {e.message}") from e
    except Exception as e:
        raise gr.Error(f"Connection error: {e}") from e
    items = data.get("items", [])
    choices = [f"{m.get('name', '')} ({m.get('title', '')})" for m in items]
    return gr.update(choices=choices), items


def search_movie(app_key: str, query: str) -> str:
    """Search for movies not in the pre-built library."""
    if not query.strip():
        raise gr.Error(t("search_placeholder"))
    client = get_client(app_key)
    data = client.get("/v2/task/commentary/search_media_information", params={"keyword": query.strip()})
    return json.dumps(data, ensure_ascii=False, indent=2)


def extract_video_url(task_result: dict[str, Any]) -> str:
    """Try to extract video download URL from a completed task result."""
    results = task_result.get("results", {})
    # Check common locations for video URLs
    for key in ("video_url", "download_url", "url", "video_oss_url"):
        if key in results and results[key]:
            return str(results[key])
    # Check in tasks array
    tasks = results.get("tasks", [])
    for t_item in tasks:
        for key in ("video_url", "download_url", "url"):
            if key in t_item and t_item[key]:
                return str(t_item[key])
    # Check file_ids
    file_ids = results.get("file_ids", [])
    if file_ids:
        return f"file_id: {file_ids[0]} (use File tab to get download link)"
    return ""


def filter_voices(language: str) -> dict[str, Any]:
    voices = DUBBING_LIST if not language else [d for d in DUBBING_LIST if d["type"] == language]
    return gr.update(choices=[v["name"] for v in voices])


def filter_styles(genre: str) -> dict[str, Any]:
    styles = NARRATION_STYLES if not genre else [s for s in NARRATION_STYLES if s["genre"] == genre]
    return gr.update(choices=[f"{s['name']} ({s['genre']})" for s in styles])


def find_voice_id(voice_name: str) -> tuple[str, str]:
    for v in DUBBING_LIST:
        if v["name"] == voice_name:
            return v["id"], v["type"]
    raise gr.Error(t("voice_not_found", name=voice_name))


def find_bgm_id(bgm_name: str) -> str:
    for b in BGM_LIST:
        if b["name"] == bgm_name:
            return b["id"]
    raise gr.Error(t("bgm_not_found", name=bgm_name))


def find_style_id(style_display: str) -> str:
    for s in NARRATION_STYLES:
        display = f"{s['name']} ({s['genre']})"
        if display == style_display:
            return s["id"]
    raise gr.Error(t("style_not_found", name=style_display))


def poll_task(client: NarratorClient, task_id: str, max_wait: int = 600) -> dict[str, Any]:
    start = time.time()
    while time.time() - start < max_wait:
        result = client.get(f"/v2/task/commentary/query/{task_id}")
        status = result.get("status_code", 0)
        if status == 2:
            return result
        if status in (3, 4):
            raise gr.Error(t("task_failed", status=result.get("status_name", "unknown")))
        time.sleep(5)
    raise gr.Error(t("task_timeout", seconds=max_wait))


# ---------------------------------------------------------------------------
# Tab 1: Wizard
# ---------------------------------------------------------------------------


def wizard_generate(
    app_key: str,
    movie_idx: str,
    materials_state: list[dict[str, Any]],
    style_display: str,
    voice_name: str,
    bgm_name: str,
    progress: Any = gr.Progress(),  # noqa: B008
) -> Generator[str, None, None]:
    client = get_client(app_key)

    if not materials_state or movie_idx is None:
        raise gr.Error(t("load_first"))

    movie = None
    for m in materials_state:
        display = f"{m.get('name', '')} ({m.get('title', '')})"
        if display == movie_idx:
            movie = m
            break
    if not movie:
        raise gr.Error(t("movie_not_found"))

    style_id = find_style_id(style_display)
    dubbing_id, dubbing_type = find_voice_id(voice_name)
    bgm_id = find_bgm_id(bgm_name)

    video_file_id = movie.get("video_file_id", "")
    srt_file_id = movie.get("srt_file_id", "")
    movie_name = movie.get("name", "Unknown")

    log_lines = []

    def log(msg: str) -> str:
        log_lines.append(msg)
        return "\n".join(log_lines)

    # Step 1: fast-writing
    progress(0.1, desc=t("prog_script"))
    yield log(t("step1", movie=movie_name))

    fw_body = {
        "playlet_name": movie_name,
        "target_mode": 1,
        "learning_model_id": style_id,
        "model": "Pro",
        "confirmed_movie_json": movie,
    }
    try:
        fw_result = client.post(TASK_ENDPOINTS["fast-writing"], json=fw_body)
    except NarratorAPIError as e:
        raise gr.Error(f"fast-writing: {e.message}") from e

    fw_task_id = fw_result.get("task_id", "")
    yield log(t("task_created", task_id=fw_task_id))
    yield log(t("waiting_script"))

    progress(0.2, desc=t("prog_wait_script"))
    fw_query = poll_task(client, fw_task_id)
    file_ids = fw_query.get("results", {}).get("file_ids", [])
    if not file_ids:
        raise gr.Error("fast-writing completed but no file_ids returned.")
    fw_file_id = file_ids[0]
    yield log(t("script_ready", file_id=fw_file_id))

    # Step 2: fast-clip-data
    progress(0.4, desc=t("prog_clip"))
    yield log(t("step2"))

    fcd_body = {
        "task_id": fw_task_id,
        "file_id": fw_file_id,
        "bgm": bgm_id,
        "dubbing": dubbing_id,
        "dubbing_type": dubbing_type,
        "episodes_data": [{"video_oss_key": video_file_id, "srt_oss_key": srt_file_id, "num": 1}],
    }
    try:
        fcd_result = client.post(TASK_ENDPOINTS["fast-clip-data"], json=fcd_body)
    except NarratorAPIError as e:
        raise gr.Error(f"fast-clip-data: {e.message}") from e

    fcd_task_id = fcd_result.get("task_id", "")
    yield log(t("task_created", task_id=fcd_task_id))
    yield log(t("waiting_clip"))

    progress(0.5, desc=t("prog_wait_clip"))
    fcd_query = poll_task(client, fcd_task_id)
    fcd_order_num = fcd_query.get("task_order_num", "")
    yield log(t("clip_ready", order_num=fcd_order_num))

    # Step 3: video-composing
    progress(0.7, desc=t("prog_video"))
    yield log(t("step3"))

    vc_body = {
        "order_num": fcd_order_num,
        "bgm": bgm_id,
        "dubbing": dubbing_id,
        "dubbing_type": dubbing_type,
    }
    try:
        vc_result = client.post(TASK_ENDPOINTS["video-composing"], json=vc_body)
    except NarratorAPIError as e:
        raise gr.Error(f"video-composing: {e.message}") from e

    vc_task_id = vc_result.get("task_id", "")
    yield log(t("task_created", task_id=vc_task_id))
    yield log(t("waiting_video"))

    progress(0.8, desc=t("prog_wait_video"))
    vc_query = poll_task(client, vc_task_id, max_wait=900)

    progress(1.0, desc=t("prog_done"))

    # Extract video URL for prominent display
    video_url = extract_video_url(vc_query)
    result_lines = [t("done"), "", f"Task ID: {vc_task_id}"]
    if video_url:
        result_lines.extend(["", f"🎬 {t('video_url')}: {video_url}"])
    else:
        result_lines.extend(["", t("no_video_url")])
    result_lines.extend(["", "--- Raw Result ---", json.dumps(vc_query, ensure_ascii=False, indent=2)])
    yield log("\n".join(result_lines))


# ---------------------------------------------------------------------------
# Tab 2: Task management
# ---------------------------------------------------------------------------


def query_task(app_key: str, task_id: str) -> str:
    client = get_client(app_key)
    result = client.get(f"/v2/task/commentary/query/{task_id}")
    return json.dumps(result, ensure_ascii=False, indent=2)


def list_tasks(app_key: str, page: float, limit: float) -> str:
    client = get_client(app_key)
    result = client.get(
        "/v2/task/commentary/list",
        params={
            "page": int(page),
            "limit": int(limit),
        },
    )
    items = result.get("items", [])
    if not items:
        return t("no_tasks")
    return json.dumps(result, ensure_ascii=False, indent=2)


def create_task_advanced(app_key: str, task_type: str, body_json: str, use_stream: bool) -> Generator[str, None, None]:
    client = get_client(app_key)
    endpoint = TASK_ENDPOINTS.get(task_type)
    if not endpoint:
        raise gr.Error(f"Unknown task type: {task_type}")

    body = json.loads(body_json)

    if use_stream:
        lines = []
        for event_type, data in client.post_sse(endpoint, json=body):
            msg = data.get("message", "")
            pct = data.get("progress", "")
            lines.append(f"[{event_type}] {msg} {f'({pct}%)' if pct else ''}")
            yield "\n".join(lines)
    else:
        result = client.post(endpoint, json=body)
        yield json.dumps(result, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Tab 3: Account
# ---------------------------------------------------------------------------


def check_balance(app_key: str) -> str:
    client = get_client(app_key)
    data = client.get("/v1/users/balance")
    return (
        f"{t('user')}: {data.get('nickname', 'N/A')}\n"
        f"{t('balance')}: {data.get('balance', 'N/A')}\n"
        f"{t('company')}: {data.get('company_name', 'N/A')}"
    )


def user_login(username: str, password: str) -> str:
    if not username.strip() or not password.strip():
        raise gr.Error(t("api_key_missing"))
    client = NarratorClient()
    try:
        data = client.post_no_auth("/v1/users/sign_in", json={"username": username, "password": password})
    except NarratorAPIError as e:
        raise gr.Error(f"Login failed: {e.message}") from e
    return json.dumps(data, ensure_ascii=False, indent=2)


def list_api_keys(app_key: str, page: float, page_size: float) -> str:
    client = get_client(app_key)
    data = client.get("/v1/users/app_key/sub/list", params={"page": int(page), "pageSize": int(page_size)})
    return json.dumps(data, ensure_ascii=False, indent=2)


def create_api_key(app_key: str, remark: str, quota: float) -> str:
    client = get_client(app_key)
    body: dict[str, Any] = {}
    if remark.strip():
        body["remark"] = remark.strip()
    if quota > 0:
        body["quota"] = quota
    data = client.post("/v1/users/app_key/create", json=body)
    return json.dumps(data, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Tab 5: File management
# ---------------------------------------------------------------------------


def upload_file(app_key: str, file: Any) -> str:
    """Upload a local file via 3-step presigned URL flow."""
    if file is None:
        raise gr.Error("No file selected.")
    client = get_client(app_key)
    import os

    file_path = file.name if hasattr(file, "name") else str(file)
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # Step 1: get presigned URL
    presign_data = client.post(
        "/v2/files/upload/presigned-url",
        json={"file_name": file_name, "file_size": file_size},
    )
    upload_url = presign_data.get("upload_url", "")
    file_id = presign_data.get("file_id", "")

    # Step 2: upload to presigned URL
    content_type = "application/octet-stream"
    client.upload_file(upload_url, file_path, content_type)

    # Step 3: callback
    callback_data = client.post("/v2/files/upload/callback", json={"file_id": file_id})
    return json.dumps(
        {"file_id": file_id, "file_name": file_name, "callback": callback_data},
        ensure_ascii=False,
        indent=2,
    )


def transfer_file(app_key: str, link: str) -> str:
    if not link.strip():
        raise gr.Error("Please enter a link.")
    client = get_client(app_key)
    data = client.post("/v2/files/upload", json={"link": link.strip()})
    return json.dumps(data, ensure_ascii=False, indent=2)


def list_files(app_key: str, page: float, page_size: float) -> str:
    client = get_client(app_key)
    data = client.get("/v2/files/list", params={"page": int(page), "pageSize": int(page_size)})
    return json.dumps(data, ensure_ascii=False, indent=2)


def download_file(app_key: str, file_id: str) -> str:
    if not file_id.strip():
        raise gr.Error("Please enter a file ID.")
    client = get_client(app_key)
    data = client.post("/v2/files/download/presigned-url", json={"file_id": file_id.strip()})
    return json.dumps(data, ensure_ascii=False, indent=2)


def check_storage(app_key: str) -> str:
    client = get_client(app_key)
    data = client.get("/v2/files/user/storage_usage")
    return json.dumps(data, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Library: voice preview
# ---------------------------------------------------------------------------

VOICE_PREVIEW_TEXT = "大家好，欢迎收看今天的电影解说，让我们一起走进这个精彩的故事。"
VOICE_PREVIEW_TEXT_EN = "Hello everyone, welcome to today's movie narration. Let's explore this amazing story together."


def preview_voice(app_key: str, voice_name: str) -> str:
    """Create a TTS sample with the selected voice."""
    if not voice_name.strip():
        raise gr.Error(t("voice_not_found", name=""))
    dubbing_id, dubbing_type = find_voice_id(voice_name)
    client = get_client(app_key)
    preview_text = VOICE_PREVIEW_TEXT if dubbing_type == "普通话" else VOICE_PREVIEW_TEXT_EN
    try:
        data = client.post(
            TASK_ENDPOINTS["tts"],
            json={"voice_id": dubbing_id, "audio_text": preview_text},
        )
        return json.dumps(data, ensure_ascii=False, indent=2)
    except NarratorAPIError as e:
        return f"Preview unavailable: {e.message}"


# ---------------------------------------------------------------------------
# Language switch
# ---------------------------------------------------------------------------


def switch_language() -> list[dict[str, Any]]:
    global _current_lang
    _current_lang = LANG_EN if _current_lang is LANG_ZH else LANG_ZH
    return build_ui_updates()


def build_ui_updates() -> list[dict[str, Any]]:
    """Return updated labels/values for all UI components after language switch."""
    return [
        gr.update(value=t("title")),  # title_md
        gr.update(label=t("api_key_label"), placeholder=t("api_key_placeholder")),  # app_key
        gr.update(value=t("lang_switch")),  # lang_btn
        # Tab 1
        gr.update(value=t("wizard_desc")),  # wizard_desc_md
        gr.update(value=t("load_movies")),  # load_btn
        gr.update(label=t("movie")),  # movie_dropdown
        gr.update(label=t("search_movie"), placeholder=t("search_placeholder")),  # search_input
        gr.update(value=t("search_btn")),  # search_btn
        gr.update(label=t("search_result")),  # search_output
        gr.update(label=t("genre_filter")),  # genre_dropdown
        gr.update(label=t("narration_style")),  # style_dropdown
        gr.update(label=t("language")),  # lang_dropdown
        gr.update(label=t("voice")),  # voice_dropdown
        gr.update(label=t("bgm")),  # bgm_dropdown
        gr.update(value=t("generate")),  # generate_btn
        gr.update(label=t("progress")),  # output_log
        # Tab 2
        gr.update(label=t("task_id"), placeholder=t("task_id_placeholder")),  # task_id_input
        gr.update(value=t("query")),  # query_btn
        gr.update(label=t("result")),  # query_output
        gr.update(label=t("page")),  # page_input
        gr.update(label=t("limit")),  # limit_input
        gr.update(value=t("list")),  # list_btn
        gr.update(label=t("result")),  # list_output
        gr.update(label=t("task_type")),  # task_type_dropdown
        gr.update(label=t("stream")),  # stream_check
        gr.update(value=t("create")),  # create_btn
        gr.update(label=t("result")),  # create_output
        # Tab 4
        gr.update(label=t("username"), placeholder=t("username")),  # login_username
        gr.update(label=t("password")),  # login_password
        gr.update(value=t("login_btn")),  # login_btn
        gr.update(label=t("login_result")),  # login_output
        gr.update(value=t("check_balance")),  # balance_btn
        gr.update(label=t("account_info")),  # balance_output
        gr.update(label=t("page")),  # keys_page
        gr.update(label=t("limit")),  # keys_size
        gr.update(value=t("list_keys")),  # list_keys_btn
        gr.update(label=t("key_result")),  # keys_output
        gr.update(label=t("key_remark"), placeholder=t("key_remark")),  # new_key_remark
        gr.update(label=t("key_quota")),  # new_key_quota
        gr.update(value=t("create_key_btn")),  # create_key_btn
        gr.update(label=t("create_key_result")),  # create_key_output
        # Tab 4: Files
        gr.update(label=t("upload_file")),  # file_input
        gr.update(value=t("upload_btn")),  # upload_btn
        gr.update(label=t("upload_result")),  # upload_output
        gr.update(label=t("link_url")),  # link_input
        gr.update(value=t("transfer_btn")),  # transfer_btn
        gr.update(label=t("transfer_result")),  # transfer_output
        gr.update(label=t("page")),  # files_page
        gr.update(label=t("limit")),  # files_size
        gr.update(value=t("list_files_btn")),  # list_files_btn
        gr.update(label=t("file_list_result")),  # files_output
        gr.update(label=t("file_id_input")),  # dl_file_id
        gr.update(value=t("download_btn")),  # download_btn
        gr.update(label=t("download_result")),  # download_output
        gr.update(value=t("storage_btn")),  # storage_btn
        gr.update(label=t("storage_result")),  # storage_output
    ]


# ---------------------------------------------------------------------------
# Build UI
# ---------------------------------------------------------------------------

CUSTOM_CSS = """
/* Mobile responsive */
@media (max-width: 768px) {
    .gradio-row { flex-direction: column !important; }
    .gradio-row > .gradio-column { min-width: 100% !important; }
    .gradio-button { min-height: 44px !important; }
    .gradio-dropdown { min-height: 44px !important; }
}
/* Loading indicator on buttons */
.gradio-button[disabled] { opacity: 0.6; cursor: wait !important; }
"""

with gr.Blocks(title="Narrator AI / AI 解说大师") as app:
    with gr.Row():
        title_md = gr.Markdown(t("title"))
        lang_btn = gr.Button(t("lang_switch"), size="sm", scale=0, min_width=80)

    app_key = gr.Textbox(
        label=t("api_key_label"),
        type="password",
        placeholder=t("api_key_placeholder"),
        elem_id="app-key",
    )
    materials_state = gr.State([])

    # ── Tab 1: Wizard ─────────────────────────────────────────────────────
    with gr.Tab("一键生成 / One-Click", id="tab-wizard"):
        wizard_desc_md = gr.Markdown(t("wizard_desc"))

        with gr.Row():
            load_btn = gr.Button(t("load_movies"), variant="secondary")
            movie_dropdown = gr.Dropdown(label=t("movie"), interactive=True)

        with gr.Accordion(t("or_search"), open=False):
            with gr.Row():
                search_input = gr.Textbox(label=t("search_movie"), placeholder=t("search_placeholder"))
                search_btn = gr.Button(t("search_btn"), variant="secondary")
            search_output = gr.Textbox(label=t("search_result"), lines=6, interactive=False)

        with gr.Row():
            genre_dropdown = gr.Dropdown(
                choices=[""] + STYLE_GENRES,
                label=t("genre_filter"),
                value="",
            )
            style_dropdown = gr.Dropdown(
                choices=[f"{s['name']} ({s['genre']})" for s in NARRATION_STYLES],
                label=t("narration_style"),
            )

        with gr.Row():
            lang_dropdown = gr.Dropdown(
                choices=[""] + DUBBING_LANGUAGES,
                label=t("language"),
                value="",
            )
            voice_dropdown = gr.Dropdown(
                choices=[v["name"] for v in DUBBING_LIST],
                label=t("voice"),
            )

        bgm_dropdown = gr.Dropdown(
            choices=[b["name"] for b in BGM_LIST],
            label=t("bgm"),
        )

        generate_btn = gr.Button(t("generate"), variant="primary", size="lg")
        output_log = gr.Textbox(label=t("progress"), lines=15, interactive=False)

        load_btn.click(load_materials, inputs=[app_key], outputs=[movie_dropdown, materials_state])
        search_btn.click(search_movie, inputs=[app_key, search_input], outputs=[search_output])
        genre_dropdown.change(filter_styles, inputs=[genre_dropdown], outputs=[style_dropdown])
        lang_dropdown.change(filter_voices, inputs=[lang_dropdown], outputs=[voice_dropdown])
        generate_btn.click(
            wizard_generate,
            inputs=[app_key, movie_dropdown, materials_state, style_dropdown, voice_dropdown, bgm_dropdown],
            outputs=[output_log],
        )

    # ── Tab 2: Tasks ──────────────────────────────────────────────────────
    with gr.Tab("任务管理 / Tasks", id="tab-tasks"):
        with gr.Accordion(t("query_task"), open=True):
            task_id_input = gr.Textbox(label=t("task_id"), placeholder=t("task_id_placeholder"))
            query_btn = gr.Button(t("query"))
            query_output = gr.Textbox(label=t("result"), lines=10, interactive=False)
            query_btn.click(query_task, inputs=[app_key, task_id_input], outputs=[query_output])

        with gr.Accordion(t("list_tasks"), open=False):
            with gr.Row():
                page_input = gr.Number(label=t("page"), value=1, minimum=1)
                limit_input = gr.Number(label=t("limit"), value=10, minimum=1, maximum=100)
            list_btn = gr.Button(t("list"))
            list_output = gr.Textbox(label=t("result"), lines=15, interactive=False)
            list_btn.click(list_tasks, inputs=[app_key, page_input, limit_input], outputs=[list_output])

        with gr.Accordion(t("create_task"), open=False):
            gr.Markdown(t("create_task_desc"))
            task_type_dropdown = gr.Dropdown(
                choices=list(TASK_ENDPOINTS.keys()),
                label=t("task_type"),
            )
            body_input = gr.Code(label=t("request_body"), language="json", value="{\n  \n}")
            stream_check = gr.Checkbox(label=t("stream"), value=False)
            create_btn = gr.Button(t("create"), variant="primary")
            create_output = gr.Textbox(label=t("result"), lines=15, interactive=False)
            create_btn.click(
                create_task_advanced,
                inputs=[app_key, task_type_dropdown, body_input, stream_check],
                outputs=[create_output],
            )

    # ── Tab 3: Library ────────────────────────────────────────────────────
    with gr.Tab("素材库 / Library", id="tab-library"):
        with gr.Accordion(t("styles"), open=True):
            gr.Dataframe(
                value=[[s["genre"], s["name"], s["id"]] for s in NARRATION_STYLES],
                headers=[t("genre"), t("name"), t("template_id")],
                interactive=False,
            )
        with gr.Accordion(t("voices"), open=False):
            gr.Dataframe(
                value=[[v["name"], v["id"], v["type"], v["tag"]] for v in DUBBING_LIST],
                headers=[t("voice"), t("dubbing_id"), t("language"), t("tag")],
                interactive=False,
            )
            with gr.Row():
                preview_voice_input = gr.Dropdown(
                    choices=[v["name"] for v in DUBBING_LIST],
                    label=t("voice"),
                    scale=3,
                )
                preview_voice_btn = gr.Button("Preview / 试听", scale=1)
            preview_voice_output = gr.Textbox(label=t("result"), lines=4, interactive=False)
            preview_voice_btn.click(
                preview_voice,
                inputs=[app_key, preview_voice_input],
                outputs=[preview_voice_output],
            )
        with gr.Accordion(t("bgm_tracks"), open=False):
            gr.Dataframe(
                value=[[b["name"], b["id"]] for b in BGM_LIST],
                headers=[t("bgm_name"), t("bgm_id")],
                interactive=False,
            )

    # ── Tab 4: Files ─────────────────────────────────────────────────────
    with gr.Tab("文件管理 / Files", id="tab-files"):
        with gr.Accordion(t("upload_file"), open=True):
            file_input = gr.File(label=t("upload_file"))
            upload_btn = gr.Button(t("upload_btn"), variant="primary")
            upload_output = gr.Textbox(label=t("upload_result"), lines=6, interactive=False)
            upload_btn.click(upload_file, inputs=[app_key, file_input], outputs=[upload_output])

        with gr.Accordion(t("transfer_link"), open=False):
            link_input = gr.Textbox(label=t("link_url"), placeholder="https://... or baidu/pikpak link")
            transfer_btn = gr.Button(t("transfer_btn"))
            transfer_output = gr.Textbox(label=t("transfer_result"), lines=6, interactive=False)
            transfer_btn.click(transfer_file, inputs=[app_key, link_input], outputs=[transfer_output])

        with gr.Accordion(t("file_list"), open=False):
            with gr.Row():
                files_page = gr.Number(label=t("page"), value=1, minimum=1)
                files_size = gr.Number(label=t("limit"), value=10, minimum=1, maximum=100)
            list_files_btn = gr.Button(t("list_files_btn"))
            files_output = gr.Textbox(label=t("file_list_result"), lines=12, interactive=False)
            list_files_btn.click(list_files, inputs=[app_key, files_page, files_size], outputs=[files_output])

        with gr.Accordion(t("download_file"), open=False):
            dl_file_id = gr.Textbox(label=t("file_id_input"), placeholder="Enter file ID")
            download_btn = gr.Button(t("download_btn"))
            download_output = gr.Textbox(label=t("download_result"), lines=6, interactive=False)
            download_btn.click(download_file, inputs=[app_key, dl_file_id], outputs=[download_output])

        with gr.Accordion(t("storage"), open=False):
            storage_btn = gr.Button(t("storage_btn"))
            storage_output = gr.Textbox(label=t("storage_result"), lines=4, interactive=False)
            storage_btn.click(check_storage, inputs=[app_key], outputs=[storage_output])

    # ── Tab 5: Account ────────────────────────────────────────────────────
    with gr.Tab("账户 / Account", id="tab-account"):
        with gr.Accordion(t("login"), open=True):
            with gr.Row():
                login_username = gr.Textbox(label=t("username"), placeholder=t("username"))
                login_password = gr.Textbox(label=t("password"), type="password")
            login_btn = gr.Button(t("login_btn"), variant="primary")
            login_output = gr.Textbox(label=t("login_result"), lines=8, interactive=False)
            login_btn.click(user_login, inputs=[login_username, login_password], outputs=[login_output])

        with gr.Accordion(t("check_balance"), open=False):
            balance_btn = gr.Button(t("check_balance"))
            balance_output = gr.Textbox(label=t("account_info"), lines=5, interactive=False)
            balance_btn.click(check_balance, inputs=[app_key], outputs=[balance_output])

        with gr.Accordion(t("api_keys"), open=False):
            with gr.Row():
                keys_page = gr.Number(label=t("page"), value=1, minimum=1)
                keys_size = gr.Number(label=t("limit"), value=10, minimum=1, maximum=100)
            list_keys_btn = gr.Button(t("list_keys"))
            keys_output = gr.Textbox(label=t("key_result"), lines=10, interactive=False)
            list_keys_btn.click(list_api_keys, inputs=[app_key, keys_page, keys_size], outputs=[keys_output])

        with gr.Accordion(t("create_key"), open=False):
            with gr.Row():
                new_key_remark = gr.Textbox(label=t("key_remark"), placeholder=t("key_remark"))
                new_key_quota = gr.Number(label=t("key_quota"), value=0, minimum=0)
            create_key_btn = gr.Button(t("create_key_btn"), variant="primary")
            create_key_output = gr.Textbox(label=t("create_key_result"), lines=8, interactive=False)
            create_key_btn.click(
                create_api_key, inputs=[app_key, new_key_remark, new_key_quota], outputs=[create_key_output]
            )

    # ── Language switch event ─────────────────────────────────────────────
    all_updatable = [
        title_md,
        app_key,
        lang_btn,
        wizard_desc_md,
        load_btn,
        movie_dropdown,
        search_input,
        search_btn,
        search_output,
        genre_dropdown,
        style_dropdown,
        lang_dropdown,
        voice_dropdown,
        bgm_dropdown,
        generate_btn,
        output_log,
        task_id_input,
        query_btn,
        query_output,
        page_input,
        limit_input,
        list_btn,
        list_output,
        task_type_dropdown,
        stream_check,
        create_btn,
        create_output,
        login_username,
        login_password,
        login_btn,
        login_output,
        balance_btn,
        balance_output,
        keys_page,
        keys_size,
        list_keys_btn,
        keys_output,
        new_key_remark,
        new_key_quota,
        create_key_btn,
        create_key_output,
        file_input,
        upload_btn,
        upload_output,
        link_input,
        transfer_btn,
        transfer_output,
        files_page,
        files_size,
        list_files_btn,
        files_output,
        dl_file_id,
        download_btn,
        download_output,
        storage_btn,
        storage_output,
    ]
    lang_btn.click(switch_language, outputs=all_updatable)


if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft(), css=CUSTOM_CSS)
