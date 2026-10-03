"""Blueprint Signal's Streamlit UI. Signal Hub imports render() and APP_INFO from here."""
from blueprintsignal import __version__
from blueprintsignal.ui import signal_theme
from blueprintsignal.ui.app import render

APP_INFO = {"product": "Blueprint Signal", "version": __version__, "repo": "service-blueprinting", "slug": "blueprint"}

__all__ = ["APP_INFO", "render", "signal_theme"]
