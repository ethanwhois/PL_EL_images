import os
import re
import pandas as pd
import plotly.offline as of
import plotly.graph_objs as go
import sys
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_PATH)
from conf import settings_plotly,settings



def get_df():
    folderdir=os.path.join(BASE_PATH,'data','200911_ME_TC8')
    dict1={
            'standard.*front.csv':'standard',
            'tape.*front.csv':'tape',
            'ME2.*SnBiAg.*front.csv':'M2_SBA',
            'ME2.*SnBiInAg.*front.csv':'M2_SBIA',
            'ME1.*SnBiAg.*front.csv':'M1_SBA',
            'ME1.*SnBiInAg.*front.csv': 'M1_SBIA',
           }
    infolist=[]
    findname='.*?(\d+\+\d+).*front.csv'
    for file in os.listdir(folderdir):
        for k,v in dict1.items():
            if re.match(k,file):
                df = pd.read_csv(
                    os.path.join(folderdir, file),
                    skiprows=12,
                    index_col=0,
                ).T.iloc[:, [1, 2, 3, 5, 8, 9]]
                df.columns = df.columns.str.replace(":", "").str.strip()
                df.iloc[0, 1] = float(df.iloc[0, 1]) / 137.075 * 1000
                df.iloc[0, 2] = float(df.iloc[0, 2]) * 137.075
                df.iloc[0, 4] = float(df.iloc[0, 4]) * 100
                df['type']=v
                df['Sample']=re.findall(findname,file)[0]
                df.set_index(['Sample'],inplace=True)
                infolist.append(df)
    df=pd.concat(infolist)
    df2=pd.read_excel(
        settings.data_excel,
        sheet_name=0,
        usecols=[0,6,9],
        names=['Sample','EL_STD',r'PL/EL STD'],
    )
    df2.set_index(['Sample'],inplace=True)
    df3=df.join(df2)
    df3.set_index(['type'],inplace=True)
    xlist = df3.columns.to_list()
    doclist = sorted(list(set(df3.index.to_list())))
    return xlist,doclist,df3

# 基本坐标轴设置
class Base_fig():
    def get_layout(self):
        layout_set = dict(
            boxmode='group',
            font=dict(
                family="Times New Roman",
                color="black"
            ),
            showlegend=False,
        )
        return layout_set


# 实际每个图数据，坐标轴
class Real_fig():
    def __init__(self, df,doclist, index,v,length,scatter_method):
        self.df = df
        self.doclist=doclist
        self.index=index
        self.v=v
        self.length=length
        self.scatter_method=scatter_method
    def get_layout(self):
        tickfontsize=11
        name=['Voc (V)','Jsc (mA&#183;cm<sup>-2</sup>)','Rs (&#937; &#183;cm<sup>2</sup>)','Pmp (W)','FF (%)','&#951; (%)','EL(STD)','PL/EL(STD)']
        layout = {
            f'xaxis{self.index + 1}': {
                'domain': [(self.length+0.03)* (self.index % 3),(self.length+0.03)* (self.index % 3)+self.length],
                'title': f'<b>{name[self.index]}</b>',
                'titlefont': {
                    'size': 11
                },
                'tickfont':{
                    'size':tickfontsize
                },
                'anchor': f'y{self.index + 1}',

            },

            f'yaxis{self.index + 1}': {
                'domain': [ 1- (self.index // 3)/2.86-self.length*0.7, 1- (self.index // 3)/2.86],
                'anchor': f'x{self.index + 1}',
                'tickfont': {
                    'size': tickfontsize
                },

            }
        }
        return layout


    def get_data(self):
        # colour=['#ffb3a7','#fff143','#7fecad']  # ffb3a7 #cca4e3
        colour=['#ff7500','#ffb3a7','orange','yellow','#7fecad','#a4e2c6',]
        data = []
        for a, b in enumerate(self.doclist):
            trace = go.Box(
                y=self.df[self.df.index==b][self.v],
                boxmean='sd',
                boxpoints=self.scatter_method,    #suspectedoutliers
                width=0.6,
                jitter=0.2,
                name=b,
                fillcolor=colour[a],
                line=dict(
                    color='#177cb0',
                ),
                xaxis=f'x{self.index + 1}',
                yaxis=f'y{self.index + 1}')
            data.append(trace)
        return data


def main(length,scatter_method, outPutName):
    xlist,doclist,df=get_df()
    layout_dict = {}
    data = []

    for index, v in enumerate(xlist):
        plotly = Real_fig(df, doclist, index, v,length,scatter_method)
        data += plotly.get_data()
        layout_dict = dict(layout_dict, **plotly.get_layout())

    base_fig = Base_fig()
    layout = {**layout_dict, **base_fig.get_layout()}
    layout = go.Layout(layout)
    fig = go.Figure(data=data, layout=layout)
    of.plot(fig, filename=outPutName)


if __name__ == '__main__':
    main(settings_plotly.length, settings_plotly.scatter_method, settings_plotly.outPutName)