# Data guide

Blueprint Signal maps one service. You can start from a process list in Excel or CSV, a complete project workbook, manual entry in the app's tables, or a JSON draft from an AI assistant. The **1 · Add your data** page offers a simple Excel example, a complete example workbook built from the fictional demo, and a CSV example. All examples are fictional; replace every row before drawing conclusions.

There are no app-imposed size limits on your own computer (see [Data limits](#data-limits)). Excel files must be `.xlsx`; CSV files must be UTF-8 (a byte-order mark is fine) with a header row and a comma, semicolon or tab delimiter.

## Simple process list: one row per service item

| Stage | Service layer | What happens | Responsible person or team | Time in minutes | Evidence status | Evidence note |
|---|---|---|---|---|---|---|
| Arrive | Customer actions | Give booking name | Guest | | assumed | Fictional example |
| Arrive | Visible staff / technology | Check booking and seat guests | Host | 4 | assumed | Fictional example |
| Order | Backstage actions | Prepare the confirmed order | Kitchen | | assumed | Fictional example |

Your columns can have other names. After uploading, choose **Simple business tables**, then pick the sheet and match each field to a column; the app suggests a column only when the name matches unambiguously.

- **Stage** (required): the phase of the service from the customer's point of view. Stages are numbered in the order they first appear in the file.
- **Service layer** (required): one of `Customer actions`, `Visible staff / technology`, `Backstage actions`, `Support processes` or `Physical / digital evidence`. Short forms such as `customer`, `frontstage`, `front stage`, `visible`, `backstage`, `support` and `evidence` are accepted.
- **What happens** (required): one action or one piece of evidence per row.
- **Responsible person or team** (optional): blank means "Owner needed" on the board and appears under questions to resolve.
- **Time in minutes** (optional): a single action's duration. Blank stays unknown, never zero. Choose dot or comma decimals for numbers stored as text.
- **Evidence status** (optional): `observed`, `assumed` or `proposed`. Blank becomes `assumed`.
- **Evidence note** (optional): what supports the row. Rows marked `observed` need one.

The uploaded file is recorded as the source of every imported row. Handoffs, failure points and improvement plans are added afterwards in **2 · Edit & review**, or supplied in a complete workbook.

## Complete project workbook

The Excel export of any project re-imports as a complete project workbook, so the easiest way to work in Excel is to download a workbook from **5 · Export**, edit it and upload it again. It has a `Case` sheet with one `Case brief` cell and six linked sheets. Reference columns link the sheets; keep them consistent when you rename a record.

| Sheet | Columns | Rows |
|---|---|---|
| Stages | Reference, Name, Order | 1 or more |
| Service items | Reference, Stage reference, Service layer (`evidence`, `customer`, `frontstage`, `backstage`, `support`), Description, Responsible person or team, Time in minutes, Evidence status, Source reference, Evidence note | any |
| Handoffs | Reference, From step, To step, Description | any |
| Failure points | Reference, Step reference, Failure, Impact (`low`, `medium`, `high`), Evidence status (`observed`, `assumed`), Source reference, Responsible person or team | any |
| Improvement plans | Reference, Failure point reference, Change, Responsible person or team, Measure, Target, Follow-up date (YYYY-MM-DD), Status (`proposed`, `testing`, `complete`) | any |
| Sources | Reference, Source title, Source URL, Notes | any |

References start with a letter and use letters, digits, `_` or `-` (at most 40 characters). Stage orders are whole numbers from 1 upwards and must be unique. Source URLs must be public `http` or `https` links, or blank for internal material such as interview notes. Result sheets in an exported workbook are ignored on import, and review records are never imported from Excel.

## AI draft (JSON)

Under **Use your AI**, describe the case and paste any notes or source material. The app writes a prompt with the current case, the exact JSON Schema and rules for the service layers and evidence labels. Copy it into the AI assistant you trust, then paste or upload the JSON it returns. The app never contacts an AI service itself.

The JSON is checked against the same schema and cross-reference rules as any other input, must keep the case brief unchanged, and is imported as an unreviewed draft. Duplicate keys, `NaN` or infinite numbers and anything other than one JSON object are rejected. If validation fails, the app shows the errors and a repair instruction to give back to the AI; your current case is unchanged.

## Data limits

**On your own computer there are no app-imposed limits.** Files, rows, columns, stages, service items, handoffs, failure points, plans and sources are limited only by your computer's memory. Streamlit's upload cap is set to 10,000 MB (`BLUEPRINTSIGNAL_MAX_UPLOAD_MB` in the launchers). If the computer runs out of memory, the app says so plainly instead of crashing.

**Very large blueprints stay readable.** When a blueprint has more than 12 stages, the board shows 12 stages at a time with a selector and a note; with more than 300 dependencies the diagram draws plain lines instead of arrows. The handoff review, questions to resolve, the standalone board download and every export always contain the whole blueprint.

**The public demo has caps** (when the operator sets `SIGNAL_PUBLIC=1`, as the public Signal Hub does): 50 MB of uploads in total; 10,000 rows and 80 columns per sheet, 30 sheets and 250,000 cells across files; 12 stages, 120 service items, 250 handoffs, 120 failure points, 120 improvement plans and 100 sources; a pasted AI reply of 1,000,000 characters and AI notes of 35,000. A refusal says it is a demo limit; the downloaded app has none. All caps live in `src/blueprintsignal/limits.py`.

In the demo the unzipped size of a workbook is also capped at ten times the upload cap and 1,000 archive entries.

## What gets rejected

The file or draft is rejected, with the reason shown and the current case left unchanged, when:

- a used column has no heading, two headings are the same, or a row has more values than headings;
- a required field is empty, a service layer or evidence status is not recognised, or minutes are negative or not a number;
- a formula has no saved result (recalculate and save in Excel first) or a cell holds an Excel error;
- the file is `.xls` (save it as `.xlsx`) or is not a readable workbook or UTF-8 CSV;
- a reference does not resolve, an ID or stage order is repeated, a dependency joins an item to itself or repeats a pair;
- an observed service item has no source or evidence note, or an observed failure point has no source;
- in the public demo only, a demo cap above is exceeded.

## Before you upload

1. Fix the scope: one service, one customer type, one start and end point.
2. Write steps from the customer's point of view first, then add what staff, systems and support processes do behind them.
3. Mark only what you have evidence for as observed, and say what the evidence is.
4. Leave unknown durations and owners blank. The board and the questions to resolve will show them.
5. Check the result with the people who deliver the service before recording a review.
