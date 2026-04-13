"""Narrator AI — Gradio Web UI."""

import json
import time

import gradio as gr

from client import NarratorClient, NarratorAPIError
from data import (
    BGM_LIST, DUBBING_LIST, DUBBING_LANGUAGES,
    NARRATION_STYLES, STYLE_GENRES,
    TASK_ENDPOINTS,
)


def get_client(app_key: str) -> NarratorClient:
    if not app_key.strip():
        raise gr.Error("Please enter your API Key first.")
    return NarratorClient(app_key=app_key.strip())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_materials(app_key: str):
    """Fetch movie materials from API."""
    client = get_client(app_key)
    data = client.get("/v2/res/movie-sucai", params={"page": 1, "size": 200})
    items = data.get("items", [])
    choices = [f"{m.get('name', '')} ({m.get('title', '')})" for m in items]
    return gr.update(choices=choices), items


def filter_voices(language: str):
    if not language:
        voices = DUBBING_LIST
    else:
        voices = [d for d in DUBBING_LIST if d["type"] == language]
    return gr.update(choices=[f"{v['name']}" for v in voices])


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
    raise gr.Error(f"Voice not found: {voice_name}")


def find_bgm_id(bgm_name: str) -> str:
    for b in BGM_LIST:
        if b["name"] == bgm_name:
            return b["id"]
    raise gr.Error(f"BGM not found: {bgm_name}")


def find_style_id(style_display: str) -> str:
    for s in NARRATION_STYLES:
        display = f"{s['name']} ({s['genre']})"
        if display == style_display:
            return s["id"]
    raise gr.Error(f"Style not found: {style_display}")


def poll_task(client: NarratorClient, task_id: str, max_wait: int = 600) -> dict:
    """Poll task until completion."""
    start = time.time()
    while time.time() - start < max_wait:
        result = client.get(f"/v2/task/commentary/query/{task_id}")
        status = result.get("status_code", 0)
        if status == 2:  # success
            return result
        if status in (3, 4):  # failed or cancelled
            raise gr.Error(f"Task failed: {result.get('status_name', 'unknown')}")
        time.sleep(5)
    raise gr.Error(f"Task timed out after {max_wait}s")


# ---------------------------------------------------------------------------
# Tab 1: Wizard — One-click video generation
# ---------------------------------------------------------------------------

def wizard_generate(app_key, movie_idx, materials_state, style_display, voice_name, bgm_name, progress=gr.Progress()):
    """Full pipeline: fast-writing → fast-clip-data → video-composing."""
    client = get_client(app_key)

    if not materials_state or movie_idx is None:
        raise gr.Error("Please load and select a movie first.")

    # Resolve selections
    movie_name_display = movie_idx
    # Find the movie in materials
    movie = None
    for m in materials_state:
        display = f"{m.get('name', '')} ({m.get('title', '')})"
        if display == movie_name_display:
            movie = m
            break
    if not movie:
        raise gr.Error("Movie not found in materials.")

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
    progress(0.1, desc="Generating narration script...")
    yield log(f"Step 1/3: Generating narration script for [{movie_name}]...")

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
        raise gr.Error(f"fast-writing failed: {e.message}")

    fw_task_id = fw_result.get("task_id", "")
    yield log(f"  Task created: {fw_task_id}")
    yield log("  Waiting for script generation...")

    progress(0.2, desc="Waiting for script...")
    fw_query = poll_task(client, fw_task_id)
    file_ids = fw_query.get("results", {}).get("file_ids", [])
    if not file_ids:
        raise gr.Error("fast-writing completed but no file_ids returned.")
    fw_file_id = file_ids[0]
    yield log(f"  Script ready. file_id: {fw_file_id}")

    # Step 2: fast-clip-data
    progress(0.4, desc="Generating clip data...")
    yield log("Step 2/3: Generating clip/editing data...")

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
        raise gr.Error(f"fast-clip-data failed: {e.message}")

    fcd_task_id = fcd_result.get("task_id", "")
    yield log(f"  Task created: {fcd_task_id}")
    yield log("  Waiting for clip data...")

    progress(0.5, desc="Waiting for clip data...")
    fcd_query = poll_task(client, fcd_task_id)
    fcd_order_num = fcd_query.get("task_order_num", "")
    yield log(f"  Clip data ready. order_num: {fcd_order_num}")

    # Step 3: video-composing
    progress(0.7, desc="Composing video...")
    yield log("Step 3/3: Composing final video...")

    vc_body = {
        "order_num": fcd_order_num,
        "bgm": bgm_id,
        "dubbing": dubbing_id,
        "dubbing_type": dubbing_type,
    }
    try:
        vc_result = client.post(TASK_ENDPOINTS["video-composing"], json=vc_body)
    except NarratorAPIError as e:
        raise gr.Error(f"video-composing failed: {e.message}")

    vc_task_id = vc_result.get("task_id", "")
    yield log(f"  Task created: {vc_task_id}")
    yield log("  Waiting for video...")

    progress(0.8, desc="Waiting for video...")
    vc_query = poll_task(client, vc_task_id, max_wait=900)

    progress(1.0, desc="Done!")
    yield log(f"  Done!\n\nTask ID: {vc_task_id}\nResult:\n{json.dumps(vc_query, ensure_ascii=False, indent=2)}")


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
        return "No tasks found."
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
        f"User: {data.get('nickname', 'N/A')}\n"
        f"Balance: {data.get('balance', 'N/A')}\n"
        f"Company: {data.get('company_name', 'N/A')}"
    )


# ---------------------------------------------------------------------------
# Build UI
# ---------------------------------------------------------------------------

with gr.Blocks(
    title="Narrator AI",
    theme=gr.themes.Soft(),
) as app:

    gr.Markdown("# Narrator AI\nAI-powered video narration generation.")

    # Shared state
    app_key = gr.Textbox(
        label="API Key (app-key)",
        type="password",
        placeholder="Enter your Narrator AI API key",
        elem_id="app-key",
    )
    materials_state = gr.State([])

    # ── Tab 1: Wizard ─────────────────────────────────────────────────────
    with gr.Tab("One-Click Generate"):
        gr.Markdown("Select a movie, style, voice, and BGM — one click to generate a narration video.")

        with gr.Row():
            load_btn = gr.Button("Load Movies", variant="secondary")
            movie_dropdown = gr.Dropdown(label="Movie", interactive=True)

        with gr.Row():
            genre_dropdown = gr.Dropdown(
                choices=[""] + STYLE_GENRES, label="Genre Filter", value="",
            )
            style_dropdown = gr.Dropdown(
                choices=[f"{s['name']} ({s['genre']})" for s in NARRATION_STYLES],
                label="Narration Style",
            )

        with gr.Row():
            lang_dropdown = gr.Dropdown(
                choices=[""] + DUBBING_LANGUAGES, label="Language", value="",
            )
            voice_dropdown = gr.Dropdown(
                choices=[v["name"] for v in DUBBING_LIST],
                label="Voice",
            )

        bgm_dropdown = gr.Dropdown(
            choices=[b["name"] for b in BGM_LIST],
            label="Background Music",
        )

        generate_btn = gr.Button("Generate Video", variant="primary", size="lg")
        output_log = gr.Textbox(label="Progress", lines=15, interactive=False)

        # Events
        load_btn.click(
            load_materials, inputs=[app_key],
            outputs=[movie_dropdown, materials_state],
        )
        genre_dropdown.change(filter_styles, inputs=[genre_dropdown], outputs=[style_dropdown])
        lang_dropdown.change(filter_voices, inputs=[lang_dropdown], outputs=[voice_dropdown])
        generate_btn.click(
            wizard_generate,
            inputs=[app_key, movie_dropdown, materials_state, style_dropdown, voice_dropdown, bgm_dropdown],
            outputs=[output_log],
        )

    # ── Tab 2: Tasks ──────────────────────────────────────────────────────
    with gr.Tab("Tasks"):
        with gr.Accordion("Query Task", open=True):
            task_id_input = gr.Textbox(label="Task ID", placeholder="Enter task UUID")
            query_btn = gr.Button("Query")
            query_output = gr.Textbox(label="Result", lines=10, interactive=False)
            query_btn.click(query_task, inputs=[app_key, task_id_input], outputs=[query_output])

        with gr.Accordion("List Tasks", open=False):
            with gr.Row():
                page_input = gr.Number(label="Page", value=1, minimum=1)
                limit_input = gr.Number(label="Limit", value=10, minimum=1, maximum=100)
            list_btn = gr.Button("List")
            list_output = gr.Textbox(label="Result", lines=15, interactive=False)
            list_btn.click(list_tasks, inputs=[app_key, page_input, limit_input], outputs=[list_output])

        with gr.Accordion("Create Task (Advanced)", open=False):
            gr.Markdown("For advanced users. Paste the full JSON body for any task type.")
            task_type_dropdown = gr.Dropdown(
                choices=list(TASK_ENDPOINTS.keys()),
                label="Task Type",
            )
            body_input = gr.Code(label="Request Body (JSON)", language="json", value='{\n  \n}')
            stream_check = gr.Checkbox(label="Stream (SSE)", value=False)
            create_btn = gr.Button("Create Task", variant="primary")
            create_output = gr.Textbox(label="Result", lines=15, interactive=False)
            create_btn.click(
                create_task_advanced,
                inputs=[app_key, task_type_dropdown, body_input, stream_check],
                outputs=[create_output],
            )

    # ── Tab 3: Library ────────────────────────────────────────────────────
    with gr.Tab("Library"):
        with gr.Accordion("Narration Styles", open=True):
            gr.Dataframe(
                value=[[s["genre"], s["name"], s["id"]] for s in NARRATION_STYLES],
                headers=["Genre", "Name", "Template ID"],
                interactive=False,
            )
        with gr.Accordion("Voices", open=False):
            gr.Dataframe(
                value=[[v["name"], v["id"], v["type"], v["tag"]] for v in DUBBING_LIST],
                headers=["Voice", "Dubbing ID", "Language", "Tag"],
                interactive=False,
            )
        with gr.Accordion("BGM", open=False):
            gr.Dataframe(
                value=[[b["name"], b["id"]] for b in BGM_LIST],
                headers=["BGM Name", "BGM ID"],
                interactive=False,
            )

    # ── Tab 4: Account ────────────────────────────────────────────────────
    with gr.Tab("Account"):
        balance_btn = gr.Button("Check Balance")
        balance_output = gr.Textbox(label="Account Info", lines=5, interactive=False)
        balance_btn.click(check_balance, inputs=[app_key], outputs=[balance_output])


if __name__ == "__main__":
    app.launch()
