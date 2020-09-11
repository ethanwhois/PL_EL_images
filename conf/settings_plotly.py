import time
import os
length=0.3
scatter_method=False    #['all', 'outliers', 'suspectedoutliers', False]四种模式选择
#命名结果文件
date=time.strftime('%Y%m%d',time.localtime(time.time()))
outPutName=os.path.join(os.path.dirname(os.path.dirname(__file__)),'data','Standard_deviation',f'{date}_PLEL.html')