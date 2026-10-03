# Changelog

All notable changes to Blueprint Signal are documented here.

## [1.1.0] - 2026-10-03

### Changed

- **No app-imposed data limits on your own computer.** File size, rows, columns, sheets, cells, stages, service items, handoffs, failure points, improvement plans, sources and pasted text are limited only by the computer's memory. Running out of memory gives a plain message instead of a crash.
- **Public demo caps** apply only when `SIGNAL_PUBLIC=1` (50 MB uploads; 10,000 rows, 80 columns, 30 sheets and 250,000 cells; 12 stages, 120 service items, 250 handoffs, 120 failure points, 120 plans, 100 sources; 1,000,000 pasted characters). They live in one module, `blueprintsignal.limits`, and every refusal says it is a demo limit.
- Upload cap raised to 10,000 MB in `.streamlit/config.toml`, both launchers (`BLUEPRINTSIGNAL_MAX_UPLOAD_MB`) and the Dockerfile (`STREAMLIT_SERVER_MAX_UPLOAD_SIZE`).
- Large blueprints stay readable: the board shows 12 stages at a time with a selector and a note, and above 300 dependencies the diagram draws plain lines. The handoff review, the standalone board and all exports keep every record.
- Rework loops are found with strongly connected components (linear time) instead of one search per handoff.
- Stage order no longer has an upper bound of 100.

## [1.0.0] - 2026-10-03

First public release.

### Added

- **Service blueprint:** one service across up to 12 stages and 120 service items in five layers (physical or digital evidence, customer actions, visible staff and technology, backstage actions, support processes), separated by the lines of interaction, visibility and internal interaction. Empty cells read "No item supplied"; owners missing on the board read "Owner needed".
- **Evidence labels:** every service item is observed, assumed or proposed, and every failure point observed or assumed. Observed items need a source and an evidence note.
- **Handoffs & improvement:** explicit dependencies with owner changes, layer crossings and rework loops flagged, a dependency diagram with equal-weight links, structural questions to resolve, failure points and improvement plans with owner, measure, target, follow-up date and status.
- Four equal ways to start: an Excel or CSV process list with column matching, a complete project workbook, manual entry in editable tables, and a copy-paste prompt for any AI assistant whose JSON is validated and imported as an unreviewed draft. The app never contacts an AI service.
- One JSON Schema and cross-reference check for every input route, with plain messages when a case exceeds the blueprint's method limits.
- A local review record bound to the inputs by SHA-256; any edit clears it.
- Exports: Excel workbook (re-importable), project JSON, printable HTML brief, evidence ZIP and a standalone board, with spreadsheet-formula neutralisation.
- Research & limits page with verified sources and interpretation boundaries.
- Fictional Fjord Table restaurant demo, preloaded in every session.
- Signal Hub entry point `blueprintsignal.ui.render()` with `APP_INFO`, `blueprint:`-namespaced keys and Hub mode (no file writes, no network calls, opens on the fictional demo, a note that the project lives only in the session).
- Windows and macOS launchers (port 8602, 50 MB uploads, `BLUEPRINTSIGNAL_PORT` and `BLUEPRINTSIGNAL_MAX_UPLOAD_MB`), Dockerfile, `AI_ANALYST.md`, data guide, methods and sources documentation.
