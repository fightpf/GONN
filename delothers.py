import pandas as pd
import numpy as np
xdata=pd.read_csv('finaldataframe1500_add0.csv')
xdata=xdata.fillna(0)
print(xdata.shape)
##drop 非碳氫氧氮磷硫矽原子
for i in range(0,xdata.shape[1]-3,4):
    i=str(i)
    print(i)
#    print(xdata[(xdata[i]!='H')&(xdata[i]!='C')&(xdata[i]!='N')&(xdata[i]!='O')&(xdata[i]!='P')&(xdata[i]!='S')])
    xdata=xdata.drop(xdata[(xdata[i]!='H')&(xdata[i]!='C')&(xdata[i]!='N')&(xdata[i]!='O')&(xdata[i]!='P')&(xdata[i]!='S')&(xdata[i]!=0)].index.tolist())
    print(xdata.shape)
xdata.to_csv('C:\\jimmy\\ch305\\oraldefense\\python\\finaldataframe1500_dropother_add0.csv',index=False)