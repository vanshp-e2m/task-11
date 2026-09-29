# Step 0 — Environment setup (repeatable walkthrough)

Target: **http://task-11.local** (Local, site id `PXH8o8TpS`, PHP 8.2.29, MySQL 8.4 on port 10053). Local only.

| # | Step | Command / action | Check |
|---|------|------------------|-------|
| 1 | Baseline snapshot of the fresh install | `backups/00-baseline-fresh-install.sql` | file > 0 bytes, ends with `Dump completed` |
| 2 | WP-CLI wrapper | `tools/wp.sh` = Local's php.exe + the site's php.ini + Local's bundled `wp-cli.phar`; exports MySQL host/port (issue #1) | `tools/wp.sh option get siteurl` → `http://task-11.local` |
| 3 | Plugins (copied from my own local practice sites, not downloaded) | DevConnect 0.3.5 + ACF Pro 6.8.5 (task-9), Elementor 4.3.1 + Elementor Pro 4.0.0 (task-10); `tools/wp.sh plugin activate …` | `tools/wp.sh plugin list` → all active |
| 4 | Theme | `hello-elementor` 3.5.1 (parent) + custom child `module11` | front end 200; `module11/assets/css/main.css` enqueued |
| 5 | DevConnect bridge | App password for `admin` created with WP-CLI (never printed); `initialize` POST → HTTP 200, serverInfo `DEV Connect v0.3.5`; registered as MCP server `dev-command` at **local scope** (not committed) | restart Claude Code → `/dev-doctor` |
| 6 | Figma access | Personal access token → `.secrets/figma-token` (gitignored), used as `FIGMA_TOKEN` for the REST API | `GET /v1/files/1oEHbyS1GjMmLsG20iEgt2` → 200 |
| 7 | Project memory for Claude Code | `CLAUDE.md` (conventions + guardrails), `project-config.json` (read by DevCommand agents) | — |
| 8 | Snapshot after the stack is installed | `tools/snapshot.sh stack-installed-theme-active` | 14 tables, utf8mb4 |
| 9 | Git | whitelist `.gitignore`: tracks the theme, docs, config and tools; excludes WP core, uploads, third-party plugins, backups and secrets | `git status` is clean |

## Theme skeleton (`wp-content/themes/module11`)
```
functions.php                bootstrap; requires inc/*
inc/setup.php                supports + menus (primary, footer)
inc/enqueue.php              main.css / main.js, mtime cache-busting
inc/acf.php                  Local JSON save/load → acf-json/, Site Settings options page
inc/global-settings.php      m11_get_setting(), brand tokens → CSS custom properties (Flow B)
inc/template-helpers.php     m11_render_sections(): FC layout → template-parts/flex-blocks/<layout>.php
templates/page-flexible.php  "Flexible Content" page template
assets/scss/{abstracts,base,layouts,components}  tokens, fluid-font/minmedia/maxmedia, one partial per layout
acf-json/                    committed field groups
```
