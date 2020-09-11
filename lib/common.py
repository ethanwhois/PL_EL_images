import logging
import os
import json
import time
import traceback

from conf import settings

# 保存日志
def savelog(img_list):
    loglist = {}
    logtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    loglist[logtime] = img_list
    loglist = json.dumps(loglist)
    with open(os.path.join(settings.BASE_PATH,'log','log.txt'), 'a', encoding='utf-8') as f:
        f.write(loglist + '\n')

    # 存储已处理过的所有图像名称
    with open(os.path.join(settings.BASE_PATH,'log','work_book.txt'), 'w+', encoding='utf-8') as f:
        f.write(loglist + '\n')
    return

logging.basicConfig(level=logging.ERROR,  # 控制台打印的日志级别
                            filename=os.path.join(settings.BASE_PATH,'log','logbook.txt'),
                            filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                            # a是追加模式，默认如果不写的话，就是追加模式
                            format=
                            '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                            # 日志格式
                            )

#保存所有错误日志
def log_all_errors(func1):
    try:
        func1
    except Exception as e:
        logging.error("Main program error:")
        logging.error(e)
        logging.error(traceback.format_exc())

