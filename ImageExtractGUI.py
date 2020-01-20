#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 22:39:10 2019

@author: israelsolha
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 22:12:11 2019

@author: israelsolha
"""


import os
import cv2
import numpy as np

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

def analysis(video_path,directory_path):
    sizep = 5/30
    areap = sizep**2
    video_path_directory = video_path[::-1].split("/",1)[1][::-1]
    video_name_comp = video_path[::-1].split("/",1)[0][::-1]
    
    os.chdir(video_path_directory)
    video_name=video_name_comp.split('.')[0]
    
    os.chdir(directory_path)
    try:
        os.mkdir('Imagens')
    except:
        pass
    # Opens the Video file
    os.chdir(video_path_directory)
    cap= cv2.VideoCapture(video_name_comp)
    frame_rate=cap.get(cv2.CAP_PROP_FPS)
    if cap.isOpened(): 
        # get vcap property 
        width = int(cap.get(3))   # float
        height = int(cap.get(4)) # float
    os.chdir(directory_path+'/Imagens')
    try:
        os.makedirs(video_name+'/Original')
    except:
        pass
    try:
        os.makedirs(video_name+'/Tratada')
    except:
        pass
    os.chdir(directory_path + '/Imagens/'+video_name)
    out = cv2.VideoWriter(video_name+'_editado.avi',cv2.VideoWriter_fourcc('M','J','P','G'),frame_rate, (width,height))
    os.chdir(directory_path + '/Imagens/'+video_name+'/Original')
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite(video_name+'_orig_'+str(i)+'.jpg',frame)
        i+=1
    n_frames=i
    cap.release()
    areas=[]
    
    for i in range(n_frames):
        os.chdir(directory_path+'/Imagens/'+video_name+'/Original')
        foundCont = False
        filename = (video_name+'_orig_{}.jpg').format(i)
        
        # read original image
        img = cv2.imread(filename = filename)
        
        # Prepocess
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(1,1),1000)
        flag, thresh = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY)
        # Find contours
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea,reverse=True)
        for cont in range(1,7):
            contarray = np.array(contours[cont])
            minx=1000000
            miny=1000000
            maxx=0
            maxy=0
            for j in range(len(contarray)):
                
                if(contarray[j][0][0]<minx):
                    minx=contarray[j][0][0]
                    
                if(contarray[j][0][0]>maxx):
                    maxx=contarray[j][0][0]
                    
                if(contarray[j][0][1]<miny):
                    miny=contarray[j][0][1]
                    
                if(contarray[j][0][1]>maxy):
                    maxy=contarray[j][0][1]
                    
            M = cv2.moments(contours[0])
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
    
            xstart=x-40
            xfinish=x+40
            ystart=y-20
            yfinish=y+20
            for incx in range(xfinish-xstart):
                for incy in range(yfinish-ystart):
                    if((cv2.pointPolygonTest(contours[cont], (xstart+incx,ystart+incy), True)) > 0):
                        foundCont = True
                        break
                if foundCont:
                    break
            if foundCont:
                break
            
        pixels=0
        if(foundCont):
            for xt in range(minx, maxx+1):
                for yt in range(miny, maxy+1):
                    if((cv2.pointPolygonTest(contours[cont], (xt,yt), True)) >= 0):
                        pixels+=1
        areas.append(round(pixels*areap,2))
        imgcont = img.copy()
        if(foundCont):
            cv2.drawContours(imgcont, [contours[cont]], 0, (255,255,255), 2)
        os.chdir(directory_path+'/Imagens/'+video_name+'/Tratada')
        cv2.imwrite(video_name+'_cont_'+str(i)+'.jpg',imgcont)
        out.write(imgcont)
        
    out.release()
    cv2.destroyAllWindows()
    os.chdir(directory_path+'/Imagens/'+video_name+'/Tratada')
    frame_max = areas.index(max(areas))
    img = cv2.imread(video_name+'_cont_'+str(frame_max)+'.jpg')
    img = cv2.resize(img, (int(img.shape[1]*0.5),int(img.shape[0]*0.5)), interpolation = cv2.INTER_AREA)
    minute = frame_max//(60*frame_rate)
    second = frame_max//frame_rate
    if(second>60):
        minute += second//60
        second = second % 60
    milisecond = round((frame_max%frame_rate)/frame_rate*100)
    txt_area=('Area maxima: '+str(max(areas))+' mm2')
    txt_frame=('Frame com a area maxima: '+str(frame_max))
    txt_timestamp=('Timestamp: {:.0f}:{:02.0f}:{:02.0f}'.format(minute,second,milisecond))
    
    return txt_area,txt_frame,txt_timestamp,img

video_path=""
directory_path = ""

def checkIfReady():
    global video_path, directory_path
    if video_path != "" and directory_path != "":
        results=analysis(video_path,directory_path)
        
        resultado = tk.Label(canvas, text = "Resultado",bg='#d3d3d3',wraplength=500,justify='center')
        resultado.place(relx=0.2, rely = 0.35, relwidth=0.6, relheight = 0.05)
        
        r1 = tk.Label(canvas, text = results[0],bg='#d3d3d3',wraplength=500,justify='center')
        r1.place(relx=0.2, rely = 0.4, relwidth=0.6, relheight = 0.05)
        
        r2 = tk.Label(canvas, text = results[1],bg='#d3d3d3',wraplength=500,justify='center')
        r2.place(relx=0.2, rely = 0.45, relwidth=0.6, relheight = 0.05)
        
        r3 = tk.Label(canvas, text = results[2],bg='#d3d3d3',wraplength=500,justify='center')
        r3.place(relx=0.2, rely = 0.5, relwidth=0.6, relheight = 0.05)
        
        image = Image.fromarray(results[3].astype('uint8'), 'RGB')
        render = ImageTk.PhotoImage(image)
        img = tk.Label(image = render)
        img.image = render
        img.place(rely = 0.6, relx = 0.5, relwidth=0.6, anchor='n')
    
def getVideo():
    global video_path, directory_path
    video_path = filedialog.askopenfilename(initialdir = "/Users/israelsolha/Desktop/Data/Masters/Valvula Mitral/",title = "Selecionar Vídeo",filetypes = (("avi files","*.avi"),("all files","*.*")))
    button_label.configure(text=video_path)
    checkIfReady()
    
def getDirectory():
    global video_path, directory_path
    directory_path = filedialog.askdirectory(initialdir = "/Users/israelsolha/Desktop/Data/Masters/Valvula Mitral/",title = "Selecionar Pasta")
    button_label2.configure(text=directory_path)
    checkIfReady()
    
def toggle(button):
    button.destroy()
    
root = tk.Tk()
root.title("Análise da Válvula Mitral")

HEIGHT = 1000
WIDTH = 800

canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

button = tk.Button(root,text="Selecionar Vídeo", command = getVideo)
button.place(relx=0.4, rely = 0.05, relwidth=0.2, relheight = 0.05)
button.pi = button.place_info()

button_label = tk.Label(canvas, text = "",bg='#d3d3d3',wraplength=500,justify='center')
button_label.place(relx=0.2, rely = 0.125, relwidth=0.6, relheight = 0.05)

button2 = tk.Button(root,text="Selecionar Pasta", command = getDirectory)
button2.place(relx=0.4, rely = 0.2, relwidth=0.2, relheight = 0.05)

button_label2 = tk.Label(canvas, text = "",bg='#d3d3d3',wraplength=500,justify='center')
button_label2.place(relx=0.2, rely = 0.275, relwidth=0.6, relheight = 0.05)

root.mainloop()
