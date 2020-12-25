import numpy as np
import random as r
def find_holes(ind,dir1):
    dir2=np.zeros_like(dir1)
    iv=1
    k=np.array([[0,1],[2,3]],int)
    for i in range(dir1.shape[0]):
        for j in range(dir1.shape[1]):
            if ind[i,j]==0:
                dir2[i:i+2,j:j+2]=iv+k
                iv+=4
    return dir2
def fill_holes(ind,dir1,mind=None):
    if mind is None:
        mind=ind.max()+1
    #dir2=np.zeros_like(dir1)

    for i in range(dir1.shape[0]):
        for j in range(dir1.shape[1]):
            if ind[i,j]==0:
                if r.random()<.5:
                    
                    dir1[i,j:j+2]=2
                    ind[i,j:j+2]=mind
                    dir1[i+1,j:j+2]=3
                    ind[i+1,j:j+2]=mind+1
                else:
                    dir1[i:i+2,j]=0
                    ind[i:i+2,j]=mind
                    dir1[i:i+2,j+1]=1
                    ind[i:i+2,j+1]=mind+1
                mind+=2
            
   
    return ind,dir1,mind
def get_b(s,bk=-1,fg=0):
    s2=s//2
    a=np.full([s,s],bk,int)
    for i in range(s):
        j=min(i,s-i-1)+1
        print(s2-j,s2+j)
        a[s2-j:s2+j,i]=fg
    return a
def expand(ind,dir1):
    
    q=np.array([[1,0],[1,2],[0,1],[2,1]],int)
    dir2=get_b(ind.shape[0]+2)
    ind2=dir2.copy()
    for i in range(dir1.shape[0]):
        for j in range(dir1.shape[1]):
            if ind[i,j]>0:
                k=tuple(q[dir1[i,j]]+[i,j])
                dir2[k]=dir1[i,j]
                ind2[k]=ind[i,j]
    return ind2,dir2
def collide(ind,dir1):
    
    q=np.array([[1,0],[1,2],[0,1],[2,1]],int)-1
    
    l=ind.shape[1]
    for i in range(dir1.shape[0]):
        for j in range(dir1.shape[1]):
            if ind[i,j]>0:
                k=tuple(q[dir1[i,j]]+[i,j])
                if  0<=k[0]<l and 0<=k[1]<l:
                    if ind[k]>0 and dir1[k]^dir1[i,j]==1:
                        dir1[k]=dir1[i,j]=0
                    
                        ind[k]=ind[i,j]=0
    return ind,dir1

import matplotlib.pyplot as plt
ind=np.zeros([2,2],int)
dir1=np.zeros([2,2],int)
mind=1
import imageio
ar=(imageio.imread("arrow2.png")>0).astype(np.uint8)
imgsz=ar.shape[0]
arrows=[ ar.swapaxes(0,1),ar.swapaxes(0,1)[:,::-1,...],ar,ar[::-1,...]]
arrows=[i*np.array([[j]]) for i,j in zip(arrows,[[128,128,255],[128,255,128],[255,255,128],[255,128,128]])]
#for i in arrows:
#    plt.imshow(i)
#    plt.show()
def render_offset(ind,dir1,ofs):
    k=np.zeros_like(ind)
    l=dir1.shape[1]+2
    vv=get_b(l,0,128).astype(np.uint8)
    
    v=np.zeros([imgsz*l,imgsz*l,3],np.uint8)
    for i in range(l):
        for j in range(l):
            if vv[i,j]>0:
                v[i*imgsz:(i+1)*imgsz,j*imgsz:(j+1)*imgsz]=128
    q=np.array([[1,0],[1,2],[0,1],[2,1]],int)-1
    for i in range(dir1.shape[0]):
        for j in range(dir1.shape[1]):
            if ind[i,j]>0 and k[i,j]==0:
                x=2 if dir1[i,j]<2 else 1
                y=3-x
                ox,oy=[imgsz+pp*ofs for pp in q[dir1[i,j]]]
                v[i*imgsz+ox:(i+x)*imgsz+ox,j*imgsz+oy:(j+y)*imgsz+oy]=arrows[dir1[i,j]]
                k[i:i+x,j:j+y]=1
            #elif ind[i,j]==0:
            #    v[i*imgsz:(i+1)*imgsz,j*imgsz:(j+1)*imgsz]=128
        
    return v
def render(ind,dir1):
    k=np.zeros_like(ind)
    l=dir1.shape[1]
    v=np.zeros([imgsz*l,imgsz*l,3],np.uint8)
    for i in range(dir1.shape[0]):
        for j in range(dir1.shape[1]):
            if ind[i,j]>0 and k[i,j]==0:
                x=2 if dir1[i,j]<2 else 1
                y=3-x
                v[i*imgsz:(i+x)*imgsz,j*imgsz:(j+y)*imgsz]=arrows[dir1[i,j]]
                k[i:i+x,j:j+y]=1
            elif ind[i,j]==0:
                v[i*imgsz:(i+1)*imgsz,j*imgsz:(j+1)*imgsz]=128
        
    return v
def render_boxes(ind,dir1):
    v=render(ind,dir1)
    k=np.zeros_like(ind)
    l=dir1.shape[1]
    
    for i in range(dir1.shape[0]):
        for j in range(dir1.shape[1]):
            
            if ind[i,j]==0 and k[i,j]==0:
                q=v[i*imgsz:(i+2)*imgsz,j*imgsz:(j+2)*imgsz]
                q[:]=0
                d=4
                q[d:-d,d:-d]=(255,186,128)
                k[i:i+2,j:j+2]=1
           
        
    return v
def p(x):
    plt.imshow(x)
    plt.show()
for i in range(10):
    
    p(render_boxes(ind,dir1))

    ind,dir1,mind=fill_holes(ind,dir1,mind)
    p(render(ind,dir1))

    ind,dir1=collide(ind,dir1)
    p(render(ind,dir1))

    p(render_offset(ind,dir1,imgsz//3))
    p(render_offset(ind,dir1,imgsz*2//3))
    ind,dir1=expand(ind,dir1)
    p(render(ind,dir1))
