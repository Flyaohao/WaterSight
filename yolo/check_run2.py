import torch
import cv2

# 加载 YOLOv5 模型
model = torch.hub.load('.', 'custom', path='pretrained/yolov5s.pt', source='local')

# 打开摄像头
cap = cv2.VideoCapture(0)  # 0 表示默认摄像头

while True:
    # 读取摄像头帧
    ret, frame = cap.read()
    if not ret:
        print("无法读取摄像头画面")
        break

    # 将 BGR 图像转换为 RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 使用模型进行推理
    results = model(img_rgb)

    # 将结果渲染到图像上
    results.render()  # 直接在原图上绘制检测框和标签
    img_with_detections = results.imgs[0]  # 获取渲染后的图像
    img_with_detections_bgr = cv2.cvtColor(img_with_detections, cv2.COLOR_RGB2BGR)  # RGB 转 BGR
    # 显示结果
    cv2.imshow('YOLOv5 摄像头检测', img_with_detections_bgr)

    # 按下 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()
cv2.destroyAllWindows()