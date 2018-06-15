# CNTK の GPU 利用を設定する
from cntk.device import gpu, try_set_default_device
import cntk as C
if C.device.try_set_default_device(C.device.gpu(0)):
    print("GPU")
else:
    warnings.warn(
        'CNTK backend warning: GPU is not detected. '
        'CNTK\'s CPU version is not fully optimized,'
        'please run with GPU to get better performance.')

# 開始時刻を記録
#from __future__ import print_function
import time
start_time = time.time()

# keras の設定
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop

# バッチサイズ、正解クラスの数、学習繰り返し回数の設定
batch_size = 128
num_classes = 10
epochs = 20

# the data, shuffled and split between train and test sets
# mnist のデータをダウンロード
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# データの形状変更。訓練データは60000個で、ひとつの画像が28*28=784ピクセルなので784次元データ
x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
# categorical_crossentropyとともに用いるためのバイナリのクラス行列に変換
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# モデル設計 add で層を追加するなどしてニューラルネットワークを構築する
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(784,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(10, activation='softmax'))

model.summary()

# モデルをコンパイル。損失関数、最適化手法、評価関数を設定
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

# データセットの反復で学習させる。反復回数は epochs など。返り値は訓練時に得られたすべての情報を持っている
history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))
# モデルの損失値と評価値を返す
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# 時間計測
end_time = time.time()
print('start: ' + str(start_time) + '(sec)')
print('end: ' + str(end_time) + '(sec)')
print('processing time: ' + str(end_time - start_time) + '(sec)')