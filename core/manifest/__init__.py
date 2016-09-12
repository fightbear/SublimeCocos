# -*- coding: utf-8 -*-
# @Author: captain
# @Date:   2016-09-11 23:05:18
# @Last Modified by:   captain
# @Last Modified time: 2016-09-13 01:44:20

import json
import os
import io
import shutil
from hashlib import md5

from .. import persist, util

ignoreList = [".DS_Store"]

versionConfig = '''{
    "packageUrl": "%s",
    "remoteVersionUrl": "%s",
    "remoteManifestUrl": "%s",
    "version": "%s",
    "engineVersion": "%s"
}''' 

projectConfig = '''{
    "packageUrl": "%s",
    "remoteVersionUrl": "%s",
    "remoteManifestUrl": "%s",
    "version": "%s",
    "engineVersion": "%s",
    "assets": %s,
    "searchPaths": %s
}''' 

assetsList = ""
def gen_manifest():
    global assetsList          
    game_projects_path = persist.settings.get("game_projects_path", None)
    if not game_projects_path or not os.path.exists(game_projects_path):
        print("warning：not find cocos projects path!!!")
        return

    projects = persist.settings.get("projects")
    if not projects:
        print("warning：no projects data!!!")
        return

    choose_cocos_project_index = util.get_choose_cocos_project_index()
    if choose_cocos_project_index < 0:
        print("warning：no choosed project!!!")
        return

    project = projects[choose_cocos_project_index]
    if not project:
        print("warning: no setting project for projects!!!")
        return

    projectName = project['name']
    projectPath = os.path.join(game_projects_path, str(projectName))
    if not projectPath or not os.path.exists(projectPath):
        print("warning：not find project name!!!")
        return

    packageUrl = project['packageUrl']
    if not packageUrl:
        print("warning: no setting project hot update packageUrl!!!")
        return

    remoteVersionUrl = project['remoteVersionUrl']
    if not remoteVersionUrl:
        print("warning: no setting project hot update remoteVersionUrl!!!")
        return

    remoteManifestUrl = project['remoteManifestUrl']
    if not remoteManifestUrl:
        print("warning: no setting project hot update remoteManifestUrl!!!")
        return

    updatePath = project['hotUpdatePath'] or os.path.join(projectPath, "hot_update")
    version = project['hotUpdateVersion'] or "1.0.0"
    engineVersion = project['engineVersion'] or "Cocos2d-x v3.13"
    searchPaths = project['searchPaths'] or []
    importList = project['hotUpdateImportList'] or ["res","src"]

    if not os.path.exists(updatePath):
        os.mkdir(updatePath)

    update_files = os.path.join(updatePath, "files")
    if not os.path.exists(update_files):
        os.mkdir(update_files)

    def isIgnored(item):
            for s in ignoreList:
                if item == s:
                    return True
            return False

    def isImported(item):
        for s in importList:
            if item == s:
                return True
        return False
        
    # 生成 version.manifest
    configStr = versionConfig % (packageUrl, remoteVersionUrl, remoteManifestUrl, version, engineVersion)
    with io.open(os.path.join(updatePath, "version.manifest"), "w", encoding='utf-8') as f:
        f.write(configStr)

    # 生成 asstes 列表，并将项目资源拷贝目录到更新文件目录中
    def generateMd5(path):
        global assetsList
        files = os.listdir(path)
        for f in files:
            if not isIgnored(f):
                fpath = os.path.join(path,f)
                if os.path.isfile(fpath):
                    m = md5()
                    b_file = open(fpath,'rb')
                    m.update(b_file.read())
                    b_file.close()

                    key = fpath[len(projectPath)+1:]
                    assetsList += key_value % (key, m.hexdigest())
                elif os.path.isdir(fpath):
                    generateMd5(fpath)

    assetsList = "{\n"
    key_value = '''        "%s": {"md5": "%s"},\n'''
    root_files = os.listdir(projectPath)
    for f in root_files:
        if isImported(f):
            # 项目资源拷贝目录到更新文件目录中
            if os.path.exists(os.path.join(update_files, f)):
                shutil.rmtree(os.path.join(update_files, f))
            shutil.copytree(os.path.join(projectPath,f), os.path.join(update_files, f))
            # 将文件夹里的文件生成 md5
            generateMd5(os.path.join(projectPath,f))
    if len(assetsList) >= 4:
        assetsList = assetsList[:-2]
    assetsList += "\n\t}"

    i = 0
    searchPathsStr = "["
    for path in searchPaths:
        i = i + 1
        if i == len(searchPaths):
            searchPathsStr += '''"%s"''' % path
        else:
            searchPathsStr += '''"%s", ''' % path
    searchPathsStr += "]"

    # 生成 project.manifest
    configStr = projectConfig % (packageUrl, remoteVersionUrl, remoteManifestUrl, version, engineVersion, assetsList, searchPathsStr)
    with io.open(os.path.join(updatePath, "project.manifest"), "w", encoding='utf-8') as f:
        f.write(configStr)

    # 将project.manifest文件保存到本地工程目录
    shutil.copyfile(os.path.join(updatePath, "project.manifest"), os.path.join(projectPath,"project.manifest"))

    print("++++++ generate manifest finish ～～")
    