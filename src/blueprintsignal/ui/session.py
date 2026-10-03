"""Session namespace and Signal Hub mode, shared by every UI module. Data limits live in blueprintsignal.limits."""
import os

NS = "blueprint"
HUB_NOTE = ("Running in Signal Hub: this project lives only in this browser session and nothing is stored on the "
            "server. Download the project JSON or the Excel workbook to keep your work.")


def k(name: str) -> str:
    """Namespace a widget or session-state key, so Blueprint Signal can share one Streamlit session in Signal Hub."""
    return f"{NS}:{name}"


def in_hub() -> bool:
    """Signal Hub sets SIGNAL_HUB=1 before importing apps. Read it on every call so tests can switch modes."""
    return os.environ.get("SIGNAL_HUB") == "1"

