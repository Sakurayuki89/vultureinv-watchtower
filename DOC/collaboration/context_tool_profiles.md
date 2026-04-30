# Watchtower Context And Tool Profiles

## Purpose

Load only the context needed for the current task. Watchtower should stay easy
to operate on the Mac mini.

## P0 - Orientation

Use when starting a session.

Load:
- `AGENTS.md`
- `README.md`
- `DOC/collaboration/ai_role_protocol.md`
- `DOC/collaboration/context_tool_profiles.md`
- `DOC/mission.md`
- `DOC/architecture.md`
- `DOC/vultureinv_integration_contract.md`

Tools:
- `rg --files`
- `git status --short`
- `./scripts/validate.sh`

Output:
- current project state,
- correct role,
- next profile.

## P1 - Planning / Architecture

Use when changing product direction, provider policy, or integration contracts.

Load:
- P0 files
- `DOC/specs/vultureinv_support_plan.md`
- `DOC/specs/settings_and_web_integration.md`
- relevant provider docs in `DOC/data_sources.md`

Output:
- decision record,
- implementation prompt for Claude.

## P2 - Telegram / UX

Use when building Telegram commands or a local settings web UI.

Load:
- P0 files
- `DOC/telegram_bot_spec.md`
- `DOC/specs/settings_and_web_integration.md`

Output:
- implemented command/UI,
- validation result,
- screenshots or terminal examples when available.

## P3 - Data Providers

Use when adding KRX, FRED, OpenDART, or SEC EDGAR.

Load:
- P0 files
- `DOC/data_sources.md`
- `DOC/vultureinv_integration_contract.md`

Rules:
- provider adapter first,
- raw snapshot before derived snapshot,
- source timestamp required,
- no secret commits.

## P4 - Backend / API / Worker

Use when implementing FastAPI, scheduler, storage, or snapshot endpoints.

Load:
- P0 files
- `DOC/architecture.md`
- `DOC/specs/settings_and_web_integration.md`

Output:
- code,
- validation result,
- run commands.

## P5 - Review / Debug

Use after implementation or when behavior is wrong.

Load:
- P0 files
- changed files only,
- validation output.

Output:
- findings first,
- concrete patch or repair prompt.

## P6 - Audit / Memory

Use for broad consistency checks.

Load:
- all docs under `DOC/`,
- `AGENTS.md`,
- prompts.

Output:
- audit findings,
- docs needing updates,
- memory/current-context update if such file exists.
