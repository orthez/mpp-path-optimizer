import sys,os
sys.path.append(os.environ["MPP_PATH"]+"mpp-robot/mpp")
sys.path.append(os.environ["MPP_PATH"]+"mpp-mathtools/mpp")
import pickle
from math import acos
from mathtools.plotter import Plotter,rotFromRPY
import numpy as np
from scipy.interpolate import interp1d
from robot.robotspecifications import *
from pylab import *
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

def getAngleAtCtr(xnew, f, ctr):
        xx = np.array((1,0))
        if ctr<len(xnew)-1:
                vc = np.array((xnew[ctr],f(xnew[ctr])))
                vn = np.array((xnew[ctr+1],f(xnew[ctr+1])))
        else:
                vc = np.array((xnew[ctr],f(xnew[ctr])))
                vn = np.array((xnew[ctr-1],f(xnew[ctr-1])))

        an = np.dot(rotFromRPY(0,0,pi/2)[:2,:2],vn-vc)
        an = an/np.linalg.norm(an)
        angle= acos(np.dot(an,xx))
        return angle


output_folder = os.environ["MPP_PATH"]+"mpp-path-planner/output/homotopy"+str(FINAL_HOMOTOPY)+"/minima"+str(FINAL_MINIMA)
svFootFname = output_folder+"/xpathFoot.dat"

##fpath contains the pos vector and ori vector, both from origin
fPath = pickle.load( open( svFootFname, "rb" ) )

#print np.around(fPath,2)
#sys.exit(0)
fig=figure(1)
ax = fig.gca()

### DEBUG
fPath = fPath[3:,:]
for i in range(0,len(fPath[:,0])):
        y = fPath[i,1]
        if np.linalg.norm(y)<1:
                d = 0.002*y
                fPath[i,0]-=d

f = interp1d(fPath[:,0],fPath[:,1], kind='linear')
xl = min(fPath[:,0])
xu = max(fPath[:,0])

xnew = np.linspace(min(fPath[:,0]), max(fPath[:,0]), 10000)

print np.around(fPath,2)
plot(fPath[:,0], fPath[:,1], 'ok')
plot(xnew, f(xnew))

plt.show()
sys.exit(0)

tstart = getAngleAtCtr(xnew, f, 0)
leftFoot = np.array((xnew[0],f(xnew[0]),0.0,tstart))
relFootArray = leftFoot
plot(xnew[0],f(xnew[0]),'ok')

ctr=0
leftFootArray=np.zeros((0,4))
rightFootArray=np.zeros((0,4))
zcomponent=0.0

ctr=0


while ctr<len(xnew)-1:
        d=0.0
        ctrstart = ctr
        ##absolute position of left foot
        
        vsupport = np.array((xnew[ctr],f(xnew[ctr])))
        dd = FOOTSTEP_INITIAL_DISTANCE

        while dd<FOOTSTEP_MAX_STEP+FOOTSTEP_INITIAL_DISTANCE and \
                        ctr<len(xnew)-1:
                ctr=ctr+1
                vc = np.array((xnew[ctr],f(xnew[ctr])))
                #vn = np.array((xnew[ctr+1],f(xnew[ctr+1])))
                dd = np.linalg.norm(vsupport-vc)

        print "dist L-R:",ctr,dd

        angle = getAngleAtCtr(xnew, f, ctr)
        rightFoot = np.array((xnew[ctr],f(xnew[ctr]),zcomponent,angle))
        rightFootArray = np.vstack([rightFootArray,rightFoot])
        rfr = rightFoot - leftFoot

        relFootArray=np.vstack([relFootArray,rfr])


        vsupport = np.array((xnew[ctr],f(xnew[ctr])))
        vleft = np.array((xnew[ctrstart],f(xnew[ctrstart])))

        ctr=ctrstart

        dd = np.linalg.norm(vsupport-vleft)

        while dd>FOOTSTEP_INITIAL_DISTANCE and ctr<len(xnew)-1:
                ctr=ctr+1
                vc = np.array((xnew[ctr],f(xnew[ctr])))
                dd = np.linalg.norm(vsupport-vc)

        angle = getAngleAtCtr(xnew, f, ctr)
        leftFoot = np.array((xnew[ctr],f(xnew[ctr]),zcomponent,angle))
        leftFootArray = np.vstack([leftFootArray,leftFoot])
        lfr = leftFoot - rightFoot
        relFootArray=np.vstack([relFootArray,lfr])

        dlr = np.linalg.norm(leftFoot[0:2]-rightFoot[0:2])
        print "dist L-R:",ctr,dlr

        ctr=ctr+1
        if dlr < FOOTSTEP_MIN_DISTANCE:
                break

        vv=np.dot(rotFromRPY(0,0,rightFoot[3])[:2,:2],np.array((1,0)))
        plot([rightFoot[0],rightFoot[0]+vv[0]],[rightFoot[1],rightFoot[1]+vv[1]],'-ok')

        vvl=np.dot(rotFromRPY(0,0,leftFoot[3])[:2,:2],np.array((1,0)))
        plot([leftFoot[0],leftFoot[0]+vvl[0]],[leftFoot[1],leftFoot[1]+vvl[1]],'-ok')
        plot(rightFoot[0],rightFoot[1],'or')
        plot(leftFoot[0],leftFoot[1],'ob')

plt.show()
f = open('rel-foot-path.txt', 'w')
relFootArray=np.around(relFootArray,2)
for i in range(0,len(relFootArray)):
        rr = relFootArray[i,:]
        rstr = str(rr[0])+" "+str(rr[1])+" "+str(rr[2])+" "+str(rr[3])+"\n"
        f.write(rstr)
f.close()





