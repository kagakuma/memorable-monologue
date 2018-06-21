
# coding: utf-8

# In[37]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import keras
df = pd.read_csv("weightdata.csv",delimiter=",").dropna()
data = []
target = []
max_len = 56
dim = 1
# 正規化
maximum = df.weight.max()
minimum = df.weight.min()
df["weight"] = (df.weight-minimum)/(maximum-minimum)
print(df["weight"].max())
print(df["weight"].min())
#maximum = df.Passengers.max()
#minimum =df.Passengers.min()


# In[38]:


# データを箱に入れる
for i in range(len(df)-max_len-1):
    data.append(df.weight.values[i:i+max_len])
    target.append(df.weight.values[i+max_len+1])
# データの整形
data = np.array(data).reshape(len(data),max_len,dim)
target = np.array(target).reshape(-1,1)


# In[39]:


from sklearn.model_selection import train_test_split
N_train = int(len(data)*0.7)
N_test = len(data) - N_train
X_train, X_validation, Y_train, Y_validation = train_test_split(data, target, test_size=N_test)


# In[40]:


from keras.models import Sequential
from keras.layers import  Dense
#一番シンプルなやつ
from keras.layers.recurrent import SimpleRNN
from keras.layers.recurrent import LSTM, GRU #改良版
model = Sequential()
# ネットワーク構成
input_shape=(max_len, dim)
print(input_shape)
print(max_len)
quart = int(max_len/4)
model.add(Dense(quart,input_shape=input_shape))
#model.add(SimpleRNN(units=64, kernel_initializer="random_uniform",input_shape=input_shape))
model.add(LSTM(units=64, input_dim=quart))
#model.add(GRU(units=64, input_shape=input_shape))

model.add(Dense(input_shape[1],activation="linear"))
# optimizerの設定
from keras.optimizers import Adam
model.compile(loss="mse", optimizer=Adam())


# In[41]:


from keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1)
epochs = 500
batch_size = 10
model.fit(X_train, Y_train,
          batch_size=batch_size, epochs=epochs,
          validation_data=(X_validation, Y_validation))
prediction = []
data_in = data.reshape(data.shape[0],data.shape[1])[N_train]


# In[42]:


iteration = len(data) - N_train
for _ in range(iteration):
#     print(data_in)
    pred = model.predict(data_in.reshape(1,-1,1))
    data_in = np.delete(data_in, 0)
    data_in = np.hstack((data_in, pred[0]))
    prediction.append(pred[0,0])
#weight = list(df.weight)
#data_num = len(weight)
weight = list(df.weight)
plt.plot(weight)
plt.plot(range(N_train+max_len, N_train+max_len+iteration), prediction)


# In[43]:


plt.plot(range(N_train+max_len, N_train+max_len+iteration), prediction)

