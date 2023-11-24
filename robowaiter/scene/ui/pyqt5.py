import importlib
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QGraphicsView, QGraphicsScene, \
    QGraphicsPixmapItem
from PyQt5.QtCore import QTimer, QPoint, QRectF
import sys

from robowaiter.scene.ui.window import Ui_MainWindow
from robowaiter.utils.basic import get_root_path
from PyQt5.QtCore import QThread
import queue
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QDrag
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

class ImageView(QGraphicsView):
    def __init__(self, parent=None):
        super(ImageView, self).__init__(parent)
        self.scene = QGraphicsScene(self)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.setScene(self.scene)
        self.setInteractive(True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and (
                event.pos() - self.drag_start_position).manhattanLength() >= QApplication.startDragDistance():
            drag = QDrag(self)
            drag.setMimeData(self.mimeData())
            drag.setPixmap(self.grab())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)
            self.drag_start_position = event.pos()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scaleView(1.2)  # 放大图片
        elif event.angleDelta().y() < 0:
            self.scaleView(1 / 1.2)  # 缩小图片

    def scaleView(self, scale):
        factor = self.transform().scale(scale, scale).mapRect(QRectF(0, 0, 100, 100)).size().width()
        if factor < 50:  # 设置最小缩放限制，避免过度缩小导致无法看清内容
            return
        self.scale(scale, scale)  # 缩小或放大视图中的所有内容，包括图形项和网格/坐标轴

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

        # 绑定说话按钮
        self.btn_say.clicked.connect(self.btn_say_on_click)
        self.img_view_bt.setDragMode(QGraphicsView.ScrollHandDrag)

        # # BT树的显示
        # self.setScaledContents(True)  # 图片将根据label的大小自动缩放
        # self.label_moved = False  # 用于判断是否移动了标签
        # self.drag_start_position = QPoint()  # 记录鼠标按下时的位置




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

        self.edit_global_history.append(f'{new_chat}')
        self.history_dict[customer_name] += new_chat + "\n"
        items = self.list_customer.findItems(customer_name, Qt.MatchExactly)
        if items:
            index = self.list_customer.indexFromItem(items[0])
            self.list_customer.setCurrentIndex(index)
        self.edit_local_history.clear()
        self.edit_local_history.append(self.history_dict[customer_name])

    def reset(self):
        self.history_dict = {
            "System": ""
        }
        self.edit_local_history.clear()
        self.edit_global_history.clear()
        self.list_customer.clear()
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
        # img_path = os.path.join(root_path, "robowaiter/utils/draw_bt/test.png")
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