# -*- coding: utf-8 -*-
# @Author: captain
# @Date:   2016-08-27 00:39:21
# @Last Modified by:   captain
# @Last Modified time: 2016-09-08 02:19:53

from functools import lru_cache
from glob import glob
import json
import locale
from numbers import Number
import os
import getpass
import re
import shutil
from string import Template
import stat
import sublime
import subprocess
import sys
import tempfile
from xml.etree import ElementTree

if sublime.platform() != 'windows':
    import pwd

PLUGIN_NAME = 'SublimeCocos'
MENU_INDENT_RE = re.compile(r'^(\s+)\$menus', re.MULTILINE)
PROJECT_MENU_ITEM = '''{
    "caption": "$name",
    "command": "switch_project_config",
    "args": {"index": $index, "value":"$name"}
}'''
KEYMAP_INDENT_RE = re.compile(r'^(\s+)\$keymaps', re.MULTILINE)
PROJECT_KEYMAP_ITEM = '''{
    "keys": ["$alt+shift+$index"],
    "command": "switch_project_config",
    "args": {"index":$index, "value":"$name"}
}'''
PROJECT_DESC = []

def auto_generate_projects_desc(projects):
    for project in projects:
        name = project['name']
        desc = project.get('desc', name)
        PROJECT_DESC.append([name, desc])

def indent_lines(text, indent):
    """Return all of the lines in text indented by prefixing with indent."""
    return re.sub(r'^', indent, text, flags=re.MULTILINE)[len(indent):]

def auto_generate_menu_key(projects):
    menu_items = []
    keymap_items = []
    for project in projects:
        name = project['name']
        item = {
            'name': name,
            'index': len(menu_items) + 1
        }
        menu_items.append(Template(PROJECT_MENU_ITEM).safe_substitute(item))
        keymap_items.append(Template(PROJECT_KEYMAP_ITEM).safe_substitute(item))

    menu_items = ',\n'.join(menu_items)
    keymap_items = ',\n'.join(keymap_items)

    generate_menu('Main', menu_items)
    sys_platform = sublime.platform()
    if sys_platform == 'windows':
        generate_keymap('Windows', keymap_items, 'ctrl', 'alt')
    elif sys_platform == 'linux':
        generate_keymap('Linux', keymap_items, 'ctrl', 'alt')
    elif sys_platform == 'osx':
        generate_keymap('OSX', keymap_items, 'super', 'option')

def generate_menu(name, menu_text):
    """Generate and return a sublime-menu from a template."""
    plugin_dir = os.path.join(sublime.packages_path(), PLUGIN_NAME)
    path = os.path.join(plugin_dir, '{}.sublime-menu.template'.format(name))

    with open(path, encoding='utf8') as f:
        template = f.read()

    # Get the indent for the menus within the template,
    # indent the chooser menus except for the first line.
    indent = MENU_INDENT_RE.search(template).group(1)
    menu_text = indent_lines(menu_text, indent)

    text = Template(template).safe_substitute({'menus': menu_text})
    path = os.path.join(plugin_dir, '{}.sublime-menu'.format(name))

    with open(path, mode='w', encoding='utf8') as f:
        f.write(text)

    return text

def generate_keymap(os_name, keymap_text, ctrl, alt):
    """Generate and return a sublime-keymap from a template."""
    plugin_dir = os.path.join(sublime.packages_path(), PLUGIN_NAME)
    path = os.path.join(plugin_dir, 'Default.sublime-keymap.template')

    with open(path, encoding='utf8') as f:
        template = f.read()

    # Get the indent for the menus within the template,
    # indent the chooser menus except for the first line.
    indent = KEYMAP_INDENT_RE.search(template).group(1)
    keymap_text = indent_lines(keymap_text, indent)

    text = Template(template).safe_substitute({'keymaps': keymap_text})
    text = Template(text).safe_substitute({'ctrl': ctrl, 'alt': alt})
    user_setting_dir = os.path.join(sublime.packages_path(), "User")
    path = os.path.join(user_setting_dir, 'SublimeCocos.sublime-keymap'.format(os_name))
    
    with open(path, mode='w', encoding='utf8') as f:
        f.write(text)

    return text

def merge_user_settings(settings):
    """Return the default cocos settings merged with the user's settings."""

    default = settings.get('default', {})
    user = settings.get('user', {})

    if user:
        default.update(user)

    return default

def save_choose_project(project):
    if not project or len(project) <= 0:
        return

    plugin_dir = os.path.join(sublime.packages_path(), "User")
    path = os.path.join(plugin_dir, 'choose_cocos_project.json')
    with open(path, mode='w', encoding='utf8') as f:
        f.write(str(project))

def get_saved_project():
    plugin_dir = os.path.join(sublime.packages_path(), "User")
    path = os.path.join(plugin_dir, 'choose_cocos_project.json')
    if not os.path.exists(path):
        return
    
    with open(path, encoding='utf8') as f:
        project = f.read()

    return eval(project)

def get_choose_cocos_project_name():
    choose_cocos_project = get_saved_project() or {}
    return choose_cocos_project.get('name')

def get_choose_cocos_project_index():
    choose_cocos_project = get_saved_project() or {}
    return choose_cocos_project.get('index')