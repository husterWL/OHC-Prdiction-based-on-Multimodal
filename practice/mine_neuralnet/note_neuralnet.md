# 神经网络回归小记
## 2023年12月7日
    回归问题的一般求解流程
    1、选定训练模型（求解框架）：线性回归模型/logistic回归等等
    2、导入训练集（dataset）
    3、选择合适的学习算法
    4、验证、测试

## 2023年12月8日
    auto_mpg问题：
    D:\Anaconda_WL\Lib\site-packages\keras\src\layers\core\dense.py:73: UserWarning: Do not pass an `input_shape`/`input_dim` argument to a layer. When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead.
    super().__init__(activity_regularizer=activity_regularizer, **kwargs)
    Traceback (most recent call last):
    File "c:\Users\WL\Desktop\Graduation_Project\IM\Work_file\Prediction_based_on_Multimodal\OHC-Prdiction-based-on-Multimodal\practice\mine_neuralnet\neural_net.py", line 69, in <module>
    model = build_model()
    File "c:\Users\WL\Desktop\Graduation_Project\IM\Work_file\Prediction_based_on_Multimodal\OHC-Prdiction-based-on-Multimodal\practice\mine_neuralnet\neural_net.py", line 66, in build_model
    model.compile(lose = 'mse', optimizer = optimizer, metrics = ['mae', 'mse'])
    File "D:\Anaconda_WL\Lib\site-packages\keras\src\utils\traceback_utils.py", line 123, in error_handler
    raise e.with_traceback(filtered_tb) from None
    File "D:\Anaconda_WL\Lib\site-packages\keras\src\utils\tracking.py", line 25, in wrapper
    return fn(*args, **kwargs)
    TypeError: compile() got an unexpected keyword argument 'lose'

## 2023年12月12日
    mpg  cylinders  displacement  horsepower  weight  acceleration  model_year  origin
    393  27.0          4         140.0        86.0  2790.0          15.6          82       1
    394  44.0          4          97.0        52.0  2130.0          24.6          82       2
    395  32.0          4         135.0        84.0  2295.0          11.6          82       1
    396  28.0          4         120.0        79.0  2625.0          18.6          82       1
    397  31.0          4         119.0        82.0  2720.0          19.4          82       1
    mpg  cylinders  displacement  horsepower  weight  acceleration  model_year  USA  Europe  Japan
    393  27.0          4         140.0        86.0  2790.0          15.6          82  1.0     0.0    0.0
    394  44.0          4          97.0        52.0  2130.0          24.6          82  0.0     1.0    0.0
    395  32.0          4         135.0        84.0  2295.0          11.6          82  1.0     0.0    0.0
    396  28.0          4         120.0        79.0  2625.0          18.6          82  1.0     0.0    0.0
    397  31.0          4         119.0        82.0  2720.0          19.4          82  1.0     0.0    0.0
                  count         mean         std     min       25%     50%      75%     max
    cylinders     314.0     5.531847    1.729449     3.0     4.000     4.0     8.00     8.0
    displacement  314.0   197.855096  106.501896    68.0   105.000   151.0   302.00   455.0
    horsepower    314.0   105.971338   39.636557    46.0    76.000    95.0   130.00   230.0
    weight        314.0  3005.745223  859.060925  1649.0  2231.000  2831.5  3641.75  4955.0
    acceleration  314.0    15.510828    2.803560     8.0    13.625    15.5    17.00    24.8
    model_year    314.0    75.910828    3.688989    70.0    73.000    76.0    79.00    82.0
    USA           314.0     0.624204    0.485101     0.0     0.000     1.0     1.00     1.0
    Europe        314.0     0.171975    0.377961     0.0     0.000     0.0     0.00     1.0
    Japan         314.0     0.203822    0.403481     0.0     0.000     0.0     0.00     1.0
    Model: "sequential"
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
    ┃ Layer (type)                       ┃ Output Shape                  ┃     Param # ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
    │ dense (Dense)                      │ (None, 64)                    │         640 │
    ├────────────────────────────────────┼───────────────────────────────┼─────────────┤
    │ dense_1 (Dense)                    │ (None, 64)                    │       4,160 │
    ├────────────────────────────────────┼───────────────────────────────┼─────────────┤
    │ dense_2 (Dense)                    │ (None, 1)                     │          65 │
    └────────────────────────────────────┴───────────────────────────────┴─────────────┘
    Total params: 4,865 (19.00 KB)
    Trainable params: 4,865 (19.00 KB)
    Non-trainable params: 0 (0.00 B)
    None
    1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 135ms/step
    [[-0.60823494]
    [-0.52716595]
    [-0.2854147 ]
    [ 0.18104734]
    [-0.01853323]
    [-0.05670723]
    [ 0.49135414]
    [-0.10936853]
    [ 0.11062308]
    [-0.6413926 ]]

## 2023年12月13日
    训练一千轮
            loss       mae       mse  val_loss   val_mae   val_mse  epoch
    995  3.207506  1.140733  3.109133  4.586595  1.682144  4.599195    995
    996  3.262425  1.175621  3.281843  4.578247  1.763736  4.592645    996
    997  3.157277  1.204019  3.164652  4.581371  1.769662  4.598663    997
    998  3.318463  1.182180  3.359146  4.277695  1.595556  4.291914    998
    999  3.074377  1.118435  3.103136  4.597200  1.729864  4.612801    999
![figure_1](C:/Users/WL/Desktop/Graduation_Project/IM/Work_file/Prediction_based_on_Multimodal/OHC-Prdiction-based-on-Multimodal/practice/mine_neuralnet/Figure_1.png)
![figure_2](C:/Users/WL/Desktop/Graduation_Project/IM/Work_file/Prediction_based_on_Multimodal/OHC-Prdiction-based-on-Multimodal/practice/mine_neuralnet/Figure_2.png)
![figure_3](C:/Users/WL/Desktop/Graduation_Project/IM/Work_file/Prediction_based_on_Multimodal/OHC-Prdiction-based-on-Multimodal/practice/mine_neuralnet/Figure_3.png)

    训练断点后
![figure_4](C:/Users/WL/Desktop/Graduation_Project/IM/Work_file/Prediction_based_on_Multimodal/OHC-Prdiction-based-on-Multimodal/practice/mine_neuralnet/Figure_4.png)
![figure_5](C:/Users/WL/Desktop/Graduation_Project/IM/Work_file/Prediction_based_on_Multimodal/OHC-Prdiction-based-on-Multimodal/practice/mine_neuralnet/Figure_5.png)
    3/3 ━━━━━━━━━━━━━━━━━━━━ 0s 16ms/step - loss: 5.0587 - mae: 1.6451 - mse: 4.6262
    testing set mean abs error : 1.73 mpg
    3/3 ━━━━━━━━━━━━━━━━━━━━ 0s 3ms/step