from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from blueprintsignal import __version__, model, portable as io
from blueprintsignal.ui import signal_theme as sig
from blueprintsignal.ui.session import NS, k
from blueprintsignal.ui.workspace import Workspace

PAGES = ["Overview", "1 · Add your data", "2 · Edit & review", "3 · Service blueprint", "4 · Handoffs & improvement",
         "5 · Export", "Research & limits"]


def render() -> None:
    """Draw the whole app on the current page. Never calls st.set_page_config or st.navigation."""
    sig.apply(NS)
    w = Workspace(NS, model)
    sig.sidebar_brand(NS, "Make the service behind the experience visible.")
    pages = PAGES
    with st.sidebar:
        page = st.radio("Navigate", pages, label_visibility="collapsed", key=k("page"))
        st.caption("EXCEL · CSV · MANUAL · OPTIONAL AI")
        if st.button("Reset fictional demo", key=k("reset")):
            w.reset()
            st.rerun()
    sig.masthead(NS, ["Service design", "Visible ownership", "Excel, CSV or AI"])
    w.status()
    try:
        if page == "Overview":
            sig.hero(NS, eyebrow="SERVICE BLUEPRINTING", title="See the whole service.", em="Improve the handoffs.",
                     body="Connect the customer's experience to the people, technology and backstage work that make it happen.",
                     pills=["Editable service layers", "Evidence and assumptions", "Improvement plans"])
            w.welcome()
            sig.cards([("01 / DESCRIBE", "Start with the customer", "Define one service, its boundaries and the customer's intended outcome."),
                       ("02 / MAP", "Expose the handoffs", "Import a process list or structure your notes with AI, then check the steps, ownership and dependencies with the team."),
                       ("03 / IMPROVE", "Make changes testable", "Link failure points to an owner, a measure, a target and a follow-up date.")])
            cols = st.columns(4)
            for col, label, value in zip(cols, ["Stages", "Service items", "Dependencies", "Questions to resolve"], [len(w.d["stages"]), len(w.d["actions"]), len(w.d["links"]), len(model.audit(w.d)["gaps"])]):
                col.metric(label, value)
            st.write("Use Add your data for your own case, or explore the fictional restaurant's service blueprint and rework loop.")
        elif page == pages[1]:
            sig.header("UPLOAD, ENTER OR USE AI", "Your data, your way.", "Start with a spreadsheet, enter steps yourself, or use your AI to structure a process description.")
            w.inputs()
        elif page == pages[2]:
            sig.header("EDIT THE SERVICE", "Confirm the process with the people delivering it.")
            w.edit(model.TITLES)
        elif page == pages[3]:
            sig.header("CUSTOMER → DELIVERY → SUPPORT", "The service blueprint", "Stage columns show sequence; rows show who or what delivers each part.")
            st.text(w.d["brief"])
            st.markdown("<style>.blueprint{overflow-x:auto;margin:20px 0}.blueprint table{border-collapse:collapse;width:100%;font-size:13px}.blueprint th,.blueprint td{padding:10px;border:1px solid #d4c7b2;vertical-align:top;min-width:140px;overflow-wrap:anywhere}.blueprint th{background:#edc8d8}.blueprint .cell{background:#f9f4ed;padding:12px;border-radius:12px;margin-bottom:10px}.blueprint small{color:#645c50}</style>" + model.board(w.d), unsafe_allow_html=True)
            st.caption("Empty cells are unanswered design questions. Explicit dependencies and rework are listed on Handoffs & improvement; adjacency alone does not imply a dependency.")
            st.download_button("Download standalone blueprint", model.printable(w.p), "blueprint-brief.html", "text/html",
                               key=k("board_html"))
        elif page == pages[4]:
            sig.header("OWNERSHIP → FAILURE POINTS → FOLLOW-UP", "Where does the service need attention?")
            result = model.audit(w.d)
            st.subheader("Dependencies and rework")
            if result["handoffs"].empty:
                st.info("No dependencies supplied. Add action-to-action links in Edit & review.")
            else:
                st.dataframe(result["handoffs"], hide_index=True, width="stretch")
                if result["handoffs"].in_rework_loop.any():
                    st.warning("The supplied process contains a rework loop. Review its trigger and ownership; action durations cannot be added into a linear service time.")
                stages = sorted(w.d["stages"], key=lambda x: x["order"])
                stage_x = {s["id"]: i for i, s in enumerate(stages)}
                positions, counts = {}, {}
                for a in w.d["actions"]:
                    cell = (a["stage_id"], a["lane"])
                    offset = counts.get(cell, 0)
                    counts[cell] = offset + 1
                    positions[a["id"]] = (stage_x[a["stage_id"]] + 0.12 * offset, list(model.LANES).index(a["lane"]) + 0.13 * offset)
                fig = go.Figure()
                for link in w.d["links"]:
                    x0, y0 = positions[link["from_action"]]
                    x1, y1 = positions[link["to_action"]]
                    fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#a19786", text="")
                for lane, label in model.LANES.items():
                    rows = [a for a in w.d["actions"] if a["lane"] == lane]
                    fig.add_trace(go.Scatter(x=[positions[a["id"]][0] for a in rows], y=[positions[a["id"]][1] for a in rows],
                                            mode="markers+text", text=[a["id"] for a in rows], textposition="top center", name=label,
                                            hovertext=[escape(a["description"]) for a in rows], hoverinfo="text", marker={"size": 13}))
                fig.update_xaxes(tickvals=list(stage_x.values()), ticktext=[escape(s["name"]) for s in stages])
                fig.update_yaxes(tickvals=list(range(5)), ticktext=list(model.LANES.values()), autorange="reversed")
                fig.update_layout(height=470, showlegend=False)
                sig.chart(NS, fig, key=k("links_chart"))
                st.caption("Each link has equal visual weight. This diagram shows dependencies, not traffic, probability or measured customer flow.")
            st.subheader("Questions to resolve")
            if result["gaps"].empty:
                st.success("No gaps found by these structural checks. Validate the service with customers and staff.")
            else:
                st.dataframe(result["gaps"], hide_index=True, width="stretch")
            st.subheader("Failure points and improvement experiments")
            st.dataframe(pd.DataFrame(w.d["hazards"]), hide_index=True, width="stretch")
            st.dataframe(pd.DataFrame(w.d["improvements"]), hide_index=True, width="stretch")
        elif page == pages[5]:
            w.export(model.printable(w.p), {**model.audit(w.d), **{k: pd.DataFrame(w.d[k]) for k in model.TITLES}})
        else:
            w.research()
    except io.DataProblem as exc:
        st.error(str(exc))
    sig.footer(NS, __version__, "Service design with ownership and evidence")
