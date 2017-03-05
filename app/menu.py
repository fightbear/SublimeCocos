# -*- coding: utf-8 -*-
# @Author: WeiXiong Hunag
# @Date:   2017-02-28 22:54:57
# @Last Modified by:   WeiXiong Hunag
# @Last Modified time: 2017-03-05 10:41:58

import os
import json

from . import constant
from . import fileutil
from . import preference

class MainMenu:
    def __init__(self, file_name):
        self.file = os.path.join(constant.cocos_root, file_name)
        self.menu = MenuItem('Main Menu')
        self.refresh()

    def getMenu(self):
        return self.menu

    def printMenu(self):
        printMenu(self.menu)

    def buildMenu(self):
        self.menu = buildMainMenu()

    def genFile(self):
        self.printMenu()
        data = convertMenuToData(self.menu)
        text = json.dumps(data, indent = 4)
        fileutil.writeFile(self.file, text)

    def refresh(self):
        self.buildMenu()
        self.genFile()

class MenuItem:
    def __init__(self, caption = '-'):
        self.caption = caption
        self.id = caption.lower()
        self.mnemonic = None
        self.children = []
        self.command = None
        self.checkbox = False
        self.args = None

    def hasSubmenu(self):
        state = False
        if self.children:
            state = True
        return state

    def getCaption(self):
        return self.caption

    def getMnemonic(self):
        return self.mnemonic

    def getId(self):
        return self.id

    def getCommand(self):
        return self.command

    def getCheckbox(self):
        return self.checkbox

    def getArgs(self):
        return self.args

    def getSubmenu(self):
        return self.children

    def addMenuItem(self, menu_item):
        self.children.append(menu_item)

    def addMenuGroup(self, menu_group):
        if self.hasSubmenu():
            seperator = MenuItem()
            self.addMenuItem(seperator)
        self.children += menu_group.getGroup()

    def setCaption(self, caption):
        self.caption = caption

    def setMnemonic(self, mnemonic):
        self.mnemonic = mnemonic

    def setId(self, ID):
        self.id = ID

    def setCommand(self, command):
        self.command = command

    def setCheckbox(self):
        self.checkbox = True

    def setArgs(self, args):
        self.args = args

    def getSubmenuItem(caption):
        subitem = None
        for item in self.children:
            if item.getCaption() == caption:
                subitem = item
        return subitem

class MenuItemGroup:
    def __init__(self):
        self.group = []

    def clear(self):
        self.group = []

    def hasMenuItem(self):
        state = False
        if self.group:
            state = True
        return state

    def addMenuItem(self, menu_item):
        self.group.append(menu_item)

    def removeMenuItem(self, menu_item):
        if menu_item in self.group:
            self.group.remove(menu_item)

    def getGroup(self):
        return self.group

def printMenu(menu, level = 0):
    caption = menu.getCaption()
    if level > 0:
        caption = '\t' * level + '|__' + caption
    print(caption)

    if menu.hasSubmenu():
        for submenu in menu.getSubmenu():
            printMenu(submenu, level+1)

def buildSublimeCocosMenu():
    sublime_cocos_menu = MenuItem("SublimeCocos")
    sublime_cocos_menu.setId("sublimecocos")

    settings_default_menu = MenuItem('Settings – Default')
    settings_default_menu.setCommand('open_file')
    settings_default_menu.setArgs({'file' : "${packages}/SublimeCocos/Cocos.sublime-settings"})

    line_menu = MenuItem()

    keymap_osx_default_menu = MenuItem('Key Bindings – Default')
    keymap_osx_default_menu.setCommand('open_file')
    keymap_osx_default_menu.setArgs({'file' : "${packages}/SublimeCocos/Default (OSX).sublime-keymap", "platform": "OSX"})

    keymap_linux_default_menu = MenuItem('Key Bindings – Default')
    keymap_linux_default_menu.setCommand('open_file')
    keymap_linux_default_menu.setArgs({'file' : "${packages}/SublimeCocos/Default (Linux).sublime-keymap", "platform": "Linux"})

    keymap_windows_default_menu = MenuItem('Key Bindings – Default')
    keymap_windows_default_menu.setCommand('open_file')
    keymap_windows_default_menu.setArgs({'file' : "${packages}/SublimeCocos/Default (Windows).sublime-keymap", "platform": "Windows"})

    sublime_cocos_menu.addMenuItem(settings_default_menu)
    sublime_cocos_menu.addMenuItem(line_menu)
    sublime_cocos_menu.addMenuItem(keymap_osx_default_menu)
    sublime_cocos_menu.addMenuItem(keymap_linux_default_menu)
    sublime_cocos_menu.addMenuItem(keymap_windows_default_menu)
    return sublime_cocos_menu

def buildPackageSettingsMenu():
    package_settings_menu = MenuItem("Package Settings")
    package_settings_menu.setMnemonic('p')
    package_settings_menu.setId("package-settings")

    sublime_cocos_menu = buildSublimeCocosMenu()

    package_settings_menu.addMenuItem(sublime_cocos_menu)
    return package_settings_menu

def buildPreferenceMenu():
    preference_menu = MenuItem('Preferences')
    preference_menu.setMnemonic('n')

    package_settings_menu = buildPackageSettingsMenu()

    preference_menu.addMenuItem(package_settings_menu)
    return preference_menu

def buildProjectMenuGroup():
    project_menu_group = MenuItemGroup()
    studio_projects = preference.getStudioProjects()
    for project in studio_projects:
        index = studio_projects.index(project)
        project_item = MenuItem(project.getName())
        project_item.setCommand('choose_project')
        project_item.setArgs({'project_tag' : index})
        project_item.setCheckbox()
        project_menu_group.addMenuItem(project_item)
    return project_menu_group

def buildToolsMenuGroup():
    tools_menu_group = MenuItemGroup()

    simulator_menu = MenuItem('Simulator')
    simulator_menu.setCommand('simulator')

    build_ios_menu = MenuItem('Build (iOS)')
    build_ios_menu.setCommand('build_ios')

    build_android_menu = MenuItem('Build (Android)')
    build_android_menu.setCommand('build_android')

    tools_menu_group.addMenuItem(simulator_menu)
    tools_menu_group.addMenuItem(build_ios_menu)
    tools_menu_group.addMenuItem(build_android_menu)
    return tools_menu_group

def buildAboutMenuGroup():
    about_menu_group = MenuItemGroup()

    about_menu = MenuItem('About')
    about_menu.setCommand('about')

    about_menu_group.addMenuItem(about_menu)
    return about_menu_group

def buildCocosMenu():
    cocos_menu = MenuItem('Cocos')

    project_menu_group = buildProjectMenuGroup()
    tools_menu_group = buildToolsMenuGroup()
    about_menu_group = buildAboutMenuGroup()

    cocos_menu.addMenuGroup(project_menu_group)
    cocos_menu.addMenuGroup(tools_menu_group)
    cocos_menu.addMenuGroup(about_menu_group)
    return cocos_menu

def buildMainMenu():
    main_menu = MenuItem('Main Menu')

    preference_menu = buildPreferenceMenu()
    cocos_menu = buildCocosMenu()

    main_menu.addMenuItem(preference_menu)
    main_menu.addMenuItem(cocos_menu)
    return main_menu

def convertMenuToData(cur_menu, level = 0):
    caption = cur_menu.getCaption()
    sub_menu_list = cur_menu.getSubmenu()
    if sub_menu_list:
        sub_data_list = []
        for sub_menu in sub_menu_list:
            sub_data = convertMenuToData(sub_menu, level + 1)
            if sub_data:
                sub_data_list.append(sub_data)
        if level > 0:
            menu_id = cur_menu.getId()
            menu_mnemonic = cur_menu.getMnemonic()
            data = {}
            data['caption'] = caption
            data['id'] = menu_id
            data['mnemonic'] = menu_mnemonic
            data['children'] = sub_data_list
        else:
            data = sub_data_list
    else:
        data = {}
        command = cur_menu.getCommand()
        if command or caption == '-':
            args = cur_menu.getArgs()
            checkbox = cur_menu.getCheckbox()
            data['caption'] = caption
            data['command'] = command
            if args:
                data['args'] = args
            if checkbox:
                data['checkbox'] = checkbox
    return data
