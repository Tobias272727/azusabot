from os import path

import nonebot
import pandas as pd
import config
import jieba
import csv


if __name__ == '__main__':
    #initializing the dictionary
    # updating the dictionary
    data = pd.read_csv('data/nickname.csv')
    for i_row in range(data.shape[0]):
        for i_col in range(data.shape[1]):
            if pd.isna(data.iloc[i_row,i_col]) == False:
                jieba.suggest_freq(data.iloc[i_row,i_col], tune=True)
                jieba.add_word(data.iloc[i_row,i_col],tag='nr')
    # from jieba import posseg
    # a = posseg.lcut('镜华老婆')
    # for i in a:
    #     print(i.word,i.flag)
    # 
    print('The dictionary of names has been updated.')
    #
    nonebot.init(config)
    # load_plugins: first para is the dir of plugin which is merged by this file's dir and folder names
    # the second para is the pre- when loading the module.
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'azusa_core', 'plugins'),
        'azusa_core.plugins'
    )
    nonebot.run()