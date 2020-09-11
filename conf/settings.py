import os

#常用参数设置
#文件来源目录
raw_data_file_name='TC_test_C8'
#生成图像分辨率
dpi = 900


#RGB模式下的参数
def RGB_settings():
    PL_EL_x=108
    PL_EL_y=-70
    PL_x=80
    PL_y=-20
    title_x=0
    title_y=1120
    return PL_EL_x,PL_EL_y,PL_x,PL_y,title_x,title_y

#Grays模式下的参数
def Greys_settings():
    PL_EL_x=130
    PL_EL_y=-70
    PL_x=0
    PL_y=-20
    title_x=0
    title_y=1120
    return PL_EL_x,PL_EL_y,PL_x,PL_y,title_x,title_y

#将文件夹名字规范化
def rename_file(dir,doc):
    doc2=doc.replace(' ','_')
    os.rename(os.path.join(dir,doc),os.path.join(dir,doc2))
    return doc2


BASE_PATH = os.path.dirname(os.path.dirname(__file__))
raw_data_dir=os.path.join(BASE_PATH,'data','Raw_Photo')
#文件夹名字处理，去掉空格
raw_data_file_name=rename_file(raw_data_dir,raw_data_file_name)
img_dir = os.path.join(raw_data_dir,raw_data_file_name)

#备份tif目录
BackUp_tif= os.path.join(img_dir,'BackUp_tif')

#结果输出目录
res_dir = os.path.join(BASE_PATH,'data','Results',raw_data_file_name)

#log目录
log_path= os.path.join(BASE_PATH,'log')



#数据保存excel目录
data_excel=os.path.join(BASE_PATH,'data','Standard_deviation',f'{raw_data_file_name}.xlsx')

#pl el 每项数据分布图目录
count_fig_path=os.path.join(BASE_PATH,'data','CountFig')

#pl,el分布合集目录
pic_list=['_PL','_EL']              #合集采样数据列表： [’_PL‘， ’_EL‘ , ’_PL_EL‘]
plotly_el_pl_fig_path=os.path.join(BASE_PATH,'data','Standard_deviation','PL_EL_results.html')

#图中缩写名字起止位置
name_star_with=8
name_end_with=18

#excel中存储图片设置
img_size = (268, 201)   #图片导入后大小设置
cell_width=40       #单元格宽度
cell_height=160     #单元格高度
data_column='H'     #单元格所在列

#不同method下，参数设置：
method_dict={1:RGB_settings,2:Greys_settings}


