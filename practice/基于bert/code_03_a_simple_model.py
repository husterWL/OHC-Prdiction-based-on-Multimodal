import torch
import numpy as np
from torch.autograd import Variable
import matplotlib.pyplot as plt
import sklearn.datasets
import torch.nn as nn
# 准备一个可以复现的随机数据
torch.manual_seed(0)
torch.cuda.manual_seed_all(0)
torch.backends.cudnn.deterministic=True
torch.backends.cudnn.benchmark=False
np.random.seed(0)
x,y=sklearn.datasets.make_moons(200,noise=0.2)

arg=np.squeeze(np.argwhere(y==0),axis=1)
arg2=np.squeeze(np.argwhere(y==1),axis=1)
plt.title("moons data")
plt.scatter(x[arg,0], x[arg,1], s=100,c='b',marker='+',label='data1')
plt.scatter(x[arg2,0], x[arg2,1],s=40, c='r',marker='o',label='data2')
plt.legend()
plt.show()

#模型定义,继承nn.module，构建网络模型
class LogicNet(nn.Module):
    def __init__(self,inputdim,hiddendim,outputdim):#初始化网络结构,包含输入层、隐藏层、输出层
        super(LogicNet,self).__init__()
        self.Linear1 = nn.Linear(inputdim,hiddendim) #定义全连接层   #将function赋给变量，这个变量有这个函数的功能？就是取别名，指向同一个空间
        self.Linear2 = nn.Linear(hiddendim,outputdim)#定义全连接层
        self.criterion = nn.CrossEntropyLoss() #定义交叉熵函数（损失函数）

    def forward(self,x): #搭建用两层全连接组成的网络模型（正向传播)     感觉这里是将形参x传入linear1，运算结果再赋给形参x；再往下也是一样的，没有开辟新的空间
        x = self.Linear1(x)#将输入数据传入第1层
        x = torch.tanh(x)#对第一层的结果进行非线性变换
        x = self.Linear2(x)#再将数据传入第2层
        #print("LogicNet")
        return x

    def predict(self,x):#实现LogicNet类的预测接口
        #调用自身网络模型，并对结果进行softmax处理,分别得出预测数据属于每一类的概率
        pred = torch.softmax(self.forward(x),dim=1)
        return torch.argmax(pred,dim=1)  #返回每组预测概率中最大的索引

    def getloss(self,x,y): #实现LogicNet类的损失值计算接口
        y_pred = self.forward(x)
        loss = self.criterion(y_pred,y)#计算损失值得交叉熵
        return loss

#定义函数计算移动平均损失值
def moving_average(a, w=10):#定义函数计算移动平均损失值
    if len(a) < w:
        return a[:]
    return [val if idx < w else sum(a[(idx-w):idx])/w for idx, val in enumerate(a)]

#定义函数展示losses曲线
def plot_losses(losses):
    avgloss= moving_average(losses) #获得损失值的移动平均值 
    plt.figure(1)
    plt.subplot(211)
    plt.plot(range(len(avgloss)), avgloss, 'b--')
    plt.xlabel('step number')
    plt.ylabel('Training loss')
    plt.title('step number vs. Training loss')
    plt.show()

#封装支持Numpy的预测接口
def predict(model,x):
    x = torch.from_numpy(x).type(torch.FloatTensor)
    ans = model.predict(x)
    return ans.numpy()

#在直角坐标系中可视化模型能力
def plot_decision_boundary(pred_func,x,y):
    #计算取值范围
    x_min, x_max = x[:, 0].min() - .5, x[:, 0].max() + .5
    y_min, y_max = x[:, 1].min() - .5, x[:, 1].max() + .5
    h = 0.01
    #在坐标系中采用数据，生成网格矩阵，用于输入模型
    xx,yy=np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    #将数据输入并进行预测
    Z = pred_func(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    #将预测的结果可视化
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.title("Linear predict")
    arg = np.squeeze(np.argwhere(y==0),axis = 1)
    arg2 = np.squeeze(np.argwhere(y==1),axis = 1)
    plt.scatter(x[arg,0], x[arg,1], s=100,c='b',marker='+')
    plt.scatter(x[arg2,0], x[arg2,1],s=40, c='r',marker='o')
    plt.show()

#模型构建与运行
model = LogicNet(inputdim=2,hiddendim=3,outputdim=2)#初始化模型     2×3×2的一个全连接模型
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)#定义优化器

xt = torch.from_numpy(x).type(torch.FloatTensor)#将Numpy数据转化为张量
yt = torch.from_numpy(y).type(torch.LongTensor)
epochs = 2000#定义迭代次数
losses = []#定义列表，用于接收每一步的损失值
for i in range(epochs):
    loss = model.getloss(xt,yt)
    losses.append(loss.item())
    optimizer.zero_grad()#清空之前的梯度
    loss.backward()#反向传播损失值
    optimizer.step()#更新参数

plot_losses(losses)

from sklearn.metrics import accuracy_score
print(accuracy_score(model.predict(xt),yt))

plot_decision_boundary(lambda x : predict(model,x) ,xt.numpy(), yt.numpy())