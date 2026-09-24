from tool_x_search.server import run


def test_refuse_by_default(monkeypatch):
    monkeypatch.delenv("TOOL_X_FIXTURES", raising=False)
    out = run({"variant": "x_keyword_search", "query": "grok"})
    assert out["ok"] is False
    assert "x_keyword_search" in out["use_server_side"]
