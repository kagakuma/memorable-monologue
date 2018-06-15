# CNTK を GPU で動かす
from cntk.device import try_set_default_device, gpu
import cntk
print(cntk.device.all_devices())
print(cntk.device.try_set_default_device(cntk.device.gpu(0)))
print(cntk.device.use_default_device())

# keras の import
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation

# 数学関係およびプロット
import numpy as np
import matplotlib.pyplot as plt

# 時間測定
import time
start_time = time.time()

# モデル定義
model = Sequential()
model.add(Dense(10,input_dim=1))
model.add(Activation('relu'))
model.add(Dense(30,input_dim=10))
model.add(Activation('relu'))
model.add(Dense(100,input_dim=30))
model.add(Activation('relu'))
model.add(Dense(30,input_dim=100))
model.add(Activation('relu'))
model.add(Dense(10,input_dim=30))
model.add(Activation('relu'))
model.add(Dense(1,input_dim=10))

# モデル設定
model.compile(optimizer='Adam',loss='mse')

# 学習させたい非線形関数の設定 y = sin(x)+2cos(2x)-3sin(3x) ここは自由に書き換えられる
# y には平均0標準偏差1の正規乱数を与えてある。これはかなり大きな誤差なのでグラフプロットで確認してほしい
x = np.linspace(-3,3,30000)
y = np.sin(x)+2.0*np.cos(2.0*x)-3.0*np.sin(3.0*x)+np.random.randn(30000)
x = np.array(x, dtype=np.float32)
y = np.array(y, dtype=np.float32)

# 学習は float32 で行われるので書き換え
x = np.array(x, dtype=np.float32)
y = np.array(y, dtype=np.float32)

# 与えられたデータのプロット
plt.plot(x,y)
plt.show()

# モデルの学習
model.fit(x, y,epochs=200,batch_size=1000,verbose=1)

# 学習結果と正解関数のプロット
y_pred = model.predict(x)
y_answer= np.sin(x)+2.0*np.cos(2.0*x)-3.0*np.sin(3.0*x)

plt.plot(x,y_answer, color='black',  linestyle='solid', linewidth = 1.0)
plt.scatter(x,y_pred, color='red',  marker='.', s=20)
plt.show()

# かかった時間の表示
end_time = time.time()
print('start: ' + str(start_time) + '(sec)')
print('end: ' + str(end_time) + '(sec)')
print('processing time: ' + str(end_time - start_time) + '(sec)')
