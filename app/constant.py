# -*- coding: utf-8 -*-
# @Author: WeiXiong Hunag
# @Date:   2017-02-28 22:58:36
# @Last Modified by:   WeiXiong Hunag
# @Last Modified time: 2017-03-05 03:14:14

import os
import sys
import locale
import codecs

import sublime

def getSTVersion():
    ST_version_text = sublime.version()
    ST_version = int(ST_version_text) / 1000
    return ST_version

def getSysPlatform():
    # platform may be "osx", "linux" or "windows"
    sys_platform = sublime.platform()
    return sys_platform

def getSysEncoding():
    sys_platform = getSysPlatform()
    if sys_platform == 'osx':
        sys_encoding = 'utf-8'
    else:
        sys_encoding = codecs.lookup(locale.getpreferredencoding()).name
    return sys_encoding

def getSysLanguage():
    sys_language = locale.getdefaultlocale()[0]
    if not sys_language:
        sys_language = 'en'
    else:
        sys_language = sys_language.lower()
    return sys_language

def getCocosRoot():
    if sys_version < 3:
        cocos_root = os.getcwd()
    else:
        for module_key in sys.modules:
            if 'CocosStarter' in module_key:
                cocos_module = sys.modules[module_key]
                break
        cocos_root = os.path.split(cocos_module.__file__)[0]
    return cocos_root

def getPackageRoot():
    return os.path.split(getCocosRoot())[0]

def getUserRoot():
    return os.path.join(getPackageRoot(), 'User')

ST_version = getSTVersion()
sys_version = int(sys.version[0])
sys_platform = getSysPlatform()
sys_encoding = getSysEncoding()
sys_language = getSysLanguage()

package_root = getPackageRoot()
user_root = getUserRoot()
cocos_root = getCocosRoot()
app_root = os.path.join(cocos_root, 'app')

global_settings_name = 'Cocos.global-settings'
cocos_settings_name = 'Cocos.sublime-settings'
