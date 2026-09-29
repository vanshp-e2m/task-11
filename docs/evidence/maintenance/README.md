# Maintenance ticket — pending

The brief asks for one maintenance ticket carried out on a site built with a **different builder**, plus a change note.
No ticket has been issued yet, and CLAUDE.md allows tooling to target `http://task-11.local` only, so nothing was done here.

To complete it, the developer provides:
1. the ticket text (what to change), and
2. the target: a **local** practice site built with another builder (e.g. one of the Local sites on this machine), with
   explicit permission to point DevConnect / WP-CLI / Playwright at it — never a client site.

The run will then follow the same rules as the rest of the project: classify the change, snapshot first, change through the
builder's own DevCommand agents (Gutenberg / Divi / Beaver …), verify with the matching QA agent, and write the change note here
(ticket → what was touched → how it was verified → rollback point).
