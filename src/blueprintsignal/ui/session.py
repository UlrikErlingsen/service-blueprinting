"""Session namespace, Signal Hub mode and the upload limit, shared by every UI module."""
import os

import streamlit as st

NS = "blueprint"
DEFAULT_UPLOAD_MB = 50
HUB_NOTE = ("Running in Signal Hub: this project lives only in this browser session and nothing is stored on the "
            "server. Download the project JSON or the Excel workbook to keep your work.")


def k(name: str) -> str:
    """Namespace a widget or session-state key, so Blueprint Signal can share one Streamlit session in Signal Hub."""
    return f"{NS}:{name}"


def in_hub() -> bool:
    """Signal Hub sets SIGNAL_HUB=1 before importing apps. Read it on every call so tests can switch modes."""
    return os.environ.get("SIGNAL_HUB") == "1"


def upload_limit_bytes() -> int:
    """The running server's upload cap (server.maxUploadSize, in MB), so in-app checks never undercut it."""
    try:
        megabytes = float(st.get_option("server.maxUploadSize"))
    except (TypeError, ValueError, RuntimeError):
        megabytes = DEFAULT_UPLOAD_MB
    return int(max(1.0, megabytes) * 1024 * 1024)
