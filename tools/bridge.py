"""Minimal DevConnect MCP client (no shell in between; see issue #29).

    from bridge import dispatch
    res = dispatch("dev/list-pages", {"per_page": 5})

The Basic-auth credential is read at runtime from the local-scope Claude config; it is never stored in the repo.
"""
import json
import urllib.request

URL = "http://task-11.local/wp-json/mcp/dev-connect-server"
_CFG = r"C:/Users/Vansh Patel/.claude.json"
_session = {"auth": None, "sid": None}


def _auth():
    if not _session["auth"]:
        d = json.load(open(_CFG, encoding="utf-8"))
        for k, v in d["projects"].items():
            if k.lower().replace("\\", "/").endswith("task-11/app/public") and "dev-command" in v.get("mcpServers", {}):
                _session["auth"] = v["mcpServers"]["dev-command"]["headers"]["Authorization"]
                break
    return _session["auth"]


def _post(body):
    headers = {"Authorization": _auth(), "Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if _session["sid"]:
        headers["Mcp-Session-Id"] = _session["sid"]
    req = urllib.request.Request(URL, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=300) as r:
        sid = r.headers.get("Mcp-Session-Id")
        if sid:
            _session["sid"] = sid
        return json.loads(r.read().decode("utf-8") or "{}")


def _init():
    if not _session["sid"]:
        _post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
               "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "task11-bridge-py", "version": "1"}}})


def call(tool, arguments):
    _init()
    r = _post({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": tool, "arguments": arguments}})
    return r.get("result", {}).get("structuredContent", r)


def dispatch(ability, parameters):
    """Returns the ability result; raises RuntimeError with the server message on failure."""
    res = call("dev-bridge-dispatch-tool", {"ability_name": ability, "parameters": parameters})
    if not res.get("ok"):
        raise RuntimeError(f"{ability}: {res.get('error') or res}")
    return res.get("result")
