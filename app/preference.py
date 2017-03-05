# -*- coding: utf-8 -*-
# @Author: WeiXiong Hunag
# @Date:   2017-02-28 22:59:42
# @Last Modified by:   WeiXiong Hunag
# @Last Modified time: 2017-03-05 10:06:47

import os
import sys
import json

import sublime

from . import constant
from . import fileutil

class Keymap:
    def __init__(self, default_folder, file_name):
        self.maps = []
        self.default_folder = default_folder
        self.file_name = file_name
        self.default_file = os.path.join(default_folder, file_name)
        self.file = self.default_file
        self.loadKeymapFile()

    def loadKeymapFile(self):
        if os.path.isfile(self.file):
            text = fileutil.readFile(self.file) or "[]"
            self.maps = json.loads(text)

    def saveKeymapFile(self):
        text = json.dumps(self.maps, sort_keys = True, indent = 4)
        fileutil.writeFile(self.file, text)

    def get(self, keys):
        for key in keys:
            for keymap in self.maps:
                if key in keymap.get("keys"):
                    return keymap
        return None

    def addKeymap(self, keymap):
        if self.get(keymap.get("keys")):
            return

        self.maps.append(keymap)
        self.saveKeymapFile()

    def changeFolder(self, folder):
        if not os.path.isdir(folder):
            self.file = self.default_file
        else:
            self.file = os.path.join(folder, self.file_name)

        if os.path.isfile(self.file):
            self.loadKeymapFile()
        else:
            self.saveKeymapFile()

class Setting:
    def __init__(self, default_folder, file_name):
        self.settings_dict = {}
        self.default_folder = default_folder
        self.file_name = file_name
        self.default_file = os.path.join(default_folder, file_name)
        self.file = self.default_file
        self.loadSettingsFile()

    def loadSettingsFile(self):
        if os.path.isfile(self.file):
            text = fileutil.readFile(self.file)
            self.settings_dict = json.loads(text)

    def saveSettingsFile(self):
        text = json.dumps(self.settings_dict, sort_keys = True, indent = 4)
        fileutil.writeFile(self.file, text)

    def get(self, key, default_value = None):
        if key in self.settings_dict:
            value = self.settings_dict[key]
        else:
            value = default_value

        try:
            value + 'string'
        except TypeError:
            pass
        else:
            cocos_folder = constant.getCocosRoot()
            st_package_folder = constant.getPackageRoot()
            value = value.replace('${cocos_root}', cocos_folder)
            value = value.replace('${packages}', st_package_folder)
        return value

    def set(self, key, value):
        self.settings_dict[key] = value
        self.saveSettingsFile()

    def changeFolder(self, folder):
        if not os.path.isdir(folder):
            self.file = self.default_file
        else:
            self.file = os.path.join(folder, self.file_name)

        if os.path.isfile(self.file):
            self.loadSettingsFile()
        else:
            self.saveSettingsFile()

class Studio:
    def __init__(self, studio):
        self.studio = studio
        self.projects = []
        self.refresh()

    def initProjects(self):
        for v in self.studio:
            idx = self.studio.index(v)
            project = Project(v)
            project.setTag(idx)
            self.projects.append(project)

    def getProjects(self):
        return self.projects

    def getProjectByTag(self, tag):
        if tag >= 0 and tag < len(self.projects):
            return self.projects[tag]
        return None

    def refresh(self):
        self.initProjects()

class Project:
    def __init__(self, project):
        self.tag = 0
        self.projectName = project.get("projectName") or ""
        self.projectPath = project.get("projectPath") or ""
        self.docsPath = project.get("docsPath") or ""
        self.artsPath = project.get("artsPath") or ""
        self.clientPath = project.get("clientPath") or ""
        self.serverPath = project.get("serverPath") or ""
        self.scriptPath = project.get("scriptPath") or ""

    def setTag(self, tag):
        self.tag = tag

    def getTag(self):
        return self.tag

    def getName(self):
        return self.projectName or "GameClient{0}".format(self.tag+1)

    def getPath(self):
        return self.projectPath

    def getDocsPath(self):
        return self.docsPath

    def getArtsPath(self):
        return self.artsPath

    def getClientPath(self):
        return self.clientPath

    def getServerPath(self):
        return self.serverPath

    def getScriptPath(self):
        return self.scriptPath

    def isExistPath(self):
        if os.path.exists(self.projectPath):
            return True
        return False

    def isExistDocsPath(self):
        if os.path.exists(self.docsPath):
            return True
        return False

    def isExistArtsPath(self):
        if os.path.exists(self.artsPath):
            return True
        return False

    def isExistClientPath(self):
        if os.path.exists(self.clientPath):
            return True
        return False

    def isExistServerPath(self):
        if os.path.exists(self.serverPath):
            return True
        return False

    def isExistScriptPath(self):
        if os.path.exists(self.scriptPath):
            return True
        return False

##############################################################################

global_settings = Setting(constant.cocos_root, constant.global_settings_name)

cocos_settings = None
studio_settings = None
def loadSettings():
    # settings
    global cocos_settings
    cocos_settings = Setting(constant.cocos_root, constant.cocos_settings_name)

    global studio_settings
    studio = cocos_settings.get('studio', [])
    studio_settings = Studio(studio)

    # keymap
    platform = constant.getSysPlatform()
    if platform == "windows":
        fileName = "Default (Windows).sublime-keymap"
    elif platform == "linux":
        fileName = "Default (Linux).sublime-keymap"
    else:
        fileName = "Default (OSX).sublime-keymap"
    user_keymap = Keymap(constant.cocos_root, fileName)
    filter_map = filter(lambda x: x.get("command") != "choose_project", user_keymap.maps)
    user_keymap.maps = list(filter_map)

    projects = studio_settings.getProjects()
    for project in projects:
        tag = project.getTag()
        key = "alt+shift+{0}".format(tag+1)
        user_keymap.addKeymap({"keys": [key], "command": "choose_project", "args": {"project_tag": tag}})
loadSettings()

def getJavaHome():
    return cocos_settings.get('java_home', None)

def getAntRoot():
    return cocos_settings.get('ant_root', None)

def getAndroidSDKRoot():
    return cocos_settings.get('android_sdk_root', None)

def getAndroidNDKRoot():
    return cocos_settings.get('android_ndk_root', None)

def getEnginePath():
    return cocos_settings.get('engine_path', None)

def isExistEnginePath():
    enginePath = getEnginePath()
    if os.path.exists(enginePath):
        return True
    return False

def getSimulatorPath():
    return cocos_settings.get('simulator_path', None)

def isExistSimulatorPath():
    simulatorPath = getSimulatorPath()
    if os.path.exists(simulatorPath):
        return True
    return False

def getStudioProjects():
    return studio_settings.getProjects()

def getSelectProject():
    chosen_project_tag = global_settings.get('project_tag', 0)
    project = studio_settings.getProjectByTag(chosen_project_tag)
    return project

