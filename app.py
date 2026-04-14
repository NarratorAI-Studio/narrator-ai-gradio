"""Narrator AI — Gradio Web UI (bilingual: Chinese / English)."""

import json
import time

import gradio as gr

from client import NarratorClient, NarratorAPIError
from data import (
    BGM_LIST, DUBBING_LIST, DUBBING_LANGUAGES,
    NARRATION_STYLES, STYLE_GENRES,
    TASK_ENDPOINTS,
)

# ---------------------------------------------------------------------------
# i18n
# ---------------------------------------------------------------------------

LANG_ZH = {
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
    "lang_switch": "English",
}

LANG_EN = {
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
    "lang_switch": "中文",
}

# Current language state — default Chinese
_current_lang = LANG_ZH


def t(key: str, **kwargs) -> str:
    return _current_lang.get(key, key).format(**kwargs) if kwargs else _current_lang.get(key, key)


def get_client(app_key: str) -> NarratorClient:
    if not app_key.strip():
        raise gr.Error(t("api_key_missing"))
    return NarratorClient(app_key=app_key.strip())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_materials(app_key: str):
    client = get_client(app_key)
    try:
        data = client.get("/v2/res/movie-sucai", params={"page": 1, "size": 200})
    except NarratorAPIError as e:
        raise gr.Error(f"API Error [{e.code}]: {e.message}")
    except Exception as e:
        raise gr.Error(f"Connection error: {e}")
    items = data.get("items", [])
    choices = [f"{m.get('name', '')} ({m.get('title', '')})" for m in items]
    return gr.update(choices=choices), items


def filter_voices(language: str):
    if not language:
        voices = DUBBING_LIST
    else:
        voices = [d for d in DUBBING_LIST if d["type"] == language]
    return gr.update(choices=[v["name"] for v in voices])


def filter_styles(genre: str):
    if not genre:
        styles = NARRATION_STYLES
    else:
        styles = [s for s in NARRATION_STYLES if s["genre"] == genre]
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


def poll_task(client: NarratorClient, task_id: str, max_wait: int = 600) -> dict:
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

def wizard_generate(app_key, movie_idx, materials_state, style_display, voice_name, bgm_name, progress=gr.Progress()):
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

    def log(msg):
        log_lines.append(msg)
        return "\n".join(log_lines)

    # Step 1: fast-writing
    progress(0.1, desc=t("prog_script"))
    yield log(t("step1", movie=movie_name))

    fw_body = {
        "playlet_name": movie_name,
        "target_mode": 1,
        "learning_model_id": style_id,
        "confirmed_movie_json": {
            "name": movie_name,
            "title": movie.get("title", ""),
        },
    }
    try:
        fw_result = client.post(TASK_ENDPOINTS["fast-writing"], json=fw_body)
    except NarratorAPIError as e:
        raise gr.Error(f"fast-writing: {e.message}")

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
        "episodes_data": [
            {"video_oss_key": video_file_id, "srt_oss_key": srt_file_id, "num": 1}
        ],
    }
    try:
        fcd_result = client.post(TASK_ENDPOINTS["fast-clip-data"], json=fcd_body)
    except NarratorAPIError as e:
        raise gr.Error(f"fast-clip-data: {e.message}")

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
        raise gr.Error(f"video-composing: {e.message}")

    vc_task_id = vc_result.get("task_id", "")
    yield log(t("task_created", task_id=vc_task_id))
    yield log(t("waiting_video"))

    progress(0.8, desc=t("prog_wait_video"))
    vc_query = poll_task(client, vc_task_id, max_wait=900)

    progress(1.0, desc=t("prog_done"))
    yield log(f"{t('done')}\n\nTask ID: {vc_task_id}\nResult:\n{json.dumps(vc_query, ensure_ascii=False, indent=2)}")


# ---------------------------------------------------------------------------
# Tab 2: Task management
# ---------------------------------------------------------------------------

def query_task(app_key, task_id):
    client = get_client(app_key)
    result = client.get(f"/v2/task/commentary/query/{task_id}")
    return json.dumps(result, ensure_ascii=False, indent=2)


def list_tasks(app_key, page, limit):
    client = get_client(app_key)
    result = client.get("/v2/task/commentary/list", params={
        "page": int(page), "limit": int(limit),
    })
    items = result.get("items", [])
    if not items:
        return t("no_tasks")
    return json.dumps(result, ensure_ascii=False, indent=2)


def create_task_advanced(app_key, task_type, body_json, use_stream):
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

def check_balance(app_key):
    client = get_client(app_key)
    data = client.get("/v1/users/balance")
    return (
        f"{t('user')}: {data.get('nickname', 'N/A')}\n"
        f"{t('balance')}: {data.get('balance', 'N/A')}\n"
        f"{t('company')}: {data.get('company_name', 'N/A')}"
    )


# ---------------------------------------------------------------------------
# Language switch
# ---------------------------------------------------------------------------

def switch_language():
    global _current_lang
    if _current_lang is LANG_ZH:
        _current_lang = LANG_EN
    else:
        _current_lang = LANG_ZH
    return build_ui_updates()


def build_ui_updates():
    """Return updated labels/values for all UI components after language switch."""
    return [
        gr.update(value=t("title")),                          # title_md
        gr.update(label=t("api_key_label"), placeholder=t("api_key_placeholder")),  # app_key
        gr.update(value=t("lang_switch")),                    # lang_btn
        # Tab 1
        gr.update(value=t("wizard_desc")),                    # wizard_desc_md
        gr.update(value=t("load_movies")),                    # load_btn
        gr.update(label=t("movie")),                          # movie_dropdown
        gr.update(label=t("genre_filter")),                   # genre_dropdown
        gr.update(label=t("narration_style")),                # style_dropdown
        gr.update(label=t("language")),                       # lang_dropdown
        gr.update(label=t("voice")),                          # voice_dropdown
        gr.update(label=t("bgm")),                            # bgm_dropdown
        gr.update(value=t("generate")),                       # generate_btn
        gr.update(label=t("progress")),                       # output_log
        # Tab 2
        gr.update(label=t("task_id"), placeholder=t("task_id_placeholder")),  # task_id_input
        gr.update(value=t("query")),                          # query_btn
        gr.update(label=t("result")),                         # query_output
        gr.update(label=t("page")),                           # page_input
        gr.update(label=t("limit")),                          # limit_input
        gr.update(value=t("list")),                           # list_btn
        gr.update(label=t("result")),                         # list_output
        gr.update(label=t("task_type")),                      # task_type_dropdown
        gr.update(label=t("stream")),                         # stream_check
        gr.update(value=t("create")),                         # create_btn
        gr.update(label=t("result")),                         # create_output
        # Tab 4
        gr.update(value=t("check_balance")),                  # balance_btn
        gr.update(label=t("account_info")),                   # balance_output
    ]


# ---------------------------------------------------------------------------
# Build UI
# ---------------------------------------------------------------------------

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

        with gr.Row():
            genre_dropdown = gr.Dropdown(
                choices=[""] + STYLE_GENRES, label=t("genre_filter"), value="",
            )
            style_dropdown = gr.Dropdown(
                choices=[f"{s['name']} ({s['genre']})" for s in NARRATION_STYLES],
                label=t("narration_style"),
            )

        with gr.Row():
            lang_dropdown = gr.Dropdown(
                choices=[""] + DUBBING_LANGUAGES, label=t("language"), value="",
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
            body_input = gr.Code(label=t("request_body"), language="json", value='{\n  \n}')
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
        with gr.Accordion(t("bgm_tracks"), open=False):
            gr.Dataframe(
                value=[[b["name"], b["id"]] for b in BGM_LIST],
                headers=[t("bgm_name"), t("bgm_id")],
                interactive=False,
            )

    # ── Tab 4: Account ────────────────────────────────────────────────────
    with gr.Tab("账户 / Account", id="tab-account"):
        balance_btn = gr.Button(t("check_balance"))
        balance_output = gr.Textbox(label=t("account_info"), lines=5, interactive=False)
        balance_btn.click(check_balance, inputs=[app_key], outputs=[balance_output])

    # ── Language switch event ─────────────────────────────────────────────
    all_updatable = [
        title_md, app_key, lang_btn,
        wizard_desc_md, load_btn, movie_dropdown, genre_dropdown, style_dropdown,
        lang_dropdown, voice_dropdown, bgm_dropdown, generate_btn, output_log,
        task_id_input, query_btn, query_output,
        page_input, limit_input, list_btn, list_output,
        task_type_dropdown, stream_check, create_btn, create_output,
        balance_btn, balance_output,
    ]
    lang_btn.click(switch_language, outputs=all_updatable)


if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft())
