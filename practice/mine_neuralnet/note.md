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