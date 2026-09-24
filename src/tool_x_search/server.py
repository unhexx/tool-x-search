"""X Search is not reproducible locally without X/xAI.

This service is an explicit facade:
- default: refuse and tell the agent to enable xAI server-side x_search
- TOOL_X_FIXTURES=1: serve a local JSON fixture pack for hermetic tests
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from tool_http import serve

TOOL = "x_search"
SCHEMA = {
    "type": "function",
    "name": "x_search",
    "description": "Local facade for X search. Without fixtures this tool MUST NOT be used; enable xAI server-side x_search / x_keyword_search / x_semantic_search / x_thread_fetch / x_user_search / view_x_video instead.",
    "parameters": {
        "type": "object",
        "properties": {
            "variant": {
                "type": "string",
                "enum": ["x_keyword_search", "x_semantic_search", "x_user_search", "x_thread_fetch", "view_x_video"],
            },
            "query": {"type": "string"},
            "username": {"type": "string"},
            "post_id": {"type": "string"},
        },
        "required": ["variant"],
    },
}


def run(arguments: dict[str, Any]) -> dict[str, Any]:
    variant = arguments.get("variant") or "x_keyword_search"
    if os.environ.get("TOOL_X_FIXTURES", "0") not in {"1", "true", "yes"}:
        return {
            "ok": False,
            "local": False,
            "error": "x_search cannot run locally without X/xAI",
            "use_server_side": [
                "x_keyword_search",
                "x_semantic_search",
                "x_user_search",
                "x_thread_fetch",
                "view_x_video",
            ],
            "docs": "https://docs.x.ai/developers/tools/advanced-usage#mixing-server-side-and-client-side-tools",
        }
    fixtures = Path(os.environ.get("X_FIXTURES", "/app/fixtures/x.json"))
    data = json.loads(fixtures.read_text(encoding="utf-8")) if fixtures.is_file() else {"posts": []}
    query = str(arguments.get("query") or arguments.get("username") or arguments.get("post_id") or "")
    posts = [p for p in data.get("posts", []) if query.lower() in json.dumps(p).lower()]
    return {"ok": True, "variant": variant, "posts": posts[:10], "source": "fixtures"}


def main() -> None:
    serve(TOOL, SCHEMA, run)


if __name__ == "__main__":
    main()
