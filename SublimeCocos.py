import sublime
import sublime_plugin

import os
import json
from string import Template
import subprocess

from .core import persist, util

def plugin_loaded():
    """The ST3 entry point for plugins."""
    persist.plugin_is_loaded = True
    persist.settings.load()

    persist.settings.on_update_call(SublimeCocos.on_settings_updated)

class SublimeCocos(sublime_plugin.EventListener):
    """The main ST3 plugin class."""

    @classmethod
    def on_settings_updated(cls, relint=False):
        """Callback triggered when the settings are updated."""

class SublimecocosCommand(sublime_plugin.TextCommand):
    """A plugin command used to generate an edit object for a view."""
    def run(self, edit):
        """Run the command."""

