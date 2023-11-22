import tkinter as tk
from robowaiter.utils.basic import get_root_path
from tkinter import PhotoImage
import os
root_path = get_root_path()

class Robot:
    def __init__(self):
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            # 在这里添加启动机器人的逻辑代码
            print("机器人正在启动...")

    def stop(self):
        if self.is_running:
            self.is_running = False
            # 在这里添加停止机器人的逻辑代码
            print("机器人正在停止...")

    def get_status(self):
        if self.is_running:
            return "运行中"
        else:
            return "已停止"


class RobotInterface:
    def __init__(self, master):
        self.master = master
        # self.robot = Robot()  # 假设这里有一个名为Robot的类，表示机器人系统

        # 创建启动机器人按钮
        self.start_button = tk.Button(master, text="启动机器人", command=self.start_robot)
        self.start_button.pack()

        # 创建停止机器人按钮
        self.stop_button = tk.Button(master, text="停止机器人", command=self.stop_robot)
        self.stop_button.pack()

        # 创建显示机器人状态的标签
        self.status_label = tk.Label(master, text="机器人状态：")
        self.status_label.pack()

        # 创建用于显示图片的三个标签
        self.image_label1 = tk.Label(master)
        self.image_label1.pack()
        self.image_label2 = tk.Label(master)
        self.image_label2.pack()
        self.image_label3 = tk.Label(master)
        self.image_label3.pack()

        # dir_path = os.path.dirname(__file__)
        # # 加载图片
        # self.image1 = PhotoImage(file=os.path.join(dir_path,"1.png"))  # 替换为实际图片路径
        # self.image2 = PhotoImage(file=os.path.join(dir_path,"2.png"))  # 替换为实际图片路径
        # self.image3 = PhotoImage(file=os.path.join(dir_path,"3.png"))  # 替换为实际图片路径
        #
        # # 显示第一张图片
        # self.show_image(1)

    def display_binary_image(self,data):
        # 创建一个Tkinter窗口

        # 创建一个像素画布
        canvas = tk.Canvas(self.master, width=len(data[0]), height=len(data), bg='white')
        canvas.pack()

        # 在画布上绘制像素点
        for i in range(len(data)):
            for j in range(len(data[0])):
                if data[i][j] == 1:
                    canvas.create_rectangle(j, i, j + 1, i + 1, fill='black')

    def show_image(self, image_number):
        if image_number == 1:
            self.image_label1.config(image=self.image1)
        elif image_number == 2:
            self.image_label2.config(image=self.image2)
        elif image_number == 3:
            self.image_label3.config(image=self.image3)
        else:
            print("无效的图片编号")

    def start_robot(self):
        self.robot.start()  # 假设Robot类有一个start方法来启动机器人
        self.update_status("机器人已启动。")

    def stop_robot(self):
        self.robot.stop()  # 假设Robot类有一个stop方法来停止机器人
        self.update_status("机器人已停止。")

    def update_status(self, status):
        self.status_label.config(text="机器人状态： " + status)


if __name__ == '__main__':

    root = tk.Tk()
    interface = RobotInterface(root)
    binary_image = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]
    interface.display_binary_image(binary_image)

    root.mainloop()