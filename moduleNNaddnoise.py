import keras
import matplotlib 
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from sklearn.model_selection import train_test_split
from keras.models import load_model
import pandas as pd
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint,ReduceLROnPlateau
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
import matplotlib.pyplot as plt
class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = {'batch':[], 'epoch':[]}
        self.accuracy = {'batch':[], 'epoch':[]}
        self.val_loss = {'batch':[], 'epoch':[]}
        self.val_acc = {'batch':[], 'epoch':[]}

    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))

    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))

    def loss_plot(self, loss_type):
        iters = range(len(self.losses[loss_type]))
        plt.figure()
        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        if loss_type == 'epoch':
            # val_loss
            plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
        plt.grid(True)
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')
        plt.legend(loc="upper right")
        plt.show()
##上述為繪圖新增
xdata=pd.read_csv('finaldataframe1500_dropother_add0.csv')
print(xdata.shape)
xdata=pd.get_dummies(xdata)
xdata=xdata.fillna(0)
xdatasize=xdata.shape[1]
xdatarow=xdata.shape[0]
print(xdata.shape)
for i in range(7):
    xdatarow=xdata.shape[0]-1
    xdata=xdata.drop(xdatarow)
xdata.columns=range(xdatasize)
ycol=list(range(3))
ydata=pd.DataFrame(xdata,columns=ycol) #將123 column作為輸出層y
xdata=xdata.drop(columns=0,axis=1)#drop H x 
xdata=xdata.drop(columns=1,axis=1)#drop H y
xdata=xdata.drop(columns=2,axis=1)#drop H z
xdatasize=xdata.shape[1]
xdata.columns=range(xdatasize)
print(xdata.shape)
ydata.plot.box()
plt.show()
#ydata=pd.read_csv('splitandonehot_y.csv',index_col=0,low_memory=False)
##add noise
# mu,sigma=0,0.003
# noise=np.random.normal(mu,sigma,[xdatarow,3])
# noise=pd.DataFrame(noise)
# noise=pd.DataFrame(noise,columns=range(xdatasize))
# noise=noise.fillna(0)
# xdata=xdata.add(noise)
x_train, x_test, y_train, y_test = train_test_split(xdata, ydata, test_size=0.2, random_state=42)
# # 建立簡單的線性執行的模型
model = Sequential()
# Add Input layer, 隱藏層(hidden layer) 有 24個輸出變數
model.add(Dense(units=256, input_dim=xdatasize, activation='elu'))
model.add(Dense(units=196, activation='elu'))
model.add(Dense(units=128, activation='elu'))
model.add(Dense(units=100, activation='elu'))
model.add(Dense(units=80, activation='elu')) 
# Add output layer
model.add(Dense(units=3, activation='linear'))
model.compile(loss='mse', optimizer='adam', metrics=['mse']) 
#callback = EarlyStopping(monitor="val_loss", patience=150, verbose=1, mode="max")
#reduce_lr = ReduceLROnPlateau(factor=0.2, 
#                              min_lr=1e-5, 
#                              monitor='mse', 
#                              patience=150,
#                              verbose=1  )
history = LossHistory()

##上述為畫圖新增
model.summary()
train_history = model.fit(x=x_train,y=y_train, validation_split=0.2, epochs=500, batch_size=800, verbose=2,callbacks=[history])  
#train_history = model.fit(x=x_train,y=y_train, validation_split=0.2, epochs=500, batch_size=800, verbose=2,callbacks=[reduce_lr,callback])  
scores = model.evaluate(x_test, y_test) 
#模型评估
score = model.evaluate(x_test, y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])

#绘制acc-loss曲线
history.loss_plot('epoch')

print(y_train.loc[[3172]],'\n',model.predict(x_train.loc[[3172]]),"1500_elu")
model.save('finaldataframe1500_dropother_add0_200.h5')
model=Sequential()
