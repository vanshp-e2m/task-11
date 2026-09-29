#!/usr/bin/env bash
# usage: bridge.sh <tools/call name> '<json arguments>'   (or @file.json to read the arguments from a file)
# Raw DevConnect MCP call for checks outside the MCP client. Credential is read at runtime from the
# local-scope Claude config (never stored in the repo).
AUTH=$(python - <<'PY'
import json
d=json.load(open(r'C:/Users/Vansh Patel/.claude.json'))
for k,v in d['projects'].items():
    if k.lower().replace(chr(92),'/').endswith('task-11/app/public') and 'dev-command' in v.get('mcpServers',{}):
        print(v['mcpServers']['dev-command']['headers']['Authorization']); break
PY
)
U=http://task-11.local/wp-json/mcp/dev-connect-server
H=(-H "Authorization: $AUTH" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream')
SID=$(curl -s -D - -o /dev/null "${H[@]}" -X POST --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"check","version":"1"}}}' $U | grep -i '^mcp-session-id' | cut -d' ' -f2 | tr -d '\r')
ARGS="$2"; case "$ARGS" in @*) ARGS=$(cat "${ARGS#@}");; esac
BODY=$(mktemp); printf '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"%s","arguments":%s}}' "$1" "$ARGS" > "$BODY"
curl -s "${H[@]}" -H "Mcp-Session-Id: $SID" -X POST --data-binary @"$BODY" $U; rm -f "$BODY"
