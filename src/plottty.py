import sys
import time
import os
import configparser
from subprocess import call
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

import matplotlib.pyplot as plt
#import cv2
from skimage import io
import matplotlib.image as mpimg
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec


#'width_ratios':[5, 1, 5, 1, 3, 1], 

#fig = plt.figure(figsize=(8,8)) # Notice the equal aspect ratio
#axes = [fig.add_subplot(3,6,i+1) for i in range(18)]

fig, axes = plt.subplots(3, 6, figsize=(20,13))

plt.subplots_adjust(wspace=0.01, hspace=0.05)
configplot = configparser.ConfigParser()

configplot.read('plotconfig.ini')
direct0=configplot['DIRECTS']['NODE_0_IMG']
rti00=configplot['IMAGES']['RTI_NODE0_CH0'] 
dop00=configplot['IMAGES']['DOP_NODE0_CH0']   

def animate(i):
    try:

        #config = configparser.ConfigParser()
        
        #config.read('/home/si/Dropbox/PyProjects/Poll_look/NeXtRAD.ini')
        #configplot.read('/home/si/Dropbox/PyProjects/Poll_look/plotconfig.ini')
      
        #NODE 0 IMAGES
        direct0=configplot['DIRECTS']['NODE_0_IMG']
        rti00=configplot['IMAGES']['RTI_NODE0_CH0']
        dop00=configplot['IMAGES']['DOP_NODE0_CH0']
        rti10=configplot['IMAGES']['RTI_NODE0_CH1']
        dop10=configplot['IMAGES']['DOP_NODE0_CH1']
        rti20=configplot['IMAGES']['RTI_NODE0_CH2']
        dop20=configplot['IMAGES']['DOP_NODE0_CH2']
        try:
            img1 = io.imread(direct0+rti00)
            img2 = io.imread(direct0+dop00)
            #img2 = cv2.resize(img2, (img2.shape[1],img1.shape[0]),interpolation = cv2.INTER_AREA)
            img3 = io.imread(direct0+rti10)
            img4 = io.imread(direct0+dop10)
            img5 = io.imread(direct0+rti20)
            img6 = io.imread(direct0+dop20)
        except:
            print('Missing Images From Directory')


        try:
            axes[0, 0].clear()
            axes[0, 0].imshow(img1) 
            axes[0, 0].set_title('Channel 0')
            pad = 0.01
            axes[0, 0].annotate('Node 0', xy=(0, 0.5), xytext=(-axes[0, 0].yaxis.labelpad - pad, 0),
                xycoords=axes[0, 0].yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center')

            axes[0, 0].axis('off') 
            #axes[0, 0].set_aspect('equal')
            axes[0, 1].clear()
            axes[0, 1].imshow(img2)
            #axes[0, 1].set_title('Range-Doppler') 
            axes[0, 1].axis('off')
            #axes[0, 1].set_aspect('equal')
            axes[0, 2].clear()
            axes[0, 2].imshow(img3)
            axes[0, 2].set_title('Channel 1')
            #axes[0, 2].set_title('Range-Doppler') 
            axes[0, 2].axis('off')
            #axes[0, 2].set_aspect('equal')
            axes[0, 3].clear()
            axes[0, 3].imshow(img4)
            #axes[0, 3].set_title('Range-Doppler') 
            axes[0, 3].axis('off')
            #axes[0, 3].set_aspect('equal')
            axes[0, 4].clear()
            axes[0, 4].imshow(img5)
            axes[0, 4].set_title('Channel 2')
            #axes[0, 4].set_title('Range-Doppler') 
            axes[0, 4].axis('off')
            #axes[0, 4].set_aspect('equal')
            axes[0, 5].clear()
            axes[0, 5].imshow(img6)
            #axes[0, 5].set_title('Range-Doppler') 
            axes[0, 5].axis('off')
            #axes[0, 5].set_aspect('equal')

        except:
            print('Could Not Plot Node 0 Images')

         #NODE 1 IMAGES
        direct1=configplot['DIRECTS']['NODE_1_IMG']
        rti01=configplot['IMAGES']['RTI_NODE1_CH0']
        dop01=configplot['IMAGES']['DOP_NODE1_CH0']
        rti11=configplot['IMAGES']['RTI_NODE1_CH1']
        dop11=configplot['IMAGES']['DOP_NODE1_CH1']
        rti21=configplot['IMAGES']['RTI_NODE1_CH2']
        dop21=configplot['IMAGES']['DOP_NODE1_CH2']
        try:
            img7 = io.imread(direct1+rti01)[:, :, :]
            img8 = io.imread(direct1+dop01)[:, :, :]
            img9 = io.imread(direct1+rti11)[:, :, :]
            img10 = io.imread(direct1+dop11)[:, :, :]
            img11 = io.imread(direct1+rti21)[:, :, :]
            img12 = io.imread(direct1+dop21)[:, :, :]
        except:
            print('Missing Images From Directory')

        try:
            axes[1, 0].clear()
            axes[1, 0].imshow(img7) 
           
            axes[1, 0].axis('off') 
            axes[1, 0].annotate('Node 1', xy=(0, 0.5), xytext=(-axes[1, 0].yaxis.labelpad - pad, 0),
                xycoords=axes[1, 0].yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center')
            axes[1, 1].clear()
            axes[1, 1].imshow(img8)
          
            axes[1, 1].axis('off')
            axes[1, 2].clear()
            axes[1, 2].imshow(img9)
            
            axes[1, 2].axis('off')
            axes[1, 3].clear()
            axes[1, 3].imshow(img10)
          
            axes[1, 3].axis('off')
            axes[1, 4].clear()
            axes[1, 4].imshow(img11)
          
            axes[1, 4].axis('off')
            axes[1, 5].clear()
            axes[1, 5].imshow(img12)
           
            axes[1, 5].axis('off')

        except:
            print('Could Not Plot Node 1 Images')

         #NODE 1 IMAGES
        direct2=configplot['DIRECTS']['NODE_2_IMG']
        rti02=configplot['IMAGES']['RTI_NODE2_CH0']
        dop02=configplot['IMAGES']['DOP_NODE2_CH0']
        rti12=configplot['IMAGES']['RTI_NODE2_CH1']
        dop12=configplot['IMAGES']['DOP_NODE2_CH1']
        rti22=configplot['IMAGES']['RTI_NODE2_CH2']
        dop22=configplot['IMAGES']['DOP_NODE2_CH2']
        try:
            img13 = io.imread(direct2+rti02)[:, :, :]
            img14 = io.imread(direct2+dop02)[:, :, :]
            img15 = io.imread(direct2+rti12)[:, :, :]
            img16 = io.imread(direct2+dop12)[:, :, :]
            img17 = io.imread(direct2+rti22)[:, :, :]
            img18 = io.imread(direct2+dop22)[:, :, :]
        except:
            print('Missing Images From Directory')

        try:
            axes[2, 0].clear()
            axes[2, 0].imshow(img13) 
           
            axes[2, 0].axis('off') 
            axes[2, 0].annotate('Node 2', xy=(0, 0.5), xytext=(-axes[2, 0].yaxis.labelpad - pad, 0),
                xycoords=axes[2, 0].yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center')
            axes[2, 1].clear()
            axes[2, 1].imshow(img14)
           
            axes[2, 1].axis('off')
            axes[2, 2].clear()
            axes[2, 2].imshow(img15)
           
            axes[2, 2].axis('off')
            axes[2, 3].clear()
            axes[2, 3].imshow(img16)
            
            axes[2, 3].axis('off')
            axes[2, 4].clear()
            axes[2, 4].imshow(img17)
           
            axes[2, 4].axis('off')
            axes[2, 5].clear()
            axes[2, 5].imshow(img18)
           
            axes[2, 5].axis('off')

        except:
            print('Could Not Plot Node 2 Images')


    except:
        print('Image Not Found')    


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
