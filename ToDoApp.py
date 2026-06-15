import customtkinter as ctk
from datetime import datetime as dt
from PIL import Image
import os
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FCT

userDataFileDir="userData.txt"
taskFileDir="taskFileData.txt"
class App(ctk.CTk):
    t_counter=0

    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW",self.on_close)
        self.geometry("1536x864+200+50")
        ctk.set_appearance_mode("dark")
        self.title("Task Tracker")
        self.resizable(False,False)
        self.main_X=self.winfo_x()
        self.main_y=self.winfo_y()
        self.main_w=self.winfo_width()
        self.main_h=self.winfo_height()
        self.popup_width=400
        self.popup_height=150
        self.spawn_x = self.main_X + (self.main_w // 2) - (self.popup_width // 2)
        self.spawn_y = self.main_y + (self.main_h // 2) - (self.popup_height // 2)
        self.data_Reset_Flag=False
        self.stat_Reset_Flag=False
        file=open(userDataFileDir,"r")
        
        if not file.read():
            file.close()
            self.Done=0
            self.Left=0
            self.Total=0
        else:
            file.close()
            with open(userDataFileDir,'r',encoding='utf-8') as file:
                data=file.readlines()
                file.close()
            self.name=data[0][6:].strip()
            self.Done=int(data[4])
            self.Left=int(data[5])
            self.Total=self.Done+self.Left

            with open(userDataFileDir,"r") as f:
                f.readline()
                f.readline()
                data=f.readline().strip()
                f.close()
            if data and str(dt.now().date())!=data:
                self.dataReset()        

    def main(self):
        currbtn=None
        menuFrame=None

        def menuSwitch(btn,tab):
            nonlocal currbtn
            tabview.set(tab)
            self.btnConfig(btn,"#00F2FF","#000000","#00F2FF")
            if not currbtn==btn:
                self.btnConfig(currbtn,"transparent","#FFFFFF","#144870")
            currbtn=btn
        
        def homeStart():            
            nonlocal currbtn
            nonlocal menuFrame

            homeFrame,menuFrame=self.homescreen(tabview.tab("Home"))
            homeFrame.place(relx=0.5,rely=0.5,anchor="center",relwidth=1,relheight=1)
            menuOptions=ctk.CTkFrame(menuFrame,fg_color="transparent")
            menuOptions.place(relx=0.5,rely=0.5,anchor="center")

            homestatFrame=ctk.CTkFrame(tabview.tab("Home"),fg_color="#303030",width=300,height=400)
            self.after(2500,lambda:homestatFrame.place(rely=0.5,relx=0.87,anchor="center"))
            self.homeStats(homestatFrame)

            w=menuOptions._current_width
            h=50
            t=20
            homeB=ctk.CTkButton(menuOptions,text="Home",command=lambda: (menuSwitch(homeB,"Home"),self.homeStats(homestatFrame)),fg_color="transparent",width=w,height=h,font=("Arial",t))
            TaskB=ctk.CTkButton(menuOptions,text="Tasks",command=lambda: menuSwitch(TaskB,"Tasks"),fg_color="transparent",width=w,height=h,font=("Arial",t))
            StatB=ctk.CTkButton(menuOptions,text="Stats",command=lambda:( menuSwitch(StatB,"Stats"),self.updateCanvas()),fg_color="transparent",width=w,height=h,font=("Arial",t))
            SetB=ctk.CTkButton(menuOptions,text="Settings",command=lambda: menuSwitch(SetB,"Settings"),fg_color="transparent",width=w,height=h,font=("Arial",t))
            ResetB=ctk.CTkButton(menuFrame,text="Reset",hover_color="#FF0000",fg_color="transparent",width=w,height=h,font=("Arial",t),command=lambda:(os.remove(userDataFileDir),os.remove(taskFileDir),self.on_close()))
            homeB.pack()
            self.btnConfig(homeB,"#00F2FF","#000000","#00F2FF")
            currbtn=homeB
            TaskB.pack()
            StatB.pack()
            SetB.pack()
            ResetB.place(relx=0.5,rely=0.9,anchor="center")

        tabview=ctk.CTkTabview(self,fg_color="transparent")
        tabview.add("Home")
        tabview.add("Tasks")
        tabview.add("Stats")
        tabview.add("Settings")
        tabview.set("Home")
        tabview._segmented_button.grid_remove()
        tabview.place(relwidth=1,relheight=1)

        taskFrame=ctk.CTkScrollableFrame(tabview.tab("Tasks"),fg_color="transparent")
        taskFrame.place(relwidth=1,relheight=1)
        self.taskMenu(taskFrame)
        statFrame=ctk.CTkScrollableFrame(tabview.tab("Stats"),fg_color="transparent")
        statFrame.place(relwidth=1,relheight=1)
        self.fig,self.ax=plt.subplots(figsize=(13,7),facecolor="#242424")
        self.canvas=FCT(self.fig,master=statFrame)       
        self.ax.set_facecolor("#242424")
        self.ax.tick_params(color="#FFFFFF")
        self.ax.grid(axis='y', color="#757575", linestyle='--', linewidth=0.5, alpha=0.5)
        self.ax.set_axisbelow(True)
        for spine in self.ax.spines.values():
            spine.set_color('gray')
        self.widget=self.canvas.get_tk_widget()
        
        self.statMenu(statFrame)
        setFrame=ctk.CTkScrollableFrame(tabview.tab("Settings"),fg_color="transparent")
        setFrame.place(relwidth=1,relheight=1)
        self.setMenu(setFrame)
        
        file=open(userDataFileDir,"r")
        if not file.read():
            self.after(1000,lambda: self.newuser())
            return
        else:
            self.after(1000,homeStart)
        file.close() 
    
    def homeStats(self,homestatFrame):
        if homestatFrame.winfo_children():
            for child in homestatFrame.winfo_children():
                child.destroy()
        self.labelgen(homestatFrame,"Today's Progress:",tfont=("system",27)).place(relx=0.5,rely=0.1,anchor="center")
        progress=self.labelgen(homestatFrame,f"Completed: {self.Done}\nIncomplete: {self.Left}",tfont=("system",35))
        progress.configure(anchor="w",justify="left",padx=45)
        totalL=self.labelgen(homestatFrame,f"Total:           {self.Total}",tfont=("system",35),tcol="#EEFF00")
        totalL.configure(anchor="w",justify="left",padx=45)
        progress.place(relx=0,rely=0.4,anchor="w")
        totalL.place(relx=0,rely=0.55,anchor="w")

    def btnAction(self,action,selTaskFrame,t_id,progress,totalL,newBtn):
        def delF(finFlag):
            selTaskFrame.destroy()
            with open(taskFileDir,"r") as f:
                data=f.readlines()
                f.close()
            flag=False
            i=0
            for line in data:
                i+=1              
                if f"t_id: {t_id}" in line:
                    Start_index=i-2
                    flag=True
                elif flag==True and ("[---EndOfTask---]" in line):
                    End_index=i
                    break
            del data[Start_index:End_index]
            with open(taskFileDir,"w") as f:
                f.writelines(data)
                f.close()          
            with open(userDataFileDir,"r") as f:
                data=f.readlines()
                f.close()
            self.Left-=1
            if finFlag==True:
                self.Done+=1
                data[4]=str(self.Done)+'\n'
                data[3*dt.now().weekday()+6+1]=str(self.Done)+'\n'
            else:
                self.Total-=1

            data[5]=str(self.Left)+'\n'
            data[3*dt.now().weekday()+6+2]=str(self.Left)+'\n'
            with open(userDataFileDir,'w',encoding='utf-8') as file:
                file.writelines(data)
                file.close()
            progress.configure(text=f"Completed: {self.Done}\nIncomplete: {self.Left}")
            totalL.configure(text=f"Total:           {self.Total}")

        def editF():
            def restoreTask(data):
                nonlocal dLabel
                con.destroy()
                can.destroy()
                newBtn.configure(state="normal")
                tText=data[0]
                title.destroy()
                dLabel.destroy()
                dText=data[1]
                desc.destroy()
                self.labelgen(selTaskFrame,tText.strip(),tfont=("system",30),tcol="#FF8000").pack(padx=20,pady=(20,20))
                dLabel=self.labelgen(selTaskFrame,"Description:",tfont=("system",20))
                dLabel.pack(anchor="w",padx=20)
                nDesc=self.labelgen(selTaskFrame,dText,tfont=("Arial",15))
                nDesc.configure(fg_color="#242424",anchor="w",padx=20,pady=20,justify="left")
                nDesc.pack(fill="x",padx=20,pady=(10,10),anchor="w")

                delImg=Image.open("D:/code/Python/icons/delete.png")
                editImg=Image.open("D:/code/Python/icons/edit.png")
                chkImg=Image.open("D:/code/Python/icons/checkbox.png")
                img=ctk.CTkImage(dark_image=delImg)
                img2=ctk.CTkImage(dark_image=editImg)
                img3=ctk.CTkImage(dark_image=chkImg)
                optFrame=ctk.CTkFrame(selTaskFrame,height=50,fg_color="transparent")                
                ctk.CTkButton(optFrame,image=img,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("delete",selTaskFrame,t_id,progress,totalL,None)).place(rely=0.5,relx=0.3,anchor="center")
                ctk.CTkButton(optFrame,image=img2,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("edit",selTaskFrame,t_id,progress,totalL,newBtn)).place(rely=0.5,relx=0.5,anchor="center")
                ctk.CTkButton(optFrame,image=img3,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("finish",selTaskFrame,t_id,progress,totalL,None)).place(rely=0.5,relx=0.7,anchor="center")
                optFrame.pack(fill="x")
            
            def setTask():
                if not title.get():
                    warn=ctk.CTkToplevel()
                    warn.title("Warning")
                    warn.geometry(f"400x150+{self.spawn_x}+{self.spawn_y}")
                    label=ctk.CTkLabel(warn,text="No title given!",font=("Arial",30))
                    label.pack(pady=(25,0))
                    ctk.CTkButton(warn,text="OK",fg_color="#303030",command=warn.destroy).pack(pady=30)
                    warn.transient(self)
                    return

                nonlocal dLabel
                con.destroy()
                can.destroy()
                newBtn.configure(state="normal")
                tText=title.get()
                title.destroy()
                dLabel.destroy()
                dText=desc.get("1.0","end-1c")
                desc.destroy()
                self.labelgen(selTaskFrame,tText.strip(),tfont=("system",30),tcol="#FF8000").pack(padx=20,pady=(20,20))
                dLabel=self.labelgen(selTaskFrame,"Description:",tfont=("system",20))
                dLabel.pack(anchor="w",padx=20)
                nDesc=self.labelgen(selTaskFrame,dText,tfont=("Arial",15))
                nDesc.configure(fg_color="#242424",anchor="w",padx=20,pady=20,justify="left")
                nDesc.pack(fill="x",padx=20,pady=(10,10),anchor="w")

                delImg=Image.open("D:/code/Python/icons/delete.png")
                editImg=Image.open("D:/code/Python/icons/edit.png")
                chkImg=Image.open("D:/code/Python/icons/checkbox.png")
                img=ctk.CTkImage(dark_image=delImg)
                img2=ctk.CTkImage(dark_image=editImg)
                img3=ctk.CTkImage(dark_image=chkImg)
                optFrame=ctk.CTkFrame(selTaskFrame,height=50,fg_color="transparent")                
                ctk.CTkButton(optFrame,image=img,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("delete",selTaskFrame,t_id,progress,totalL,None)).place(rely=0.5,relx=0.3,anchor="center")
                ctk.CTkButton(optFrame,image=img2,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("edit",selTaskFrame,t_id,progress,totalL,newBtn)).place(rely=0.5,relx=0.5,anchor="center")
                ctk.CTkButton(optFrame,image=img3,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("finish",selTaskFrame,t_id,progress,totalL,None)).place(rely=0.5,relx=0.7,anchor="center")
                optFrame.pack(fill="x")

                taskStart="[---Task---]"
                taskEnd="[---EndOfTask---]"
                task=[f"{taskStart}\n",f"t_id: {t_id}\n",f"{tText}\n",f"{dText}\n",f"{taskEnd}\n"]
                with open(taskFileDir,"r") as f:
                    data=f.readlines()
                    f.close()
                flag=False
                i=0
                Start_index=0
                End_index=0
                for line in data:
                    i+=1              
                    if f"t_id: {t_id}" in line:
                        Start_index=i-2
                        flag=True
                    elif flag==True and ("[---EndOfTask---]" in line):
                        End_index=i
                        break
                data[Start_index:End_index]=task
                with open(taskFileDir,"w") as f:
                    f.writelines(data)
                    f.close()          
                with open(userDataFileDir,"r") as f:
                    data=f.readlines()
                    f.close()

            data=list()
            for child in selTaskFrame.winfo_children():
                if str(type(child))=="<class 'customtkinter.windows.widgets.ctk_label.CTkLabel'>":
                    text=child.cget("text")
                    if text!="Description:":
                        data.append(text)
                    child.destroy()
                else:
                    child.destroy()
                    newBtn.configure(state="disabled")
            dLabel=self.labelgen(selTaskFrame,"Description",tfont=("system",20))
            title=ctk.CTkEntry(selTaskFrame,placeholder_text="Task Title",font=("Arial",30))
            title.pack(fill="x",padx=20,pady=20)
            title.insert(0,data[0])            
            dLabel.pack(anchor="w",padx=20)
            desc=ctk.CTkTextbox(selTaskFrame)
            desc.pack(fill="x",padx=20,pady=(10,20))
            desc.insert("1.0",data[1])
            con=ctk.CTkButton(selTaskFrame,text="Confirm",command=lambda:setTask())
            con.pack(side="left",padx=250,pady=25)
            can=ctk.CTkButton(selTaskFrame,text="Cancel",command=lambda:(restoreTask(data),newBtn.configure(state="normal")))
            can.pack(side="right",padx=250,pady=25)

        def finF():
            init_hex="#242424"
            p=0.0
            if type(init_hex)==tuple:
                r,g,b=int(init_hex[1][1:3],16),int(init_hex[1][3:5],16),int(init_hex[1][5:7],16)
            else:
                r,g,b=int(init_hex[1:3],16),int(init_hex[3:5],16),int(init_hex[5:7],16)
            def fade():
                nonlocal p
                target_hex="#008B21"
                tr,tg,tb=int(target_hex[1:3],16),int(target_hex[3:5],16),int(target_hex[5:7],16)
                if p<=1.0:
                    nr,ng,nb=int(r+(tr-r)*p),int(g+(tg-g)*p),int(b+(tb-b)*p)
                    p+=0.1
                    new_hex=f"#{nr:02x}{ng:02x}{nb:02x}"
                    selTaskFrame.configure(fg_color=new_hex)
                    self.after(30,lambda: fade())
                else:
                    p=0.0
                    self.after(500,delF(True))
            fade()
                
            
        if action=="delete":
            delF(False)
        elif action=="edit":
            editF()
        else:
            finF()

    def taskMenu(self,taskFrame):        
        self.labelgen(taskFrame,"Tasks").pack(padx=(185,0))
        topFrame=ctk.CTkFrame(taskFrame,fg_color="transparent")
        topFrame.pack(fill="x")
        progressFrame=ctk.CTkFrame(topFrame,fg_color="transparent")
        progress=self.labelgen(progressFrame,f"Completed: {self.Done}\nIncomplete: {self.Left}",tfont=("system",30))
        progress.configure(anchor="w",justify="left")
        totalL=self.labelgen(progressFrame,f"Total:           {self.Total}",tfont=("system",30),tcol="#EEFF00")
        totalL.configure(anchor="w",justify="left")
        progress.pack(anchor="w")
        totalL.pack(anchor="w")
        progressFrame.pack(anchor="w",padx=(350,0),side="left",pady=50)

        newTasks=ctk.CTkFrame(taskFrame,fg_color="transparent")
        newTasks.pack(pady=5,padx=(200,0),fill="x")

        def taskRetrive():
            def taskPack(tText,dText,t_id):
                newTaskFrame=ctk.CTkFrame(newTasks)
                newTaskFrame.pack(pady=5,fill="x")
                dLabel=self.labelgen(newTaskFrame,"Description:",tfont=("system",20))
                self.labelgen(newTaskFrame,tText.strip(),tfont=("system",30),tcol="#FF8000").pack(padx=20,pady=(20,20))
                dLabel.pack(anchor="w",padx=20)
                nDesc=self.labelgen(newTaskFrame,dText,tfont=("Arial",15))
                nDesc.configure(fg_color="#242424",anchor="w",padx=20,pady=20,justify="left")
                nDesc.pack(fill="x",padx=20,pady=(10,10),anchor="w")
                

                delImg=Image.open("D:/code/Python/icons/delete.png")
                editImg=Image.open("D:/code/Python/icons/edit.png")
                chkImg=Image.open("D:/code/Python/icons/checkbox.png")
                img=ctk.CTkImage(dark_image=delImg)
                img2=ctk.CTkImage(dark_image=editImg)
                img3=ctk.CTkImage(dark_image=chkImg)
                optFrame=ctk.CTkFrame(newTaskFrame,height=50,fg_color="transparent")                
                ctk.CTkButton(optFrame,image=img,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("delete",newTaskFrame,t_id,progress,totalL,None)).place(rely=0.5,relx=0.3,anchor="center")
                ctk.CTkButton(optFrame,image=img2,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("edit",newTaskFrame,t_id,progress,totalL,newBtn)).place(rely=0.5,relx=0.5,anchor="center")
                ctk.CTkButton(optFrame,image=img3,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("finish",newTaskFrame,t_id,progress,totalL,None)).place(rely=0.5,relx=0.7,anchor="center")
                optFrame.pack(fill="x")
                        
            with open(taskFileDir,"r") as f:
                data=f.readlines()
                f.close()
            tidflag=False
            tflag=False
            dText=""
            for line in data:                
                if "[---Task---]" in line:
                    tflag=True
                    tidflag=True
                elif tidflag==True:
                    self.t_counter=int(line[6:].strip())
                    t_id=self.t_counter
                    tidflag=False
                elif tflag==True:
                    tText=line
                    tflag=False
                elif "[---EndOfTask---]" in line:
                    if not dText.strip():
                        dText="\n"
                    taskPack(tText,dText.strip(),t_id)
                    dText=""            
                else:
                    dText+=line

        taskRetrive()

        def newTask():            
            def setTask():
                if not title.get():
                    warn=ctk.CTkToplevel()
                    warn.title("Warning")
                    warn.geometry(f"400x150+{self.spawn_x}+{self.spawn_y}")
                    label=ctk.CTkLabel(warn,text="No title given!",font=("Arial",30))
                    label.pack(pady=(25,0))
                    ctk.CTkButton(warn,text="OK",fg_color="#303030",command=warn.destroy).pack(pady=30)
                    warn.transient(self)
                    return

                self.t_counter+=1
                t_id=self.t_counter
                nonlocal dLabel
                con.destroy()
                can.destroy()
                newBtn.configure(state="normal")
                tText=title.get()
                title.destroy()
                dLabel.destroy()
                dText=desc.get("1.0","end-1c")
                desc.destroy()
                self.labelgen(newTaskFrame,tText.strip(),tfont=("system",30),tcol="#FF8000").pack(padx=20,pady=(20,20))
                dLabel=self.labelgen(newTaskFrame,"Description:",tfont=("system",20))
                dLabel.pack(anchor="w",padx=20)
                nDesc=self.labelgen(newTaskFrame,dText,tfont=("Arial",15))
                nDesc.configure(fg_color="#242424",anchor="w",padx=20,pady=20,justify="left")
                nDesc.pack(fill="x",padx=20,pady=(10,10),anchor="w")

                delImg=Image.open("D:/code/Python/icons/delete.png")
                editImg=Image.open("D:/code/Python/icons/edit.png")
                chkImg=Image.open("D:/code/Python/icons/checkbox.png")
                img=ctk.CTkImage(dark_image=delImg)
                img2=ctk.CTkImage(dark_image=editImg)
                img3=ctk.CTkImage(dark_image=chkImg)
                optFrame=ctk.CTkFrame(newTaskFrame,height=50,fg_color="transparent")                
                ctk.CTkButton(optFrame,image=img,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("delete",newTaskFrame,t_id,progress,totalL,None)).place(rely=0.5,relx=0.3,anchor="center")
                ctk.CTkButton(optFrame,image=img2,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("edit",newTaskFrame,t_id,progress,totalL,newBtn)).place(rely=0.5,relx=0.5,anchor="center")
                ctk.CTkButton(optFrame,image=img3,text="",fg_color="#DC6E00",corner_radius=100,width=50,command=lambda:self.btnAction("finish",newTaskFrame,t_id,progress,totalL,None)).place(rely=0.5,relx=0.7,anchor="center")
                optFrame.pack(fill="x")
                self.update_idletasks()
                taskFrame._parent_canvas.yview_moveto(1.0)  
                self.Left+=1
                self.Total=self.Left+self.Done
                with open(userDataFileDir,'r',encoding='utf-8') as file:
                    data = file.readlines()
                    file.close()
                data[5]=str(self.Left)+'\n'
                data[3*dt.now().weekday()+6+2]=str(self.Left)+'\n'
                with open(userDataFileDir,'w',encoding='utf-8') as file:
                    file.writelines(data)
                    file.close()
                progress.configure(text=f"Completed: {self.Done}\nIncomplete: {self.Left}")
                totalL.configure(text=f"Total:           {self.Total}")
                taskStart="[---Task---]"
                taskEnd="[---EndOfTask---]"
                task=f"""{taskStart}
t_id: {t_id}
{tText}
{dText}
{taskEnd}
"""
                with open(taskFileDir,"a") as f:
                    f.write(task)
                    f.close()
            
            newBtn.configure(state="disabled")
            newTaskFrame=ctk.CTkFrame(newTasks)
            newTaskFrame.pack(pady=5,fill="x")
            title=ctk.CTkEntry(newTaskFrame,placeholder_text="Task Title",font=("Arial",30))
            title.pack(fill="x",padx=20,pady=20)
            dLabel=self.labelgen(newTaskFrame,"Description:",tfont=("system",20))
            dLabel.pack(anchor="w",padx=20)
            desc=ctk.CTkTextbox(newTaskFrame)
            desc.pack(fill="x",padx=20,pady=(10,20))
            con=ctk.CTkButton(newTaskFrame,text="Confirm",command=lambda:setTask())
            con.pack(side="left",padx=250,pady=25)
            can=ctk.CTkButton(newTaskFrame,text="Cancel",command=lambda:(newTaskFrame.destroy(),newBtn.configure(state="normal")))
            can.pack(side="right",padx=250,pady=25)
            self.update_idletasks()
            taskFrame._parent_canvas.yview_moveto(1.0)  
        
        def clcTasks():
            clrBtn.configure(state="disabled")
            def clc():
                for widget in newTasks.winfo_children():
                    widget.destroy()
                clrBtn.configure(state="normal")
                newBtn.configure(state="normal")
                self.Left=0
                self.Total=self.Left+self.Done
                with open(userDataFileDir,'r',encoding='utf-8') as file:
                    data = file.readlines()
                    file.close()
                data[5]=str(self.Left)+'\n'
                data[3*dt.now().weekday()+6+2]=str(self.Left)+'\n'
                with open(userDataFileDir,'w',encoding='utf-8') as file:
                    file.writelines(data)
                    file.close()
                with open(taskFileDir,"w") as f:
                    f.write("")
                    f.close()
                progress.configure(text=f"Completed: {self.Done}\nIncomplete: {self.Left}")
                totalL.configure(text=f"Total:           {self.Total}")

            warn=ctk.CTkToplevel()
            warn.title("Warning")
            warn.geometry(f"400x150+{self.spawn_x}+{self.spawn_y}")
            label=ctk.CTkLabel(warn,text="Are you sure?",font=("Arial",30))
            label.pack(pady=(25,0))
            yes=ctk.CTkButton(warn,text="Yes",fg_color="#303030",command=lambda:(clc(),warn.destroy(),newBtn.configure(state="normal")),width=100)
            no=ctk.CTkButton(warn,text="No",fg_color="#303030",command=lambda:(warn.destroy(),clrBtn.configure(state="normal")),width=100)
            yes.pack(side="left",padx=(40,0))
            no.pack(side="right",padx=(0,40))
            warn.transient(self)
            warn.grab_set()
        
        btnFrame=ctk.CTkFrame(topFrame)
        newBtn=ctk.CTkButton(btnFrame,text="New Task",font=("Arial",25),fg_color="#00A640",hover_color="#007C2F",command=lambda:newTask(),corner_radius=5)
        clrBtn=ctk.CTkButton(btnFrame,text="Clear Tasks",font=("Arial",25),fg_color="#FF0000",hover_color="#B90000",command=lambda:clcTasks(),corner_radius=5)
        newBtn.pack()
        clrBtn.pack(pady=10)
        btnFrame.pack(anchor="e",side="right",padx=(0,200))

    def statMenu(self,statFrame):
        self.labelgen(statFrame,"Statistics").pack(padx=(185,0))
        self.widget.pack(padx=(185,0))
        N=7
        with open(userDataFileDir,"r") as f:
            data=f.readlines()
            f.close()
        
        Done=data[7::3]
        NotDone=data[8::3]
        fDone=list()
        fNotDone=list()
        for i in Done:
            fDone.append(int(i.strip()))
        for i in NotDone:
            fNotDone.append(int(i.strip()))
        del Done
        del NotDone
        
        try: top=max(fDone)+max(fNotDone)
        except ValueError: 
            top=10
            fDone=[0,0,0,0,0,0,0]
            fNotDone=[0,0,0,0,0,0,0]
        if top<10:
            top=10

        arr=np.arange(N)

        p1=plt.bar(arr,fDone,color='green',width=0.7)
        p2=plt.bar(arr,fNotDone,bottom=fDone,color='red',width=0.7)

        plt.legend((p1[0], p2[0]), ('Done', 'Not Done'))
        plt.xticks(arr,["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],color="#FFFFFF")
        plt.yticks(np.arange(0,top,1),color="#FFFFFF")
        plt.title("Task Statistics",color="#FFFFFF")
        plt.xlabel("Days",color="#FFFFFF")
        plt.ylabel("Tasks",color="#FFFFFF")

    def updateCanvas(self):
        self.ax.clear()
        self.ax.set_facecolor("#242424")
        self.ax.tick_params(axis='y', colors="#FFFFFF")
        self.ax.grid(axis='y', color="#757575", linestyle='--', linewidth=0.5, alpha=0.5)
        self.ax.set_axisbelow(True)
        for spine in self.ax.spines.values():
            spine.set_color('gray')

        N=7
        with open(userDataFileDir,"r") as f:
            data=f.readlines()
            f.close()
        
        Done=data[7::3]
        NotDone=data[8::3]
        fDone=list()
        fNotDone=list()
        for i in Done:
            fDone.append(int(i.strip()))
        for i in NotDone:
            fNotDone.append(int(i.strip()))
        del Done
        del NotDone
        
        top=max(fDone)+max(fNotDone)
        if top<10:
            top=10

        arr=np.arange(N)
        
        p1=self.ax.bar(arr,fDone,color='green',width=0.7)
        p2=self.ax.bar(arr,fNotDone,bottom=fDone,color='red',width=0.7)
        
        self.ax.set_xlabel("Days",color="#FFFFFF")
        self.ax.set_ylabel("Tasks",color="#FFFFFF")
        plt.title("Task Statistics",color="#FFFFFF")
        self.ax.legend((p1[0], p2[0]), ('Done', 'Not Done'))
        self.ax.set_yticks(np.arange(0,top,1))
        self.ax.set_xticks(arr,labels=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],color="#FFFFFF")
        self.canvas.draw_idle()

    def setMenu(self,setFrame):
        self.labelgen(setFrame,"Settings").pack(padx=(185,0))

    def btnConfig(self,btn,btncol,tcol,hcol):
        btn.configure(fg_color=btncol,text_color=tcol,hover_color=hcol)
    
    def labelgen(self,master,t="Placeholder",tcol="#FFFFFF",tfont=("system",50)):
        if not master:
            master=self
        label=ctk.CTkLabel(master,text=t,text_color=tcol,font=tfont,fg_color="transparent")
        return label

    def fadeout(self,l):
        init_hex=l.cget("text_color")
        p=0.0
        if type(init_hex)==tuple:
            r,g,b=int(init_hex[1][1:3],16),int(init_hex[1][3:5],16),int(init_hex[1][5:7],16)
        else:
            r,g,b=int(init_hex[1:3],16),int(init_hex[3:5],16),int(init_hex[5:7],16)
        def fade():
            nonlocal p
            tr,tg,tb=24,24,24
            if p<=1.0:
                nr,ng,nb=int(r+(tr-r)*p),int(g+(tg-g)*p),int(b+(tb-b)*p)
                p+=0.05
                new_hex=f"#{nr:02x}{ng:02x}{nb:02x}"
                l.configure(text_color=new_hex)
                self.after(30,lambda: fade())
            else:
                p=0.0
                l.destroy()
                return
        fade()
    
    def fadein(self,l,target="#FFFFFF"):
        p=0.0
        init_hex=l.cget("text_color")
        if type(init_hex)==tuple:
            r,g,b=int(init_hex[1][1:3],16),int(init_hex[1][3:5],16),int(init_hex[1][5:7],16)
        else:
            r,g,b=int(init_hex[1:3],16),int(init_hex[3:5],16),int(init_hex[5:7],16)
        def fade():
            nonlocal p
            tr,tg,tb=int(target[1:3],16),int(target[3:5],16),int(target[5:7],16)
            if p<=1.0:
                nr,ng,nb=int(r+(tr-r)*p),int(g+(tg-g)*p),int(b+(tb-b)*p)
                p+=0.05
                new_hex=f"#{nr:02x}{ng:02x}{nb:02x}"
                l.configure(text_color=new_hex)
                self.after(30,lambda: fade())
            else:
                p=0.0
                return
        fade()

    def dataReset(self):
        with open(userDataFileDir,"r") as f:
            data=f.readlines()
            f.close()
        data[4]="0\n"
        data[5]="0\n"
        with open(userDataFileDir,"w") as f:
            f.writelines(data)
            f.close()
        wt=(3600*24)-(dt.now().hour*3600)-(dt.now().minute*60)-(dt.now().second)
        self.after(wt*1000,lambda:(self.dataReset()))

        firstWeekday=dt.now().weekday()-dt.now().day%7+1
        if firstWeekday<0:
            firstWeekday+=7
        else:
            firstWeekday%=7
        weekno=(dt.now().day+firstWeekday-1)//7+1
        day,month,year=0,0,0
        with open(userDataFileDir,"r") as f:
            f.readline()
            f.readline()
            data=f.readline().strip()
            if data:
                day=int(data[8:])
                month=int(data[5:7])
                year=int(data[0:4])
            f.close()
        if day!=0:
            prevweekno=(day+firstWeekday-1)//7+1
            if weekno!=prevweekno or month!=dt.now().month or year!=dt.now().year:
                self.statReset()

    def statReset(self):
        with open(userDataFileDir,"w") as f:
            f.write(f"""Name: {self.name}
LC:
0000-00-00
DP:
0
0
M:  
0
0
T:  
0
0
W:  
0
0
Th: 
0
0
F:  
0
0
S:  
0
0
Su: 
0
0""")
        # self.updateCanvas()
        wt=((6-dt.now().weekday())*3600*24)+(24*3600)-(dt.now().hour*3600)-(dt.now().minute*60)-(dt.now().second)
        self.after(wt*1000,self.statReset)

    def homescreen(self,tabview):
        homeFrame=ctk.CTkFrame(tabview,fg_color="transparent")
        def greeting():
            if dt.now().hour>=17:
                return "Good Evening,"
            elif dt.now().hour>=12:
                return "Good Afternoon,"
            else:  
                return "Good Morning,"
        greetingL=ctk.CTkLabel(homeFrame,text=greeting(),font=("system",60),text_color="#242424")
        greetingL.place(relx=0.5,rely=0.1,anchor="center")
        nameL=ctk.CTkLabel(homeFrame,text=self.name,font=("system",60),text_color="#242424")
        nameL.place(relx=0.5,rely=0.19,anchor="center")
        self.fadein(nameL,"#00F2FF")
        self.fadein(greetingL)

        days=("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
        day=days[dt.now().weekday()]
        dd=f"{dt.now().day:02}"
        mm=f"{dt.now().month:02}"
        month=""
        match mm:
            case '01':
                month="January"
            case '02':
                month="February"
            case '03':
                month="March"
            case '04':
                month="April"
            case '05':
                month="May"
            case '06':
                month="June"
            case '07':
                month="July"
            case '08':
                month="August"
            case '09':
                month="September"
            case '10':
                month="October"
            case '11':
                month="November"
            case '12':
                month="December"
            case _:
                month="An Error occurred"
        yyyy=str(dt.now().year)
        date=f"{month} {dd}, {yyyy}"
        time=str(dt.now().time())[:8]

        dFrame=ctk.CTkFrame(homeFrame,fg_color="transparent")
        dateL=ctk.CTkLabel(dFrame,text=date,font=("system",45),text_color="#FFFFFF")
        dateL.pack()
        dayL=ctk.CTkLabel(dFrame,text=day,font=("system",50),text_color="#F6FF00")
        dayL.pack()

        w=300
        h=150
        tFrame=ctk.CTkFrame(homeFrame,fg_color="#00C8FF",corner_radius=40,width=w,height=h)
        tFrameI=ctk.CTkFrame(tFrame,fg_color="#000000",corner_radius=40)
        tFrameI.place(relx=0.5,rely=0.5,relwidth=0.9,relheight=0.85,anchor="center")
        timeL=ctk.CTkLabel(tFrameI,text=time,text_color="#FFFFFF",font=("system",50),fg_color="transparent")
        timeL.place(relx=0.5,rely=0.5,anchor="center")

        menuFrame=ctk.CTkFrame(self,fg_color="#303030")
        menuL=self.labelgen(menuFrame,"Menu",tfont=("system",30))
        menuL.pack(pady=20)
        self.after(2500,lambda:(tFrame.place(relx=0.5,rely=0.75,anchor="center"),dFrame.place(relx=0.5,rely=0.45,anchor="center"),menuFrame.place(relheight=1.01,relwidth=0.13,relx=0,rely=0.5,anchor="w")))

        def greetingF():
            if dt.now().hour>=17:
                greet="Good Evening,"
                wt=(24*3600)-(dt.now().hour*3600)-(dt.now().minute*60)-(dt.now().second)
            elif dt.now().hour>=12:
                greet="Good Afternoon,"
                wt=(17*3600)-(dt.now().hour*3600)-(dt.now().minute*60)-(dt.now().second)
            else:  
                greet="Good Morning,"
                wt=(12*3600)-(dt.now().hour*3600)-(dt.now().minute*60)-(dt.now().second)
            greetingL.configure(text=greet)
            self.after(wt,greetingF)
        
        def timeF():
            time=str(dt.now().time())[:8]
            timeL.configure(text=time)
            self.after(1000,timeF)

        def dateF():
            days=("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
            day=days[dt.now().weekday()]
            dd=f"{dt.now().day:02}"
            mm=f"{dt.now().month:02}"
            month=""
            match mm:
                case '01':
                    month="January"
                case '02':
                    month="February"
                case '03':
                    month="March"
                case '04':
                    month="April"
                case '05':
                    month="May"
                case '06':
                    month="June"
                case '07':
                    month="July"
                case '08':
                    month="August"
                case '09':
                    month="September"
                case '10':
                    month="October"
                case '11':
                    month="November"
                case '12':
                    month="December"
                case _:
                    month="An Error occurred"
            yyyy=str(dt.now().year)
            date=f"{month} {dd}, {yyyy}"
            dateL.configure(text=date)
            dayL.configure(text=day)
            wt=(3600*24)-(dt.now().hour*3600)-(dt.now().minute*60)-(dt.now().second)
            self.after(wt*1000,lambda:(dateF()))
        greetingF()
        dateF()
        timeF()
        return (homeFrame,menuFrame)
    
    def newuser(self):
        def welcomeF():
            welcome=self.labelgen(self,"Welcome","#242424",("system",80))
            welcome.place(relx=0.5,rely=0.3,anchor="center")
            self.fadein(welcome)
            self.after(2000,lambda: self.fadeout(welcome))
        def entryF():
            nameL=self.labelgen(self,"What's your name?","#242424",("system",60))
            nameL.place(relx=0.5,rely=0.4,anchor="center")
            self.fadein(nameL)
            entry=ctk.CTkEntry(self,placeholder_text="Enter your name", text_color="#FFFFFF", width=600, height=40,font=("Arial",20))
            self.after(1600,lambda *args: (entry.place(relx=0.5,rely=0.52,anchor="center")),entry.focus())
            
            def getname(*args):
                file=open("D:/Code/Python/userData.txt","w")
                self.name=entry.get()
                file.write(f"""Name: {self.name}
LC:
0000-00-00
DP:
0
0
M:  
0
0
T:  
0
0
W:  
0
0
Th: 
0
0
F:  
0
0
S:  
0
0
Su: 
0
0""")
                file.close()
                entry.destroy()
                self.after(1000,lambda: self.fadeout(nameL))
                self.after(2000,lambda: self.main())
            
            entry.bind("<Return>",command=getname)

        welcomeF()
        self.after(3500,entryF)
    
    def on_close(self):
        self.quit()
        plt.close('all')
        self.destroy()
        try:
            with open(userDataFileDir,"r") as f:
                data=f.readlines()
                f.close()
        except FileNotFoundError:
            pass
        else:
            if data:
                data[2]=f"{dt.now().date()}\n"
                with open(userDataFileDir,"w") as f:
                    f.writelines(data)
                    f.close()
    

try:
    file=open(userDataFileDir,"x")
    file.close()
except FileExistsError:
    pass
try:
    file=open(taskFileDir,"x")
    file.close()
except FileExistsError:
    pass
app=App()


app.main()
app.mainloop()