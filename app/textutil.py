# -*- coding: utf-8 -*-
# @Author: WeiXiong Hunag
# @Date:   2017-02-28 23:05:20
# @Last Modified by:   WeiXiong Hunag
# @Last Modified time: 2017-02-28 23:05:26

def getKeyValue(line):
    line = line.strip()
    if '=' in line:
        index = line.index('=')
        key = line[:index].strip()
        value = line[(index+1):].strip()
    else:
        key = ''
        value = ''
    return (key, value)

def getBlockList(lines, sep = '.name'):
    block_list = []
    block = []
    for line in lines:
        line = line.strip()
        if line and (not '#' in line):
            if (sep in line) and (not '.menu' in line):
                block_list.append(block)
                block = [line]
            else:
                block.append(line)
    block_list.append(block)
    return block_list
