import sklearn
import numpy as np
import pandas   as pd
import matplotlib.pyplot as plt
import math
import random
import torch
from torch import nn
import os
os.environ["KERAS_BACKEND"] = 'torch'   #需要设置之后才能正常导入，或者在.keras/keras.json文件中将backend属性改成torch（tensorflow/jax）

import keras
import keras.layers as layers
import seaborn as sns

#构建一个用来预测70年代末到80年代初汽车燃油效率的模型，数据集包含汽车描述：气缸数，排量，马力以及重量等等
column_names = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year', 'origin']
raw_dataset = pd.read_csv('C:/Users/WL/Desktop/Graduation_Project/IM/Work_file/Prediction_based_on_Multimodal/auto-mpg/auto-mpg.data', names=column_names, na_values='?', comment='\t', sep=' ', skipinitialspace=True)
dataset = raw_dataset.copy()
# dataset.tail()
print(dataset.tail())

#清洗数据
dataset.isna().sum()    #is NA(缺失值表示missing values也就是 not available)
dataset = dataset.dropna()

#origin分类转换成独热编码
origin = dataset.pop('origin')
dataset['USA'] = (origin == 1)*1.0
dataset['Europe'] = (origin == 2)*1.0
dataset['Japan'] = (origin == 3)*1.0
print(dataset.tail())

#拆分数据集：训练集、测试集
train_dataset = dataset.sample(frac=0.8, random_state=42)
test_dataset = dataset.drop(train_dataset.index)

#快速查看训练集中几个列的联合分布与数据统计
sns.pairplot(train_dataset[['mpg', 'cylinders', 'displacement', 'weight']], diag_kind='kde')
train_status = train_dataset.describe()
train_status.pop('mpg')
train_status = train_status.transpose()
print(train_status) #figure_1

#从标签中分离特征,即训练模型时需要预测的值
train_labels = train_dataset.pop('mpg')
test_labels = test_dataset.pop('mpg')

#数据归一化：将测试数据集放入到与已经训练过的模型相同的分布中。
def norm(x):
    return (x-train_status['mean'])/train_status['std']
normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)

#模型构建
def build_model():
    model = keras.Sequential([
        #UserWarning: Do not pass an `input_shape`/`input_dim` argument to a layer. 
        #When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead.
        #layers.Input()
        layers.Dense(64, activation = 'relu', input_shape = [len(train_dataset.keys())]),
        layers.Dense(64, activation = 'relu'),
        layers.Dense(1)
    ])
    # model = nn.Sequential #都可以，以后可以多尝试不同的包

    optimizer = keras.optimizers.RMSprop(0.001)
    
    model.compile(loss = 'mse', optimizer = optimizer, metrics = ['mae', 'mse'])
    return model

model = build_model()
# #检查模型，.summary()函数可以打印该模型的简单描述
# print(model.summary())
# #试用模型:从训练数据中批量获取‘10’条例子并对这些例子调用 model.predict
# example_batch = normed_train_data[:10]
# example_out = model.predict(example_batch)
# print(example_out)

#训练模型：进行1000个epoch的训练，在history对象中记录训练、验证的准确性

#打印.显示训练进度
class printdot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if epoch % 100 ==0:
            print('')
        print('.', end = '')
        return super().on_epoch_end(epoch, logs)
epoch = 1000


#使用history对象中存储的统计信息进行可视化
# his = pd.DataFrame(history.history)
# his['epoch'] = history.epoch
# print(his.tail())

def plot_his(history):
    his = pd.DataFrame(history.history)
    his['epoch'] = history.epoch
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [mpg]')
    plt.plot(his['epoch'], his['mae'], label = 'train error')
    plt.plot(his['epoch'], his['val_mae'], label = 'val error')
    plt.ylim([0, 5])
    plt.legend()

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$mpg^2$]')
    plt.plot(his['epoch'], his['mse'], label = 'train error')
    plt.plot(his['epoch'], his['val_mse'], label = 'val error')
    plt.ylim([0,20])
    plt.legend()
    plt.show()

#设置断点，当验证值没有提高时自动结束训练
early_stop = keras.callbacks.EarlyStopping(monitor = 'val_loss', patience = 10)
history = model.fit(
    normed_train_data,
    train_labels,
    epochs = epoch,
    validation_split = 0.2,
    verbose = 0,
    callbacks = [early_stop, printdot()]
)

plot_his(history)

#查看泛化效果
loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose = 1)
print('testing set mean abs error :{:5.2f} mpg'.format(mae))

#预测：使用测试集数据来预测MPG值
test_pridic = model.predict(normed_test_data).flatten()
plt.scatter(test_labels, test_pridic)
plt.xlabel('true mpg values')
plt.ylabel('predict mpg values')
plt.axis('equal')
plt.axis('square')
plt.xlim([0, plt.xlim()[1]])
plt.ylim([0, plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100,100])

#预测的误差分布：
error = test_pridic - test_labels
plt.hist(error, bins = 25)
plt.xlabel('prediction error mpg')
_ = plt.ylabel('count')