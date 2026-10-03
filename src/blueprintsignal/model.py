"""Service blueprint structure. Audits describe the supplied design, not measured failure rates."""
from html import escape

import pandas as pd

from blueprintsignal import limits, portable as io

LANES = {"evidence": "Physical / digital evidence", "customer": "Customer actions", "frontstage": "Visible staff / technology",
         "backstage": "Backstage actions", "support": "Support processes"}
NULL_TEXT = {"anyOf": [io.text(120), {"type": "null"}]}
STAGE = io.obj({"id": io.ID, "name": io.text(100), "order": {"type": "integer", "minimum": 1}})
ACTION = io.obj({"id": io.ID, "stage_id": io.ID, "lane": {"enum": list(LANES)}, "description": io.text(700),
                 "owner": io.text(120, True), "minutes": io.number(0, 100000, True),
                 "basis": {"enum": ["observed", "assumed", "proposed"]}, "source_id": NULL_TEXT, "evidence_note": io.text(1000, True)})
LINK = io.obj({"id": io.ID, "from_action": io.ID, "to_action": io.ID, "description": io.text(500)})
HAZARD = io.obj({"id": io.ID, "action_id": io.ID, "failure": io.text(700), "impact": {"enum": ["low", "medium", "high"]},
                "basis": {"enum": ["observed", "assumed"]}, "source_id": NULL_TEXT, "owner": io.text(120, True)})
PLAN = io.obj({"id": io.ID, "hazard_id": io.ID, "change": io.text(700), "owner": io.text(120, True),
              "measure": io.text(400, True), "target": io.text(400, True),
              "check_date": {"anyOf": [io.DATE, {"type": "null"}]}, "status": {"enum": ["proposed", "testing", "complete"]}})
SCHEMA = io.obj({"schema_version": {"const": "1.0"}, "brief": io.text(2500), "stages": io.array(STAGE, 1),
                 "actions": io.array(ACTION), "links": io.array(LINK), "hazards": io.array(HAZARD),
                 "improvements": io.array(PLAN), "sources": io.array(io.SOURCE)})
TITLES = {"stages": "Stages · chronological order", "actions": "Actions and visible evidence · one item per row",
          "links": "Dependencies and handoffs · action IDs", "hazards": "Potential failure points",
          "improvements": "Improvement experiments", "sources": "Sources or supplied process notes"}
REFERENCES = [("Shostack, G. L. (1982). How to design a service. European Journal of Marketing, 16(1), 49–63.",
               "https://doi.org/10.1108/EUM0000000004799"),
              ("Shostack, G. L. (1984). Designing services that deliver. Harvard Business Review, January 1984.",
               "https://hbr.org/1984/01/designing-services-that-deliver"),
              ("Bitner, M. J., Ostrom, A. L., & Morgan, F. N. (2008). Service blueprinting: A practical technique for service "
               "innovation. California Management Review, 50(3), 66–94.", "https://doi.org/10.2307/41166446")]
METHOD = ("A service blueprint connects customer actions to visible service delivery, backstage work, support processes and tangible evidence. "
          "The diagram separates interaction, visibility and internal interaction. Stages are ordered by the user; explicit links record dependencies, including rework. "
          "The audits are application rules that identify missing ownership, missing evidence and incomplete follow-up plans. They are not a validated quality score.")
LIMITS = ["The board describes one declared service scope; it is not a measured customer journey or a causal analysis.",
          "Observed means the author cites evidence. Local review records a human check, not independent verification.",
          "Assumed and proposed steps remain labelled. An empty cell means no item was supplied, not proof that no activity exists.",
          "Action minutes are individual inputs. Parallel work, waiting and rework mean they cannot simply be summed into end-to-end time.",
          "Impact categories are ordinal discussion labels. Counts of gaps and hazards are not probabilities or a service-quality index.",
          "Trace Signal can supply observed journey evidence. Blueprint adds service responsibilities, dependencies and redesign plans."]
AI_RULES = ("Use the five lanes evidence, customer, frontstage, backstage, support. Separate customer-visible work from backstage work. "
            "Use assumed or proposed for unverified descriptions. Observed actions need a cited source and an evidence note; observed hazards need a source. "
            "Use null for unknown action minutes and source IDs. Preserve genuine rework links instead of forcing a linear process. "
            "Propose improvement measures but do not invent owners, observed durations, deadlines or completed work.")
REVIEW_GUIDANCE = "Check the process with the people delivering it. Confirm owners, lane placement, source alignment and whether each step is observed, assumed or proposed."


# The board shows this many stages at once; larger blueprints are paged on screen, never cut in exports.
BOARD_PAGE_STAGES = 12


def check_capacity(data):
    """Public demo only: refuse oversized cases with a plain message. Locally there is no table limit."""
    if not isinstance(data, dict):
        return
    for name in TITLES:
        cap, rows = limits.table(name), data.get(name)
        if cap is not None and isinstance(rows, list) and len(rows) > cap:
            raise io.DataProblem(limits.demo(
                f"This case has {len(rows):,} {limits.TABLE_NAMES[name]}; the demo takes at most {cap}."))


def validate(data):
    check_capacity(data)
    d = io.validate_schema(data, SCHEMA)
    stages, actions, sources = [io.unique(d[k]) for k in ["stages", "actions", "sources"]]
    io.unique(d["stages"], "order")
    hazards = io.unique(d["hazards"])
    io.unique(d["links"])
    io.unique(d["improvements"])
    for a in d["actions"]:
        if a["stage_id"] not in stages:
            raise io.DataProblem(f"Action {a['id']} refers to a missing stage.")
        if a["source_id"] and a["source_id"] not in sources:
            raise io.DataProblem("An action refers to a missing source.")
        if a["basis"] == "observed" and (not a["source_id"] or not a["evidence_note"].strip()):
            raise io.DataProblem("Observed actions need a source ID and an evidence note. Otherwise label them assumed or proposed.")
    edges = set()
    for link in d["links"]:
        if link["from_action"] not in actions or link["to_action"] not in actions:
            raise io.DataProblem("A dependency refers to a missing action.")
        edge = (link["from_action"], link["to_action"])
        if edge[0] == edge[1] or edge in edges:
            raise io.DataProblem("Dependencies must join different actions without duplicate pairs.")
        edges.add(edge)
    for h in d["hazards"]:
        if h["action_id"] not in actions or (h["source_id"] and h["source_id"] not in sources):
            raise io.DataProblem("A failure point refers to a missing action or source.")
        if h["basis"] == "observed" and not h["source_id"]:
            raise io.DataProblem("Observed failure points need a source; otherwise label them assumed.")
    for plan in d["improvements"]:
        if plan["hazard_id"] not in hazards:
            raise io.DataProblem("An improvement refers to a missing failure point.")
    return d


def starter(brief):
    return {"schema_version": "1.0", "brief": brief, "stages": [{"id": "S1", "name": "Start", "order": 1}],
            "actions": [], "links": [], "hazards": [], "improvements": [], "sources": []}


def demo():
    d = starter("FICTIONAL DEMO: Fjord Table restaurant. Map the evening dine-in service from booking to payment and examine the kitchen-to-table handoff.")
    d["stages"] = [{"id": f"S{i}", "name": label, "order": i} for i, label in enumerate(["Book", "Arrive", "Order", "Prepare", "Serve", "Pay"], 1)]
    d["sources"] = [{"id": "N1", "title": "Fictional staff walkthrough", "url": None, "note": "Invented training example. No real restaurant or customer was observed."}]
    rows = [
        ("S1", "evidence", "Booking confirmation", "Booking system", None), ("S1", "customer", "Reserve a table", "Guest", 3),
        ("S1", "support", "Record reservation and dietary notes", "Booking system", None),
        ("S2", "customer", "Arrive and give booking name", "Guest", 1), ("S2", "frontstage", "Confirm booking and seat guests", "Host", 4),
        ("S3", "evidence", "Menu and allergen information", "Menu owner", None), ("S3", "customer", "Choose a meal and explain dietary needs", "Guest", 8),
        ("S3", "frontstage", "Confirm order and dietary requirements", "Server", 4), ("S3", "support", "Send the order ticket to kitchen", "POS system", 1),
        ("S4", "backstage", "Prepare dishes against the order ticket", "Kitchen lead", 18), ("S4", "support", "Keep ingredient and allergen records current", "Kitchen lead", None),
        ("S5", "backstage", "Check the completed ticket and mark ready", "Kitchen lead", 2),
        ("S5", "frontstage", "Collect and deliver dishes to the correct table", "", 3), ("S5", "customer", "Receive and check the meal", "Guest", 1),
        ("S6", "customer", "Request bill and pay", "Guest", 3), ("S6", "frontstage", "Confirm bill, take payment and say goodbye", "Server", 4),
        ("S6", "evidence", "Itemized receipt", "POS system", None)]
    d["actions"] = [{"id": f"A{i}", "stage_id": s, "lane": lane, "description": desc, "owner": owner, "minutes": minutes,
                     "basis": "assumed", "source_id": "N1", "evidence_note": "Illustrative service design and durations, not measurements."}
                    for i, (s, lane, desc, owner, minutes) in enumerate(rows, 1)]
    pairs = [(2,3), (3,5), (4,5), (7,8), (8,9), (9,10), (11,10), (10,12), (12,13), (13,14), (14,10), (15,16), (16,17)]
    d["links"] = [{"id": f"L{i}", "from_action": f"A{a}", "to_action": f"A{b}", "description": "Rework if meal is wrong" if (a,b)==(14,10) else "Service dependency"} for i,(a,b) in enumerate(pairs,1)]
    d["hazards"] = [
        {"id": "F1", "action_id": "A13", "failure": "Dishes wait at the pass because no one owns collection.", "impact": "high", "basis": "assumed", "source_id": "N1", "owner": "Shift manager"},
        {"id": "F2", "action_id": "A9", "failure": "Dietary notes are lost between the server and kitchen ticket.", "impact": "high", "basis": "assumed", "source_id": "N1", "owner": ""}]
    d["improvements"] = [{"id": "I1", "hazard_id": "F1", "change": "Trial a named pass runner during peak service.", "owner": "Shift manager",
                          "measure": "Time from ready ticket to delivery", "target": "Agree a baseline and target before the trial", "check_date": None, "status": "proposed"}]
    return io.accept(io.project("blueprint", validate(d), "FICTIONAL DEMO — all processes and review decisions are illustrative"),
                     "Fictional reviewer", "Checked example structure only. All steps and timings remain assumptions.")


def loop_components(nodes, links):
    """Strongly connected components (iterative Tarjan), linear in items + links.

    A link a -> b lies in a rework loop exactly when b can reach a again, i.e. when a and b share a component.
    """
    adjacency = {node: [] for node in nodes}
    for a, b in links:
        adjacency[a].append(b)
    index, low, component, on_stack, stack, counter = {}, {}, {}, set(), [], 0
    for root in nodes:
        if root in index:
            continue
        work = [(root, 0)]
        while work:
            node, i = work.pop()
            if i == 0:
                index[node] = low[node] = counter
                counter += 1
                stack.append(node)
                on_stack.add(node)
            if i < len(adjacency[node]):
                work.append((node, i + 1))
                nxt = adjacency[node][i]
                if nxt not in index:
                    work.append((nxt, 0))
                elif nxt in on_stack:
                    low[node] = min(low[node], index[nxt])
                continue
            if low[node] == index[node]:
                while True:
                    member = stack.pop()
                    on_stack.discard(member)
                    component[member] = node
                    if member == node:
                        break
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[node])
    return component


def audit(d):
    actions = {a["id"]: a for a in d["actions"]}
    gaps = []
    for a in d["actions"]:
        if not a["owner"].strip():
            gaps.append({"record": a["id"], "issue": "No responsible owner", "detail": a["description"]})
    with_customer = {a["stage_id"] for a in d["actions"] if a["lane"] == "customer"}
    for stage in d["stages"]:
        if stage["id"] not in with_customer:
            gaps.append({"record": stage["id"], "issue": "No customer action supplied", "detail": stage["name"]})
    planned = {plan["hazard_id"] for plan in d["improvements"]}
    for h in d["hazards"]:
        if not h["owner"].strip():
            gaps.append({"record": h["id"], "issue": "Failure point has no owner", "detail": h["failure"]})
        if h["id"] not in planned:
            gaps.append({"record": h["id"], "issue": "No improvement linked", "detail": h["failure"]})
    for plan in d["improvements"]:
        for field in ["owner", "measure", "target", "check_date"]:
            if not plan[field] or not str(plan[field]).strip():
                gaps.append({"record": plan["id"], "issue": "Improvement missing " + field, "detail": plan["change"]})
    component = loop_components(list(actions), [(x["from_action"], x["to_action"]) for x in d["links"]])
    handoffs = []
    for link in d["links"]:
        a, b = actions[link["from_action"]], actions[link["to_action"]]
        handoffs.append({**link, "from_owner": a["owner"] or "Unassigned", "to_owner": b["owner"] or "Unassigned",
                         "changes_owner": a["owner"].strip().casefold() != b["owner"].strip().casefold(),
                         "crosses_lane": a["lane"] != b["lane"],
                         "in_rework_loop": component[a["id"]] == component[b["id"]]})
    return {"gaps": pd.DataFrame(gaps, columns=["record", "issue", "detail"]),
            "handoffs": pd.DataFrame(handoffs, columns=list(LINK["properties"]) + ["from_owner", "to_owner", "changes_owner", "crosses_lane", "in_rework_loop"])}


def ordered_stages(d):
    return sorted(d["stages"], key=lambda s: s["order"])


def board(d, stage_ids=None):
    """The blueprint as an HTML table. stage_ids limits it to some stages (on-screen paging); exports pass None."""
    e = escape
    stages = [s for s in ordered_stages(d) if stage_ids is None or s["id"] in stage_ids]
    cells = {}
    for a in d["actions"]:
        cells.setdefault((a["stage_id"], a["lane"]), []).append(a)
    parts = ["<div class='blueprint'><table><thead><tr><th>Service layer</th>"]
    parts.extend(f"<th>{e(s['name'])}<br><small>{e(s['id'])}</small></th>" for s in stages)
    parts.append("</tr></thead><tbody>")
    boundaries = {"customer": "Line of interaction", "frontstage": "Line of visibility", "backstage": "Line of internal interaction"}
    for lane, title in LANES.items():
        parts.append(f"<tr><th>{title}</th>")
        for stage in stages:
            rows = cells.get((stage["id"], lane), [])
            parts.append("<td>" + ("".join(f"<div class='cell'><b>{e(a['id'])}</b> · {e(a['description'])}<br><small>{e(a['owner'] or 'Owner needed')} · {e(a['basis'])}</small></div>" for a in rows) or "<small>No item supplied</small>") + "</td>")
        parts.append("</tr>")
        if lane in boundaries:
            parts.append(f"<tr><td colspan='{len(stages)+1}' style='border-top:2px dashed #aa5d83;color:#894166'>{boundaries[lane]}</td></tr>")
    parts.append("</tbody></table></div>")
    return "".join(parts)


def printable(p):
    d = p["data"]
    results = audit(d)
    sections = [("Service blueprint", board(d)), ("Handoffs and dependencies", results["handoffs"]), ("Gaps to examine", results["gaps"]),
                ("Failure points", pd.DataFrame(d["hazards"])), ("Improvement plan", pd.DataFrame(d["improvements"])), ("Action evidence and timing", pd.DataFrame(d["actions"]))]
    return io.report("Blueprint Signal · service design brief", p, sections, REFERENCES, LIMITS)
