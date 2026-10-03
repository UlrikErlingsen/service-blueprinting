"""Every data limit in Blueprint Signal, in one place.

On someone's own computer (standalone, a local Hub, an internal deployment) there are no app-imposed limits: the
machine's memory is the limit. A public demo sets SIGNAL_PUBLIC=1, and only then do the caps below apply, to protect
a shared server. The environment is read on every call, so tests and the Hub can switch modes.
"""
import os

MB = 1024 * 1024

# Public-demo caps. They are generous for one service and only apply when SIGNAL_PUBLIC=1.
DEMO_UPLOAD_BYTES = 50 * MB
DEMO_ROWS = 10_000            # per sheet or CSV
DEMO_COLUMNS = 80
DEMO_SHEETS = 30
DEMO_CELLS = 250_000          # across all uploaded files
DEMO_UNZIPPED_FACTOR = 10     # an .xlsx may expand to ten times the upload cap
DEMO_ZIP_ENTRIES = 1000
DEMO_PASTED_CHARS = 1_000_000  # a pasted AI reply
DEMO_NOTES_CHARS = 35_000      # notes for the AI prompt
DEMO_TABLES = {"stages": 12, "actions": 120, "links": 250, "hazards": 120, "improvements": 120, "sources": 100}
TABLE_NAMES = {"stages": "stages", "actions": "service items", "links": "handoffs", "hazards": "failure points",
               "improvements": "improvement plans", "sources": "sources"}

DEMO_NOTE = "This is a limit of the public demo; the downloaded app has none."
MEMORY_NOTE = ("There is not enough memory on this computer for this input. Close other programs, or split the "
               "service into several blueprints.")


def public() -> bool:
    return os.environ.get("SIGNAL_PUBLIC") == "1"


def _cap(value):
    return value if public() else None


def upload_bytes():
    """Total bytes of uploaded spreadsheets or JSON, or None when unlimited."""
    return _cap(DEMO_UPLOAD_BYTES)


def rows():
    return _cap(DEMO_ROWS)


def columns():
    return _cap(DEMO_COLUMNS)


def sheets():
    return _cap(DEMO_SHEETS)


def cells():
    return _cap(DEMO_CELLS)


def unzipped_bytes():
    return _cap(DEMO_UNZIPPED_FACTOR * DEMO_UPLOAD_BYTES)


def zip_entries():
    return _cap(DEMO_ZIP_ENTRIES)


def pasted_chars():
    return _cap(DEMO_PASTED_CHARS)


def notes_chars():
    return _cap(DEMO_NOTES_CHARS)


def table(name):
    """Maximum records in one blueprint table, or None when unlimited."""
    return _cap(DEMO_TABLES[name])


def demo(message: str) -> str:
    """Append the standard demo-limit sentence to a refusal."""
    return f"{message} {DEMO_NOTE}"


def megabytes(value: int) -> str:
    return f"{value / MB:g} MB"
