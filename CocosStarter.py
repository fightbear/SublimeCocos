import os
import sublime
import sublime_plugin

st_version = int(sublime.version())
if st_version < 3000:
    import app
else:
    from . import app

class CocosListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        basename = os.path.basename(view.file_name())
        if basename == app.constant.cocos_settings_name:
            app.preference.loadSettings()
            app.main_menu.refresh()

class ChooseProjectCommand(sublime_plugin.WindowCommand):
    def run(self, project_tag):
        app.preference.global_settings.set('project_tag', project_tag)

    def is_checked(self, project_tag):
        state = False
        chosen_project_tag = app.preference.global_settings.get('project_tag', -1)
        if project_tag == chosen_project_tag:
            state = True
        return state

class SimulatorCommand(sublime_plugin.WindowCommand):
    def run(self):
        app.simulator.launch()

class BuildIosCommand(sublime_plugin.WindowCommand):
    def run(self):
        print("Build iOS are being developed ...")

class BuildAndroidCommand(sublime_plugin.WindowCommand):
    def run(self):
        print("Build android are being developed ...")

class AboutCommand(sublime_plugin.WindowCommand):
    def run(self):
        sublime.run_command('open_url', {'url': "https://github.com/fightbear/SublimeCocos"})
