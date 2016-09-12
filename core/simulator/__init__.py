# -*- coding: utf-8 -*-
# @Author: captain
# @Date:   2016-09-11 23:04:20
# @Last Modified by:   captain
# @Last Modified time: 2016-09-13 00:41:20

import os
import subprocess

from .. import persist, util

def launch_simulator():
    choose_cocos_project_index = util.get_choose_cocos_project_index()
    if choose_cocos_project_index < 0:
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

    project = projects[choose_cocos_project_index]
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
    launch_cmd = cocos_simulator_path + launch_arg
    subprocess.Popen(launch_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)