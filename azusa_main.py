from os import path

import nonebot

import config

if __name__ == '__main__':
    nonebot.init(config)
    # load_plugins: first para is the dir of plugin which is merged by this file's dir and folder names
    # the second para is the pre- when loading the module.
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'azusa_core', 'plugins'),
        'azusa_core.plugins'
    )
    nonebot.run()