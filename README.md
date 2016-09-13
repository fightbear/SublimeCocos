# SublimeCocos

用户工程配置
{
    "user":{
        "cocos_path": "/Users/captain/Repos/game-engine/cocos2dx/",
        "cocos_simulator_path": "/Users/captain/Repos/game-engine/cocos2d-x/tools/simulator/runtime/mac/Simulator.app/Contents/MacOS/Simulator",
        "game_doc_path": "/Users/captain/Repos/game-doc/",
        "game_arts_path": "/Users/captain/Repos/game-arts/",
        "game_projects_path": "/Users/captain/Repos/game-projects/",
        "projects":
        [
            {
                "name": "Project1",
                "res": "res/",
                "src": "src/",
                "config": "src/app/config/",
                "hotUpdatePath": "/Users/captain/Desktop/hot_update",
                "packageUrl": "http://27.126.181.90:10000/update/files/",
                "remoteVersionUrl": "http://27.126.181.90:10000/update/version/version.manifest",
                "remoteManifestUrl": "http://27.126.181.90:10000/update/version/project.manifest",
                "hotUpdateVersion": "1.0.0",
                "engineVersion": "Cocos2d-x v3.13",
                "searchPaths": ["res","src"],
                "hotUpdateImportList": ["res","src"]
            },
            {
                "name": "Project2",
                "res": "res/",
                "src": "src/",
                "config": "src/app/config/",
                "hotUpdatePath": "/Users/captain/Desktop/hot_update",
                "packageUrl": "http://27.126.181.90:10000/update/files/",
                "remoteVersionUrl": "http://27.126.181.90:10000/update/version/version.manifest",
                "remoteManifestUrl": "http://27.126.181.90:10000/update/version/project.manifest",
                "version": "1.0.0",
                "engineVersion": "Cocos2d-x v3.13",
                "searchPaths": ["res", "src"],
                "hotUpdateImportList": ["res","src"]
            }
        ]
    }
}

增加项目后在 user keymap 里追加如：
{
    "keys": ["alt+shift+1"],
    "command": "switch_project_config",
    "args": {"index":1, "value":"Project1"}
},
{
    "keys": ["alt+shift+2"],
    "command": "switch_project_config",
    "args": {"index":2, "value":"Project2"}
}