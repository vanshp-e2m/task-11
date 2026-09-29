# Checkpoint — products

> Machine-readable build state. Owned by scripts/checkpoint.py. Do not edit by hand.

## Pipeline phases — Extraction + Plan

- [ ] figma-extracted
- [ ] sections-detected
- [ ] plan-created
- [ ] page-created

## Phase 1 — Foundation (foundation-builder)

- [ ] phase-1-globals
- [ ] phase-1-header
- [ ] phase-1-footer
- [ ] phase-1-foundation-complete

## Phase 2 — Fast-build (default path — elementor-fast-build-qa)

- [ ] body-built
<!-- qa-passed / qa-blocked recorded under Finalization below — same marks, one outcome -->

## Phase 2..N — Strict per-section path (OPT-IN — elementor-section-orchestrator, only if used instead of fast-build)

> Three sub-marks per section; section N+1 cannot start until N has all three. Only present on
> pages built via the explicit strict path — a fast-build page has no per-section marks.

- [ ] all-sections-complete

## Finalization

- [ ] globals-verified
- [ ] qa-passed
<!-- qa-blocked instead of qa-passed if fast-build's 2 correction passes are exhausted -->

## Maintenance (maint-runner / maint-qa; ACF only)

> Present only on pages touched by a maintenance task. A build-only page never carries these
> marks. maint-qa-blocked is a terminal outcome, not a retry state — it deliberately does NOT
> promote page status, so a blocked page never reads as verified.

- [ ] maint-intent-captured
- [ ] maint-baseline-captured
- [ ] maint-applied
- [x] maint-qa-passed
<!-- maint-qa-blocked instead of maint-qa-passed if the 3 fix passes are exhausted, the task type
     is unverifiable through the bridge, or Phase 0 blocked the run -->
- [ ] maint-qa-blocked

## Event log (JSON, append-only)

```json
{"agent": "maint-qa", "note": "content_update, pass 1, 0 open findings", "phase": "maint-qa-passed", "ts": "2026-09-28T14:18:40Z"}
```
