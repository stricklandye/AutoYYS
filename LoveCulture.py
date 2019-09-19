import ctypes
import random
import threading
import tkinter as tk
from tkinter import scrolledtext

import cv2
import keyboard
import pyautogui
import time


class Application(object):



    def __init__(self):
        self.root = tk.Tk()
        self.root.title("热爱中国传统文化")
        self.root.geometry("500x650")
        self.root.resizable(width=False, height=False)
        self.control = None #控制线程

        self.fixedX1 = 417
        self.fixedY1 = 139
        self.estimateTimeVal = None
        self.loopTimeVal = None
        self.isBegin = False

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
        self.tupo = tk.Radiobutton(self.root, text="突破", variable=self.model, value=5, )
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
        self.tupo.place(x=440,y=270)

        #按钮组排版
        self.begin_btn.place(x=140, y=310)
        self.cancel_btn.place(x=240, y=310)

        #日志排版
        self.logging.place(x = 140, y = 360)
        # self.scrollbar.place(x = 200, y = 300)

    def begin_play(self):
        if self.isBegin is False:
            self.isBegin = True
            self.control = ControlThread(target = self.begin, name = "LoveCulture")
            self.control.start()
            keyboard.add_hotkey("alt+q", self.cancel_play) #结束任务热键
        else:
            pyautogui.alert("刚才任务还没结束，不要老是开始！")

    def cancel_play(self):
        if self.isBegin is False:
            pyautogui.alert("还没开始就不要想着结束")
        else:
            self.isBegin = False
            self.logging.insert(tk.END, "\n任务结束\n")
            self.logging.see(tk.END)
            self.control.kill()

    def begin(self):
        try:
            self.estimateTimeVal = int(self.estimateTime.get())
            self.loopTimeVal = int(self.loopTime.get())
        except ValueError as e:
            pyautogui.alert("输入参数有误")
            self.cancel_play()
            return

        modes = ['御魂', '业原火', '御灵', '合卡','突破']
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
            elif model == 5:
                self.throughTuPo()
            else:
                #如果是御灵，御魂，业原火，执行单人普通地图模式
                self.singleModel()

    def captainModel(self):
        #队长副本模式
        self.throughDungeon("./image/fight.png")
        self.cancel_play()

    def notCaptainModel(self):
        #非队长模式
        while True:
            time.sleep(3)
            pyautogui.click(self.fixedX1+random.randint(20, 50), self.fixedY1+random.randint(20, 50), button="left")


    def singleModel(self):
        #单人模式普通副本，御灵，御魂，业原火
        self.throughDungeon("./image/start.png")
        self.cancel_play()

    def throughTuPo(self):
        #通过结界突破
        coordinates = [(240,145),(633,170),(1017,186),
                       (249,318),(629,323),(1011,322),
                       (257,469),(628,474),(1010,469)]
        count = 0
        for cor in coordinates:
            time.sleep(5)
            count = count+1
            self.logging.insert(tk.END, "\n次数:{count}".format(count = count))
            self.logging.see(tk.END)
            if count ==4 or count == 7:
                x3 = 323 + random.randint(1, 50)
                y3 = 99 + random.randint(1, 10)
                pyautogui.moveTo(x3,y3,duration =0.8)
                pyautogui.click(x3,y3, button = "left")
            #在3,6这两次会出现奖励，点击鼠标
            # x3 = 314 + random.randint(1, 50)
            # y3 = 57 + random.randint(1, 10)
            # pyautogui.moveTo(x3,y3,duration=0.8)
            # pyautogui.click(x3,y3,button='left')

            x1 = cor[0]+random.randint(10,180)
            y1 = cor[1]+random.randint(5,70)
            pyautogui.moveTo(x1,y1,duration=0.8)
            time.sleep(1)
            pyautogui.click(x1,y1,button='left')
            #寻找进攻按钮
            pyautogui.screenshot('./image/foo.PNG', region=(0, 0, 1423, 843))
            location = None
            try:
                location = pyautogui.locateCenterOnScreen("./image/attack.png", confidence=0.8)
            except TypeError as e:
                self.logging.insert(tk.END, "\n这个已经打过了!")
                self.logging.see(tk.END)
                #有时候会点到目标头像,所以在发送异常的时候，原地点一下
                pyautogui.click(button='left')
                continue

            x3 = location[0] + random.randint(1, 50)
            y3 = location[1] + random.randint(1, 30)
            pyautogui.moveTo(x=x3, y=y3, duration=0.7)
            pyautogui.click(x=x3, y=y3, button='left')
            time.sleep(self.estimateTimeVal)
            while True:
                pyautogui.screenshot("./image/foo.png")
                if self.match("./image/foo.png","./image/victory.png"):
                    pyautogui.click(button='left')
                    break
                else:
                    #如果没有匹配，等待10秒
                    time.sleep(10)
        self.cancel_play()
    def match(self,img,template):
        img_src = cv2.imread(img)
        gary_img = cv2.cvtColor(img_src, cv2.COLOR_RGB2GRAY)

        template_src = cv2.imread(template)
        gary_temp = cv2.cvtColor(template_src, cv2.COLOR_RGB2GRAY)

        result = cv2.matchTemplate(gary_img, gary_temp, cv2.TM_CCOEFF_NORMED)

        '''
        min_val,max_val:result矩阵中的最大值以及最小值,如果不匹配min_val接近-1，匹配的区域max_val接近1
        min_loc,max_loc:min_val,max_val在result矩阵中的坐标,因此max_val为匹配区域的左上角坐标
        '''
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        thresh_val = 0.8 #如果成功匹配到目标,max_val的值会接近于1
        # if max_val > thresh_val:
            #max_loc为左上角坐标，因此加上一半的宽高，就是中心点坐标
            # x1 = max_loc[0]+width/2
            # y1 = max_loc[1]+height/2
        return max_val > thresh_val #大于thresh_val,说明存在匹配区域
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
                pyautogui.click(self.fixedX1+random.randint(20, 50), self.fixedY1+random.randint(20, 50), button="left")
                time.sleep(1)
            location = pyautogui.locateCenterOnScreen(image, confidence=confidence)

        x1 = location[0] + random.randint(1, 50)
        y1 = location[1] + random.randint(1, 30)
        pyautogui.moveTo(x= x1, y= y1, duration=0.7)
        pyautogui.click(x= x1, y= y1, button='left')

    def composeCard(self):
        #合成结界卡

        coordinates = [(225,422),(269, 557),(271, 710)]#三张低级卡的坐标
        pyautogui.screenshot('./image/foo.PNG',region=(0, 0, 1423, 843))
        i = 0
        while i < self.loopTimeVal :
            # print("hello world")
            # time.sleep(1)
            # i +=1
            for cor in coordinates:
                x1 = cor[0]+random.randint(20,200)
                y1 = cor[1]+random.randint(10,55)
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

        count = 0
        while  count < self.loopTimeVal:

            self.logging.insert(tk.END, "\n第{times}次开始!".format(times=count + 1))
            self.logging.see(tk.END)

            time.sleep(5)
            self.autoClick(btn, 0.7) #寻找开始副本的按钮
            time.sleep(self.estimateTimeVal)
            for i in range(7):
                #结束后重复点击页面,结束到御魂掉落界面的等待时间。
                pyautogui.click(89+random.randint(20, 50), 413+random.randint(20, 50), button="left")
                time.sleep(1)
            self.logging.insert(tk.END, "\n副本次数:{times}，结束!".format(times=count+1))
            count = count+1
#
class ControlThread(threading.Thread):
    #任务控制线程,每次点击开始按钮创建一个新的线程
    def __init__(self,target,name):
        self._stop_event = threading.Event()
        threading.Thread.__init__(self,target = target,name = name)

    #杀死线程
    def kill(self):
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.ident),ctypes.py_object(SystemExit)
        )


def main():
    app = Application()
    app.setLayout()
    tk.mainloop()
if __name__ == "__main__":
    main()