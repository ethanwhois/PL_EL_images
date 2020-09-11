# re 自动判断文件名,plt RGB TO GREY
import shutil
from PIL import Image as Img
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import pandas as pd
from conf import settings,settings_plotly
from lib import common
from core import plotly_box_plot


#彩色转黑白
def rgb2g(img_path):
    img=Img.open(img_path).convert('L')
    img2=img.crop((0,0,1000,)+img.size[1:])
    img2.save(img_path[:-3]+'tif')
    return

# 读取文件名
def get_docname():
    img_com_list = []
    errors = []
    samplelist = {}
    legalsamplelist = {}
    method = input('1. RGB files; 2. GreyScale files:')
    if method == '1':
        # 创造文件夹进行备份
        if not os.path.exists(settings.BackUp_tif): os.mkdir(settings.BackUp_tif)
        # 备份文件
        if not os.listdir(settings.BackUp_tif): [shutil.move(os.path.join(settings.img_dir, images), settings.BackUp_tif)
                                                 for images in os.listdir(settings.img_dir) if re.match('.*tif$', images)]
        # 转换图像
        [rgb2g(os.path.join(settings.img_dir, images)) for images in os.listdir(settings.img_dir) if re.match('.*.png$', images)]
        print('Transform RGB into Greys Completed!')

    # 读取已处理过的图像列表
    if os.path.exists(settings.res_dir):
        if os.listdir(settings.res_dir):
            for img_name in os.listdir(settings.res_dir):
                findname = re.compile('(.*).jpg')
                samplename = re.findall(findname, img_name)
                if samplename: img_com_list.append(samplename[0])
    else:
        os.mkdir(settings.res_dir)

    # 读取所有文件名并排除已经处理过的文件名
    for img_name in os.listdir(settings.img_dir):
        findname = re.compile('.*?(\d+\+\d+).*.tif')
        samplename = re.findall(findname, img_name)
        # 筛选tif
        if samplename:
            samplename = samplename[0]
            # 去除已经处理过的
            if samplename not in img_com_list:
                # 是否有该sample的字典，没有就创建
                if samplename not in samplelist.keys(): samplelist[samplename] = {}
                # 判断EL，PL归类
                if re.match('.*?EL.*', img_name):
                    samplelist[samplename]['EL'] = img_name
                else:
                    samplelist[samplename]['PL'] = img_name

    # 判断文件是否完整
    for k, values in samplelist.items():
        if 'EL' in values.keys() and 'PL' in values.keys():
            legalsamplelist[k] = values
        else:
            errortype = 'PL' if 'EL' in values.keys() else 'EL'
            errors.append(f'FileNotFoundError:"{k}":"{errortype}"')

    return legalsamplelist, errors

def normalization(data):
    _range = np.max(data) - np.min(data)
    color_arr = (data - np.min(data)) / _range * 100
    return color_arr

def standardization(data, name):
    one_arr = data.ravel()
    Count_Num = len(one_arr)
    arr_std = np.std(one_arr).round(3)  # std
    arr_mean = np.mean(one_arr).round(3)  # mean
    return arr_std, arr_mean, Count_Num

def getplot(img_normal, img_name,arr_std_str,arr_mean_std_pl,arr_mean_std_el):
    plt.figure(dpi=settings.dpi)
    plt.axis('off')
    plt.text(100, -70, f'{img_name}')
    plt.text(100, -20, f'PL/EL Standard Deviation = {arr_std_str}')
    plt.text(100, 1070, f'PL: SD = {arr_mean_std_pl}')
    plt.text(100, 1120, f'EL: SD = {arr_mean_std_el} ')
    plt.imshow(img_normal, cmap=plt.cm.jet)
    plt.colorbar()
    plt.savefig(os.path.join(settings.res_dir, f'{img_name}.jpg'))
    plt.close()
    return

def getMatrix(imgdict):
    info = []
    for img_name, filenamedict in imgdict.items():
        el = plt.imread(os.path.join(settings.img_dir, filenamedict['EL']))
        pl = plt.imread(os.path.join(settings.img_dir, filenamedict['PL']))
        img_arr = pl / el
        img_normal = normalization(img_arr)
        arr_std, arr_mean, Count_pl_el = standardization(img_arr, '_PL_EL')
        arr_std_str = f'{arr_mean}±{arr_std}'
        arr_std_pl, arr_mean_pl, Count_pl = standardization(pl, '_PL')
        arr_mean_std_pl = f'{arr_mean_pl}±{arr_std_pl}'
        arr_std_el, arr_mean_el, Count_el = standardization(el, '_EL')
        arr_mean_std_el = f'{arr_mean_el}±{arr_std_el}'
        getplot(img_normal, img_name, arr_std_str, arr_mean_std_pl, arr_mean_std_el)

        # 保存数据信息
        info_list = [img_name, Count_pl, arr_mean_pl, arr_std_pl, Count_el, arr_mean_el, arr_std_el, Count_pl_el,
                     arr_mean, arr_std]
        info.append(info_list)
        print(f'COMPLETED : "{img_name}"')
    return info

# 获得矩阵
def saveToExcel(info,imgDict):
    imgList = list(imgDict.keys())
    column = ['Sample', 'PL(counts)', 'PL(mean)', 'PL(STD)', 'El(counts)', 'EL(mean)', 'EL(STD)', 'Pl/EL(counts)',
              'PL/EL(mean)', 'PL/EL(STD)']
    df = pd.DataFrame(data=info, index=imgList, columns=column).sort_values('Sample')
    df.to_excel(settings.data_excel, index=False)
    return


# main
def run():
    imgDict, errors = get_docname()
    if imgDict:
        info=getMatrix(imgDict)
        saveToExcel(info,imgDict)
        common.savelog(imgDict)
        plotly_box_plot.main(settings_plotly.length,settings_plotly.scatter_method, settings_plotly.outPutName)
        if errors:
            common.savelog(errors)
            print(errors)
    else:
        print('New data is not found.')
    return


if __name__ == '__main__':
    run()
