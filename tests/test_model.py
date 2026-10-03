from copy import deepcopy
from io import BytesIO
import json
from zipfile import ZipFile

import pytest

from blueprintsignal import model as m, portable as io


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
