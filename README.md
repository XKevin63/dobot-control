# dobot机械臂
dobot机械臂和海康威士相机实现不同颜色的物块抓取。
本程序环境为ubuntu，且需要安装海康威士的MVS软件。
图像处理采用opencv处理，包含了颜色的识别及物体堆叠高度的识别。
摄像头与机械臂需要进行坐标的转化，采用棋盘格的九点标定法实现。
