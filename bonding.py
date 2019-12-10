import numpy as np
import pandas as pd
import re 
def splitdata(loadfilename):
    fopen=open(loadfilename)
    text = []
    for line in fopen:
        text.append(line)
    p_head=text.index(" COORDINATES OF ALL ATOMS ARE (ANGS)\n")
    p_tail=text.index("          1 ELECTRON INTEGRALS\n")
    flength=len(text)
    del text[p_tail:flength]
    del text[0:p_head]
    flength=len(text)
    del text[flength-2:flength]
    del text[0:3]
    flength=len(text)
    for i in range(flength):
        text[i]=re.split("\s+",text[i])
        del text[i][6]
        del text[i][2]
        del text[i][0]
    fopen.close()
    #text_temp=text[0]
    #text=pd.DataFrame(text,columns=text_temp)
    text=pd.DataFrame(text)
    text=text.apply(pd.to_numeric , errors='ignore')
    # text=text.drop(columns=0,axis=1)
    # print(text)
    # text=text.drop(columns=2,axis=1)
    return text

#測定最短的鍵長與相連接的原子編號
def bond_length_selection(molestructure):
    mindistance=[]
    atomindex=[]
    #print(molestructure)
    for i in range(molestructure.shape[0]): 
        if molestructure.iloc[i,0]=="H":
            distance=[]
            for j in range(molestructure.shape[0]):
                if molestructure.iloc[j,0]=="H":
                    continue
                temp_distance=((molestructure.iloc[j,1]-molestructure.iloc[i,1])**2+(molestructure.iloc[j,2]-molestructure.iloc[i,2])**2+(molestructure.iloc[j,3]-molestructure.iloc[i,3])**2)**0.5
                if temp_distance!=0:#扣除自己本身 否則minimun會選到自己
                    distance.append(temp_distance)
            mindistance.append(min(distance))
            atomindex.append(i)
    return mindistance,atomindex

#將半徑為radius(angstron)以內的的原子挑出
def environment_drop(molestructure,radius):
    environment_index=[]
    #atomindex
    for i in range(molestructure.shape[0]):
        if molestructure.iloc[i,0]=="H":
            distance=[]
            for j in range(molestructure.shape[0]):
                #if molestructure.iloc[j,0]=="H": #是否忽略周圍的氫
                #    continue
                #計算距離
                temp_distance=((molestructure.iloc[j,1]-molestructure.iloc[i,1])**2+(molestructure.iloc[j,2]-molestructure.iloc[i,2])**2+(molestructure.iloc[j,3]-molestructure.iloc[i,3])**2)**0.5
                distance.append(temp_distance)
            k = [index for index,value in sorted(list(enumerate(distance)),key=lambda x:x[1])]#將鍵長小排到大
            environment_index.append([k[l] for l in range(len(distance)) if distance[k[l]] <= radius])
            #atomindex.append(i)
    return environment_index

#將index feature化
def environment_selection(text,environment_index):
    text2=pd.DataFrame()
    for i in range(len(environment_index)):
        for j in range(len(environment_index[i][:])*4): #以氫為中心,將原子座標轉化為特徵，並以四進位取得0~3的cloumn內數值
            if j%4==0: #原子為字串不須做處裡直接複製
                text2.loc[i,j]=text.loc[environment_index[i][j//4],j%4]
            elif j>0:  
                text2.loc[i,j]=text.loc[environment_index[i][j//4],j%4] #如需要平移則在此加
                #-text.loc[atomindex[i],j%4]#將與該氫圍成的球形半徑內所有的原子以氫為中心normalize
            else:#python除以0會發生未預期錯誤
                text2.loc[i,j]=text.loc[environment_index[i][j],0]#如需要平移則在此加
    return text2
##建立一個在原子column都有所有原子種類的DataFrame，使get_dummies時能正常one-hot encoding
def insert_all_kindatoms(text):
    dictatom={0:'H',1:'C',2:'N',3:'O',4:'P',5:'S',6:0}  
    for k in range(len(dictatom)):
        dic=[]
        key=range(text.shape[1]) #根據讀近來資料的最大值
        #key=range(140) #根據固定值改變最大值
        #for i in range(140//4):#根據有指定原子數目
        for i in range(text.shape[1]//4):#根據有多少原子數目
            dic.append(dictatom[k])
            for j in range(3):
                dic.append(0)
        dic=dict(zip(key,dic))
        if k==0: 
            datadic=pd.DataFrame([dic])
        if k !=0 :
            dfatom=pd.DataFrame([dic])
            datadic=pd.concat([datadic ,dfatom],ignore_index = True )
    text=pd.concat([text,datadic],ignore_index = True)
    return text

#開啟檔案並做特徵化
def environmemttofeature(number):
    finaldataframe=pd.DataFrame()
    for i in range(number):
        try:
            loadfilename=str(i+1)
            loadfilename=loadfilename.zfill(9)
            loadfilename_temp="{temp}.b3lyp_6-31g(d).log"
            loadfilename=loadfilename_temp.format(temp=loadfilename)
            loadfilename='C:\jimmy\ch305\oraldefense\python\{temp}'.format(temp=loadfilename)
            
            text=splitdata(loadfilename)
            #檢查內容
#            print(text)
##去除其他原子
#            if text[(text['0']!='H')&(text['0']!='C')&(text['0']!='N')&(text['0']!='O')&(text['0']!='P')&(text['0']!='S')] :
#                continue
            #text=pd.read_table(open(loadfilename),header=None,delim_whitespace=True,engine='python')
            #text=pd.read_table(text,header=None,delim_whitespace=True,engine='python')
            #text=text.apply(pd.to_numeric,errors='coerce')
            environment_index = environment_drop(text,4)
            atomindex=bond_length_selection(text)[1]
            text2=environment_selection(text,environment_index)
            #text2=pd.get_dummies(text2)
            if i ==0 :
                finaldataframe=text2       
            else:   
                finaldataframe=finaldataframe.append(text2 , ignore_index=True)
            print(i)
        except:
            continue
    return finaldataframe
if __name__=="__main__":
    #finaldataframe=pd.read_csv('C:\\jimmy\\ch305\\oraldefense\\python\\finaldataframe.csv')    
    finaldataframe=environmemttofeature(1500)
    finaldataframe=insert_all_kindatoms(finaldataframe)
    finaldataframe.to_csv('C:\\jimmy\\ch305\\oraldefense\\python\\finaldataframe1500_add0.csv',index=False) #儲存檔案
