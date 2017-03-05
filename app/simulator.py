# -*- coding: utf-8 -*-
# @Author: WeiXiong Hunag
# @Date:   2017-03-05 08:57:43
# @Last Modified by:   WeiXiong Hunag
# @Last Modified time: 2017-03-05 09:50:08

import os
import subprocess

from . import preference

def launch():
    if not preference.isExistSimulatorPath():
        print("error：no gen simulator")
        return False

    selectProject = preference.getSelectProject()
    if not selectProject:
        print("error：no choosed project!!!")
        return False

    if not selectProject.isExistClientPath():
        print("error：no project client path")
        return False

    if not selectProject.isExistScriptPath():
        print("error：no client script path")
        return False

    simulatorPath = preference.getSimulatorPath()
    projectName = selectProject.getName()
    clientPath = selectProject.getClientPath()
    scriptPath = selectProject.getScriptPath()

    os.chdir(clientPath)
    launch_arg = " -workdir " + clientPath + " -search-path " + scriptPath
    launch_cmd = simulatorPath + launch_arg
    subprocess.Popen(launch_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
