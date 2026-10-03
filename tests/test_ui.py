from pathlib import Path
import json

import pytest
from streamlit.testing.v1 import AppTest
from blueprintsignal import portable as io

APP = Path(__file__).resolve().parents[1] / "app.py"


def open_page(a, i):
    a.sidebar.radio[0].set_value(a.sidebar.radio[0].options[i]).run()
    assert not a.exception


@pytest.mark.parametrize("i", range(7))
def test_pages_render(i):
    a = AppTest.from_file(str(APP), default_timeout=30).run()
    open_page(a, i)
    assert not a.error


def test_import_review_and_edit_invalidates_review():
    a = AppTest.from_file(str(APP), default_timeout=30).run()
    d = a.session_state["blueprint:project"]["data"]
    open_page(a, 1)
    a.radio(key="blueprint:input_mode").set_value("Use your AI").run()
    a.text_area(key="blueprint:ai_json").set_value(json.dumps(d))
    a.button(key="blueprint:import").click().run()
    assert not io.reviewed(a.session_state["blueprint:project"])
    open_page(a, 2)
    next(x for x in a.text_input if x.label == "Reviewed by").set_value("Test reviewer")
    next(x for x in a.text_area if x.label == "What did you check?").set_value("Staff confirmed the process and assumptions.")
    a.checkbox[0].check()
    next(x for x in a.button if x.label == "Record review").click().run()
    assert not a.exception and io.reviewed(a.session_state["blueprint:project"])
    next(x for x in a.button if x.label == "Save edited inputs").click().run()
    assert not a.exception and not a.error
    assert not io.reviewed(a.session_state["blueprint:project"])


def test_blank_case_flow_and_invalid_ai_is_non_destructive():
    a = AppTest.from_file(str(APP), default_timeout=30).run()
    open_page(a, 1)
    a.radio(key="blueprint:input_mode").set_value("Use your AI").run()
    next(x for x in a.text_area if x.label == "Your business, question and scope").set_value("Customer onboarding for our service")
    next(x for x in a.button if x.label == "Start blank case").click().run()
    p = a.session_state["blueprint:project"]
    assert p["data"]["actions"] == []
    a.text_area(key="blueprint:ai_json").set_value("bad json")
    a.button(key="blueprint:import").click().run()
    assert a.error and not a.exception
    assert a.session_state["blueprint:project"] == p
    for i in [2, 3, 4, 5]:
        open_page(a, i)
        assert not a.error
