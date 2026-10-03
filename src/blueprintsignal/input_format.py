"""Friendly spreadsheet layouts for service process data."""
from . import model, portable as io

TABLE_NAMES = {"stages": "Stages", "actions": "Service items", "links": "Handoffs", "hazards": "Failure points", "improvements": "Improvement plans", "sources": "Sources"}
LABELS = {"stage_id": "Stage reference", "lane": "Service layer", "description": "Description", "owner": "Responsible person or team", "minutes": "Time in minutes", "basis": "Evidence status", "evidence_note": "Evidence note", "from_action": "From step", "to_action": "To step", "action_id": "Step reference", "hazard_id": "Failure point reference", "check_date": "Follow-up date"}
INTRO = "Start with a process list: which stage each step belongs to, what happens, and who does it. One row becomes one item on the blueprint."
QUICK = {"process": {"title": "Process steps", "aliases": ["process", "steps", "service", "actions"], "fields": {
    "stage": ("Stage", "text", ["phase", "stage name", "journey stage"]),
    "lane": ("Service layer", "lane", ["lane", "layer", "type"]),
    "description": ("What happens", "text", ["action", "step", "description", "activity"]),
    "owner": ("Responsible person or team", "optional_text", ["owner", "team", "responsible"]),
    "minutes": ("Time in minutes", "optional_number", ["minutes", "duration", "time"]),
    "basis": ("Evidence status", "basis", ["basis", "status"]),
    "evidence_note": ("Evidence note", "optional_text", ["evidence", "note", "notes"]),
}}}
HELP = "Use Customer actions, Visible staff / technology, Backstage actions, Support processes, or Physical / digital evidence for the service layer. Stages follow their first appearance in the file. Without an evidence status, steps are labelled Assumed. Handoffs and improvement plans can be added in Edit & review or the complete workbook."
EXAMPLES = {"process": [
    {"stage": "Arrive", "lane": "Customer actions", "description": "Give booking name", "owner": "Guest", "minutes": None, "basis": "assumed", "evidence_note": "Fictional example"},
    {"stage": "Arrive", "lane": "Visible staff / technology", "description": "Check booking and seat guests", "owner": "Host", "minutes": 4, "basis": "assumed", "evidence_note": "Fictional example"},
    {"stage": "Order", "lane": "Backstage actions", "description": "Prepare the confirmed order", "owner": "Kitchen", "minutes": None, "basis": "assumed", "evidence_note": "Fictional example"},
]}


def build(brief, tables, settings, source):
    d = model.starter(brief)
    rows = tables["process"]
    stages = list(dict.fromkeys(r["stage"] for r in rows))
    ids = {label: f"S{i}" for i, label in enumerate(stages, 1)}
    d["stages"] = [{"id": ids[label], "name": label, "order": i} for i, label in enumerate(stages, 1)]
    d["sources"] = [{"id": "FILE1", "title": source[:300], "url": None, "note": "User-supplied spreadsheet. Its contents and evidence status require review."}]
    d["actions"] = [{"id": f"A{i}", "stage_id": ids[r["stage"]], "lane": r["lane"], "description": r["description"], "owner": r["owner"], "minutes": r["minutes"], "basis": r["basis"], "source_id": "FILE1", "evidence_note": r["evidence_note"]} for i, r in enumerate(rows, 1)]
    if not rows:
        raise io.DataProblem("Add at least one process step to your file.")
    return model.validate(d)
