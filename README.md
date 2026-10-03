<p align="center">
  <img src="assets/blueprintsignal-banner.png" alt="Blueprint Signal: How is the customer experience actually delivered, and where do the handoffs fail?" width="100%">
</p>

<p align="center">
  <a href="https://github.com/UlrikErlingsen/service-blueprinting/actions"><img alt="Tests" src="https://github.com/UlrikErlingsen/service-blueprinting/actions/workflows/tests.yml/badge.svg"></a>
  <a href="https://github.com/UlrikErlingsen/signal-hub"><img alt="Signal · Customer" src="https://img.shields.io/badge/Signal-Customer-aa5d83?labelColor=2e2b25"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-2e2b25?logo=python&logoColor=f9f4ed">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-app-aa5d83?logo=streamlit&logoColor=f9f4ed">
  <a href="LICENSE"><img alt="License: AGPL-3.0-or-later" src="https://img.shields.io/badge/License-AGPL--3.0--or--later-645c50"></a>
</p>

<p align="center"><strong>Map one service from the customer's actions to the backstage work, and fix the handoffs.</strong></p>

**Blueprint Signal** helps service, customer-experience and marketing teams map how one service is delivered, from what the customer does through visible staff and technology, backstage work and support processes. It combines an editable service blueprint with a handoff review and an improvement plan, and keeps what is evidenced apart from what is assumed or proposed.

> How is the customer experience actually delivered, and where do the handoffs fail?

Everything runs locally with open-source Python packages. There is no account, telemetry, external AI call, remote database, or built-in persistence.

## Read this first

> **A blueprint describes the service as you entered it.** It is not observed process data, a measured customer journey or a causal analysis. Its value comes from the people who deliver the service checking it together.

- **Every service item carries an evidence status.** *Observed* means the author cites a source and writes an evidence note. *Assumed* and *proposed* items stay labelled as such everywhere, including the exports. The app cannot check that a cited source says what the note claims.
- **The handoff review is structural.** It flags dependencies that change owner or cross a service layer, and links that sit in a rework loop. It does not measure how often a handoff fails, how long it takes, or what it costs.
- **"Questions to resolve" are application rules, not a quality score.** Missing owners, stages with no customer action, failure points with no owner or plan, and plans without an owner, measure, target or follow-up date are listed so the team can discuss them. A short list does not mean the service is good.
- **A recorded review is a human check, not independent verification.** It is tied to the exact inputs by a SHA-256 fingerprint, and any edit clears it.

## Scope

**Version 1.0 supports:**

- one service per blueprint, with up to 12 stages, 120 service items, 250 handoffs, 120 failure points, 120 improvement plans and 100 sources;
- five service layers (physical or digital evidence, customer actions, visible staff and technology, backstage actions, support processes) separated by the lines of interaction, visibility and internal interaction;
- four ways to start, on equal footing: an Excel or CSV process list, a complete project workbook, manual entry in editable tables, or a copy-paste prompt for the AI assistant of your choice;
- explicit dependencies between service items, including rework loops, with owner and layer changes flagged;
- failure points linked to service items, and improvement plans with an owner, measure, target, follow-up date and status;
- a local review record bound to the inputs, and Excel, JSON, HTML and ZIP exports.

**It does not:** observe or mine processes from logs, measure customer journeys, time, cost, frequency or failure rates, score service quality, prioritise failure points statistically, simulate queues or capacity, contact an AI service, or scrape the source links you enter. Logged journeys belong in **[Trace Signal](https://github.com/UlrikErlingsen/journey-path-analysis)**, which experiences move with satisfaction in **[Driver Signal](https://github.com/UlrikErlingsen/survey-driver-analysis)**, and testing whether an improvement worked in **[Experiment Signal](https://github.com/UlrikErlingsen/experiment-analysis)**.

## Try the demo in three minutes

1. Start the app. **Overview** opens on a fictional restaurant, Fjord Table: an evening dine-in service from booking to payment in 6 stages, 17 service items and 13 dependencies.
2. Open **3 · Service blueprint** and read the board stage by stage. The dashed rows mark the lines of interaction, visibility and internal interaction; "Owner needed" marks the dish delivery step nobody owns.
3. Open **4 · Handoffs & improvement**. Of the 13 dependencies, 11 change owner, 12 cross a layer and 4 sit in the rework loop that starts when a guest reports a wrong meal. Below them are five questions to resolve, two failure points and one improvement plan.
4. Open **5 · Export** and download the Excel workbook, the project JSON, the printable brief or the evidence ZIP.

The demo is hand-written fictional data. Every step, owner and duration is labelled assumed, and its review is a fictional reviewer's. It represents no real restaurant, customer, course case or empirical finding.

## Data contract

Start from a process list: one row per service item. Excel (.xlsx) and UTF-8 CSV (comma, semicolon or tab delimited) are supported, and you match your own column names to the fields after uploading. The **1 · Add your data** page offers a simple Excel example, a complete example workbook and a CSV example.

| Stage | Service layer | What happens | Responsible person or team | Time in minutes | Evidence status | Evidence note |
|---|---|---|---|---|---|---|
| Arrive | Customer actions | Give booking name | Guest | | assumed | Fictional example |
| Arrive | Visible staff / technology | Check booking and seat guests | Host | 4 | assumed | Fictional example |

- **Required:** stage, service layer and what happens. Stages are ordered by their first appearance in the file.
- **Optional:** owner, minutes (blank stays unknown, never zero), evidence status (`observed`, `assumed` or `proposed`; blank becomes `assumed`) and evidence note. Observed rows need an evidence note.
- **Complete project workbook:** a `Case` sheet with the brief and six linked sheets (Stages, Service items, Handoffs, Failure points, Improvement plans, Sources). The Excel export of any project re-imports as one.
- **AI route:** the app writes a prompt containing the exact JSON schema and your notes. Paste the AI's JSON back; it is validated and imported as an unreviewed draft.

**Limits.** Uploads are capped at 50 MB when run locally. A blueprint itself is limited by method, not file size: one service on one readable board holds at most 12 stages and 120 service items, and the app says so and suggests splitting the service when a file has more. To stop reading early, each sheet is limited to 10,000 rows and 80 columns, a workbook to 30 sheets, and all files together to 250,000 cells.

Files are rejected, with the reason shown, for blank or duplicate column headings, rows with more values than headings, unknown service layers or evidence statuses, negative or non-numeric minutes, formulas without a saved result, Excel error cells, `.xls` files, references that do not resolve, and observed items without a source or note.

See the [data guide](docs/data-guide.md).

## Methods

1. **Validate.** Every case, however it arrives, passes one JSON Schema plus cross-checks: unique IDs and stage orders, every reference resolves, no self-links or duplicate dependencies, finite numbers, public HTTP(S) source links only, and the evidence rules for observed items.
2. **Draw the blueprint.** Stages run left to right; the five service layers run top to bottom with the lines of interaction, visibility and internal interaction between them (Shostack, 1982, 1984; Bitner, Ostrom & Morgan, 2008). Empty cells read "No item supplied": an unanswered design question, not proof that nothing happens.
3. **Review the handoffs.** For each explicit dependency the app reports the two owners, whether the owner changes (compared case-insensitively), whether it crosses a service layer, and whether it sits in a rework loop (the target can reach the source again through the links). A diagram shows the dependencies with equal visual weight.
4. **List questions to resolve.** Fixed rules flag service items without an owner, stages without a customer action, failure points without an owner or a linked plan, and plans missing an owner, measure, target or follow-up date.
5. **Plan improvements.** Failure points (impact low, medium or high, observed or assumed) link to service items; plans link to failure points with an owner, measure, target, date and status.
6. **Review.** A named reviewer records what was checked. The record carries the SHA-256 of the inputs, so an edit or a different file invalidates it.

Action minutes are kept as individual inputs. Parallel work, waiting and rework mean they are never summed into an end-to-end service time.

See [methods](docs/methods.md).

## Decision statuses

Blueprint Signal does not return a go/no-go status or a quality score. It shows:

- **UNREVIEWED DRAFT:** the inputs have changed since the last recorded review, or were never reviewed. Every import starts here.
- **LOCAL REVIEW RECORDED:** a named person recorded a check of exactly these inputs. It does not authenticate the reviewer or recheck sources.
- **QUESTIONS TO RESOLVE:** one or more structural rules flagged a record. Each row names the record and the issue.
- **NO GAPS FOUND BY THESE CHECKS:** none of the rules fired. Validate the service with customers and staff anyway.

## Exports

From **5 · Export**:

- **Excel workbook:** a read-me sheet, the case brief, the six input sheets with readable column names, and the questions to resolve and handoff review as result sheets. It re-imports as a complete project workbook.
- **Project JSON:** the inputs, their origin and the review record. Restoring it is refused if the saved review no longer matches the inputs.
- **Printable brief (HTML):** the blueprint, handoffs, questions to resolve, failure points, improvement plan, service-item evidence and timing, sources, interpretation limits, references and the project fingerprint. Open it in a browser to print or save as PDF.
- **Evidence ZIP:** `project.json`, `brief.html`, `references.json` and one CSV per input and result table.

The **3 · Service blueprint** page also downloads the board on its own. Exports contain everything you entered, including owner names and evidence notes, so treat them like the source material. CSV text that begins with `=`, `+`, `-`, `@`, a tab or a carriage return is prefixed with an apostrophe, and Excel cells are written as text, so nothing is read as a spreadsheet formula.

## Run locally

You need Python 3.10 or newer and a local copy of this folder.

**macOS:** double-click `run_app.command`. **Windows:** double-click `run_app.bat`.

The first launch creates a private `.venv` and downloads open-source dependencies. Later launches reuse it. Or use a terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Then open the local address shown in the terminal. Blueprint Signal prefers local port 8602; the macOS launcher falls back to another free port if it is taken. Both launchers accept `BLUEPRINTSIGNAL_PORT` and `BLUEPRINTSIGNAL_MAX_UPLOAD_MB` (default 50), and the macOS launcher also accepts `BLUEPRINTSIGNAL_NO_BROWSER=1`. The in-app file check follows the server's upload cap.

### Docker

```bash
docker build -t blueprintsignal .
docker run --rm -p 8602:8602 blueprintsignal
```

Then open http://127.0.0.1:8602. The container runs as a non-root user and caps uploads at 50 MB (`STREAMLIT_SERVER_MAX_UPLOAD_SIZE`).

## Privacy

Uploaded files and pasted text are processed in memory by the running Streamlit app; nothing is sent to an external service and nothing is saved to disk, and the AI route is copy and paste only. Inside Signal Hub the app writes no files and makes no network calls; on any hosted deployment the operator is responsible for transport security, access control, logs and retention. See [PRIVACY.md](PRIVACY.md).

## No install? Give this file to an AI

[AI_ANALYST.md](AI_ANALYST.md) is a standalone protocol for a capable AI assistant, with the same service layers, evidence rules, checks and honesty rules. The local app is the more private option: a cloud AI sees whatever you upload or paste.

## Development

```bash
python -m pip install -e ".[test]"
python -m pytest
python -m ruff check .
python -m build
```

The core installs without Streamlit or Plotly; `pip install -e ".[ui]"` adds the app dependencies. Tests cover schema and cross-reference validation, evidence rules, rework-loop detection, the structural checks, review binding and project round trips, markup escaping in the board, spreadsheet mapping and round trips, file and method limits, spreadsheet-safe exports, every Streamlit page, and the Signal Hub contract (`blueprintsignal.ui.render`, namespaced keys, Hub mode, no repo-root file reads).

## Where this fits in Signal

Blueprint Signal shows how a service is meant to be delivered and who owns each handoff. Use **[Trace Signal](https://github.com/UlrikErlingsen/journey-path-analysis)** to see how logged customer journeys actually unfold, **[Driver Signal](https://github.com/UlrikErlingsen/survey-driver-analysis)** to find which measured experiences move with satisfaction, and **[Experiment Signal](https://github.com/UlrikErlingsen/experiment-analysis)** to test whether an improvement made a practical difference.

<!-- signal-suite:start (generated from signal-hub/apps.yaml by scripts/sync_readme_suite.py) -->
| Family | App | Asks |
|---|---|---|
| Brand | [Track Signal](https://github.com/UlrikErlingsen/brand-tracking) | Is the brand moving, or is the tracker just noisy? |
| Brand | [Position Signal](https://github.com/UlrikErlingsen/brand-positioning) | Where do brands sit relative to competitors? |
| Market | [Prospect Signal](https://github.com/UlrikErlingsen/b2b-prospecting) | Which Norwegian companies fit your ideal customer, and which first? |
| Market | [Listen Signal](https://github.com/UlrikErlingsen/media-listening) | Who is talking about the brand in Norwegian media, and in what tone? |
| Market | [Influence Signal](https://github.com/UlrikErlingsen/influencer-campaigns) | Which creators delivered, and was every post labelled properly? |
| Market | [Season Signal](https://github.com/UlrikErlingsen/marketing-calendar) | What does the Norwegian marketing year look like, worked backwards? |
| Market | [Adopt Signal](https://github.com/UlrikErlingsen/adoption-forecasting) | When will a new product be adopted? |
| Market | [Rival Signal](https://github.com/UlrikErlingsen/competitor-analysis) | Which rivals matter, and how could they respond? |
| Market | [Reach Signal](https://github.com/UlrikErlingsen/location-catchment-analysis) | Where could a new location reach, and how would it share demand with existing sites? |
| Customer | [Worth Signal](https://github.com/UlrikErlingsen/customer-value-analytics) | What are customers and relationships worth? |
| Customer | [Segment Signal](https://github.com/UlrikErlingsen/customer-segmentation) | Do customers form stable, useful groups? |
| Customer | [Trace Signal](https://github.com/UlrikErlingsen/journey-path-analysis) | How do logged customer journeys actually unfold? |
| Customer | **Blueprint Signal** (this app) | How is the customer experience actually delivered, and where do the handoffs fail? |
| Customer | [Recommend Signal](https://github.com/UlrikErlingsen/recommender-evaluation) | Which recommendation policy should be tested live? |
| Research | [Choice Signal](https://github.com/UlrikErlingsen/conjoint-analysis) | How do product attributes drive choice? |
| Research | [Driver Signal](https://github.com/UlrikErlingsen/survey-driver-analysis) | Which measured experiences move with satisfaction? |
| Research | [Measure Signal](https://github.com/UlrikErlingsen/measurement-validation) | Does a multi-item score have a defensible structure? |
| Research | [Text Signal](https://github.com/UlrikErlingsen/open-text-analysis) | What recurring patterns appear in open-ended responses? |
| Research | [Tag Signal](https://github.com/UlrikErlingsen/pricing-analysis) | What price range is supported, and how does profit move? |
| Research | [Learn Signal](https://github.com/UlrikErlingsen/research-prioritization) | Which uncertainty is worth paying to research before you decide? |
| Decide | [Experiment Signal](https://github.com/UlrikErlingsen/experiment-analysis) | Did the treatment cause a practically meaningful change? |
| Decide | [Gate Signal](https://github.com/UlrikErlingsen/launch-decision-gate) | Does a concept deserve the next investment? |
| Decide | [Shift Signal](https://github.com/UlrikErlingsen/cannibalization-analysis) | Does a launch grow the portfolio, or move existing demand around? |
| Decide | [Alloc Signal](https://github.com/UlrikErlingsen/marketing-mix-allocation) | Where should the next marketing budget go? |

All 24 apps run side by side in [Signal Hub](https://github.com/UlrikErlingsen/signal-hub), each opening with fictional demo data. Every repo carries the [`signal-suite`](https://github.com/topics/signal-suite) topic, and the suite is listed at [ulrikerlingsen.com](https://ulrikerlingsen.com). Freddo CRM is a separate product.
<!-- signal-suite:end -->

## References

- Bitner, M. J., Ostrom, A. L., & Morgan, F. N. (2008). Service blueprinting: A practical technique for service innovation. *California Management Review, 50*(3), 66–94. https://doi.org/10.2307/41166446
- Shostack, G. L. (1982). How to design a service. *European Journal of Marketing, 16*(1), 49–63. https://doi.org/10.1108/EUM0000000004799
- Shostack, G. L. (1984, January). Designing services that deliver. *Harvard Business Review*. https://hbr.org/1984/01/designing-services-that-deliver

The citations describe the blueprinting technique: the service layers, the lines between them and the idea of locating fail points. None of them validates the app's structural checks, its limits or its evidence labels, which are transparent design choices.

## Originality and license

Blueprint Signal is an independent implementation based on public service-design literature and original synthetic examples. It does not reproduce lecture slides, institution-specific cases, teaching diagrams, exercises, exam questions, screenshots, tables or other institution-specific teaching material. See [sources and originality](docs/sources-and-originality.md).

The software and documentation are free under AGPL-3.0-or-later. The license covers this project's expression, not ownership of published methods.

This application was developed with AI coding assistance and checked through source review, deterministic fixtures, automated app tests and visual inspection. Verify material decisions independently; no warranty is provided.

---

<p>
  <img src="assets/blueprintsignal-mark-64.png" width="20" height="20" alt="" align="absmiddle">
  <strong>Blueprint Signal</strong> is part of <a href="https://github.com/UlrikErlingsen/signal-hub"><strong>Signal</strong></a>, open marketing-evidence tools by <a href="https://ulrikerlingsen.com">Ulrik Erlingsen</a>.
</p>
