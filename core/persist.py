# -*- coding: utf-8 -*-
# @Author: captain
# @Date:   2016-08-27 00:35:28
# @Last Modified by:   captain
# @Last Modified time: 2016-09-13 00:54:38

from collections import defaultdict
from copy import deepcopy
import json
import os
import re
import sublime
import sys
from string import Template

from . import util

class Settings:
    """This class provides global access to and management of plugin settings."""
    def __init__(self):
        """Initialize a new instance."""
        self.settings = {}
        self.previous_settings = {}
        self.changeset = set()
        self.plugin_settings = None
        self.on_update_callback = None

    def load(self, force=False):
        """Load the plugin settings."""
        if force or not self.settings:
            self.observe()
            self.on_update()

    def has_setting(self, setting):
        """Return whether the given setting exists."""
        return setting in self.settings

    def get(self, setting, default=None):
        """Return a plugin setting, defaulting to default if not found."""
        return self.settings.get(setting, default)

    def set(self, setting, value, changed=False):
        """
        Set a plugin setting to the given value.

        Clients of this module should always call this method to set a value
        instead of doing settings['foo'] = 'bar'.

        If the caller knows for certain that the value has changed,
        they should pass changed=True.

        """

        self.copy()
        self.settings[setting] = value

        if changed:
            self.changeset.add(setting)

    def pop(self, setting, default=None):
        """
        Remove a given setting and return default if it is not in self.settings.

        Clients of this module should always call this method to pop a value
        instead of doing settings.pop('foo').

        """

        self.copy()
        return self.settings.pop(setting, default)

    def copy(self):
        """Save a copy of the plugin settings."""
        self.previous_settings = deepcopy(self.settings)

    def observe(self, observer=None):
        """Observer changes to the plugin settings."""
        self.plugin_settings = sublime.load_settings('SublimeCocos.sublime-settings')
        self.plugin_settings.clear_on_change('sublimecocos-change-settings')
        self.plugin_settings.add_on_change('sublimecocos-change-settings', observer or self.on_update)

    def on_update_call(self, callback):
        """Set a callback to call when user settings are updated."""
        self.on_update_callback = callback

    def on_update(self):
        """
        Update state when the user settings change.

        The settings before the change are compared with the new settings.
        Depending on what changes, views will either be redrawn or relinted.

        """

        settings = util.merge_user_settings(self.plugin_settings)
        self.settings.clear()
        self.settings.update(settings)

        if ('cocos_path' in self.changeset or (self.previous_settings.get('cocos_path') != self.settings.get('cocos_path'))):
            self.changeset.discard('cocos_path')

        if ('cocos_simulator_path' in self.changeset or (self.previous_settings.get('cocos_simulator_path') != self.settings.get('cocos_simulator_path'))):
            self.changeset.discard('cocos_simulator_path')

        if ('game_doc_path' in self.changeset or (self.previous_settings.get('game_doc_path') != self.settings.get('game_doc_path'))):
            self.changeset.discard('game_doc_path')

        if ('game_arts_path' in self.changeset or (self.previous_settings.get('game_arts_path') != self.settings.get('game_arts_path'))):
            self.changeset.discard('game_arts_path')

        if ('game_projects_path' in self.changeset or (self.previous_settings.get('game_projects_path') != self.settings.get('game_projects_path'))):
            self.changeset.discard('game_projects_path')

        if ('projects' in self.changeset or (self.previous_settings.get('projects') != self.settings.get('projects'))):
            self.changeset.discard('projects')

        projects = self.settings.get('projects')

        util.PROJECT_DESC = []
        util.auto_generate_projects_desc(projects)
        util.auto_generate_menu(projects)

    def save(self, view=None):
        """
        Regenerate and save the user settings.

        User settings are updated with the default settings and the defaults
        from every linter, and if the user settings are currently being edited,
        the view is updated.

        """

        self.load()

if 'plugin_is_loaded' not in globals():
    settings = Settings()

    # Set to true when the plugin is loaded at startup
    plugin_is_loaded = False