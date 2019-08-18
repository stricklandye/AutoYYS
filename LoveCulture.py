import random
import threading
import tkinter as tk
from tkinter import scrolledtext

import keyboard
import pyautogui
import time


class Application(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("热爱中国传统文化")
        self.root.geometry("450x650")
        self.root.resizable(width=False, height=False)
        self.control = None #控制线程

        #各个初始化数据的int类型
        self.estimateTimeVal = None
        self.loopTimeVal = None

        self.slogan = tk.Label(self.root,text = "痒痒鼠自己玩游戏",font=('Arial', 20), width=100, height=2)
        self.hint =  tk.Label(self.root,text = "预计时间最好比实际所用时间多5-10秒",font=('Arial', 12), width=100, height=2)
        self.estimate_label = tk.Label(self.root, text='预计时间')
        self.loop_label = tk.Label(self.root, text='次数')
        self.logging_label = tk.Label(self.root, text='日志信息')
        self.captain_label = tk.Label(self.root, text = "是否队长")
        self.model_label = tk.Label(self.root, text="模式选择")

        self.estimateTime = tk.Entry(self.root, width=5)
        self.loopTime = tk.Entry(self.root, width=5)

        #是否为队长
        self.captain= tk.IntVar()
        self.isCaptain = tk.Radiobutton(self.root, text = "是",variable = self.captain, value=1)
        self.notCaptain = tk.Radiobutton(self.root, text = "不是",variable = self.captain, value=2)
        self.single = tk.Radiobutton(self.root, text = "单人",variable = self.captain, value=3,)
        self.single.select()

        #模式选择
        self.model= tk.IntVar()
        self.yuhun = tk.Radiobutton(self.root, text = "御魂",variable = self.model, value=1)
        self.yeyuanhuo = tk.Radiobutton(self.root, text = "业原火",variable = self.model, value=2)
        self.yuling= tk.Radiobutton(self.root, text = "御灵",variable = self.model, value=3,)
        self.jiejieka= tk.Radiobutton(self.root, text = "合卡",variable = self.model, value=4,)
        self.yuhun.select()

        self.logging = scrolledtext.ScrolledText(self.root,width = 30, height = 15)

        self.begin_btn = tk.Button(self.root,command = self.begin_play,text = "开始")
        self.cancel_btn = tk.Button(self.root, command=self.cancel_play, text="结束")

    def setLayout(self):
        self.slogan.pack(side ='top')
        self.hint.pack(side = 'top')

        #标签信息排版
        self.estimate_label.place(x=60, y= 140)
        self.loop_label.place(x=200, y= 140)
        self.logging_label.place(x = 60, y = 360 )
        self.captain_label.place(x = 60, y = 230)
        self.model_label.place(x=60,y=270)

        #输入框排版
        self.estimateTime.place(x=135, y=140)
        self.loopTime.place(x=290, y=140)

        #是否为队长单选框
        self.isCaptain.place(x = 140, y = 230)
        self.notCaptain.place(x = 220, y=230)
        self.single.place(x=300, y=230)

        #模式选择
        self.yuhun.place(x = 140, y = 270)
        self.yeyuanhuo.place(x = 220, y=270)
        self.yuling.place(x=300, y=270)
        self.jiejieka.place(x=380, y=270)

        #按钮组排版
        self.begin_btn.place(x=140, y=310)
        self.cancel_btn.place(x=240, y=310)

        #日志排版
        self.logging.place(x = 140, y = 360)
        # self.scrollbar.place(x = 200, y = 300)
    def begin_play(self):
        if self.control is None or self.control.stopped is True:
            self.control = ControlThread(target = self.begin, name = "LoveCulture")
            self.control.start()
        else:
            pyautogui.alert("刚才任务还没结束，不要老是开始！")

    def cancel_play(self):
        if self.control is not None:
            #此时任务线程不为空,那么结束线程,并且将任务线程设置为None
            # 如果只是设置为None但是不terminate,造成线程过多
            self.control.terminate()
            self.control = None
            self.logging.insert(tk.END, "\n任务结束\n")
            self.logging.see(tk.END)
    def begin(self):
        try:
            self.estimateTimeVal = int(self.estimateTime.get())
            self.loopTimeVal = int(self.loopTime.get())
        except ValueError as e:
            pyautogui.alert("输入参数有误")
            self.cancel_play()

        modes = ['御魂', '业原火', '御灵', '合卡']
        captain = self.captain.get()
        model = self.model.get()
        self.logging.insert(tk.END, "\n------------------\n")
        self.logging.insert(tk.END, "\n任务次数:{times}\n".format(times=self.loopTimeVal))
        self.logging.insert(tk.END, "\n任务名称:{mode}\n".format(mode = modes[model-1]))
        self.logging.insert(tk.END, "\n倒数5秒后开始\n")
        for i in range(5,0,-1):
            self.logging.insert(tk.END, "{i}\n".format(i = i))
            self.logging.see(tk.END)
            time.sleep(1)

        if captain == 1: #是队长
            self.captainModel()
        elif captain == 2: #不是队长
            self.notCaptainModel()
        else:
            #单人模式
            if model == 4:
                #合成结界卡
                self.composeCard()
            else:
                #如果是御灵，御魂，业原火，执行单人普通地图模式
                self.singleModel()

    def captainModel(self):
        #队长副本模式
        self.throughDungeon("./image/fight.png")
        self.cancel_play()

    def notCaptainModel(self):
        times = int(self.loopTime.get())
        count = 0
        while count < times and not keyboard.is_pressed("alt+q"):
            #按下alt+q结束任务
            time.sleep(2)
            pyautogui.click(417+random.randint(20, 50), 139+random.randint(20, 50), button="left")
        self.cancel_play()

    def singleModel(self):
        #单人模式普通副本，御灵，御魂，业原火
        self.throughDungeon("./image/start.png")
        self.cancel_play()

    def singelModelGouLiang(self):
        #单人模式狗粮副本
        pass

    def autoClick(self, image, confidence):
        pyautogui.screenshot('./image/foo.PNG', region=(0, 0, 1423, 843))
        location = None
        try:
            location = pyautogui.locateCenterOnScreen(image, confidence=confidence)
        except TypeError as e:
            self.logging.insert(tk.END, "\n未捕捉到目标，稍后继续,15秒后继续\n")
            time.sleep(15)
            for i in range(5):
                #这里发生异常的原因有时候是在结束副本的时候
                #由于网络不好，一直在转转转，没有跳转到挑战页面
                #因此发生这种情况重复点击页面，一旦恢复可以跳转
                pyautogui.click(417+random.randint(20, 50), 139+random.randint(20, 50), button="left")
                time.sleep(1)
            location = pyautogui.locateCenterOnScreen(image, confidence=confidence)

        startX = location[0] + random.randint(1, 50)
        startY = location[1] + random.randint(1, 30)
        pyautogui.moveTo(x=startX, y=startY, duration=0.7)
        pyautogui.click(x=startX, y=startY, button='left')

    def composeCard(self):
        #合成结界卡

        coordinates = [(397,390),(397, 550),(397, 722)]#三张低级卡的坐标
        pyautogui.screenshot('./image/foo.PNG',region=(0, 0, 1423, 843))
        times = int(self.loopTime.get())
        i = 0
        while i < times and not keyboard.is_pressed("alt+q"):
            for cor in coordinates:
                x1 = cor[0]+random.randint(20,200)
                y1 = cor[1]+random.randint(20,100)
                pyautogui.moveTo(x1, y1 ,duration=0.7)
                time.sleep(0.3)
                pyautogui.click(x1,y1,button='left')

            position = pyautogui.locateCenterOnScreen("./image/hecheng.png",confidence = 0.9) #合成按钮
            pyautogui.moveTo(position[0],position[1],duration = 0.6)
            pyautogui.click(position[0]+random.randint(1, 50), position[1]+random.randint(1, 30),button='left')
            i = i+1
        self.cancel_play()

    def throughDungeon(self, btn):
        """
        单人通关副本和队长模式有点相同，只是在单人副本当中，
        按钮为挑战，队长模式当中，按钮为开始战斗
        :param btn:
        :return:
        """
        times = int(self.loopTime.get())
        estimateTime = int(self.estimateTime.get())

        count = 0
        while self.control is not  None and count < times:
            #当控制线程为None时，停止任务
            self.logging.insert(tk.END, "\n第{times}次开始!".format(times=count + 1))
            self.logging.see(tk.END)

            time.sleep(5)
            self.autoClick(btn, 0.7)
            time.sleep(estimateTime)
            for i in range(7):
                #结束后重复点击页面,结束到御魂掉落界面的等待时间。
                pyautogui.click(417+random.randint(20, 50), 139+random.randint(20, 50), button="left")
                time.sleep(1)
            self.logging.insert(tk.END, "\n副本次数:{times}，结束!".format(times=count+1))
            count = count+1

class ControlThread(threading.Thread):
    #任务控制线程,每次点击开始按钮创建一个新的线程
    def __init__(self,target,name):
        self._stop_event = threading.Event()
        threading.Thread.__init__(self,target = target,name = name)

    def terminate(self):
        #标志位设置为False,停止线程
        self._stop_event.set()

    def stopped(self):
        #返回当前线程是否停止
        return self._stop_event.is_set()

def main():
    app = Application()
    app.setLayout()
    tk.mainloop()
if __name__ == "__main__":
    main()