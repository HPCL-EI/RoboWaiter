import importlib
import os

from PyQt5.QtSvg import QGraphicsSvgItem, QSvgWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QGraphicsView, QGraphicsScene, \
    QGraphicsPixmapItem, QGraphicsProxyWidget, QLineEdit
from PyQt5.QtCore import QTimer, QPoint, QRectF
from PyQt5 import QtCore
import sys

from robowaiter.scene.ui.window import Ui_MainWindow
from robowaiter.utils.basic import get_root_path
from PyQt5.QtCore import QThread
import queue
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QDrag, QPainter
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
more_example_list = ("VLM_AC","CafeDaily")
dic_more2zh={
    "VLM_AC":"开空调并调节空调温度",
    "CafeDaily":"咖啡厅的一天"
}
more_example_list_zh = [value for value in dic_more2zh.values()]

class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def wheelEvent(self, event):
        factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(factor, factor)
        else:
            self.scale(1.0 / factor, 1.0 / factor)

class UI(QMainWindow, Ui_MainWindow):
    scene = None
    history_dict = {
        "System": ""
    }

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

        MainWindow.setWindowTitle("RoboWatier")
        # MainWindow.setWindowIcon(QIcon("icons/umbrella.ico"))

        # 绑定说话按钮
        self.btn_say.clicked.connect(self.btn_say_on_click)
        self.verticalLayout_2.removeWidget(self.img_view_bt)
        self.img_view_bt = GraphicsView(self.centralwidget)
        self.img_view_bt.setObjectName("img_view_bt")
        self.verticalLayout_2.addWidget(self.img_view_bt)
        self.img_view_bt.setDragMode(QGraphicsView.ScrollHandDrag)

        lineEdit = QLineEdit()
        lineEdit.setReadOnly(True)  # 设置只读
        lineEdit.setAlignment(Qt.AlignCenter)  # 设置文字居中
        lineEdit.setPlaceholderText("请选择其他任务")
        self.cb_task.setLineEdit(lineEdit)



        # 下拉菜单绑定函数
        # 下拉菜单.seleted.connect(self.你写的函数)

        # # BT树的显示
        # self.setScaledContents(True)  # 图片将根据label的大小自动缩放
        # self.label_moved = False  # 用于判断是否移动了标签
        # self.drag_start_position = QPoint()  # 记录鼠标按下时的位置

        self.cb_task.setCurrentIndex(-1)
        self.cb_task.setPlaceholderText("请选择更多任务")

        # 多个添加条目
        self.cb_task.addItems(more_example_list_zh)
        # 当下拉索引发生改变时发射信号触发绑定的事件
        self.cb_task.currentIndexChanged.connect(self.cb_selectionchange)

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
        self.list_customer.itemClicked.connect(self.show_customer_history)

        sys.exit(app.exec_())

    def cb_selectionchange(self, i):
        print(i)
        self.create_example_click(more_example_list[i])()

    def get_semantic_info(self, semantic_info_str):
        # self.textEdit_5.clear()
        # self.textEdit_5.append(semantic_info_str)
        self.textBrowser_5.clear()
        self.textBrowser_5.append(semantic_info_str)

    def new_history(self,customer_name,chat):
        role = chat["role"]
        content = chat["content"].strip()
        function_call = chat.get("function_call",None)
        if function_call:
            return
        if role == "function":
            new_chat = f'Robot:\n 工具调用-{chat["name"]}\n'
        elif role == "user":
            new_chat = f'{customer_name}:\n {content}\n'
        else:
            new_chat = f'Robot:\n {content}\n'

        self.history_dict[customer_name] += new_chat + "\n"
        self.history_dict["Global"] += new_chat + "\n"
        items = self.list_customer.findItems(customer_name, Qt.MatchExactly)
        if items:
            index = self.list_customer.indexFromItem(items[0])
            self.list_customer.setCurrentIndex(index)
        self.edit_local_history.clear()
        self.edit_local_history.append(self.history_dict["Global"])

    def reset(self):
        self.history_dict = {
            "Global":"",
            "System": "",
        }
        self.edit_local_history.clear()
        self.list_customer.clear()
        item = QListWidgetItem("Global")
        self.list_customer.addItem(item)
        item = QListWidgetItem("System")
        self.list_customer.addItem(item)




    def create_example_click(self,name):
        def btn_example_on_click():
            self.reset()

            self.thread.requestInterruption()
            self.thread.wait()  # 等待线程安全退出

            self.scene_queue = queue.Queue()
            self.ui_queue = queue.Queue()
            self.thread = TaskThread(run_scene, self.scene_cls, self.robot_cls,self.scene_queue,self.ui_queue)
            self.thread.start()

            self.scene_func((f"run_{name}",))
        return btn_example_on_click

    def add_walker(self,name):
        self.history_dict[name] = ""
        item = QListWidgetItem(name)
        self.list_customer.addItem(item)


    def show_customer_history(self, item):
        # 此处为示例，实际上你可能需要从数据库或其他地方获取聊天记录
        name = item.text()
        self.edit_local_history.clear()
        self.edit_local_history.append(self.history_dict[name])

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
        # img_path = os.path.join(root_path, "robowaiter/utils/draw_bt/llm_test.png")
        # self.draw_from_file("img_label_bt",img_path)
        # self.label.setAlignment(Qt.AlignCenter)  # 图片居中显示

    def draw_from_file(self,control_name,file_name):

        control = getattr(self,control_name,None)
        # 加载并显示图片
        pixmap = QPixmap(file_name) # 替换为你的图片路径

        if control_name == "img_view_bt":
            # self.img_view_bt = ImageView()
            scene = QGraphicsScene(self.img_view_bt)
            self.img_view_bt.setScene(scene)
            pixmap_item = QGraphicsPixmapItem(pixmap)
            scene.addItem(pixmap_item)


            # widget = QSvgWidget(file_name)
            # # widget.resize(10000, 1600)
            # svg_width = widget.width()
            # widget.resize(svg_width*2, 1600)
            # proxy = QGraphicsProxyWidget()
            # proxy.setWidget(widget)
            # scene.addItem(+proxy)


        elif control_name == "img_label_obj":
            return
            # self.label.setPixmap(pixmap)
        else:
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