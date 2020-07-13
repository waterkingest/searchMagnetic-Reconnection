import os
from spacepy import pycdf
import spacepy.time as spt
import spacepy.coordinates as spc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体,使plot图像可以显示中文
matplotlib.rcParams['axes.unicode_minus'] = False    # 解决保存图像是负号'-'显示为方块的问题
#ax = plt.figure().add_subplot(111,projection='3d')#获取绘制三维图像的类
os.environ["CDF_LIB"] = "D:\CDF\lib"#打开CDF阅读环境
MFI_path = r"D:\CDUT\intership\experiment3\DATA\isee2_4sec_mfi_19780812_v01.cdf"
FPE_path = r"D:\CDUT\intership\experiment3\DATA\isee2_h1_fpe_19780812_v01.cdf"
def readfile():
    MFIdata = pycdf.CDF(MFI_path)
    FPEdata = pycdf.CDF(FPE_path)
    MFI = {
        "EPOCH":MFIdata["Epoch"][:],#获取时间
        "BX":smooth(MFIdata["BX"][:]),      #磁场强度分量
        "BY":smooth(MFIdata["BY"][:]),
        "BZ":smooth(MFIdata["BZ"][:]),
        "BT":smooth(MFIdata["BT"][:])       #磁场总强度
    }
    FPE = {
        "EPOCH":FPEdata["Epoch"][:], #获取时间
        "DEN":smooth(FPEdata["DEN"][:]),     #等离子体密度
        "ENDEN":smooth(FPEdata["ENDEN"][:]), #能量密度
        "TEMP":smooth(FPEdata["T"][:]),      #温度
        "GSEX":FPEdata["GSEX"][:],   #GSE坐标分量
        "GSEY":FPEdata["GSEY"][:],
        "GSEZ":FPEdata["GSEZ"][:],
        "VX":smooth(FPEdata["VX"][:]),       #速度分量
        "VY":smooth(FPEdata["VY"][:])
    }
    print(FPE)
    print(MFI)
    return MFI,FPE
def smooth(interval):
    window_size=5
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')  # numpy的卷积函数

def GSE2GSM_MFI(MFI):
    MFIGSE=np.vstack((MFI["BX"][:],MFI["BY"][:],MFI["BZ"][:]))
    SM = spc.Coords(MFIGSE.T,'GSE','car')
    SM.ticks = spt.Ticktock(MFI["EPOCH"][:],'ISO')
    SM = SM.convert('GSM','car')
    x=SM.data.T[0]
    y=SM.data.T[1]
    z=SM.data.T[2]
    MFI["BX"]=x
    MFI["BY"]=y
    MFI["BZ"]=z
    return MFI
    
def GSE2GSM_FPE(FPE):
    FPEGSE=np.vstack((FPE["GSEX"][:],FPE["GSEY"][:],FPE["GSEZ"][:]))
    SM = spc.Coords(FPEGSE.T,'GSE','car')
    SM.ticks = spt.Ticktock(FPE["EPOCH"][:],'ISO')
    SM = SM.convert('GSM','car')
    x=SM.data.T[0]
    y=SM.data.T[1]
    z=SM.data.T[2]
    FPE["GSEX"]=x
    FPE["GSEY"]=y
    FPE["GSEZ"]=z
    return FPE
def changetime(data):
    Time=np.zeros(len(data["EPOCH"]))
    for i in range(len(data['EPOCH'])):
        Time[i]=data['EPOCH'][i].hour+data['EPOCH'][i].minute/60
    data["EPOCH"]=Time
    return data
def drawB(MFI):
    time=MFI["EPOCH"]
    bx=MFI["BX"]
    by=MFI["BY"]
    bz=MFI["BZ"]
    bt=MFI["BT"]
    l1=0
    l2=0
    r1=0
    for i in time:
        if (i <=24):
            l2+=1
    for j in time:
        if (j<17):
            l1+=1
    for i in time:
        if (i <17):
            r1+=1
    plt.figure()
    plt.subplot(4,1,1)
    #plt.title('磁场总强度的变化')
    plt.plot(time[l1:l2],bt[l1:l2],label='磁场强度')
    plt.hlines(0,17,24,colors = "r", linestyles = "dashed")
    #plt.plot(time[r1:],bt[r1:],'royalblue')
    #print(time[l1:l2])
    plt.legend()
    plt.grid()
    #plt.scatter(time[l1:l2],bt[l1:l2],s=5,c='r',marker='*',alpha=1)
    # plt.xlim(5,10)
    #plt.xlabel('TIME')
    plt.ylabel('BT')
    #plt.figure()
    plt.subplot(4,1,2)
    #plt.title('磁场X分量变化')
    #plt.scatter(time[l1:l2],bx[l1:l2],s=5,c='r',marker='*',alpha=1)
    plt.plot(time[l1:l2],bx[l1:l2],label='BX')
    plt.hlines(0,17,24,colors = "r", linestyles = "dashed")
    #plt.plot(time[r1:],bx[r1:],'royalblue')
    # plt.xlim(5,10)
    plt.legend()
    plt.grid()
    plt.ylabel('BX')
    #plt.xlabel('TIME')
    #plt.figure()
    plt.subplot(4,1,3)
    #plt.title('磁场y分量变化')
    #plt.scatter(time[l1:l2],by[l1:l2],s=5,c='r',marker='*',alpha=1)
    plt.hlines(0,17,24,colors = "r", linestyles = "dashed")
    plt.plot(time[l1:l2],by[l1:l2],label='BY')
    #plt.plot(time[r1:],by[r1:],'b')
    # # plt.xlim(5,10)
    plt.ylabel('BY_GSM')
    plt.legend()
    plt.grid()
    #plt.xlabel('TIME')
    #plt.figure()
    plt.subplot(4,1,4)
    #plt.title('磁场z分量变化')
    #plt.scatter(time[l1:l2],bz[l1:l2],s=5,c='r',marker='*',alpha=1)
    plt.plot(time[l1:l2],bz[l1:l2],label='BZ')
    # plt.plot(time[r1:],bz[r1:],'b')
    # # plt.xlim(5,10)
    plt.xlabel('TIME')
    plt.ylabel('BZ_GSM')
    plt.hlines(0,17,24,colors = "r", linestyles = "dashed")
    plt.legend()
    plt.grid()
    plt.show()
def drawptoton(FPE):
    time=FPE["EPOCH"]
    vx=FPE["VX"]
    vy=FPE["VY"]
    den=FPE["DEN"]
    enden=FPE["ENDEN"]
    temp=FPE["TEMP"]
    l1=0
    l2=0
    r1=0
    for i in time:
        if (i <10):
            l2+=1
    for j in time:
        if (j<4):
            l1+=1
    for i in time:
        if (i <17):
            r1+=1
    # plt.figure()
    # plt.plot(vx[l1:l2],vy[l1:l2])
    # plt.show()
    #plt.subplot(5,1,1)
    plt.title('温度变化')
    plt.scatter(time,temp,s=5,c='r',marker='*',alpha=1)
    plt.plot(time,temp,'b',label='温度')
    plt.ylabel('TEMP')
    plt.legend()
    plt.grid()
    plt.xlabel('TIME')
    plt.figure()
    # plt.subplot(4,1,1)
    plt.title('X方向速度变化')
    plt.scatter(time,vx,s=5,c='r',marker='*',alpha=1)
    plt.plot(time,vx,'b',label='VX')
    plt.ylabel('VX')
    plt.legend()
    plt.grid()
    plt.xlabel('TIME')
    plt.figure()
    # plt.subplot(4,1,2)
    plt.title('Y方向速度变化')
    plt.scatter(time,vy,s=5,c='r',marker='*',alpha=1)
    plt.plot(time,vy,'b',label='VY')
    plt.ylabel('VY')
    plt.legend()
    plt.grid()
    plt.xlabel('TIME')
    plt.figure()
    #plt.subplot(5,1,4)
    plt.title('质子浓度变化')
    plt.scatter(time,den,s=5,c='r',marker='*',alpha=1)
    plt.plot(time,den,'b',label='质子密度')
    plt.ylabel('DEN')
    plt.legend()
    plt.grid()
    plt.xlabel('TIME')
    plt.figure()
    #plt.subplot(3,1,3)
    plt.title('能量密度变化')
    plt.scatter(time,enden,s=1,c='r',marker='*',alpha=1)
    plt.plot(time,enden,'r',label='能量密度')
    plt.ylabel('ENDEN')
    plt.xlabel('TIME')
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    MFI,FPE=readfile()
    #MFIsametime=searchSameTime_(FPE,MFI)
    MFI_GSM=GSE2GSM_MFI(MFI)
    # FPE_GSM=GSE2GSM_FPE(FPE)
    MFI_CT=changetime(MFI_GSM)
    # FPE_CT=changetime(FPE_GSM)
    # drawptoton(FPE_CT)
    drawB(MFI_CT)