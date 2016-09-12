# -*- coding: utf-8 -*-
# @Author: captain
# @Date:   2016-09-08 00:28:36
# @Last Modified by:   captain
# @Last Modified time: 2016-09-13 00:51:32

import sublime
import sublime_plugin

import os
import json
from string import Template

from .core import persist, util
from .core.simulator import *
from .core.manifest import *

class ChooseSettingCommand(sublime_plugin.WindowCommand):
    """An abstract base class for commands that choose a setting from a list."""

    def __init__(self, window, setting=None, preview=False):
        """Initialize a new instance."""
        super().__init__(window)
        self.setting = setting
        self._settings = None
        self.preview = preview
        self.choose_index = 0

    def description(self, **args):
        """Return the visible description of the command, used in menus."""
        return args.get('value', None)

    def is_checked(self, **args):
        """Return whether this command should be checked in a menu."""
        if 'value' not in args:
            return False

        item = self.transform_setting(args['value'], matching=True)
        setting = self.setting_value(matching=True)
        return item == setting

    def _get_settings(self):
        """Return the list of settings."""
        if self._settings is None:
            self._settings = self.get_settings()

        return self._settings

    settings = property(_get_settings)

    def get_settings(self):
        """Return the list of settings. Subclasses must override this."""
        raise NotImplementedError

    def transform_setting(self, setting, matching=False):
        """
        Transform the display text for setting to the form it is stored in.

        By default, returns a lowercased copy of setting.

        """
        
        return str(setting).lower()

    def setting_value(self, matching=False):
        """Return the current value of the setting."""
        return self.transform_setting(persist.settings.get(self.setting, ''), matching=matching)

    def on_highlight(self, index):
        """If preview is on, set the selected setting."""
        if self.preview:
            self.set(index)

    def choose(self, **kwargs):
        """
        Choose or set the setting.

        If 'value' is in kwargs, the setting is set to the corresponding value.
        Otherwise the list of available settings is built via get_settings
        and is displayed in a quick panel. The current value of the setting
        is initially selected in the quick panel.

        """
        if 'value' in kwargs:
            setting = self.transform_setting(kwargs['value'])
        else:
            setting = self.setting_value(matching=True)

        index = 0
        for i, s in enumerate(self.settings):
            if isinstance(s, (tuple, list)):
                s = self.transform_setting(s[0])
            else:
                s = self.transform_setting(s)

            if s == setting:
                index = i
                break

        if 'value' in kwargs:
            self.set(index)
        else:
            self.previous_setting = self.setting_value()

            self.window.show_quick_panel(
                self.settings,
                on_select=self.set,
                selected_index=index,
                on_highlight=self.on_highlight)

    def set(self, index):
        """Set the value of the setting."""
        if index == -1:
            if self.settings_differ(self.previous_setting, self.setting_value()):
                self.update_setting(self.previous_setting)
            return

        self.choose_index = index
        setting = self.selected_setting(index)

        if isinstance(setting, (tuple, list)):
            setting = setting[0]

        setting = self.transform_setting(setting)

        if not self.settings_differ(persist.settings.get(self.setting, ''), setting):
            return

        self.update_setting(setting)

    def update_setting(self, value):
        """Update the setting with the given value."""
        persist.settings.set(self.setting, value, changed=True)
        self.setting_was_changed(value)
        persist.settings.save()

    def settings_differ(self, old_setting, new_setting):
        """Return whether two setting values differ."""
        if isinstance(new_setting, (tuple, list)):
            new_setting = new_setting[0]

        new_setting = self.transform_setting(new_setting)
        return new_setting != old_setting

    def selected_setting(self, index):
        """
        Return the selected setting by index.

        Subclasses may override this if they want to return something other
        than the indexed value from self.settings.

        """
        return self.settings[index]

    def setting_was_changed(self, setting):
        """
        Do something after the setting value is changed but before settings are saved.

        Subclasses may override this if further action is necessary after
        the setting's value is changed.

        """
        pass

def choose_setting_command(setting, preview):
    """Return a decorator that provides common methods for concrete subclasses of ChooseSettingCommand."""

    def decorator(cls):
        def init(self, window):
            super(cls, self).__init__(window, setting, preview)
            self.update_setting(setting)

        def run(self, **kwargs):
            """Run the command."""
            self.choose(**kwargs)

        cls.setting = setting
        cls.__init__ = init
        cls.run = run
        return cls

    return decorator

@choose_setting_command("cocos_project_name", preview=False)
class SwitchProjectConfigCommand(ChooseSettingCommand):
    """A plugin command used to generate an edit object for a view."""
    def get_settings(self):
        """Return a list of the lint modes."""
        return [[name.capitalize(), description] for name, description in util.PROJECT_DESC]

    def setting_was_changed(self, setting):
        """Update all views when the lint mode changes."""
        if setting != "cocos_project_name":
            util.save_choose_project({'name':setting, 'index':self.choose_index})
        else:
            setting = util.get_choose_cocos_project_name()
            if setting:
                choose_index = util.get_choose_cocos_project_index()
                self.update_setting(setting)
                util.save_choose_project({'name':setting, 'index':choose_index})

class LaunchSimulatorCommand(sublime_plugin.TextCommand):
    """A plugin command used to generate an edit object for a view."""
    def run(self, edit):
        """Run the command."""
        launch_simulator()

class ProcessingImagesCommand(sublime_plugin.TextCommand):
    """A plugin command used to generate an edit object for a view."""
    def run(self, edit):
        """Run the command."""
        print("ProcessingImagesCommand")

class ExportConfigurationCommand(sublime_plugin.TextCommand):
    """A plugin command used to generate an edit object for a view."""
    def run(self, edit):
        """Run the command."""
        print("ExportConfigurationCommand")

class CompileScriptCommand(sublime_plugin.TextCommand):
    """A plugin command used to generate an edit object for a view."""
    def run(self, edit):
        """Run the command."""
        print("CompileScriptCommand")

class BatchPackagingCommand(sublime_plugin.TextCommand):
    """A plugin command used to generate an edit object for a view."""
    def run(self, edit):
        """Run the command."""
        print("BatchPackagingCommand")

class GenerateManifestCommand(sublime_plugin.TextCommand):
    """A plugin command used to generate an edit object for a view."""
    def run(self, edit):
        """Run the command."""
        gen_manifest()