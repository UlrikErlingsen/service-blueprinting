from copy import deepcopy
from io import BytesIO
import json
from zipfile import ZipFile

import random

import pandas as pd
import pytest

from blueprintsignal import limits, model as m, portable as io


def test_demo_has_explicit_assumptions_and_detects_rework():
    p = m.demo()
    assert io.reviewed(p)
    assert all(a["basis"] == "assumed" for a in p["data"]["actions"])
    results = m.audit(p["data"])
    assert set(results["handoffs"].loc[results["handoffs"].in_rework_loop, "from_action"]) == {"A10", "A12", "A13", "A14"}
    assert "No responsible owner" in list(results["gaps"].issue)
    assert "Improvement missing check_date" in list(results["gaps"].issue)


def test_acyclic_process_and_starter_are_supported():
    d = m.demo()["data"]
    d["links"] = [x for x in d["links"] if x["from_action"] != "A14"]
    assert not m.audit(d)["handoffs"].in_rework_loop.any()
    blank = m.validate(m.starter("New service"))
    assert m.audit(blank)["handoffs"].empty
    assert len(m.audit(blank)["gaps"]) == 1


@pytest.mark.parametrize("mutate", [
    lambda d: d["actions"][0].update(stage_id="missing"),
    lambda d: d["actions"][0].update(minutes=-1),
    lambda d: d["actions"][0].update(minutes=float("nan")),
    lambda d: d["actions"][0].update(basis="observed", source_id=None),
    lambda d: d["actions"][0].update(basis="observed", evidence_note=""),
    lambda d: d["links"][0].update(to_action="missing"),
    lambda d: d["links"][0].update(to_action=d["links"][0]["from_action"]),
    lambda d: d["stages"][1].update(order=1),
    lambda d: d["hazards"][0].update(basis="observed", source_id=None),
    lambda d: d["improvements"][0].update(hazard_id="missing"),
    lambda d: d["sources"][0].update(url="javascript:alert(1)"),
])
def test_inconsistent_data_is_rejected(mutate):
    d = m.demo()["data"]
    mutate(d)
    with pytest.raises(io.DataProblem):
        m.validate(d)


@pytest.mark.parametrize("payload", ['{"x":1,"x":2}', '{"x":NaN}', '{"x":1e999}', '[]', 'not json'])
def test_untrusted_json_rejected(payload):
    with pytest.raises(io.DataProblem):
        io.parse(payload)


def test_review_bound_to_inputs_and_export_roundtrip():
    p = m.demo()
    assert io.restore(io.json_bytes(p), "blueprint", m.validate) == p
    changed = deepcopy(p)
    changed["data"]["actions"][0]["description"] = "Changed activity"
    assert not io.reviewed(changed)
    with pytest.raises(io.DataProblem, match="does not match"):
        io.restore(io.json_bytes(changed), "blueprint", m.validate)
    assert not io.reviewed(io.project("blueprint", p["data"]))
    with pytest.raises(io.DataProblem):
        m.validate(p)
    with ZipFile(BytesIO(io.bundle(p, m.printable(p), m.audit(p["data"]), m.REFERENCES))) as z:
        assert io.restore(z.read("project.json"), "blueprint", m.validate) == p


def test_board_escapes_markup_and_keeps_lines_and_all_stages():
    p = m.demo()
    p["data"]["actions"][0]["description"] = '<img src="https://example.com/x" onerror="alert(1)">'
    html = m.printable(p)
    assert "<img" not in html and "&lt;img" in html
    assert "Line of visibility" in html and "Line of interaction" in html
    assert "No item supplied" in html
    assert "@media print" in html
    assert len(json.loads(io.json_bytes(p))["data"]["stages"]) == 6


def big_case(stages=30, per_stage=14, extra_links=200):
    """A blueprint well beyond every public-demo cap."""
    d = m.starter("Large service")
    d["stages"] = [{"id": f"S{i}", "name": f"Stage {i}", "order": i} for i in range(1, stages + 1)]
    lanes = list(m.LANES)
    d["actions"] = [{"id": f"A{s}_{j}", "stage_id": f"S{s}", "lane": lanes[j % 5], "description": f"Step {j}",
                     "owner": "Team" if j % 3 else "", "minutes": None, "basis": "assumed", "source_id": None,
                     "evidence_note": ""} for s in range(1, stages + 1) for j in range(per_stage)]
    ids = [a["id"] for a in d["actions"]]
    pairs = list(zip(ids, ids[1:])) + [(ids[i + 7], ids[i]) for i in range(0, extra_links * 2, 2)]
    d["links"] = [{"id": f"L{i}", "from_action": a, "to_action": b, "description": "Dependency"}
                  for i, (a, b) in enumerate(pairs, 1)]
    d["hazards"] = [{"id": f"F{i}", "action_id": ids[i], "failure": "Could fail", "impact": "low", "basis": "assumed",
                     "source_id": None, "owner": ""} for i in range(150)]
    d["improvements"] = [{"id": f"I{i}", "hazard_id": f"F{i}", "change": "Change", "owner": "", "measure": "",
                          "target": "", "check_date": None, "status": "proposed"} for i in range(130)]
    d["sources"] = [{"id": f"N{i}", "title": "Note", "url": None, "note": "Internal"} for i in range(110)]
    return d


def test_local_mode_has_no_table_limits(monkeypatch):
    monkeypatch.delenv("SIGNAL_PUBLIC", raising=False)
    d = big_case()
    assert {k: len(d[k]) for k in m.TITLES} == {"stages": 30, "actions": 420, "links": 619, "hazards": 150,
                                                 "improvements": 130, "sources": 110}
    assert all(len(d[k]) > limits.DEMO_TABLES[k] for k in m.TITLES)
    assert m.validate(d) == d
    results = m.audit(d)
    assert len(results["handoffs"]) == 619 and results["handoffs"].in_rework_loop.any()
    full, page = m.printable(io.project("blueprint", d)), m.board(d, {"S1", "S2"})
    assert "Stage 30" in full and "Stage 30" not in page and "Stage 2<" in page


def test_public_demo_enforces_table_caps(monkeypatch):
    monkeypatch.setenv("SIGNAL_PUBLIC", "1")
    with pytest.raises(io.DataProblem, match="the demo takes at most 12") as exc:
        m.validate(big_case())
    assert limits.DEMO_NOTE in str(exc.value)
    assert m.validate(m.demo()["data"])  # the demo itself stays inside the caps


def test_rework_loops_match_brute_force_reachability():
    rng = random.Random(7)
    for _ in range(60):
        nodes = [f"A{i}" for i in range(rng.randint(1, 25))]
        edges = {(rng.choice(nodes), rng.choice(nodes)) for _ in range(rng.randint(0, 40))}
        edges = [(a, b) for a, b in edges if a != b]
        component = m.loop_components(nodes, edges)
        adjacency = {n: [b for a, b in edges if a == n] for n in nodes}

        def reaches(start, end):
            stack, seen = [start], set()
            while stack:
                node = stack.pop()
                if node == end:
                    return True
                if node not in seen:
                    seen.add(node)
                    stack.extend(adjacency[node])
            return False

        for a, b in edges:
            assert (component[a] == component[b]) == reaches(b, a)


def test_json_has_no_local_size_limit_but_a_public_demo_cap(monkeypatch):
    payload = '{"x": "' + "a" * (limits.DEMO_UPLOAD_BYTES + 10) + '"}'
    monkeypatch.delenv("SIGNAL_PUBLIC", raising=False)
    assert len(io.parse(payload)["x"]) == limits.DEMO_UPLOAD_BYTES + 10
    monkeypatch.setenv("SIGNAL_PUBLIC", "1")
    with pytest.raises(io.DataProblem, match="public demo"):
        io.parse(payload)


def test_csv_text_is_neutralised():
    raw = io.csv_bytes(pd.DataFrame({"text": ["=1+1", "\tcmd", " @x", "plain"]})).decode("utf-8-sig")
    assert "'=1+1" in raw and "'\tcmd" in raw and "' @x" in raw and "\nplain" in raw.replace("\r", "")
