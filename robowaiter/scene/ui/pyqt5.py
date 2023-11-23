import importlib
import os

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import sys

from robowaiter.scene.ui.window import Ui_MainWindow
from robowaiter.utils.basic import get_root_path
from PyQt5.QtCore import QThread
import queue
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread, pyqtSignal
from robowaiter.scene.ui.scene_ui import SceneUI
from  robowaiter.scene.ui import scene_ui

root_path = get_root_path()

class TaskThread(QThread):
    stop_signal = pyqtSignal()

    def __init__(self, task, scene_cls,robot_cls,scene_queue,ui_queue, *args, **kwargs):
        super(TaskThread, self).__init__(*args, **kwargs)
        self.task = task
        self.scene_cls = scene_cls
        self.robot_cls = robot_cls
        self.scene_queue = scene_queue
        self.ui_queue = ui_queue
        self.stoped = True

    def run(self):
        self.scene = self.task(self.scene_cls,self.robot_cls,self.scene_queue,self.ui_queue)
        self.scene._run()
        # scene._run()

        while not self.isInterruptionRequested():
            self.scene.step()

    # def stop(self):
    #     del self.scene

def run_scene(scene_cls,robot_cls,scene_queue,ui_queue):
    scene = scene_cls(robot_cls(),scene_queue,ui_queue)

    scene.reset()
    # scene.run()
    return scene
    # try:
    #     # 机器人系统的主循环
    #
    # except Exception as e:
    #     # 打印异常信息到命令行
    #     print("Robot system error:", str(e))

example_list = ("AEM","VLN","VLM",'GQA',"OT","AT","reset")

class UI(QMainWindow, Ui_MainWindow):
    scene = None

    def __init__(self,robot_cls):
        app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        super(UI, self).__init__(MainWindow)
        # 创建线程安全的队列
        self.scene_queue = queue.Queue()
        self.ui_queue = queue.Queue()

        self.scene_cls = SceneUI
        self.robot_cls = robot_cls

        self.setupUi(MainWindow)  # 初始化UI

        # 绑定说话按钮
        self.btn_say.clicked.connect(self.btn_say_on_click)
        # 绑定任务演示按钮
        for example in example_list:
            btn = getattr(self,f"btn_{example}")
            btn.clicked.connect(self.create_example_click(example))

        # 设置一个定时器，每隔100ms检查一次队列
        timer = QTimer()
        timer.setInterval(100)  # 设置检查队列的间隔时间
        timer.timeout.connect(self.handle_queue_messages)  # 当定时器超时时，处理队列中的消息
        timer.start()  # 启动定时器

        MainWindow.show()

        self.thread = TaskThread(run_scene,self.scene_cls,self.robot_cls,self.scene_queue,self.ui_queue)
        self.thread.start()

        sys.exit(app.exec_())

    def create_example_click(self,name):
        def btn_example_on_click():
            self.thread.requestInterruption()
            self.thread.wait()  # 等待线程安全退出

            self.scene_queue = queue.Queue()
            self.ui_queue = queue.Queue()
            self.thread = TaskThread(run_scene, self.scene_cls, self.robot_cls,self.scene_queue,self.ui_queue)
            self.thread.start()

            self.scene_func((f"run_{name}",))
        return btn_example_on_click

    def btn_say_on_click(self):
        question = self.edit_say.text()
        if question[-1] == ")":
            print(f"设置目标:{question}")
            self.scene_func(("new_set_goal",question))
            # self.scene.new_set_goal(question)
        else:
            self.scene_func(("customer_say","System",question))
            # self.scene.customer_say("System", question)

    def scene_func(self,args):
        self.scene_queue.put(args)

    def handle_queue_messages(self):
        while not self.ui_queue.empty():
            message = self.ui_queue.get()
            function_name = message[0]
            function = getattr(self, function_name, None)

            args = []
            if len(message)>1:
                args = message[1:]

            result = function(*args)

    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self,MainWindow)

        # dir_path = os.path.dirname(__file__)

        # 加载并显示图片
        # img_path = os.path.join(root_path, "robowaiter/utils/draw_bt/test.png")
        # self.draw_from_file("img_label_bt",img_path)
        # self.label.setAlignment(Qt.AlignCenter)  # 图片居中显示

    def draw_from_file(self,control_name,file_name):
        control = getattr(self,control_name,None)
        # 加载并显示图片
        pixmap = QPixmap(file_name) # 替换为你的图片路径
        # self.label.setPixmap(pixmap)
        control.setPixmap(self.scale_pixmap_to_label(pixmap, control))

    def draw_img(self,control_name,img):
        control = getattr(self,control_name,None)
        # # 加载并显示图片
        # print(img)
        # img = self.ndarray_to_qimage(img)
        # print(img)

        # image = Image.open(io.BytesIO(img))
        # print(image)
        pixmap = QPixmap.fromImage(QImage.fromData(img))

        # self.label.setPixmap(pixmap)
        control.setPixmap(self.scale_pixmap_to_label(pixmap, control))
        # control.setPixmap(pixmap)

    def draw_canvas(self,control_name,canvas):
        control = getattr(self,control_name,None)
        # 加载并显示图片

        pixmap = QApplication.grabWidget(canvas)

        # self.label.setPixmap(pixmap)
        control.setPixmap(self.scale_pixmap_to_label(pixmap, control))


    def ndarray_to_qimage(self,array: np.ndarray) -> QImage:
        # 假设你的ndarray是uint8类型的，且是RGB格式（三个通道）
        height, width, channels = array.shape
        if channels ==3:
            bytes_per_line = channels * width
            image = QImage(array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        else:
            # 对于灰度图像
            image = QImage(array.data, width, height, QImage.Format_Grayscale8)

        return image

    def scale_pixmap_to_label(self, pixmap, label):
        # 获取QLabel的大小
        label_width = label.width()
        label_height = label.height()

        # 保持图片的长宽比，同时确保图片的一个维度适应QLabel的大小
        scaled_pixmap = pixmap.scaledToWidth(label_width, Qt.SmoothTransformation)
        if scaled_pixmap.height() > label_height:
            scaled_pixmap = pixmap.scaledToHeight(label_height, Qt.SmoothTransformation)

        return scaled_pixmap

    def set_scene(self, scene):
        self.scene = scene


if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    ui = UI()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())