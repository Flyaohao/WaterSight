import torch
import cv2 as cv

# 加载自定义的 YOLOv5 模型
# 该模型用于执行目标检测任务

'''
参数解释如下：
.：表示当前目录作为 torch.hub 的根目录。
'custom'：指定加载的是一个自定义模型。YOLOv5 支持多种预训练模型（如 'yolov5s', 'yolov5m' 等），而 'custom' 表示加载的是用户自定义或本地训练的模型，而不是官方提供的标准模型。
path='pretrained/yolov5s.pt'：指定模型文件的路径，这里是相对路径，指向名为 yolov5s.pt 的预训练模型文件。
source='local'：表示从本地加载模型，而不是从远程仓库加载。
'''
model = torch.hub.load('.', 'custom', path='pretrained/yolov5s.pt', source='local')

# 读取图像，格式为 BGR
img_bgr = cv.imread("data/images/baby.jpg")

# 将图像从 BGR 格式转换为 RGB 格式
# 这一步是必要的，因为模型期望输入的图像是 RGB 格式
img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)

# 使用模型对 RGB 图像进行目标检测
results = model(img_rgb)

# 保存检测结果
# 默认情况下，结果会保存在 'runs/detect' 目录下
results.save()

# 下面这行代码被注释掉了
# 如果取消注释，它会将检测结果保存到名为 "result" 的指定目录或文件中
# results.save("result")
