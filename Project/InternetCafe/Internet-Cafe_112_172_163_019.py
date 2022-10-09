#tkinterนี้ไม่ได้ทำแบบresponsive เพื่อLayoutที่สวยงานโปรดตั้งค่าSettings > Display > Scale and layout แก้เป็น 100% > resolution 1920x1800(fullhd)
from enum import Enum
from abc import ABC
import time
import logging
from tkinter import *
import tkinter as tk
from datetime import datetime
from datetime import timedelta
import tkinter.ttk as ttk
import customtkinter
from PIL import Image, ImageTk
import os

from setuptools import Command 

PATH = os.path.dirname(os.path.realpath(__file__))
customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root_tk = customtkinter.CTk()
root_tk.geometry("1366x1005")
root_tk.title("Internet Cafe")

class PaymentStatus(Enum):
     PAID, NOTPAID = 1, 2

class ComputerStatus(Enum):
     ON, OFF = 1, 2

logging.basicConfig(filename="history.log", format="%(asctime)s - %(levelname)s  %(message)s", filemode="w") 
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

class Log :
    
    @staticmethod
    def save_start_log(serial_num):
        date_time = time.localtime()
        print(f"{time.asctime(date_time)} - START at Computer No.{serial_num}")#
        logger.info(f"[Start] Computer No.{serial_num}") 
    @staticmethod
    def save_stop_log(serial_num):
        date_time = time.localtime()
        print(f"{time.asctime(date_time)} - STOP at Computer No.{serial_num}")#
        logger.info(f"[Stop] Computer No.{serial_num}") 
#ตอนนี้ยังไม่ใช้
class Account:
    def __init__(self,user_name,password):
        self.__user_name = user_name
        self.__password = password
#mother class
class Computer(ABC):
    computer_list = []
    def __init__(self,serial_num,time_remain,status=ComputerStatus.OFF,**kwargs):
        super().__init__(**kwargs)
        self.serial_num = serial_num
        self.time_remain = time_remain
        self.status = status
        self.payment = PaymentStatus.NOTPAID
    #debug time(did not use)
    def countdown(self,temp):
        
        if temp == None:
            start = True
            t = 0
            while start:
                
                mins, secs = divmod(t, 60)
                hours, mins = divmod(mins, 60)
                timer = "{:02d}:{:02d}:{:02d}".format(hours,mins, secs)
                if self.status == ComputerStatus.OFF:
                        #print("Computer stop")
                        
                        start = False
                        break
                else:
                        self.time_remain = timer
                        #d.text3.set(f"เวลาที่ใช้U : {self.time_remain}")
                        #print(f"Unlimit ({self.time_remain})", end="\r") #
                        time.sleep(1)
                        t += 1
            self.time_remain = timer
            total_time = round(t/3600)   
            print(Rate.calculate(total_time,Rate.get_rate)) 
        else:
            t = temp*3600
            while t:
                mins, secs = divmod(t, 60)
                hours, mins = divmod(mins, 60)
                timer = "{:02d}:{:02d}:{:02d}".format(hours,mins, secs)
                if self.status == ComputerStatus.OFF:
                    #print("Computer stop")
                    t = 0
                else:
                    self.time_remain = timer
                    Dashboard.text3.set(f"เวลาที่ใช้ : {self.time_remain}")
                    #print(self.time_remain, end="\r") #
                    time.sleep(1)
                    t -= 1
            self.time_remain = timer    
            print("Time up")   
#child class            
class Admin(Account,Computer):
    
    count = 0
    used = 0
    total_used = 0
    def __init__(self, user_name, password):
        Account.__init__(self,user_name, password)
        self.today_rate = 0
        
    def add_computer(self,num):
        x = int(num)
        for i in range(x):
            Computer.computer_list.append(Computer(serial_num= Admin.count , time_remain= None,status= ComputerStatus.OFF))
            Admin.count += 1
        #print("ADDED")
    
    def list_computer(self):
        for i in range (len(Computer.computer_list)):
            print(f" com : {i} : {Computer.computer_list[i]} ") # rate :{Computer.computer_list[i].today_rate.rate}
            print("\n")
        
    def computer_off (self,serial_num):
        for i in range (len(Computer.computer_list)):
            if i == serial_num:
                Admin.total_used -= 1
                current_computer = Computer.computer_list[i]
                Log.save_stop_log(current_computer.serial_num)
                current_computer.status = ComputerStatus.OFF

    def edit_rate (self,new_rate):

        self.today_rate = float(new_rate)
        #print(f"today rate : {self.today_rate}")
        

    def computer_on (self,serial_num,time_remain):
        for i in range (len(Computer.computer_list)):
            if i == serial_num:
                current_computer = Computer.computer_list[i]
                current_computer.status = ComputerStatus.ON
                Log.save_start_log(current_computer.serial_num)
                Admin.used += 1
                Admin.total_used +=1
                if time_remain == 0:
                    time_remain = None
                else:
                    print(f"price : {Rate.calculate(time_remain,self.today_rate)} ฿")
                    current_computer.payment = PaymentStatus.PAID ####
                current_computer.time_remain = time_remain
                print(f"{current_computer.serial_num} : {current_computer.time_remain} : {current_computer.status.name} :{self.today_rate}")
                #current_computer.countdown(time_remain)
                break
        else:
                print("OUT of Range") 
        
class Rate :
    def __init__(self,rate):
        self.rate = rate
        
    @property
    def get_rate(self):
        return self.rate
    @staticmethod
    def calculate(hrs,rate):
        return hrs*rate
#มี2methodหลักshow display(frame1-5),show realtime(upate value)       
class Dashboard(Computer): 
    countl = 0
    tv_num =  IntVar()
    tv_search =  IntVar()
    tv_time = IntVar()
    tv_rate = DoubleVar()
    current_computer = None
    num = 0
    millis_sec = 0
    list_time = {"none":None}
    list_stamp = {}

    root_tk.grid_rowconfigure((0, 1, 2), weight=1)
    root_tk.grid_columnconfigure((0, 1), weight=1)
    def __init__(self,root_tk):
        self.root_tk = root_tk
        self.f1 = customtkinter.CTkFrame(self.root_tk,height=275)
        self.f1.grid(padx=20, pady=20, row=0, column=0, columnspan=2, sticky="nsew")
        self.f5 = customtkinter.CTkFrame(self.root_tk)
        self.f5.grid(padx=20, pady=20, row=1, column=0, sticky="nsew")
        self.f3 = customtkinter.CTkFrame(self.root_tk,height=280)
        self.f3.grid(padx=20, pady=20, row=1, column=1, sticky="nsew")
        self.f4 = customtkinter.CTkFrame(self.root_tk)
        self.f4.grid(padx=20, pady=20, row=2, column=0, sticky="nsew")
        self.f2 = customtkinter.CTkFrame(self.root_tk)
        self.f2.grid(padx=20, pady=20, row=2, column=1, sticky="nsew")
        self.text1 = StringVar()
        self.text1.set("เครื่องที่ -- : NO.--")
        self.text2 = StringVar()
        self.text2.set("เครื่องที่ -- : --:-- ชม.(-- ฿) ")
        self.text3 = StringVar()
        self.text3.set("เวลาที่ใช้ : ไม่จำกัด ")
        self.text_b = StringVar()
        self.text_b.set("เปิดใช้งาน")
        self.switch_2 = customtkinter.CTkSwitch(self.root_tk,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")
        self.now = datetime.now()
        self.current_time = self.now.strftime("%H:%M:%S")
        self.ttime = StringVar()
        self.ttime.set(f"time : {self.current_time}")
        self.text_btn = customtkinter.CTkButton(self.root_tk,textvariable=self.text_b,command=self.btn_on ,width=20).grid(row=2, column=1, pady=20, padx=20)
        image = Image.open("bg.jpg")
        image = image.resize((780,270))
        render = ImageTk.PhotoImage(image)
        img = tk.Label(self.f5, image=render)
        img.image = render
        img.place(x=22, y=35)


    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def frame_2(self):
        self.f2_label1 = customtkinter.CTkLabel(self.f2,textvariable=self.text1,text_font=("Roboto Medium", -20))
        self.f2_label1.pack()
        self.f2_label2 = customtkinter.CTkLabel(self.f2,textvariable=self.text2,text_font=("Roboto Medium", -20))
        self.f2_label2.pack()
        self.f2_label3 = customtkinter.CTkLabel(self.f2,textvariable=self.text3,text_font=("Roboto Medium", -20))
        self.f2_label3.pack()
        
        #self.text_btn = Button(self.f2,textvariable=self.text_b,borderwidth=1, relief="raised",command=self.btn_on).pack(pady=5) 
    def on_click_on(self):
        self.text_b.set(" ปิดใช้งาน")
        
        #print("on_click_on")
        self.top.after(300,lambda:self.top.destroy())
        num = Dashboard.tv_search.get()
        #print(f"serial:{num}")
        #print(type(Dashboard.tv_time.get()))
        Dashboard.list_time[f"{num}"] = Dashboard.tv_time.get()
        dt = datetime.today()
        seconds = dt.timestamp()
        Dashboard.list_stamp[f"{num}"] = seconds
        #print(f"st{Dashboard.list_stamp}")
        admin.computer_on(num,Dashboard.tv_time.get())
        #self.text3.set(f"เวลาที่ใช้ : {Dashboard.current_computer.countdown(Dashboard.tv_time)}")
        serial = Dashboard.tv_search.get()
        f = "{:02d}".format(serial)
        #print(serial)
        customtkinter.CTkLabel(self.f1, text=f"NO.{f} : ON ",borderwidth=5, relief="solid",fg="blue" ,text_font=("Roboto Medium", -20),text_color="green").grid(row=serial // 9, column=serial % 9,padx=10,pady=10)
        self.mylist.insert(END, f"{self.ctime} - START No.{serial}" )
    def btn_on(self):
            #print("btn_on")
            self.top= Toplevel(root_tk)
            self.top.geometry("350x100")
            self.top.title("Add computer")
            Label(self.top, text= "ใส่จำนวนชั่วโมง", font=("consolas 15 bold")).pack()
            Entry(self.top, textvariable=Dashboard.tv_time, width=7, justify="right").pack(side=LEFT, padx=10)
            Button(self.top, text="Enter", bg="grey", command=self.on_click_on).pack(side=LEFT)
    def btn_off(self):
            #print("btn_off")
            self.text_b.set("เปิดใช้งาน")
            self.text_btn = customtkinter.CTkButton(self.root_tk,textvariable=self.text_b,command=self.btn_on ,width=20).grid(row=2, column=1, pady=20, padx=20)
            serial = Dashboard.tv_search.get()
            f = "{:02d}".format(serial)
            #print(serial)
            customtkinter.CTkLabel(self.f1, text=f"NO.{f} : OFF",borderwidth=1, relief="solid",text_font=("Roboto Medium", -20)).grid(row=serial // 9, column=serial % 9,padx=10,pady=10)
            self.mylist.insert(END, f"{self.ctime} - STOP No.{serial}" )
            admin.computer_off(serial)
        
    def to_frame_2(self,serial,com):
        
        #print(serial)
        self.text1.set(f"เครื่องที่ {serial} : NO.{serial}")
        self.text2.set(f"เครื่องที่ {serial} : {com.time_remain} ชม.({admin.today_rate} ฿) ")
        self.text3.set(f"เวลาที่ใช้ : {Dashboard.current_computer.time_remain}")
        #self.f2_label2.configure()
        #customtkinter.CTkLabel(self.f2,text="เครื่องที่ 01 : NO.01").pack()
        #customtkinter.CTkLabel(self.f2,text="เครื่องที่ 02 : 00:00 ชม.(20 ฿) ").pack()   
       # customtkinter.CTkLabel(self.f2,text="เวลาที่ใช้ : ไม่จำกัด ").pack(side=TOP)
        #button1 = Button(self.f2,text="จำกัดการใช้งาน",borderwidth=1, relief="raised").pack(side=LEFT,padx=20,pady=10)
        #button1 = Button(self.f2,text="เปิดใช้งาน",borderwidth=1, relief="raised",command=self.btn_on).pack(pady=10)####  
        pass

    def on_click_add(self):
        num = Dashboard.tv_num.get()
        #print(num)
        
        if num > 45:
            #print("error")
            Label(self.top, text="maximum 45").pack(side=LEFT, padx=10)
        else:
            admin.add_computer(num)
            self.top.after(300,lambda:self.top.destroy())
            for i, c in enumerate(range(num)):    
                f = "{:02d}".format(Dashboard.countl)
                #print(f)
                customtkinter.CTkLabel(self.f1, text=f"NO.{f} : {ComputerStatus.OFF.name}",borderwidth=1, relief="solid",text_font=("Roboto Medium", -20)).grid(row=i // 9, column=i % 9,padx=10,pady=10)
                Dashboard.countl +=1
            
    def btn_add(self): 
        self.top= Toplevel(root_tk)
        self.top.geometry("350x100")
        self.top.title("Add computer")
        Label(self.top, text= "ใส่จำนวนเครื่อง", font=("consolas 15 bold")).pack()
        Entry(self.top, textvariable=Dashboard.tv_num, width=7, justify="right").pack(side=LEFT, padx=10)
        Button(self.top, text="Enter", bg="grey", command=self.on_click_add).pack(side=LEFT)
        #customtkinter.CTkLabel(top, textvariable=tv_lbs).pack(side=LEFT)
        #num = Dashboard.tv_num.get()
        #print(f"to num{num}")
    def frame_3(self):
        label3 = customtkinter.CTkLabel(self.f3,text="\nประวัติการใช้งาน",text_font=("Roboto Medium", -20))
        label3.pack(side=TOP,padx=1,pady=1) 
        self.mylist = Listbox(self.f3 ,width=20,height=15,bg="grey38",fg="white")
        self.mylist.pack(side=TOP,fill=BOTH)
    
    def on_click_del(self):
        num = Dashboard.tv_num.get()
        
        for i in range (len(Computer.computer_list)):
            current_computer = Computer.computer_list[i]
            if current_computer.serial_num == num:
                del Computer.computer_list[i]

        pass
    def btn_del(self):
        self.top= Toplevel(root_tk)
        self.top.geometry("350x100")
        self.top.title("Remove computer")
        customtkinter.CTkLabel(self.top, text= "ใส่หมายเลขเครื่อง", font=("consolas 15 bold")).pack()
        Entry(self.top, textvariable=Dashboard.tv_num, width=7, justify="right").pack(side=LEFT, padx=10)
        Button(self.top, text="Enter", bg="grey", command=self.on_click_del).pack(side=LEFT)
    
    def on_click_search(self):
        num = Dashboard.tv_search.get()
        
        for i in range (len(Computer.computer_list)):
            Dashboard.current_computer = Computer.computer_list[i]
            if Dashboard.current_computer.serial_num == num:
                self.top.after(30,lambda:self.top.destroy())
                self.to_frame_2(num,Dashboard.current_computer)
        else:
            #print("search error")
            customtkinter.CTkLabel(self.top, text="Mismatch").pack(side=LEFT, padx=10)

    def btn_search(self):
        Dashboard.tv_num = 0
        self.top= Toplevel(root_tk)
        self.top.geometry("300x100")
        self.top.title("Search computer")
        Label(self.top, text= "หมายเลขเครื่อง", font=("consolas 15 bold")).pack()
        Entry(self.top, textvariable=Dashboard.tv_search, width=7, justify="right").pack(side=LEFT, padx=10)
        Button(self.top, text="Enter", bg="grey", command=self.on_click_search).pack(side=LEFT)
    def on_click_rate(self):
        if Dashboard.tv_rate.get() >= 0:
            self.top.after(30,lambda:self.top.destroy())
            num = Dashboard.tv_rate.get()
            admin.today_rate = num
        else:
            #print("search error")
            customtkinter.CTkLabel(self.top, text="กรุณาใส่จำนวนเงินให้ถูกต้อง").pack(side=LEFT, padx=10) 
    def btn_rate(self):
        self.top= Toplevel(root_tk)
        self.top.geometry("300x100")
        self.top.title("Today rate")
        Label(self.top, text= "อัตราค่าบริการ", font=("consolas 15 bold")).pack()
        Entry(self.top, textvariable=Dashboard.tv_rate, width=7, justify="right").pack(side=LEFT, padx=10)
        Button(self.top, text="Enter", bg="grey", command=self.on_click_rate).pack(side=LEFT)
        pass
    def btn_us(self):
        self.top= Toplevel(root_tk)
        self.top.geometry("300x100")
        self.top.title("Among us")
        Label(self.top, text= "G7", font=("consolas 15 bold")).pack(side=TOP)

    def frame_4(self):
        label4 = customtkinter.CTkLabel(self.f4,text="สถานะปัจจุบัน",text_font=("Roboto Medium", -20))
        label4.grid(row=0,column=0,sticky="w")
        label4 = customtkinter.CTkLabel(self.f4,text="Staff name : G7 ",text_font=("Roboto Medium", -20))
        label4.grid(row=1,column=0,sticky="w")
        
        #self.label5 = customtkinter.CTkLabel(self.f4,textvariable=self.ttime)
        #self.label5.grid(row=3,column=1,sticky="nw")
        button4 = customtkinter.CTkButton(self.f4,text="search", relief="raised",command=self.btn_search)
        button4.grid(row=0,column=2,sticky="nw",padx=5,pady=5)
        button4 = customtkinter.CTkButton(self.f4,text="Adjust Rate", relief="raised",command=self.btn_rate)
        button4.grid(row=1,column=2,sticky="nw",padx=5,pady=5)
        button4 = customtkinter.CTkButton(self.f4,text="Add Computer", relief="raised",command=self.btn_add)
        button4.grid(row=2,column=2,sticky="nw",padx=5,pady=5)
        button4 = customtkinter.CTkButton(self.f4,text="About Us", relief="raised",command=self.btn_us)
        button4.grid(row=3,column=2,sticky="nw",padx=5,pady=5)
    def show_display(self):
        self.frame_2()
        self.frame_3()
        self.frame_4()
        self.show_realtime()
        pass
    
    def show_realtime(self):
        now = datetime.now()
        Dashboard.millis_sec +=1
        currentTime = now.strftime("Current time : %H:%M:%S")
        self.ctime = datetime.today().strftime("At %H:%M:%S")
        dt = datetime.today()
        seconds = dt.timestamp()
        #print(seconds)
        #print(now)
        mins, secs = divmod(Dashboard.millis_sec, 60)
        hours, mins = divmod(mins, 60)
        timer = "{:02d}:{:02d}:{:02d}".format(hours,mins, secs)
        label = customtkinter.CTkLabel(self.f4, text="placeholder",text_font=("Roboto Medium", -20))
        label.grid(row=3,column=1)
        label["text"] = currentTime

        label4 = customtkinter.CTkLabel(self.f4,text=f"อัตราค่าบริการ : {admin.today_rate}",text_font=("Roboto Medium", -20))
        label4.grid(row=2,column=1,sticky="nw")
        label4 = customtkinter.CTkLabel(self.f4,text=f"Total worktime : {timer} ",text_font=("Roboto Medium", -20))
        label4.grid(row=2,column=0,sticky="w")
        label4 = customtkinter.CTkLabel(self.f4,text=f"จำนวนผู้ใช้งาน : {admin.total_used}/{Dashboard.countl} เครื่อง",text_font=("Roboto Medium", -20))
        label4.grid(row=3,column=0,sticky="w")
        label4 = customtkinter.CTkLabel(self.f4,text=f"USED COUNT : {admin.used}",text_font=("Roboto Medium", -20))
        label4.grid(row=1,column=1,sticky="nw")
        for i in range (len(Computer.computer_list)):
            Dashboard.current_computer = Computer.computer_list[i]
            #print(Dashboard.current_computer.status.name)
            #print(type(Dashboard.current_computer.status))
            #print(ComputerStatus.OFF.name)
            if Dashboard.current_computer.serial_num == Dashboard.tv_search.get():
                if  Dashboard.current_computer.status.name==ComputerStatus.OFF.name :
                    self.text_b.set("เปิดใช้งาน")
                    self.text_btn = customtkinter.CTkButton(self.root_tk,textvariable=self.text_b,command=self.btn_on,width=20).grid(row=2, column=1, pady=20, padx=20)
                    #self.text3.set(f"เวลาที่ใช้ : 00:00:00")
                    #print("on")
                elif  Dashboard.current_computer.status.name==ComputerStatus.ON.name :
                    self.text_b.set(" ปิดใช้งาน")
                    self.text_btn = customtkinter.CTkButton(self.root_tk,textvariable=self.text_b,command=self.btn_off ,width=20).grid(row=2, column=1, pady=20, padx=20)
                    
                    #self.text3.set(f"เวลาที่ใช้ : {true_time}")
                    #print("off")
            
        try:
            #print( Dashboard.list_time[f"{Dashboard.tv_search.get()}"])
            t = Dashboard.list_time[f"{Dashboard.tv_search.get()}"]
            if t == 0 :
                self.text2.set(f"เครื่องที่ {Dashboard.tv_search.get()} : UNLIMIT ชม.({admin.today_rate} ฿) ")
            else:
                self.text2.set(f"เครื่องที่ {Dashboard.tv_search.get()} : {t} ชม.({Rate.calculate(admin.today_rate,t)} ฿) ")
            time_remain = int(seconds - Dashboard.list_stamp[f"{Dashboard.tv_search.get()}"])
            #true_time = datetime.fromtimestamp(time_remain).strftime("%H:%M:%S")
            true_time = str(timedelta(seconds=time_remain))
            for i in range (len(Computer.computer_list)):
                Dashboard.current_computer = Computer.computer_list[i]
                #print(Dashboard.current_computer.status.name)
                #print(type(Dashboard.current_computer.status))
                #print(ComputerStatus.OFF.name)
                if Dashboard.current_computer.serial_num == Dashboard.tv_search.get():
                    if  Dashboard.current_computer.status.name==ComputerStatus.OFF.name :
                        self.text3.set(f"เวลาที่ใช้ : 00:00:00")
                        #print("on")
                    elif  Dashboard.current_computer.status.name==ComputerStatus.ON.name :
                        self.text3.set(f"เวลาที่ใช้ : {true_time}")
                        #print("off")
                #self.text3.set(f"เวลาที่เหลือ : {true_time}")
                #print(true_time)
        except KeyError:
            #print("Key doesn't exist in dic")
            pass
        
        
        root_tk.after(1000, self.show_realtime)

if __name__ =="__main__"  :
    
    admin = Admin(None,None)
    d = Dashboard(root_tk)
    d.show_display()
    root_tk.mainloop()