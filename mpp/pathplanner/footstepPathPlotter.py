import sys,os
sys.path.append(os.environ["MPP_PATH"]+"mpp-path-planner/mpp")
sys.path.append(os.environ["MPP_PATH"]+"mpp-robot/mpp")
sys.path.append(os.environ["MPP_PATH"]+"mpp-mathtools/mpp")
sys.path.append(os.environ["MPP_PATH"]+"mpp-environment/mpp")

import numpy as np
import cvxpy as cvx
import pickle
import networkx as nx
from mathtools.plotter import Plotter,rotFromRPY
from numpy import inf,array,zeros
from cvxpy import *
from math import tan,pi
from mathtools.util import *
from mathtools.linalg import *
from mathtools.timer import *
from mathtools.walkable import WalkableSurface, WalkableSurfacesFromPolytopes
from robot.htoq import *
from robot.robotspecifications import * 
from pathplanner.connectorsGetMiddlePath import * 
from pathplanner.connectorComputeNormal import * 
from pathplanner.surfaceMiddlePath import * 
from environment.fileparser import fileToPolytopes


def footstepPathPlotter(env_fname, K = inf, plotscene=True ):
        env_folder = os.environ["MPP_PATH"]+"mpp-environment/output"
        Wsurfaces = pickle.load( open( env_folder+"/wsurfaces.dat", "rb" ) )

        pobjects = fileToPolytopes(env_fname)
        wplot=Plotter()
        if plotscene:
                wplot.allPolytopes(pobjects)

        wplot.allWalkableSurfaces(Wsurfaces)

        ctr=0
        fname = env_folder+"/footsteppath"+str(ctr)+".dat"
        colors="kgmb"
        while os.path.exists(fname) and ctr<K:
                print "Plotting path in homotopy class",ctr
                pts=pickle.load( open( fname, "rb") )
                if len(pts)>0:
                        X=pts[:,0]
                        Y=pts[:,1]
                        Z=pts[:,2]
                        X=np.squeeze(X)
                        Y=np.squeeze(Y)
                        Z=np.squeeze(Z)
                        #wplot.ax.scatter(X,Y,Z,marker='o',c='r',s=5)
                        wplot.ax.plot3D(X,Y,Z,'-ok',color=colors[ctr%len(colors)],linewidth=3,markersize=5,zorder=100)

                ctr+=1
                fname = env_folder+"/footsteppath"+str(ctr)+".dat"


        #wplot.set_view(-90,90)
        wplot.set_view(40,40)

        wplot.show()

if __name__ == "__main__":
        #env_fname = os.environ["MPP_PATH"]+"mpp-environment/urdf/staircase_stones.urdf"
        #env_fname = os.environ["MPP_PATH"]+"mpp-environment/urdf/quatro_homotopy.urdf"
        env_fname = os.environ["MPP_PATH"]+"mpp-environment/urdf/wall.urdf"
        footstepPathPlotter(env_fname,1)
