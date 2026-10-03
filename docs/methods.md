# Methods

Blueprint Signal structures a description of one service and checks it for gaps. It does not estimate anything from data: every count it shows is a count of records you supplied.

## 1. The case

A case has a brief (the service, its boundaries and the question) and six linked tables:

- **Stages:** the service's phases from the customer's point of view, ordered explicitly.
- **Service items:** one action or piece of evidence each, placed in a stage and a service layer, with an owner, an optional duration, an evidence status, an optional source and an evidence note.
- **Handoffs:** explicit dependencies from one service item to another, with a description. Rework links that point back to an earlier item are allowed.
- **Failure points:** what can go wrong at a service item, with an ordinal impact (low, medium, high), an evidence status, an optional source and an owner.
- **Improvement plans:** a change linked to a failure point, with an owner, a measure, a target, a follow-up date and a status.
- **Sources:** the material behind observed items, with a public link or none for internal notes.

There are no table limits on your own computer. A blueprint is easiest to discuss when it fits on one board, so the board shows 12 stages at a time when there are more; the analysis and exports always use every record. The public demo caps table sizes (see the [data guide](data-guide.md#data-limits)).

## 2. Validation

Every input route (spreadsheet, manual edit, AI JSON, restored project) passes the same checks before it replaces the current case:

1. a JSON Schema (Draft 2020-12) for types, required fields, text lengths, allowed values and dates (table sizes are checked only in the public demo);
2. finite numbers only; missing numbers are `null`, never `NaN` or zero;
3. unique IDs in every table and unique stage orders;
4. every stage, service item, failure point and source reference resolves;
5. a handoff joins two different items and each ordered pair appears once;
6. an observed service item has a source and an evidence note; an observed failure point has a source;
7. source links are public `http`/`https` addresses without credentials (no local, internal or private hosts), or empty.

A rejected input leaves the current case unchanged.

## 3. The blueprint

Stages run left to right in their declared order. Rows are the five service layers in the order used by Bitner, Ostrom and Morgan (2008):

1. physical or digital evidence;
2. customer actions;
3. visible staff and technology (onstage);
4. backstage actions;
5. support processes.

Three dashed lines separate them: the **line of interaction** below customer actions, the **line of visibility** below visible staff and technology, and the **line of internal interaction** below backstage actions. Each cell lists its items with ID, description, owner (or "Owner needed") and evidence status. An empty cell reads "No item supplied": an unanswered design question, not proof that nothing happens there. Adjacent cells are not treated as dependent; only explicit handoffs are.

## 4. Handoff review

For each handoff from item *a* to item *b* the app reports:

- the owner of each side ("Unassigned" when blank);
- **changes owner:** the two owners differ after trimming and case-folding;
- **crosses layer:** *a* and *b* sit in different service layers;
- **in rework loop:** *b* can reach *a* again by following handoffs. The app finds this with strongly connected components (Tarjan's algorithm), which takes time proportional to items plus handoffs, so very large blueprints stay fast.

When any handoff is in a loop, the app warns that action durations cannot be added into a linear service time. The dependency diagram places items by stage and layer and draws every handoff with the same weight (as plain lines without arrowheads above 300 handoffs): it shows structure, not traffic, probability or measured customer flow.

## 5. Questions to resolve

Fixed rules list records for discussion:

| Rule | Record |
|---|---|
| No responsible owner | a service item with a blank owner |
| No customer action supplied | a stage with no item in the customer layer |
| Failure point has no owner | a failure point with a blank owner |
| No improvement linked | a failure point that no plan refers to |
| Improvement missing owner, measure, target or check date | a plan with that field blank |

The rules are application choices. They are not drawn from a validated instrument, are not weighted, and their count is not a quality index. An empty list means none of these rules fired, nothing more.

## 6. Failure points and improvement plans

Failure points follow Shostack's (1984) idea of marking where a service can fail, attached here to a specific service item. Impact is an ordinal discussion label. Plans make a change testable by naming who owns it, what will be measured, the target and when it will be checked. The app does not rank failure points, estimate their likelihood or evaluate whether a plan worked; a randomised or before-and-after test of the change belongs in a separate study.

## 7. Review and provenance

A review records a reviewer's name, what they checked and the date, together with the SHA-256 fingerprint of the case data. The case counts as reviewed only while the fingerprint still matches, so any edit, import or restore of different data returns it to an unreviewed draft. A saved project whose review does not match its data is refused on restore. The review does not authenticate the reviewer or recheck the sources.

Each project also carries its origin (fictional demo, spreadsheet draft with file names, manual case, AI draft, edited case), shown at the top of every page and in the exports.

## 8. Durations

Minutes belong to individual service items. Parallel work, waiting and rework mean they cannot be summed into an end-to-end service time, and the app never does so.

## Evidence pack

**5 · Export** produces an Excel workbook (inputs plus questions to resolve and handoff review), the project JSON, a printable HTML brief and a ZIP with `project.json`, `brief.html`, `references.json` and one CSV per table. CSV text that starts with `=`, `+`, `-`, `@`, a tab or a carriage return is prefixed with an apostrophe, and Excel cells are written as text.
