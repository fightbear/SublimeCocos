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

class ChooseSettingCommand(sublime_plugin.WindowCommand):
    """An abstract base class for commands that choose a setting from a list."""

    def __init__(self, window, setting=None, preview=False):
        """Initialize a new instance."""
        super().__init__(window)
        self.setting = setting
        self._settings = None
        self.preview = preview
        self.choose_index = -1
        self.previous_index = -1

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
            self.previous_index = index

            self.window.show_quick_panel(
                self.settings,
                on_select=self.set,
                selected_index=index,
                on_highlight=self.on_highlight)

    def set(self, index):
        """Set the value of the setting."""
        if index == -1:
            if self.settings_differ(self.previous_setting, self.setting_value()):
                self.choose_index = self.previous_index
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

@choose_setting_command(persist.choose_cocos_project_name, preview=False)
class SwitchProjectConfigCommand(ChooseSettingCommand):
    """A plugin command used to generate an edit object for a view."""
    def get_settings(self):
        """Return a list of the lint modes."""
        return [[name.capitalize(), description] for name, description in util.PROJECT_DESC]

    def setting_was_changed(self, setting):
        """Update all views when the lint mode changes."""
        if setting:
            persist.choose_cocos_project_name = setting
            persist.choose_cocos_project_index = self.choose_index
            print("choose_cocos_project_name ", persist.choose_cocos_project_name)
            print("choose_cocos_project_index ", persist.choose_cocos_project_index)
            util.save_choose_project({'name':setting, 'index':self.choose_index})

class LaunchSimulatorCommand(sublime_plugin.TextCommand):
    """A plugin command used to generate an edit object for a view."""
    def run(self, edit):
        """Run the command."""
        print("xxxx choose_cocos_project_index ", persist.gettest())
        if not persist.choose_cocos_project_index:
            print("warning：no choosed project!!!")
            return

        cocos_simulator_path = persist.settings.get("cocos_simulator_path", None)
        if not cocos_simulator_path or not os.path.exists(cocos_simulator_path):
            print("warning：not find cocos simulator path!!!")
            return

        game_projects_path = persist.settings.get("game_projects_path", None)
        if not game_projects_path or not os.path.exists(game_projects_path):
            print("warning：not find cocos projects path!!!")
            return

        projects = persist.settings.get("projects")
        if not projects:
            print("warning：no projects data!!!")
            return

        project = projects[persist.choose_cocos_project_index]
        if not project:
            print("warning: no setting project for projects!!!")
            return

        projectName = project['name']
        project_path = os.path.join(game_projects_path, str(projectName))
        if not project_path or not os.path.exists(project_path):
            print("warning：not find project name!!!")
            return

        projectSrc = project['src']
        project_src_dir = os.path.join(project_path, str(projectSrc))
        if not project_src_dir or not os.path.exists(project_src_dir):
            print("warning：not find project src dir!!!")
            return

        os.chdir(project_path)
        launch_arg = " -workdir " + project_path + " -search-path " + project_src_dir
        launch_cmd= cocos_simulator_path + launch_arg
        subprocess.Popen(launch_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)