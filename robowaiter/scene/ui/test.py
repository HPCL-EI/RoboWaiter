import sys
from PyQt5.QtWidgets import QApplication, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, \
    QWidget, QMainWindow
from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtGui import QPixmap, QDrag


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)
        self.setPixmap(QPixmap("image.jpg"))  # 替换为你的图片路径
        self.setScaledContents(True)  # 图片将根据label的大小自动缩放
        self.label_moved = False  # 用于判断是否移动了标签
        self.drag_start_position = QPoint()  # 记录鼠标按下时的位置

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            self.label_moved = False

    def mouseMoveEvent(self, event):
        if not self.label_moved and (event.buttons() & Qt.LeftButton):
            distance = (event.pos() - self.drag_start_position).manhattanLength()
            if distance >= QApplication.startDragDistance():
                self.label_moved = True
                drag = QDrag(self)
                drag.setMimeData(self.mimeData())
                drag.setPixmap(self.grab())
                drag.exec_(Qt.CopyAction | Qt.MoveAction)
                self.drag_start_position = event.pos()

    def mouseReleaseEvent(self, event):
        self.label_moved = False


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    layout = QVBoxLayout()
    # image_label = ImageLabel()  # 显示图片的标签控件
    image_view = ImageView()  # 显示图片的视图控件