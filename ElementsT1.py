# -*- coding: utf-8 -*-
#
# "CHANGES" library 
#
#  brings chinese philosophy to life
#
# (C) Ivan Makarov, 2015-2016
# Email: ivmakarov@yahoo.com
#
from __future__ import division
#from __future__ import unicode_literals # do not use !!!
import dill
import os
import time
from datetime import datetime
import networkx as nx
import numpy as np
#import pylab
import matplotlib.pyplot as plt
#import rpy2.robjects as robjects
import random
import codecs
from matplotlib.font_manager import FontProperties


homedir = os.environ['HOME']
libdir ='/Changesv001'
#ChineseFont2 = FontProperties(fname='/usr/share/fonts/truetype/wp010-05.ttf')

# for Linux and  Mac Os X :
WorkingDirectory = homedir+libdir
# for Windows :
#WorkingDirectory = r"C:\Changesv001\"

# for Linux and  Mac Os X :
SetsDirectory =  homedir+libdir
# for Windows :
#SetsDirectory = r"C:\Changesv001\"

# for Linux and  Mac Os X :
ChImagesDirectory =  homedir+libdir+'/images/channels/'
# for Windows :
#ChImagesDirectory = r"C:\Changesv001\images\channels\"

# for Linux and  Mac Os X :
PImagesDirectory =  homedir+libdir+'/images/points/'
# for Windows :
#PImagesDirectory = r"C:\Changesv001\images\points\"

#Default Set names definition for Linux/Mac Os and Win
#these sets would be loaded as default sets.

#Linux/Mac Os X

taijiLName = SetsDirectory+"/taiji5"

liangyiLName = SetsDirectory+"/liangyi5"

sixiangLName = SetsDirectory+"/sixiang5"

baguaLName = SetsDirectory+"/baguaQ9R"

HextableLName  = SetsDirectory+"/hextable27R"

wuxingLName = SetsDirectory+'/wuxing2'

stemsLName = SetsDirectory+'/stems3'

branchesLName = SetsDirectory+'/branches3'

channelsLName = SetsDirectory+'/channels4'

pointsLName = SetsDirectory+'/points4'

#Win path+name

taijiWName = r"C:\Changesv001\taiji5"

liangyiWName = r"C:\Changesv001\liangyi5"

sixiangWName = r"C:\Changesv001\sixiang5"

baguaWName = r"C:\Changesv001\baguaQ9R"

HextableWName  = r"C:\Changesv001\hextable27R"

wuxingWName = r"C:\Changesv001\wuxing2"

stemsWName = r"C:\Changesv001\stems3"

branchesWName = r"C:\Changesv001\branches3"

channelsWName = r"C:\Changesv001\channels4"

pointsWName = r"C:\Changesv001\points4"




def save_to_file(obj, filename):
    """saves obj to file"""
    with open(filename, 'wb') as f:
            dill.dump(obj, f)
            
def load_from_file(filename):
    """loads obj from file"""
    with open(filename, 'rb') as f:
            obj = dill.load(f)
    return obj



class ElProperty(object):
    """describes Property of the Element"""
   
    def __init__(self, PrName, PrValue=None, PrRel=None):
        self.PrName = PrName
        self.PrValue = PrValue
        self.PrRel = PrRel
        
        
class ElOwnProperty(object):
   
    def __init__(self, ElOwnName, ElOwnRel=None, ElOwnValue=None):
        self.ElOwnName = ElOwnName
        self.ElOwnRel = ElOwnRel
        self.ElOwnValue = ElOwnValue
        

        
class ElGroup(object):
    
    def __init__(self, ElGrName, ElGrValue=None, ElGrPos=None):
        self.ElGrName = ElGrName
        self.ElGrValue = ElGrValue
        self.ElGrPos = ElGrPos
        
        
class ElRelationship(object):
    
    def __init__(self, ElRelName, ElRelPos=None, ElRelValue=None):
        self.ElRelName = ElRelName
        self.ElRelPos = ElRelPos
        self.ElRelValue = ElRelValue
        self.Follows = None
        self.Precedes = None
        
class EChRelationship(object):
    
    def __init__(self, ElChName, ElChPos=None, ElChFrom=None, ElChTo=None):
        self.ElChName = ElChName
        self.ElChPos = ElChPos
        self.ElChFrom = ElChFrom
        self.ElChTo = ElChTo
        self.Follows = None
        self.Precedes = None
        
class pointEn(object):
    
    def __init__(self,pName,pNameSN=None):
        self.pName = pName
        self.pNameSN = pNameSN
        
class pointFr(object):
    
    def __init__(self,pName,pNameSN=None):
        self.pName = pName
        self.pNameSN = pNameSN
        



class Link(object):  
    """Describes a link between elements""" 
    
    def __init__(self, El1,El2, Directed=None, N=None, lname = None, lcolor = None): 
        """inits link if directed from 1 to 2"""
        self.El1 = El1
        self.El2 = El2
        self.Directed = Directed
        self.N = N
        self.lname = lname
        self.value = None
        self.ChName = None
        self.ChValue = None
        self.lcolor = lcolor
        
class Relationship(object):
    """Describes relationship in the group Name and boolean Directed are requied!"""
    
    def __init__(self, Name, Directed, Rtype=None, NofElements=None):
        """Inits relationship"""
        
        self.elements = {}      #  elements[Name] --> e
        self.numbers = {}       #  numbers[Name] --> N
        self.nnames ={}         #  nname[N] --> Name
        self.Ncounter = 0
        
        self.links = {}         #  links[Name] --> link
        self.lnumbers = {}      #  lnumbers[Name] --> N
        self.lnnames = {}       #  lnnames[N] --> Name
        self.Lcounter = 0
        
        self.labels = {}
        
        self.Name = Name
        self.Directed = Directed
        self.NofElements = NofElements
        self.NofLinks = None
        self.Rtype = Rtype
        
    def Rel_SetElements(self, NameofElGroup, label=None):
        """Add all elements from the group NameofElGroup to relationship"""
        self.NameofElementsGroup = NameofElGroup
        for e in NameofElGroup.elements:
            self.Ncounter = self.Ncounter +1
            N = self.Ncounter
            Name = NameofElGroup.elements[e].Name
            self.elements[e] =  NameofElGroup.elements[e]
            self.numbers[Name] = N
            self.nnames[N] = Name
            if label is not None :
                self.labels[e] = NameofElGroup.elements[e].label.decode('utf-8')
            
            
    def Rel_AddElement(self, NameofElGroup, ElName):
        """Add one element from the group NameofElGroup to relationship """
        self.Ncounter = self.Ncounter +1
        N = self.Ncounter
        e = NameofElGroup.elements[ElName]
        self.elements[ElName] = e
        self.numbers[ElName] = N
        self.nnames[N] = ElName
        
    def Rel_AddNElement(self, NameofElGroup, N, ElName):
        """Add one element and assign number N from the group NameofElGroup to relationship """
        self.Ncounter = self.Ncounter +1
        e = NameofElGroup.elements[ElName]
        self.elements[ElName] = e
        self.numbers[ElName] = N
        self.nnames[N] = ElName
        
     
    def Rel_DelElement(self, ElName):
        """Delete one element"""
        self.elements.pop(ElName,None)
        N = self.numbers[ElName]
        self.numbers[ElName].pop
        self.nnames[N].pop
        self.Ncounter = self.Ncounter -1
        
    def Rel_DelNElement(self, N):
        """Delete one element"""
        ElName = self.nnames[N]
        self.elements.pop(ElName,None)
        self.numbers[ElName].pop
        self.nnames[N].pop
        self.Ncounter = self.Ncounter -1
        
        
    def Rel_SetLink(self, El1, El2, Directed=None, lname = None, lcolor = None):
        """Set Link"""
        self.Lcounter = self.Lcounter + 1
        l = Link(El1, El2, Directed, self.Lcounter, lname, lcolor)
        s = str(El1)+' '+str(El2)
        self.links[s] = l
        N1 = self.numbers[El1]
        N2 = self.numbers[El2]
        sn = str(N1) + " " +str(N2)
        self.lnumbers[s] = sn
        self.lnnames[sn] = s
        
    def Rel_SetNNLink(self, N1, N2, Directed=None, lname = None, lcolor = None):
        """Set Link between N1 and N2 elements"""
        self.Lcounter = self.Lcounter + 1
        El1 = self.nnames[N1]
        El2 = self.nnames[N2]
        l = Link(El1, El2, Directed, self.Lcounter, lname, lcolor)
        s = str(El1)+' '+str(El2)
        self.links[s] = l
        sn = str(N1) + " " +str(N2)
        self.lnumbers[s] = sn
        self.lnnames[sn] = s
        
    def Rel_DelLink(self, El1, El2):
        """Deletes link"""
        s = str(El1)+' '+str(El2)
        sn = self.lnumbers[s]
        self.links.pop(s,None)
        self.lnnames.pop(sn,None)
        self.lnumbers.pop(s,None)
        self.Lcounter = self.Lcounter - 1
        
    def Rel_DelNNLink(self, N1, N2):
        """Deletes link between N1 and N2 """
        El1 = self.nnames[N1]
        El2 = self.nnames[N2]
        s = str(El1)+' '+str(El2)
        sn = self.lnumbers[s]
        self.links.pop(s,None)
        self.lnnames.pop(sn,None)
        self.lnumbers.pop(s,None)
        self.Lcounter = self.Lcounter - 1
        
    
                
            
class RELationships(object):
    """Array for Relationships"""
    
    def __init__(self):
        """Defines the Array"""
        self.Relatioships ={}
        self.Graphs = {}
        
    def add(self, Name, Directed, Rtype=None, NofElements=None):
        """Adds Relationship Name and Directed( 1 or 0, True of False)"""
        r = Relationship(Name, Directed, Rtype, NofElements)
        self.Relatioships[Name] = r
        if self.Relatioships[Name].Directed :
            G = nx.DiGraph()
        else : G = nx.Graph()
        self.Graphs[Name] =  G
        
    def add_GroupEl(self, RName, GRElName):
        """Adds a group of elements syntax: add_GroupEl("RName",GRElName) """
        self.Relatioships[RName].Rel_SetElements(GRElName)
        for e in GRElName.elements:
            self.Graphs[RName].add_node(GRElName.elements[e].Name)
        
        
    def add_El(self, RName, GRElName, El):
        """Adds an element to the relationship"""
        self.Relatioships[RName].Rel_AddElement(GRElName, El)
        self.Graphs[RName].add_node(GRElName.elements[El].Name)
        
    def add_NEl(self,  RName, GRElName, N, El):
        """Adds an element to the relationship under N"""
        self.Relatioships[RName].Rel_AddNElement(GRElName, N, El)
        self.Graphs[RName].add_node(GRElName.elements[El].Name)
        
    def del_El(self, RName, El):
        """Deletes an element """
        self.Relatioships[RName].Rel_DelElement(El)
        self.Graphs[RName].remove_node(self.Relatioships[RName].elements[El].Name)
        
    def del_NEl(self,RName, N):
        """Deletes an element N"""
        ElName = self.Relatioships[RName].nnames[N]
        self.Graphs[RName].remove_node(self.Relatioships[RName].elements[ElName].Name)
        self.Relatioships[RName].Rel_DelNElement(N)
        
    def add_Link(self, RName, El1, El2, Directed=None, lname = None, lcolor = None):
        """Set link between element"""
        self.Relatioships[RName].Rel_SetLink(El1, El2, Directed, lname, lcolor)
        self.Graphs[RName].add_edge(El1, El2 )
        
    def add_NNLink(self, RName, N1, N2, Directed=None, lname = None, lcolor = None ):
        """Set link between N1 N2 elements"""
        El1 = self.Relatioships[RName].nnames[N1]
        El2 = self.Relatioships[RName].nnames[N2]
        self.Relatioships[RName].Rel_SetNNLink(N1,N2,Directed, lname, lcolor)
        self.Graphs[RName].add_edge(El1, El2 )
        
        
    def del_Link(self, RName, El1, El2):
        """Deletes the link"""
        self.Relatioships[RName].Rel_DelLink(El1, El2)
        self.Graphs[RName].remove_edge(El1,El2)
        
    def del_NNLink(self, RName, N1, N2):
        """Deletes the link N1 N2"""
        El1 = self.Relatioships[RName].nnames[N1]
        El2 = self.Relatioships[RName].nnames[N2]
        self.Relatioships[RName].Rel_DelNNLink(N1,N2)
        self.Graphs[RName].remove_edge(El1,El2)
        
    def circ_1toNLink(self, RName, N1,N2,Directed = None, lname = None, lcolor = None):
        """Set circular links between first N1 to last N2 elements"""
        for i in range(N1,N2):
            self.add_NNLink(RName, i, i+1, Directed, lname = None, lcolor = None)
        self.add_NNLink(RName, N2, N1, Directed, lname = None, lcolor = None)    #circle it
    
    
    
        
    def polar_plot_El(self,ax,RelName,Name,cc,d,Si,N=None,n=None,ecolor=None):
        """plots an element in polar plot"""
        w=np.pi/(2*N)
        
        #cc = np.pi - np.pi*(n-1)/N

        kr = range(1,7)
 
        q1 = cc +w 
        q2 = cc -w 
        
        self.Relatioships[RelName].elements[Name].polar = 1
        self.Relatioships[RelName].elements[Name].ang = cc
        self.Relatioships[RelName].elements[Name].rc = d
        if ecolor is not None :
            self.Relatioships[RelName].elements[Name].ecolor = ecolor
        else:
            self.Relatioships[RelName].elements[Name].ecolor = 'k'
            ecolor = 'k'
        
        l={}
        if self.Relatioships[RelName].elements[Name].Y1 is not None :
            l[1] = self.Relatioships[RelName].elements[Name].Y1
        else : l[1] = -1
        if self.Relatioships[RelName].elements[Name].Y2 is not None :
            l[2] = self.Relatioships[RelName].elements[Name].Y2
        else : l[2] = -1
        if self.Relatioships[RelName].elements[Name].Y3 is not None :
            l[3] = self.Relatioships[RelName].elements[Name].Y3
        else : l[3] = -1
        if self.Relatioships[RelName].elements[Name].Y4 is not None :
            l[4] = self.Relatioships[RelName].elements[Name].Y4
        else : l[4] = -1
        if self.Relatioships[RelName].elements[Name].Y5 is not None :
            l[5] = self.Relatioships[RelName].elements[Name].Y5
        else : l[5] = -1
        if self.Relatioships[RelName].elements[Name].Y6 is not None :
            l[6] = self.Relatioships[RelName].elements[Name].Y6
        else : l[6] = -1
        
 
        for k in kr :
            dr = d +k*Si
            q1 = cc +w  #-Si*np.sin(cc-w)*k/6
            q2 = cc -w  #+Si*np.sin(cc-w)*k/6
            if l[k] != -1 :
                if l[k] == 1:
                      ax.plot([q1,q2],[dr,dr],color=ecolor,lw=4)
                else : 
                    
                    q3 = cc +w/12
                    q4 = cc -w/12
                    ax.plot([q1,q2],[dr,dr],color=ecolor,lw=4)
                    ax.plot([q3,q4],[dr,dr],color='w',lw=12)
                    
            #print k
            #print dr
            #print q1
            #print q2

        ax.plot([q1,q2],[dr+dr*0.3,dr+dr*0.3],color='w',lw=4)
        
        s = self.Relatioships[RelName].elements[Name].Name
        sch = self.Relatioships[RelName].elements[Name].ChName
    
        ax.text(cc, dr+dr*0.3*np.sin(cc/2)*np.sign(np.sin(cc/2)), str(Name),size=18)
        #ax.text(cc, dr+dr*0.3*np.sin(cc/2)*np.sign(np.sin(cc/2)),  sch ,size= 20, fontproperties = ChineseFont2)
        
        plt.draw()
        
    def polar_plot_NEl(self, ax,RelName,Number,cc,d,Si,N=None,n=None,ecolor=None ):
        """plots  Number element in polar plot"""
        Name = self.Relatioships[RelName].nnames[Number]
        self.polar_plot_El(ax, RelName, Name, cc, d, Si, N, n,ecolor)
        
        
    def polar_plot_arrow(self,ax,q1,q2,r1,r2,dir=None, lcolor = None):
        """plots arrow"""
        if lcolor == None :
            lcolor = 'k'
       
        ax.plot([q1,q2],[r1,r2],color=lcolor,lw=2)
        if dir  == None :
            dir =1 #arrows direction

        if dir == 1:
            
            ah1 = q2 + dir*np.abs(q2-q1)/10
            adr1 = r2 #+ dr/30

            ah2 = q2 + dir*np.abs(q2-q1)/10
            adr2 = r2

            ax.plot([ah1,q2],[adr1,r2],color=lcolor,lw=3)
            #ax.plot([ah2,q2],[adr2,dr],color='k',lw=2)
        elif dir == -1 :
            ah1 = q1 + dir*np.abs(q2-q1)/10
            adr1 = r1 #+ dr/30

            ah2 = q1 + dir*np.abs(q2-q1)/10
            adr2 = r1

            ax.plot([ah1,q1],[adr1,r1],color=lcolor,lw=3)
            #ax.plot([ah2,q2],[adr2,dr],color='k',lw=2)
        
    def polar_plot_Link(self,ax, RelName, Name1, Name2, dir = None, lname = None, lcolor = None):
        """plots a link (arrow) between elements Name1, Name2 (only directed now) """
        k = 0.95 #reduction of the radius for arrow start/end point
        if self.Relatioships[RelName].elements[Name1].polar == 1 :
            ang1 = self.Relatioships[RelName].elements[Name1].ang
            rc1 = self.Relatioships[RelName].elements[Name1].rc
        if self.Relatioships[RelName].elements[Name2].polar == 1 :
            ang2 = self.Relatioships[RelName].elements[Name2].ang
            rc2 = self.Relatioships[RelName].elements[Name2].rc
        if dir == 1 :
            self.polar_plot_arrow(ax,ang1,ang2,k*rc1,k*rc2,1,lcolor)
            
    def polar_plot_NNLink(self, ax, RelName, N1, N2, dir = None, lname = None, lcolor = None):
        """plots a link (arrow) between elements N1, N2 (only directed now) """
        Name1 = self.Relatioships[RelName].nnames[N1]
        Name2 = self.Relatioships[RelName].nnames[N2]
        self.polar_plot_Link(ax, RelName, Name1, Name2, dir, lname, lcolor)
            
    def polar_plot_NSEW(self,ax,rc,tcolor=None):
        """plots Nord Sud East West"""
        d=np.pi/32 #position correction
        dr = rc/8
        ax.text(np.pi/2+d, rc, 'S',size=20,color=tcolor)
        ax.text(-np.pi/2-d, rc+dr, 'N',size=20,color=tcolor)
        ax.text(np.pi+d, rc+dr, 'E',size=20,color=tcolor)
        ax.text(0-d, rc-dr, 'W',size=20,color=tcolor)
        
            
        
            
    
    def plot_circular(self, RelName, StartPoint,Direct,N, lname = None, lcolor = None, ecolor = None):
        """plots a circular relationship RelName from StartPoint in format np.pi,
        in direction Direct ( 1 or -1 ) total elements N.
        requied to have numbered elements from 1 to N (use add_NEl function ) """
        ax = plt.subplot(111, polar=True)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        
        rc = 4      #radius for element start
        rca = 3.8   #radius for arrow start/end
        w = 0.25    # line 
        
        self.polar_plot_NSEW(ax, rc*0.72,'orangered')
        
        delta = 2*np.pi/N
        for k in range(1,N+1) :
            Name = self.Relatioships[RelName].nnames[k]
            ang = StartPoint + Direct*delta*(k-1)
            self.polar_plot_El(ax,RelName,Name,ang,rc,w,N,1,ecolor)
            ang1 = StartPoint + Direct*delta*k
            
            self.polar_plot_arrow(ax,ang,ang1,rca,rca,1,lcolor)
            
        plt.draw()
        plt.show()
        
        
            
                    
            
        
        
        
    def circ_Rel(self, RName, GRElName,  Directed=None, *arg):
        """obsolete !!! do not use creates cyclic relationship"""
        L = list(arg)
        for i in range(len(L)-1):
            self.Relatioships[RName].Rel_AddElement(GRElName, L[i])
            self.Graphs[RName].add_node(GRElName.elements[L[i]].Name)
            #print i, L[i]
        self.Relatioships[RName].Rel_AddElement(GRElName, L[len(L)-1])
        self.Graphs[RName].add_node(GRElName.elements[L[len(L)-1]].Name)    
            
        for i in range(len(L)-1):    
            self.Relatioships[RName].Rel_SetLink(L[i], L[i+1], Directed)
            self.Graphs[RName].add_edge(L[i], L[i+1])
            #print i, L[i]
        self.Relatioships[RName].Rel_SetLink(L[len(L)-1], L[0], Directed)
        self.Graphs[RName].add_edge(L[len(L)-1], L[0])
        self.Relatioships[RName].Rtype = "cyclic"
        G = nx.cycle_graph(len(L), self.Graphs[RName])
        self.Graphs[RName] = G
            
            
    def add_labelsEl(self, RName, lname):
        """obsolete dont use!!!Add label to the elements in Relationship - second argument is the name of the attribut in Element,
         in the group ( bagua ) for which we define the Relationship - in this case Ucode - unicode sybdol of the trigramm.
         usage example R.add_labelsEl("WenWang", "Ucode") """
        for e in self.Relatioships[RName].elements:
            self.Relatioships[RName].labels[e] =getattr(self.Relatioships[RName].elements[e], lname)
          
        
             
         
    def draw_Rel(self, RName, DrHow=None):
        """ Draws the relationship graph DrHow can be "circular" "spectral """
        pos=nx.circular_layout(self.Graphs[RName])
        dlabels = {}
        i = 0
        for e in self.Relatioships[RName].elements:
            self.Relatioships[RName].labels[e] =self.Relatioships[RName].elements[e].Ucode.decode('utf-8') #.Ucode
            #dlabels[i] = self.Relatioships[RName].elements[e].Name
            i = i + 1
        for node in self.Graphs[RName].nodes():
            dlabels[node] = node
        
        
        if DrHow is None :
            nx.draw(self.Graphs[RName], with_labels=False)
        elif DrHow == "circular" :
            nx.draw_circular(self.Graphs[RName], node_size=200, with_labels=False)
        elif DrHow =="spectral" :
            nx.draw_spectral(self.Graphs[RName], with_labels=False)
        nx.draw_networkx_labels(self.Graphs[RName],pos,dlabels,font_size=16)
        plt.show()

    
        
    
    
class Element(object):
    """basic class describing Element
    dont call the functions directly, use the functions from Elements instead"""
    
    def __init__(self, Name, Y1=None, Y2=None, Y3=None, Y4=None, Y5=None, Y6=None,flo=None,flo2=None,flo3=None,flo4=None,flo5=None,flo6=None):
        """Initialization of the Element, moment of creation is in the crdatetime""" 
        #self.Yaos={}
        self.ElProperties={}
        self.ElOwnProperties={}
        self.ElGroups={}
        self.ElRelationships={}
        self.ElChRelationships={}
        self.pointsFR = {}
        self.pointsEN = {}
        
        self.Name = Name
        self.ChName = None 
        self.ChNote = None
        self.ChPyName = None
        self.ChPyNote = None
        self.EngName = None
        self.Note = None 
        self.RName = None
        self.RNote = None 
        self.FrName = None
        self.FrNote = None
        self.hex = None # boolean for hexagram 1 or 0
        self.HNumber = None 
        self.GrName = None 
        self.GrNumber = None 
        self.t = None    # warning
        self.Ucode = None
        self.Y1 = Y1
        self.Y2 = Y2
        self.Y3 = Y3
        self.Y4 = Y4
        self.Y5 = Y5
        self.Y6 = Y6
        self.flo = flo
        self.flo2 = flo2 
        self.flo3 = flo3
        self.flo4 = flo4
        self.flo5 = flo5
        self.flo6 = flo6
        
        self.Y1com = None
        self.Y2com = None
        self.Y3com = None
        self.Y4com = None
        self.Y5com = None
        self.Y6com = None
        
        self.start = None
        self.end = None
        
        self.p = None
        self.p1 = None
        self.long = None
        self.lat = None
        
        self.Pname = None
        self.Pdiagnosis = None
        self.Pbirthday = None
        self.Pcomment = None
        self.channels = None
        self.PTimages = None
        
        self.tag = None
        
        self.stat_model = None
        
        self.PW = None
        self.NPW = None
        self.PR = None
        self.NPR = None
        
        self.P6 = None
        self.P5 = None
        self.P4 = None
        self.P3 = None
        self.P2 = None
        self.P1 = None
        self.P0 = None
        self.Pall = None
        
        self.NP6 = None
        self.NP5 = None
        self.NP4 = None
        self.NP3 = None
        self.NP2 = None
        self.NP1 = None
        self.NP0 = None
        self.NPall = None
        self.NPtotal = None
        
        self.polar = None
        self.ang = None
        self.rc = None
        self.xc = None
        self.yc = None
        self.Ninrel = None
        self.ecolor = None
        
        self.image = None
        
        self.ChannelSN = None
        self.FrChannelSN = None
        self.InnYang = None
        self.HandFoot = None
        self.ChType = None
        self.CFullName = None
        self.ZangFu = None
        self.ConPoints = None
        self.Description = None
        self.EnTime = None
        
        self.PointSN = None
        self.SecondPointSN = None
        self.FrPointSN = None
        self.FrSecondSN = None
        self.Location = None
        self.HowToFind = None
        self.Needling = None
        self.Moxa = None
        self.Warning = None
        self.Comment = None
        self.ClNotes = None
        
        self.ischannel = None
        self.ispoint = None
        
        
        self.crdatetime = datetime.now()
    
    def add_yaos(self,Y1=None, Y2=None, Y3=None, Y4=None, Y5=None, Y6=None,flo=None,flo2=None,flo3=None,flo4=None,flo5=None,flo6=None ):
        """adds yaos and floating yaos to an element"""
        self.Y1 = Y1
        self.Y2 = Y2
        self.Y3 = Y3
        self.Y4 = Y4
        self.Y5 = Y5
        self.Y6 = Y6
        self.flo = flo
        self.flo2 = flo2 
        self.flo3 = flo3
        self.flo4 = flo4
        self.flo5 = flo5
        self.flo6 = flo6
    
        
    def add_chname(self, chname):
        """Adds chinese name to an Element""" 
        self.ChName = chname
        
    def add_chpyname(self, chpyname):
        """Adds chinese pynjin name to an Element""" 
        self.ChPyName = chpyname
        
    def add_engname(self, engname):
        """Adds english name to an Element""" 
        self.EngName = engname
        
    def add_frname(self, frname):
        """Adds french name to an Element""" 
        self.FrName = frname
        
    def add_rname(self, rname):
        """Adds cyrillic name to an Element""" 
        self.RName = rname
        
    def add_chnote(self, chnote):
        """Adds chinese note to an Element""" 
        self.ChNote = chnote
        
    def add_chpynote(self, chpynote):
        """Adds chinese pynjin note to an Element""" 
        self.ChPyNote = chpynote
        
    def add_engnote(self, engnote):
        """Adds english note to an Element""" 
        self.Note = engnote
        
    def add_frnote(self, frnote):
        """Adds french note to an Element""" 
        self.FrNote = frnote
        
    def add_rnote(self, rnote):
        """Adds cyrillic note to an Element""" 
        self.RNote = rnote
        
    def add_pointEn(self, point,pointSN):
        """adds a point pointsEN list"""
        #print str(point)
        pen = pointEn(point,pointSN)
        self.pointsEN[point] = pen
        #else:
        #    Not_Exist = True
        #    for p in self.pointsEN :
        #        if self.pointsEN[p] == str(point):
        #            Not_Exist = False
        #    if Not_Exist :
        #        p = pointEn(point,point)
        #        self.pointsEN[point] = p
        #    else:
        #        print 'point already exists in EN list'
        
    def add_pointFr(self, point,pointSN):
        """adds a point pointsFR list"""
        #if self.pointsFR is None:
        p = pointFr(point,pointSN)
        self.pointsFR[point] = p
        #else:
        #    Not_Exist = True
        #    for p in self.pointsFR :
        #        if self.pointsFr[p] == str(point):
        #            Not_Exist = False
        #    if Not_Exist :
        #       p = pointFr(point,point)
        #        self.pointsFR[point] = p
        #    else:
        #        print 'point already exists in FR list'
        
    def del_pointEn(self, point):
        """deletes a point from pointsEN"""
        self.pointsEN.pop(point)
        #Not_Exist = True
        #for p in self.pointsEN :
        #    if p == point:
        #        Not_Exist = False
        #if not Not_Exist :
        #    self.pointsEN.pop(point)
        #else:
        #    print 'point not in EN list'
        
    
    def del_pointFr(self, point):
        """deletes a point from pointsFr"""
        self.pointsFR.pop(point)
        #Not_Exist = True
        #for p in self.pointsFR :
        #    if p == point:
        #        Not_Exist = False
        #if not Not_Exist :
        #    self.pointsFr.pop(point, None)
        #else:
        #    print 'point not in FR list'
           
    
    def get_chname(self):
        """gets chinese name to an Element""" 
        return self.ChName
    
    def get_chpyname(self):
        """gets chinese pynjin name to an Element""" 
        return self.ChPyName
        
    def get_engname(self):
        """gets english name to an Element""" 
        return self.EngName
    
    def get_frname(self):
        """gets french name to an Element""" 
        return self.FrName
        
    def get_rname(self):
        """gets cyrillic name to an Element""" 
        return self.RName
        
    def get_chnote(self):
        """gets chinese note to an Element""" 
        return self.ChNote
    
    def get_chpynote(self):
        """gets chinese pynjin note to an Element""" 
        return self.ChPyNote
        
    def get_engnote(self):
        """gets english note to an Element""" 
        return self.Note
    
    def get_frnote(self):
        """gets french note to an Element""" 
        return self.FrNote
        
    def get_rnote(self):
        """gets cyrillic note to an Element""" 
        return self.RNote
    
    def get_pointEn(self, point):
        """gets point from PointsEN"""
        return self.pointsEN[point].pNameSN
    
    def get_pointFr(self, point):
        """gets point from PointsEr"""
        return self.pointsFr[point].pNameSN
    
    def get_all_pointsEn(self):
        """gets all points from PointsEN"""
        s = ''
        for point in sorted(self.pointsEN) :
            s += self.pointsEN[point].pNameSN+' '
        return s
    
    def get_all_pointsFr(self):
        """gets all points from PointsFR"""
        s = ''
        for point in sorted(self.pointsFR) :
            s += self.pointsFR[point].pNameSN+' '
        return s
    
    
            
        
    def add_Ucode(self, Ucode):
        """Adds unicode symbol to an Element """
        self.Ucode = Ucode
        
    def add_HNumber(self, HNumber):
        """Adds HNumber to hex or trigram"""
        self.HNumber = HNumber
        
    def add_Warning(self,W):
        """adds warning to hex or trigram"""
        self.t = W
        
    def add_ChannelSN(self,SN):
        """adds short notation to hex or trigram"""
        self.ChannelSN = SN
        
    def add_FrChannelSN(self,SN):
        """adds fr short notation to hex or trigram"""
        self.FrChannelSN = SN
        
    def add_InnYang(self,InnYang):
        """adds InnYang  to hex or trigram"""
        self.InnYang = InnYang
        
    def add_HandFoot(self,HandFoot):
        """adds HandFoot  to hex or trigram"""
        self.HandFoot = HandFoot
        
    def add_ChType(self,ChType):
        """adds ChType  to hex or trigram"""
        self.ChType = ChType
        
    def add_CFullName(self,CFullName):
        """adds CFullName  to hex or trigram"""
        self.CFullName = CFullName

    def add_ZangFu(self,ZangFu):
        """adds ZangFu to hex or trigram"""
        self.ZangFu = ZangFu
        
    def add_ConPoints(self,ConPoints):
        """adds ConPoints  to hex or trigram"""
        self.ConPoints = ConPoints
        
    def add_Description(self,Description):
        """adds Description to hex or trigram"""
        self.Description = Description
        
    def add_EnTime(self,EnTime):
        """adds EnTime  to hex or trigram"""
        self.EnTime = EnTime
        
    def add_PointSN(self,SN):
        """adds short notation to hex or trigram"""
        self.PointSN = SN
        
    def add_SecondPointSN(self,SN):
        """adds short notation to hex or trigram"""
        self.SecondPointSN = SN
        
    def add_FrPointSN(self,SN):
        """adds french short notation to hex or trigram"""
        self.FrPointSN = SN
        
    def add_FrSecondSN(self,SN):
        """adds short notation to hex or trigram"""
        self.FrSecondSN = SN
    
    def add_Location(self,Location):
        """adds Location info to hex or trigram"""
        self.Location = Location
        
    def add_HowToFind(self,S):
        """adds HowToFind info to hex or trigram"""
        self.HowToFind = S
        
    def add_Needling(self,S):
        """adds Needling info to hex or trigram"""
        self.Needling = S
        
    def add_Moxa(self,S):
        """adds Moxa info to hex or trigram"""
        self.Moxa = S
        
    def add_PointWarning(self,S):
        """adds point Warning to hex or trigram"""
        self.Warning = S
        
    def add_Comment(self,S):
        """adds Comment to hex or trigram"""
        self.Comment = S
        
    def add_ClNotes(self,S):
        """adds ClNotes to hex or trigram"""
        self.ClNotes = S
    
    def get_ChannelSN(self):
        """gets ChannelSN """ 
        return self.ChannelSN
    
    def get_FrChannelSN(self):
        """gets FrChannelSN """ 
        return self.FrChannelSN
    
    def get_InnYang(self):
        """gets InnYang """ 
        return self.InnYang
    
    def get_HandFoot(self):
        """gets  HandFoot""" 
        return self.HandFoot
    
    def get_ChType(self):
        """gets  ChType""" 
        return self.ChType
    
    def get_CFullName(self):
        """gets  CFullName""" 
        return self.CFullName
    
    def get_ZangFu(self):
        """gets ZangFu  """ 
        return self.ZangFu
    
    def get_ConPoints(self):
        """gets ConPoints """ 
        return self.ConPoints
    
    def get_Description(self):
        """gets  Description""" 
        return self.Description
    
    def get_EnTime(self):
        """gets  EnTime""" 
        return self.EnTime
    
    def get_PointSN(self):
        """gets  PointSN""" 
        return self.PointSN
    
    def get_SecondPointSN(self):
        """gets  SecondPointSN""" 
        return self.SecondPointSN
    
    def get_FrPointSN(self):
        """gets  FrPointSN""" 
        return self.FrPointSN
    
    def get_FrSecondSN(self):
        """gets  FrSecondSN""" 
        return self.FrSecondSN
    
    def get_Location(self):
        """gets  Location""" 
        return self.Location
    
    def get_HowToFind(self):
        """gets  HowToFind""" 
        return self.HowToFind
    
    def get_Needling(self):
        """gets Needling """ 
        return self.Needling
    
    def get_Moxa(self):
        """gets Moxa """ 
        return self.Moxa
    
    def get_PointWarning(self):
        """gets  Point Warning""" 
        return self.Warning
    
    def get_Comment(self):
        """gets Comment """ 
        return self.Comment
    
    def get_ClNotes(self):
        """gets ClNotes """ 
        return self.ClNotes
        
            
    def if_hex(self):
        """If hexagram returns 1 otherwise 0"""
        if (self.Y1 is not None) and (self.Y2 is not None) and (self.Y3 is not None) and (self.Y4 is not None) and (self.Y5 is not None) and (self.Y6 is not None):
            return 1
        else : return 0
        
    def if_gua(self):
        """If trigramm returns 1 otherwise 0"""
        if (self.Y1 is not None) and (self.Y2 is not None) and (self.Y3 is not None) and (self.Y4 is None) and (self.Y5 is None) and (self.Y6 is  None):
            return 1
        else : return 0
        
    def if_duo(self):
        """If duogramm returns 1 otherwise 0"""
        if (self.Y1 is not None) and (self.Y2 is not None) and (self.Y3 is None) and (self.Y4 is None) and (self.Y5 is None) and (self.Y6 is  None):
            return 1
        else : return 0
        
    def if_equal_gua(self):
        """if upper and lower gua are the same returns 1"""
        if (self.Y1 == self.Y4 ) and (self.Y2 ==self.Y5) and (self.Y3 == self.Y6) :
            return 1
        else : return 0
        
    def if_opp_gua(self):
        """if upper and lower gua are the opposite returns 1"""
        if (self.Y1 == 1-self.Y4 ) and (self.Y2 == 1-self.Y5) and (self.Y3 == 1-self.Y6) :
            return 1
        else : return 0
        
        
    def if_mirror_gua(self):
        """if upper gua is mirror reflection of lower returns 1"""
        if (self.Y1 == self.Y6 ) and (self.Y2 ==self.Y5) and (self.Y3 == self.Y4) :
            return 1
        else : return 0
        
    def if_mirror_opp_gua(self):
        """if upper gua is opposite mirror reflection of lower returns 1"""
        if (self.Y1 == 1-self.Y6 ) and (self.Y2 ==1-self.Y5) and (self.Y3 == 1-self.Y4) :
            return 1
        else : return 0
    
    def add_crdatetime(self, dt): 
        """Adds crdatetime dt"""  
        self.crdatetime = dt     
    
        
    def add_info(self, hex , Ucode = None, ChName = None , ChNote =None, RName = None, EngName =None, Note = None, RNote = None, HNumber = None, t=None):
        """Adds info : hex 1 or 0- hexagram or not
        Ucode - unicode symbol
        ChName - name in chinese
        ChNote - notation in chinese
        RName - ukranian/russian name
        EngName -english name
        None - short notation in english : "Lake"
        RNote - short notation in russian/ukranian "озеро"
        HNumber - number of hexagram
        t - warning
        """
        self.hex = hex # boolean for hexagram 1 or 0
        self.Ucode = Ucode
        self.ChName = ChName 
        self.ChNote = ChNote
        self.RName = RName
        self.EngName = EngName
        self.Note = Note
        self.RNote = RNote
        self.HNumber = HNumber 
        self.t = t
        
    def add_pinfo(self, Pname, Pbirthday, Pdiagnosis):
        """adds pinfo"""
        self.Pname = Pname
        self.Pbirthday = Pbirthday
        self.Pdiagnosis = Pdiagnosis
        
    def inc_W(self):
        """increments NPW"""
        if self.NPW is None :
            self.NPW = 1
        else : self.NPW = self.NPW +1
        
        
    def inc_R(self):
        """increments NPR"""
        if self.NPR is None :
            self.NPR = 1
        else : self.NPR = self.NPR +1
        
    def inc_float(self, N):
        """increments floating Yao N - from0 to 6 - 0==no floating"""
        if N == 0 :
            if self.NP0 is None :
                self.NP0 = 1
            else : self.NP0 = self.NP0 +1
        if N == 1 :
            if self.NP1 is None :
                self.NP1 = 1
            else : self.NP1 = self.NP1 +1
        if N == 2 :
            if self.NP2 is None :
                self.NP2 = 1
            else : self.NP2 = self.NP2 +1
        if N == 3 :
            if self.NP3 is None :
                self.NP3 = 1
            else : self.NP3 = self.NP3 +1
        if N == 4 :
            if self.NP4 is None :
                self.NP4 = 1
            else : self.NP4 = self.NP4 +1
        if N == 5 :
            if self.NP5 is None :
                self.NP5 = 1
            else : self.NP5 = self.NP5 +1
        if N == 6 :
            if self.NP6 is None :
                self.NP6 = 1
            else : self.NP6 = self.NP6 +1
        
        
            
        
    
        
        
    def add_float_yao_info(self, flo = None, flo2 = None, flo3 = None, flo4 = None, flo5 = None, flo6 = None  ):
        """Adds info about floating yaos"""
         
        self.flo = flo
        self.flo2 = flo2 
        self.flo3 = flo3 
        self.flo4 = flo4
        self.flo5 = flo5
        self.flo6 = flo6
        
    def del_float_yao_info(self):
        """deletess info about floating yaos"""
        self.flo = None
        self.flo2 = None 
        self.flo3 = None
        self.flo4 = None
        self.flo5 = None
        self.flo6 = None
        
    def get_crdatetime(self):
        """gives the time of the creation """
        s = str(self.crdatetime)
        return s
    
    def get_property(self,PrName):
        """gives property value"""
        s= self.ElProperties[PrName].PrValue
        return s
        
    def add_property(self, PrName, PrValue):
        """Adds Property to the Element, Property
        Name and the Value are requied"""
        p=ElProperty(PrName,PrValue)
        self.ElProperties[PrName] = p
        
    def del_property(self, PrName):
        """Deletes property"""
        self.ElProperties.pop(PrName)
        
    def edit_property(self, PrName, PrNewValue):
        """Edit the property"""
        if self.ElProperties[PrName].PrName is not None:
            self.ElProperties[PrName].PrValue = PrNewValue
            
    def get_properties(self):
        """returns dict propertyName : PropertyValue"""
        l = {}
        for p in self.ElProperties  :
            str1 = self.ElProperties[p].PrValue
            str2 = self.ElProperties[p].PrName 
            l[str2]=str1 
        return l
        
        
        
            
    def find_in_properties(self, SearchStr):
        """finds searchstr in properties
        returns dict propertyName : PropertyValue"""
        l={}
        s1 = "basic"
        s2 = ""
        if self.Ucode is not None :
            s = self.Ucode 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.ChName is not None :
            s = self.ChName
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.ChNote  is not None :
            s = self.ChNote
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.ChPyName is not None :
            s = self.ChPyName
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.ChPyNote  is not None :
            s = self.ChPyNote
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.RName is not None :
            s = self.RName 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.EngName is not None :
            s = self.EngName 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.Note is not None :
            s = self.Note 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.FrName is not None :
            s = self.FrName 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.FrNote is not None :
            s = self.FrNote 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.RNote is not None :
            s = self.RNote 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.HNumber is not None : 
            s = str(self.HNumber) 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.t is not None :
            s = self.t 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if s2 != "" :
            l[s1] = s2
        s1 = "channels points"
        s2 = ""        
        
        if self.ChannelSN is not None :
            s = self.ChannelSN 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.FrChannelSN is not None :
            s = self.FrChannelSN 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.InnYang is not None :
            s = self.InnYang 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.HandFoot is not None :
            s = self.HandFoot 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.ChType is not None :
            s = self.ChType 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.CFullName is not None :
            s = self.CFullName 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.ZangFu is not None :
            s = self.ZangFu 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.ConPoints is not None :
            s = self.ConPoints 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.Description is not None :
            s = self.Description 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.EnTime is not None :
            s = self.EnTime 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.PointSN is not None :
            s = self.PointSN 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.SecondPointSN is not None :
            s = self.SecondPointSN 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.FrPointSN is not None :
            s = self.FrPointSN 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.FrSecondSN is not None :
            s = self.FrSecondSN 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.Location is not None :
            s = self.Location 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.HowToFind is not None :
            s = self.HowToFind 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.Needling is not None :
            s = self.Needling 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.Moxa is not None :
            s = self.Moxa 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.Warning is not None :
            s = self.Warning 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.Comment is not None :
            s = self.Comment 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.ClNotes is not None :
            s = self.ClNotes 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if s2 != "" :
            l[s1] = s2
        s1 = "medical"
        s2 = ""
        if self.Pname is not None :
            s = self.Pname 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.Pbirthday is not None :
            s = self.Pbirthday
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.Pdiagnosis  is not None :
            s = self.Pdiagnosis
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.Pcomment is not None :
            s = self.Pcomment 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.channels is not None :
            s = self.channels 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if self.tag is not None :
            s = self.tag 
            if s.find(SearchStr) != -1 :
                s2 = s2  + s
        if s2 != "" :
            l[s1] = s2
        for p in self.ElProperties  :
            str1 = self.ElProperties[p].PrValue
            str2 = self.ElProperties[p].PrName 
            #print str2 
            #print str1
     
            if str1.find(SearchStr) != -1 :
                l[str2]=str1
            elif str2.find(SearchStr) != -1 :
                l[str2]=str1
            
        if l is not None :
            return l
        else : return None
            
        
        
    def print_property(self, PrName):
        """Prints the Property"""
        s = 'Element:    '+self.Name +'           \n'
        if self.Ucode is not None:
            s += '      '+self.Ucode+'           \n'
        else: s +=  ' \n '
        if self.ElProperties[PrName].PrName is not None:
            s += 'Property:      '+self.ElProperties[PrName].PrName+'          \n '
        if self.ElProperties[PrName].PrValue is not None : 
            s += 'Value:      '+self.ElProperties[PrName].PrValue+'           \n '
        #print s
        return s
    
    def print_n_ucode(self):
        """"""
        s=""
        if self.HNumber is not None:
            s += '    '+ repr(self.HNumber)+' '
        if self.Ucode is not None:
            s += self.Ucode
        #debug
        
        return s    
    
 
                
        
    def __str__(self):
        """Prints the whole element and the properties"""
        s = '    '+self.Name +'           \n'
        if self.Pname is not None:
            s += '  '+ 'CrDate: '+str(self.crdatetime.date())+'           \n'
        if self.HNumber is not None:
            s += '  '+ repr(self.HNumber)+'           \n'
        if self.Ucode is not None:
            s += '      '+self.Ucode+'           \n'
        if self.ChName is not None:
            s += '      '+self.ChName+'           \n'
        if self.Pname is not None:
            s += '      '+self.Pname+'           \n'
        if self.Pbirthday is not None:
            s += '      '+self.Pbirthday+'           \n'
        if self.Pdiagnosis is not None:
            s += '      '+self.Pdiagnosis+'           \n'
        if self.Pcomment is not None:
            s += '      '+self.Pcomment+'           \n'
        if self.channels is not None:
            s += '      '+self.channels+'           \n'
        if self.tag is not None:
            s += '      '+self.tag+'           \n'
            
       
        if self.Y6 is not None:
            if self.Y6 == 1 :
                s += '    -----'
            if self.Y6 == 0 :
                s += '    -- --'
            if self.flo == 6 or self.flo2 == 6 or self.flo3 == 6 or self.flo4 == 6 or self.flo5 == 6 or self.flo6 == 6:
                if self.Y6 == 1 :
                    s += ' x '
                if self.Y6 == 0 :
                    s += ' o '
            else : s += '   '
            if self.Y6com is not None:
                s += str(self.Y6com)
            if self.P6 is not None:
                s += ' P= '+str(self.P6)+ ' N= '+str(self.NP6)
            s += '   \n'        
                
        if self.Y5 is not None:
            if self.Y5 == 1 :
                s += '    -----'
            if self.Y5 == 0 :
                s += '    -- --'
            if self.flo == 5 or self.flo2 == 5 or self.flo3 == 5 or self.flo4 == 5 or self.flo5 == 5 or self.flo6 == 5 :
                if self.Y5 == 1 :
                    s += ' x '
                if self.Y5 == 0 :
                    s += ' o '
            else : s += '   '
            if self.Y5com is not None:
                s += str(self.Y5com)
            if self.P5 is not None:
                s += ' P= '+str(self.P5)+ ' N= '+str(self.NP5)
            s += '   \n'
        if self.Y4 is not None:
            if self.Y4 == 1 :
                s += '    -----'
            if self.Y4 == 0 :
                s += '    -- --'
            if self.flo == 4 or self.flo2 == 4 or self.flo3 == 4 or self.flo4 == 4 or self.flo5 == 4 or self.flo6 == 4 :
                if self.Y4 == 1 :
                    s += ' x '
                if self.Y4 == 0 :
                    s += ' o '
            else : s += '   '
            if self.Y4com is not None:
                s += str(self.Y4com)
            if self.P4 is not None:
                s += ' P= '+str(self.P4)+ ' N= '+str(self.NP4)
            s += '   \n'
        if self.Y3 is not None:
            if self.Y3 == 1 :
                s += '    -----'
            if self.Y3 == 0 :
                s += '    -- --'
            if self.flo == 3 or self.flo2 == 3 or self.flo3 == 3 or self.flo4 == 3 or self.flo5 == 3 or self.flo6 == 3 :
                if self.Y3 == 1 :
                    s += ' x '
                if self.Y3 == 0 :
                    s += ' o '
            else : s += '   '
            if self.Y3com is not None:
                s += str(self.Y3com)
            if self.P3 is not None:
                s += ' P= '+str(self.P3)+ ' N= '+str(self.NP3)
            s += '   \n'
        if self.Y2 is not None:
            if self.Y2 == 1 :
                s += '    -----'
            if self.Y2 == 0 :
                s += '    -- --'
            if self.flo == 2 or self.flo2 == 2 or self.flo3 == 2 or self.flo4 == 2 or self.flo5 == 2 or self.flo6 == 2 :
                if self.Y2 == 1 :
                    s += ' x '
                if self.Y2 == 0 :
                    s += ' o '
            else : s += '   '
            if self.Y2com is not None:
                s += str(self.Y2com)
            if self.P2 is not None:
                s += ' P= '+str(self.P2)+ ' N= '+str(self.NP2)
            s += '   \n'
        if self.Y1 is not None:
            if self.Y1 == 1 :
                s += '    -----'
            if self.Y1 == 0 :
                s += '    -- --'
            if self.flo == 1 or self.flo2 == 1 or self.flo3 == 1 or self.flo4 == 16 or self.flo5 == 1 or self.flo6 == 1 :
                if self.Y1 == 1 :
                    s += ' x '
                if self.Y1 == 0 :
                    s += ' o '
            else : s += '   '
            if self.Y1com is not None:
                s += str(self.Y1com)
            if self.P1 is not None:
                s += ' P= '+str(self.P1)+ ' N= '+str(self.NP1)
            s += '   \n'
        if self.P0 is not None:
            s += ' P0= '+str(self.P0)+ ' NP0= '+str(self.NP0)
            s += '   \n'
        if self.PW is not None:
            s += '      PW='+str(self.PW)+'          \n'
        if self.NPW is not None:
            s += '      NPW='+str(self.NPW)+'          \n'
        if self.PR is not None:
            s += '      PR='+str(self.PR)+'          \n'
        if self.NPR is not None:
            s += '      NPR='+str(self.NPR)+'          \n'
        if self.ChName is not None:
            s += '      '+self.ChName+'           \n'
        if self.ChNote is not None:
            s += '      '+self.ChNote+'           \n'
        if self.ChPyName is not None:
            s += '      pinyin :'+self.ChPyName+'           \n'
        if self.ChPyNote is not None:
            s += '      pinyin :'+self.ChPyNote+'           \n'
        if self.EngName is not None:
            s += '      '+self.EngName+'           \n'
        if self.Note is not None:
            s += '      '+self.Note+'           \n'
        if self.FrName is not None:
            s += '      '+self.FrName+'           \n'
        if self.FrNote is not None:
            s += '      '+self.FrNote+'           \n'
        if self.RName is not None:
            s += '      '+self.RName+'           \n'
        if self.RNote is not None:
            s += '      '+self.RNote+'           \n'
        if self.t is not None:
            s += '      '+self.t+'           \n'
        if self.ChannelSN is not None:
            s += '      EN: '+self.ChannelSN+'           \n'
        if self.FrChannelSN is not None:
            s += '      FR: '+self.FrChannelSN+'           \n'
        if self.InnYang is not None:
            s += '      Inn/Yang: '+self.InnYang+'           \n'
        if self.HandFoot is not None:
            s += '      Hand/Foot: '+self.HandFoot+'           \n'
        if self.ChType is not None:
            s += '      Type: '+self.ChType+'           \n'
        if self.CFullName is not None:
            s += '      Full Name: '+self.CFullName+'           \n'
        if self.ZangFu is not None:
            s += '      Zang Fu: '+self.ZangFu+'           \n'
        if self.ConPoints is not None:
            s += '      Connection points: '+self.ConPoints+'           \n'
        if self.Description is not None:
            s += '      Description: '+self.Description+'           \n'
        if self.EnTime is not None:
            s += '      Time: '+self.EnTime+'           \n'
        if self.PointSN is not None:
            s += '      EN: '+self.PointSN+'           \n'
        if self.SecondPointSN is not None:
            s += '      2EN: '+self.SecondPointSN+'           \n'
        if self.FrPointSN is not None:
            s += '      FR: '+self.FrPointSN+'           \n'
        if self.FrSecondSN is not None:
            s += '      2FR: '+self.FrSecondSN+'           \n'
        if self.Location is not None:
            s += '      Location:'+self.Location+'           \n'
        if self.HowToFind is not None:
            s += '      How to find: '+self.HowToFind+'           \n'
        if self.Needling is not None:
            s += '      Needling: '+self.Needling+'           \n'
        if self.Moxa is not None:
            s += '      Moxa: '+self.Moxa+'           \n'
        if self.Warning is not None:
            s += '      Warning: '+self.Warning+'           \n'
        if self.Comment is not None:
            s += '      Comment: '+self.Comment+'           \n'
        if self.ClNotes is not None:
            s += '      Combinations/Clinical notes: '+self.ClNotes+'           \n'
        if self.ElProperties is not None:
            for p in sorted(self.ElProperties):
                s += ' '+self.ElProperties[p].PrName+' :  '+self.ElProperties[p].PrValue+'  \n '
        return s
                
        
             
class Elements(object):
    """Array for the group of Elements.
    Use these functions to work with Elements"""
    
    def __init__(self):
        """Initialisation of the Elements array"""
        self.elements={}
        
    def add(self, Name, Y1=None, Y2=None, Y3=None, Y4=None, Y5=None, Y6=None,flo=None,flo2=None,flo3=None,flo4=None,flo5=None,flo6=None):
        """Adds one element to the group.
        Yao should be indicated from 1st to top Yao by 0 or 1 for Yin and Yang,
        devided by the comma like add("Qian",1,1,1)
        Enter 3 for trigram or 6 for hexagram or less.
        for hexagram, numbers for floating yaos can be entered"""
        e = Element(Name, Y1, Y2, Y3, Y4, Y5, Y6, flo, flo2, flo3, flo4,flo5,flo6)
        self.elements[Name]= e
    
    def add_ElYaos(self,Name, Y1=None, Y2=None, Y3=None, Y4=None, Y5=None, Y6=None,flo=None,flo2=None,flo3=None,flo4=None,flo5=None,flo6=None):
        """adds yaos and floating yaos to element Name """
        self.elements[Name].add_yaos(Y1, Y2, Y3, Y4, Y5, Y6, flo, flo2, flo3, flo4,flo5,flo6)
    
    def add_Elcrdatetime(self,Name,dt):
        """Adds crdatetime """
        self.elements[Name].add_crdatetime(dt)
        
    def delete(self, Name):
        """Deletes an element from the group"""
        self.elements.pop(Name, None)
        
    def delete_all(self):
        """Deletes all elements from the group"""
        names = {}
        i = 0
        for p in self.elements :
            names[i] = self.elements[p].Name
            #print names[i]
            i = i + 1
        i = 0
        for name in names:
            self.delete(names[i])
            #print names[i]
            i = i+ 1
        
    def add_ElChname(self, Name, ChName):
        """Adds Chinese name to the element"""
        self.elements[Name].add_chname(ChName)
        
    def add_ElChPyname(self, Name, ChPyName):
        """Adds Chinese pynjin name to the element"""
        self.elements[Name].add_chpyname(ChPyName)
        
    def add_ElEngname(self, Name, EngName):
        """Adds English name to the element"""
        self.elements[Name].add_engname(EngName)
        
    def add_ElFrname(self, Name, FrName):
        """Adds french name to the element"""
        self.elements[Name].add_frname(FrName)
        
    def add_ElRname(self, Name, RName):
        """Adds cyrrilic name to the element"""
        self.elements[Name].add_rname(RName)
        
    def add_ElChnote(self, Name, ChNote):
        """Adds Chinese note to the element"""
        self.elements[Name].add_chnote(ChNote)
        
    def add_ElChPynote(self, Name, ChPyNote):
        """Adds Chinese note to the element"""
        self.elements[Name].add_chpynote(ChPyNote)
        
    def add_ElEngnote(self, Name, EngNote):
        """Adds English note to the element"""
        self.elements[Name].add_engnote(EngNote)
    
    def add_ElFrnote(self, Name, FrNote):
        """Adds french note to the element"""
        self.elements[Name].add_frnote(FrNote)
        
    def add_ElRnote(self, Name, RNote):
        """Adds cyrrilic note to the element"""
        self.elements[Name].add_rnote(RNote)
        
    def get_ElChname(self, Name):
        """gets Chinese name to the element"""
        return self.elements[Name].get_chname()
    
    def get_ElChPyname(self, Name):
        """gets Chinese pynjin name to the element"""
        return self.elements[Name].get_chpyname()
        
    def get_ElEngname(self, Name):
        """gets English name to the element"""
        return self.elements[Name].get_engname()
    
    def get_ElFrname(self, Name):
        """gets french name to the element"""
        return self.elements[Name].get_frname()
        
    def get_ElRname(self, Name):
        """gets cyrrilic name to the element"""
        return self.elements[Name].get_rname()
        
    def get_ElChnote(self, Name):
        """gets Chinese note to the element"""
        return self.elements[Name].get_chnote()
    
    def get_ElChPynote(self, Name):
        """gets Chinese pynjin note to the element"""
        return self.elements[Name].get_chpynote()
            
    def get_ElEngnote(self, Name):
        """gets English note to the element"""
        return self.elements[Name].get_engnote()
    
    def get_ElFrnote(self, Name):
        """gets french note to the element"""
        return self.elements[Name].get_frnote()
        
    def get_ElRnote(self, Name):
        """gets cyrrilic note to the element"""
        return self.elements[Name].get_rnote()
        
    def add_ElUcode(self, Name, Ucode):
        """Adds Unicode symbol  to the element"""
        self.elements[Name].add_Ucode(Ucode)
        
    def add_ElHNumber(self, Name, HNumber):
        """Adds HNumber to the hex or trigramm"""
        self.elements[Name].add_HNumber(HNumber)
        
   
    def add_ElWarning(self,Name,W):
        """adds warning to hex or trigram"""
        self.elements[Name].add_Warning(W)
        
    def add_ElChannelSN(self,Name,W):
        """adds ChannelSN to hex or trigram"""
        self.elements[Name].add_ChannelSN(W)
        
    def add_ElFrChannelSN(self,Name,W):
        """adds FrChannelSN to hex or trigram"""
        self.elements[Name].add_FrChannelSN(W)
        
    def add_ElInnYang(self,Name,W):
        """adds InnYang to hex or trigram"""
        self.elements[Name].add_InnYang(W)
        
    def add_ElHandFoot(self,Name,W):
        """adds HandFoot to hex or trigram"""
        self.elements[Name].add_HandFoot(W)
        
    def add_ElChType(self,Name,W):
        """adds ChType to hex or trigram"""
        self.elements[Name].add_ChType(W)
        
    def add_ElCFullName(self,Name,W):
        """adds CFullName to hex or trigram"""
        self.elements[Name].add_CFullName(W)
        
    def add_ElZangFu(self,Name,W):
        """adds ZangFu to hex or trigram"""
        self.elements[Name].add_ZangFu(W)
        
    def add_ElConPoints(self,Name,W):
        """adds ConPoints to hex or trigram"""
        self.elements[Name].add_ConPoints(W)
        
    def add_ElDescription(self,Name,W):
        """adds Description to hex or trigram"""
        self.elements[Name].add_Description(W)
        
    def add_ElEnTime(self,Name,W):
        """adds EnTime to hex or trigram"""
        self.elements[Name].add_EnTime(W)
        
    def add_ElPointSN(self,Name,W):
        """adds PointSN to hex or trigram"""
        self.elements[Name].add_PointSN(W)
        
    def add_ElSecondPointSN(self,Name,W):
        """adds SecondPointSN to hex or trigram"""
        self.elements[Name].add_SecondPointSN(W)
        
    def add_ElFrPointSN(self,Name,W):
        """adds FrPointSN to hex or trigram"""
        self.elements[Name].add_FrPointSN(W)
        
    def add_ElFrSecondSN(self,Name,W):
        """adds FrSecondSN to hex or trigram"""
        self.elements[Name].add_FrSecondSN(W)
        
    def add_ElLocation(self,Name,W):
        """adds Location to hex or trigram"""
        self.elements[Name].add_Location(W)
        
    def add_ElHowToFind(self,Name,W):
        """adds HowToFind to hex or trigram"""
        self.elements[Name].add_HowToFind(W)
        
    def add_ElNeedling(self,Name,W):
        """adds Needling to hex or trigram"""
        self.elements[Name].add_Needling(W)
        
    def add_ElMoxa(self,Name,W):
        """adds Moxa to hex or trigram"""
        self.elements[Name].add_Moxa(W)
        
    def add_ElPointWarning(self,Name,W):
        """adds Point Warning to hex or trigram"""
        self.elements[Name].add_PointWarning(W)
        
    def add_ElComment(self,Name,W):
        """adds Comment to hex or trigram"""
        self.elements[Name].add_Comment(W)
        
    def add_ElClNotes(self,Name,W):
        """adds ClNotes to hex or trigram"""
        self.elements[Name].add_ClNotes(W)
        
    def add_ElpointEn(self,Name,p,psn):
        """add a point in eng.not. to point list"""
        self.elements[Name].add_pointEn(p,psn)
        
    def add_ElpointFr(self,Name,p,psn):
        """add a point in fr.not. to point list"""
        self.elements[Name].add_pointFr(p,psn)
        
    def del_ElpointEn(self,Name,p):
        """deletes a point in eng.not. to point list"""
        self.elements[Name].del_pointEn(p)
        
    def del_ElpointFr(self,Name,p):
        """deletes a point in fr.not. to point list"""
        self.elements[Name].del_pointFr(p)
        
    def get_ElpointEn(self,Name,p):
        """returnes a point in eng.not. from point list"""
        return self.elements[Name].get_pointEn(p)
    
    def get_ElpointFr(self,Name,p):
        """returnes a point in fr.not. from point list"""
        return self.elements[Name].get_pointFr(p)
    
    def get_all_ElpointsEn(self,Name):
        """returnes all points in eng.not. from point list"""
        return self.elements[Name].get_all_pointsEn()
    
    def get_all_ElpointsFr(self,Name):
        """returnes all points in fr.not. from point list"""
        return self.elements[Name].get_all_pointsFr()
        
        
    def add_float_yao(self, Name, flo, flo2=None, flo3=None, flo4=None,flo5=None,flo6=None):
        """adds floating yao"""
        self.elements[Name].add_float_yao_info(flo,flo2,flo3,flo4,flo5,flo6)
        
    def del_float_yao(self, Name, f=None):
        """deletes all floating yao"""
        self.elements[Name].del_float_yao_info()
        
        
    def add_Elinfo(self, Name, hex , Ucode = None, ChName = None ,ChNote =None, RName = None, EngName =None, Note = None, RNote = None, HNumber = None ):
        """ Adds info for element Name
        hex 1 or 0- hexagram or not
        Ucode - unicode symbol
        ChName - name in chinese
        ChNote - note in chinese,
        RName - ukranian/russian name
        EngName -english name
        None - short notation in english : "Lake"
        RNote - short notation in russian/ukranian "озеро"
        HNumber - number of hexagram
        """
        self.elements[Name].add_info(hex , Ucode, ChName, ChNote, RName, EngName, Note, RNote, HNumber)
        
    def set_tag(self, Name, tag):
        """sets a tag W -for working, R -for resulting """
        self.elements[Name].tag = tag
    
    def del_tag(self, Name):
        """deletes a tag  """
        self.elements[Name].tag = None
        
    
    
    def compare_Els(self, El1, El2):
        """compare elements El1 and El2
        if they have the same Yaos returns 1 otherwise 0"""
        if (El1.Y1 == El2.Y1)and(El1.Y2 == El2.Y2)and(El1.Y3 == El2.Y3)and(El1.Y4 == El2.Y4)and(El1.Y5 == El2.Y5)and(El1.Y6 == El2.Y6) : 
            return 1
        else : return 0
        
    def if_El_hex(self,El):
        """If hexagram returns 1 otherwise 0"""
        return self.elements[El].if_hex()
    
    def if_El_gua(self,El):
        """If trigramm returns 1 otherwise 0"""
        return self.elements[El].if_gua()
    
    def if_El_duo(self,El):
        """If duogramm returns 1 otherwise 0"""
        return self.elements[El].if_duo()
    
    def if_El_equal_gua(self,El):
        """if El has equal gua returns 1 otherwise 0"""
        return self.elements[El].if_equal_gua()
    
    def if_El_opp_gua(self,El):
        """if El has opposite gua returns 1 otherwise 0"""
        return self.elements[El].if_opp_gua()
        
        
    def if_El_mirror_gua(self,El):
        """if El has mirrored gua returns 1 otherwise 0""" 
        return self.elements[El].if_mirror_gua()   
    
    def if_El_mirror_opp_gua(self,El):
        """if El has opposite mirrored gua returns 1 otherwise 0""" 
        return self.elements[El].if_mirror_opp_gua()    
        
    def copy_El(self, Name, El):
        """element El is copied and added to current group under the Name
        ATTN: floating yaos are not copied! use carrefully"""
        e = Element(Name, El.Y1, El.Y2, El.Y3, El.Y4, El.Y5, El.Y6)#, El.flo,El.flo2,El.flo3)#,El.flo4,El.flo5,El.flo6)
        self.elements[Name]= e
        
    def basic_copy(self, Name, El):
        """element El is copied ( not float!)  and basic properties too"""
        self.copy_El(Name, El)
        self.elements[Name].add_crdatetime(El.crdatetime)
        self.elements[Name].add_info(El.hex , El.Ucode, El.ChName, El.ChNote, El.RName, El.EngName, El.Note, El.RNote, El.HNumber,El.t)
    
    def copy_properties(self,Name,El):
        """element El properties are copied to Name element"""
        #self.basic_copy(Name, El)
        l = El.get_properties()
        for p in l :
            self.add_ElProperty(self.elements[Name].Name, p , l[p]) 
            
    def copy_Pinfo(self, Name, El):
        """copies P info to Name element """
        self.elements[Name].add_pinfo(El.Pname,El.Pbirthday,El.Pdiagnosis)
        #self.elements[Name].Pcomment = El.Pcomment
        #self.elements[Name].channels = El.channels
        #self.elements[Name].tag = El.tag
        
        
    def copy_stats(self, Name, El): 
        """copies stats to Name element"""
        self.elements[Name].stat_model = El.stat_model
        self.elements[Name].PW = El.PW 
        self.elements[Name].NPW = El.NPW
        self.elements[Name].PR = El.PR
        self.elements[Name].NPR = El.NPR
        self.elements[Name].P1 = El.P1
        self.elements[Name].P2 = El.P2
        self.elements[Name].P3 = El.P3
        self.elements[Name].P4 = El.P4
        self.elements[Name].P5 = El.P5
        self.elements[Name].P6 = El.P6
        self.elements[Name].P0 = El.P0
        self.elements[Name].Pall = El.Pall
        self.elements[Name].NP1 = El.NP1
        self.elements[Name].NP2 = El.NP2
        self.elements[Name].NP3 = El.NP3
        self.elements[Name].NP4 = El.NP4
        self.elements[Name].NP5 = El.NP5
        self.elements[Name].NP6 = El.NP6
        self.elements[Name].NP0 = El.NP0
        self.elements[Name].NPall = El.NPall
        self.elements[Name].NPtotal = El.NPtotal
        
    def copy_yao_properties(self, Name, El): 
        """copies yao properties to Name element"""
        self.elements[Name].Y1com = El.Y1com
        self.elements[Name].Y2com = El.Y2com
        self.elements[Name].Y3com = El.Y3com
        self.elements[Name].Y4com = El.Y4com
        self.elements[Name].Y5com = El.Y5com
        self.elements[Name].Y6com = El.Y6com
        
    def copy_channels_points(self, Name, El): 
        """copies channels and points information to Name element"""
        self.elements[Name].ChannelSN = El.ChannelSN
        self.elements[Name].FrChannelSN = El.FrChannelSN
        self.elements[Name].InnYang = El.InnYang
        self.elements[Name].HandFoot = El.HandFoot
        self.elements[Name].ChType = El.ChType
        self.elements[Name].CFullName = El.CFullName
        self.elements[Name].ZangFu = El.ZangFu
        self.elements[Name].ConPoints = El.ConPoints
        self.elements[Name].Description = El.Description
        self.elements[Name].EnTime = El.EnTime
        self.elements[Name].PointSN = El.PointSN
        self.elements[Name].SecondPointSN = El.SecondPointSN
        self.elements[Name].FrPointSN = El.FrPointSN
        self.elements[Name].FrSecondSN = El.FrSecondSN
        self.elements[Name].Location = El.Location
        self.elements[Name].HowToFind = El.HowToFind
        self.elements[Name].Needling = El.Needling
        self.elements[Name].Moxa = El.Moxa
        self.elements[Name].Warning = El.Warning
        self.elements[Name].Comment = El.Comment
        self.elements[Name].ClNotes = El.ClNotes
        self.elements[Name].ischannel = El.ischannel
        self.elements[Name].ispoint = El.ispoint
        self.elements[Name].image = El.image
        
 
           
        
    def copy_El_float(self, Name, El):
        """Element is copied including floating Yaos"""
        e = Element(Name, El.Y1, El.Y2, El.Y3, El.Y4, El.Y5, El.Y6, El.flo,El.flo2,El.flo3,El.flo4,El.flo5,El.flo6)
        self.elements[Name]= e
        self.elements[Name].add_crdatetime(El.crdatetime)
        self.elements[Name].add_info(El.hex , El.Ucode, El.ChName, El.ChNote, El.RName, El.EngName, El.Note, El.RNote, El.HNumber,El.t)
    
    def copy_full_El(self,Name,El):
        """copies full El - yaos,float yaos, basic info and properties (patient info and stats too if present)"""
        e = Element(Name, El.Y1, El.Y2, El.Y3, El.Y4, El.Y5, El.Y6, El.flo,El.flo2,El.flo3,El.flo4,El.flo5,El.flo6)
        self.elements[Name]= e
        self.elements[Name].add_crdatetime(El.crdatetime)
        self.elements[Name].add_info(El.hex , El.Ucode, El.ChName, El.ChNote, El.RName, El.EngName, El.Note, El.RNote, El.HNumber,El.t)
        if El.FrName is not None:
            self.elements[Name].FrName = El.FrName
        if El.FrNote is not None:
            self.elements[Name].FrNote = El.FrNote
        if El.ChPyName is not None:
            self.elements[Name].ChPyName = El.ChPyName
        if El.ChPyNote is not None:
            self.elements[Name].ChPyNote = El.ChPyNote
        l = El.get_properties()
        for p in l :
            self.add_ElProperty(self.elements[Name].Name, p , l[p])
        if El.Pname is not None:
            self.copy_Pinfo(self.elements[Name].Name, El)
            self.elements[Name].Pcomment = El.Pcomment
            self.elements[Name].channels = El.channels
        if El.tag is not None:
            self.elements[Name].tag = El.tag
        if El.NPW is not None:
            self.copy_stats(self.elements[Name].Name, El)
        if El.ChannelSN is not None or El.PointSN is not None :
            self.copy_channels_points(self.elements[Name].Name, El)
        self.copy_yao_properties(self.elements[Name].Name, El)    
    
    def copy_reformat_El(self,Name,El):
        """(technical !!!) copies and reformates  El ( used for sets rewriting) - yaos,float yaos, basic info and properties (patient info and stats too if present)"""
        e = Element(Name, El.Y1, El.Y2, El.Y3, El.Y4, El.Y5, El.Y6, El.flo,El.flo2,El.flo3,El.flo4,El.flo5,El.flo6)
        self.elements[Name]= e
        self.elements[Name].add_crdatetime(El.crdatetime)
        self.elements[Name].add_info(El.hex , El.Ucode, El.ChName, El.ChNote, El.RName, El.EngName, El.Note, El.RNote, El.HNumber,El.t)
        #if El.FrName is not None:
        #   self.elements[Name].FrName = El.FrName
        #if El.FrNote is not None:
        #    self.elements[Name].FrNote = El.FrNote
        #if El.ChPyName is not None:
        #    self.elements[Name].ChPyName = El.ChPyName
        #if El.ChPyNote is not None:
        #    self.elements[Name].ChPyNote = El.ChPyNote
        l = El.get_properties()
        for p in l :
            self.add_ElProperty(self.elements[Name].Name, p , l[p])
        if El.Pname is not None:
            self.copy_Pinfo(self.elements[Name].Name, El)
            self.elements[Name].Pcomment = El.Pcomment
            self.elements[Name].channels = El.channels
        if El.tag is not None:
            self.elements[Name].tag = El.tag
        if El.NPW is not None:
            self.elements[Name].copy_stats(self.elements[Name].Name, El)
        #if El.ChannelSN is not None or El.PointSN is not None :
        #    self.elements[Name].copy_channels_points(self.elements[Name].Name, El)
        self.copy_yao_properties(self.elements[Name].Name, El)    
        
        
    def copy_by_name(self,ElName,Name):  
        """element Elname is copied inside the group and assigned name Name"""
        self.copy_El_float(Name, self.elements[ElName])
        self.copy_properties(Name, self.elements[ElName])
        self.copy_yao_properties(Name, self.elements[ElName])
                
          
        
    def find_in_set(self, Name, FoundName, SetName):
        """finds element with the same yaos like Name in Setname
        found element is added to the group under name FoundName
        if FoundName = Name basic info and properties from set is added,
        ATTN: floating yao info is conserved like in original hexagram,
        not copied from the set """
        
        flo = None
        flo2 = None
        flo3 = None
        flo4 = None
        flo5 = None
        flo6 = None
        

        
        if self.elements[Name].flo is not None :
            flo = self.elements[Name].flo
        if self.elements[Name].flo2 is not None :
            flo2 = self.elements[Name].flo2
        if self.elements[Name].flo3 is not None :
            flo3 = self.elements[Name].flo3
        if self.elements[Name].flo4 is not None :
            flo4 = self.elements[Name].flo4
        if self.elements[Name].flo5 is not None :
            flo5 = self.elements[Name].flo5
        if self.elements[Name].flo6 is not None :
            flo6 = self.elements[Name].flo6
        
        i = 0
        for p in SetName.elements:
            if self.compare_Els(self.elements[Name], SetName.elements[p]) :
                dt = self.elements[Name].crdatetime
                self.basic_copy(FoundName, SetName.elements[p])
                self.copy_properties(FoundName, SetName.elements[p])
                self.copy_yao_properties(FoundName, SetName.elements[p])
                if flo is not None :
                    self.add_float_yao(FoundName, flo, flo2, flo3, flo4, flo5, flo6)
                #print "one element found"
                self.elements[FoundName].crdatetime = dt
                i = i +1
        if i == 0 : 
            i = 0#print "Nothing found" development option
        elif i > 1 : print "More than one found to one element"
    
    def update_stats_in_set(self, Name, SetName):
        """updates statistics(W,R,float) in set - Name -name of the working W hexagram"""
        temp = Elements()
        for p in SetName.elements:
            if self.compare_Els(self.elements[Name], SetName.elements[p]) :
                SetName.elements[p].inc_W()
                
                if self.elements[Name].flo is  None :
                    SetName.elements[p].inc_float(0)
                    SetName.elements[p].inc_R()
                else : 
                    f = self.elements[Name].flo
                    SetName.elements[p].inc_float(f)
                if self.elements[Name].flo2 is not  None :
                    f = self.elements[Name].flo2
                    SetName.elements[p].inc_float(f)
                if self.elements[Name].flo3 is not  None :
                    f = self.elements[Name].flo3
                    SetName.elements[p].inc_float(f)
                if self.elements[Name].flo4 is not  None :
                    f = self.elements[Name].flo4
                    SetName.elements[p].inc_float(f)
                if self.elements[Name].flo5 is not  None :
                    f = self.elements[Name].flo5
                    SetName.elements[p].inc_float(f)
                if self.elements[Name].flo6 is not  None :
                    f = self.elements[Name].flo6
                    SetName.elements[p].inc_float(f)
        if self.elements[Name].flo is not None :
            temp.copy_El_float(Name, self.elements[Name])
            #print temp.__call__(Name)
            temp.change_float_yaos(Name, 'C'+Name)
            for p in SetName.elements:
                if temp.compare_Els(temp.elements['C'+Name], SetName.elements[p]) :
                    SetName.elements[p].inc_R()
                    #print temp.__call__('C'+Name)
        
            
                
    def calc_stats_in_set(self, SetName):
        """calculates statistics in set using BA model""" 
        NPWtotal = 0
        NPRtotal = 0
        for p in SetName.elements:
            if SetName.elements[p].NPW is not None :
                NPWtotal += SetName.elements[p].NPW
            if SetName.elements[p].NPR is not None :
                NPRtotal += SetName.elements[p].NPR
        #print NPWtotal
        #print NPRtotal
        for p in SetName.elements:
            if SetName.elements[p].NPW is not None :
                SetName.elements[p].stat_model = "BA"
                SetName.elements[p].PW = SetName.elements[p].NPW/NPWtotal
                if SetName.elements[p].NP0 is None :
                    SetName.elements[p].NP0 = 0
                if SetName.elements[p].NP1 is None :
                    SetName.elements[p].NP1 = 0
                if SetName.elements[p].NP2 is None :
                    SetName.elements[p].NP2 = 0
                if SetName.elements[p].NP3 is None :
                    SetName.elements[p].NP3 = 0
                if SetName.elements[p].NP4 is None :
                    SetName.elements[p].NP4 = 0
                if SetName.elements[p].NP5 is None :
                    SetName.elements[p].NP5 = 0
                if SetName.elements[p].NP6 is None :
                    SetName.elements[p].NP6 = 0
                                    
                Ntotal = SetName.elements[p].NP0 +SetName.elements[p].NP1 +SetName.elements[p].NP2 +SetName.elements[p].NP3 +SetName.elements[p].NP4 +SetName.elements[p].NP5 +SetName.elements[p].NP6
                SetName.elements[p].P0 = SetName.elements[p].NP0/Ntotal
                SetName.elements[p].P1 = SetName.elements[p].NP1/Ntotal
                SetName.elements[p].P2 = SetName.elements[p].NP2/Ntotal
                SetName.elements[p].P3 = SetName.elements[p].NP3/Ntotal
                SetName.elements[p].P4 = SetName.elements[p].NP4/Ntotal
                SetName.elements[p].P5 = SetName.elements[p].NP5/Ntotal
                SetName.elements[p].P6 = SetName.elements[p].NP6/Ntotal
                
                SetName.elements[p].Pall = SetName.elements[p].P1*SetName.elements[p].P2*SetName.elements[p].P3*SetName.elements[p].P4*SetName.elements[p].P5*SetName.elements[p].P6
                
                
            if SetName.elements[p].NPR is not None :
                SetName.elements[p].PR = SetName.elements[p].NPR/NPRtotal
    
    def export_set_stats(self, SetName, FileName): 
        """export Set stats to CSV file"""
        sep = ','
        f = open(FileName,'w')
        f.write('Name '+sep+'Number '+sep+'stat_model'+sep+'PW '+sep+'NPW '+sep+'PR '+sep+'NPR '+sep+'P0 '+sep+'P1 '+sep+'P2 '+sep+'P3 '+sep+'P4 '+sep+'P5 '+sep+'P6 '+sep+'Pall '+sep+'NP0 '+sep+'NP1 '+sep+'NP2 '+sep+'NP3 '+sep+'NP4 '+sep+'NP5 '+sep+'NP6 ')
        f.write('\n')
        for p in SetName.elements:
            if SetName.elements[p].NPW is not None or SetName.elements[p].NPR is not None :
                f.write(SetName.elements[p].Name+' '+sep)
                f.write(str(SetName.elements[p].HNumber)+' '+sep)
                f.write(str(SetName.elements[p].stat_model)+' '+sep)
                f.write(str(SetName.elements[p].PW)+' '+sep)
                f.write(str(SetName.elements[p].NPW)+' '+sep)
                f.write(str(SetName.elements[p].PR)+' '+sep)
                f.write(str(SetName.elements[p].NPR)+' '+sep)
                f.write(str(SetName.elements[p].P0)+' '+sep)
                f.write(str(SetName.elements[p].P1)+' '+sep)
                f.write(str(SetName.elements[p].P2)+' '+sep)
                f.write(str(SetName.elements[p].P3)+' '+sep)
                f.write(str(SetName.elements[p].P4)+' '+sep)
                f.write(str(SetName.elements[p].P5)+' '+sep)
                f.write(str(SetName.elements[p].P6)+' '+sep)
                f.write(str(SetName.elements[p].Pall)+' '+sep)
                f.write(str(SetName.elements[p].NP0)+' '+sep)
                f.write(str(SetName.elements[p].NP1)+' '+sep)
                f.write(str(SetName.elements[p].NP2)+' '+sep)
                f.write(str(SetName.elements[p].NP3)+' '+sep)
                f.write(str(SetName.elements[p].NP4)+' '+sep)
                f.write(str(SetName.elements[p].NP5)+' '+sep)
                f.write(str(SetName.elements[p].NP6)+' '+sep)
                f.write('\n')
                
                
        f.close()
                    

    def print_by_Number(self, HN, Hset):
        """prints hexagram by number"""
        for e in Hset.elements :
            #print str(Hset.elements[e].HNumber)
            if Hset.elements[e].HNumber == HN :
                print Hset.elements[e].__str__()
                    
                
    def check_int_rels(self, Name):
        """checking relationships between yaos in hexagram"""
        if self.if_El_hex(Name) :
            print "Checking : Odd Yao - Yin, Even Yao - Yang \n"
            if self.elements[Name].Y6 == 0 :
                print "Top Yao - Yin - True  -- correct position\n"
            else : print "Top Yao - Yin - False \n"
            if self.elements[Name].Y5 == 1 :
                print "5th Yao - Yang - True -- correct position \n"
            else : print "5th Yao - Yang - False \n"
            if self.elements[Name].Y4 == 0 :
                print "4th Yao - Yin - True -- correct position \n"
            else : print "4th Yao - Yin - False \n"
            if self.elements[Name].Y3 == 1 :
                print "3d Yao - Yang - True -- correct position\n"
            else : print "3d Yao - Yang - False \n"
            if self.elements[Name].Y2 == 0 :
                print "2nd Yao - Yin - True -- correct position\n"
            else : print "2nd Yao - Yin - False \n"
            if self.elements[Name].Y1 == 1 :
                print "1st Yao - Yang - True -- correct position\n"
            else : print "1st Yao - Yang - False \n"
            print "\n"
            print "Checking : Ying yao Correlations : 1 - 4, 2 - 5, 3 - 6 \n"
            if self.elements[Name].Y3 == 1 and self.elements[Name].Y6 == 1 :
                print "3 - 6 : both Yang -- bu Ying \n"
            elif self.elements[Name].Y3 == 0 and self.elements[Name].Y6 == 0 :
                print "3 - 6 : both Yin -- bu Ying\n"
            elif self.elements[Name].Y3 == 1 and self.elements[Name].Y6 == 0 :
                print "3 - 6 : Yang -  Yin -- Zheng Ying\n"
            elif self.elements[Name].Y3 == 0 and self.elements[Name].Y6 == 1 :
                print "3 - 6 : Yin - Yang -- Zheng Ying \n"
            
            if self.elements[Name].Y2 == 1 and self.elements[Name].Y5 == 1 :
                print "2 - 5 : both Yang -- bu Ying\n"
            elif self.elements[Name].Y2 == 0 and self.elements[Name].Y5 == 0 :
                print "2 - 5 : both Yin -- bu Ying\n"
            elif self.elements[Name].Y2 == 1 and self.elements[Name].Y5 == 0 :
                print "2 - 5 : Yang -  Yin -- Zheng Ying\n"
            elif self.elements[Name].Y2 == 0 and self.elements[Name].Y5 == 1 :
                print "2 - 5 : Yin - Yang -- Zheng Ying \n"
            
            if self.elements[Name].Y1 == 1 and self.elements[Name].Y4 == 1 :
                print "1 - 4 : both Yang -- bu Ying\n"
            elif self.elements[Name].Y1 == 0 and self.elements[Name].Y4 == 0 :
                print "1 - 4 : both Yin -- bu Ying\n"
            elif self.elements[Name].Y1 == 1 and self.elements[Name].Y4 == 0 :
                print "1 - 4 : Yang -  Yin -- Zheng Ying\n"
            elif self.elements[Name].Y1 == 0 and self.elements[Name].Y4 == 1 :
                print "1 - 4 : Yin - Yang -- Zheng Ying \n"
            print "\n"
            
            print "Checking : Juxtapositions - yao correlations : 1 - 2, 2 - 3, 3 - 4, 4 - 5, 5 - 6 \n"
            
            if self.elements[Name].Y5 == 1 and self.elements[Name].Y6 == 1 :
                print "5 - 6 : both Yang -- bu bi\n "
            elif self.elements[Name].Y5 == 0 and self.elements[Name].Y6 == 0 :
                print "5 - 6 : both Yin -- bu bi\n"
            elif self.elements[Name].Y5 == 1 and self.elements[Name].Y6 == 0 :
                print "5 - 6 : Yang -  Yin -- Zheng bi\n"
            elif self.elements[Name].Y5 == 0 and self.elements[Name].Y6 == 1 :
                print "5 - 6 : Yin - Yang -- Zheng bi\n"
            
            if self.elements[Name].Y4 == 1 and self.elements[Name].Y5 == 1 :
                print "4 - 5 : both Yang -- bu bi\n"
            elif self.elements[Name].Y4 == 0 and self.elements[Name].Y5 == 0 :
                print "4 - 5 : both Yin -- bu bi\n"
            elif self.elements[Name].Y4 == 1 and self.elements[Name].Y5 == 0 :
                print "4 - 5 : Yang -  Yin -- Zheng bi\n"
            elif self.elements[Name].Y4 == 0 and self.elements[Name].Y5 == 1 :
                print "4 - 5 : Yin - Yang -- Zheng bi\n"
            
            if self.elements[Name].Y3 == 1 and self.elements[Name].Y4 == 1 :
                print "3 - 4 : both Yang -- bu bi\n"
            elif self.elements[Name].Y3 == 0 and self.elements[Name].Y4 == 0 :
                print "3 - 4 : both Yin -- bu bi\n"
            elif self.elements[Name].Y3 == 1 and self.elements[Name].Y4 == 0 :
                print "3 - 4 : Yang -  Yin -- Zheng bi\n"
            elif self.elements[Name].Y3 == 0 and self.elements[Name].Y4 == 1 :
                print "3 - 4 : Yin - Yang -- Zheng bi\n"
            
            if self.elements[Name].Y1 == 2 and self.elements[Name].Y3 == 1 :
                print "2 - 3 : both Yang -- bu bi\n"
            elif self.elements[Name].Y2 == 0 and self.elements[Name].Y3 == 0 :
                print "2 - 3 : both Yin -- bu bi\n"
            elif self.elements[Name].Y2 == 1 and self.elements[Name].Y3 == 0 :
                print "2 - 3 : Yang -  Yin -- Zheng bi\n"
            elif self.elements[Name].Y2 == 0 and self.elements[Name].Y3 == 1 :
                print "2 - 3 : Yin - Yang -- Zheng bi\n"
                
            if self.elements[Name].Y1 == 1 and self.elements[Name].Y2 == 1 :
                print "1 - 2 : both Yang -- bu bi\n"
            elif self.elements[Name].Y1 == 0 and self.elements[Name].Y2 == 0 :
                print "1 - 2 : both Yin -- bu bi\n"
            elif self.elements[Name].Y1 == 1 and self.elements[Name].Y2 == 0 :
                print "1 - 2 : Yang -  Yin -- Zheng bi\n"
            elif self.elements[Name].Y1 == 0 and self.elements[Name].Y2 == 1 :
                print "1 - 2 : Yin - Yang -- Zheng bi\n"
            print "\n"
            
            
            
            
                
            
            
            
            
            
         
    def add_from_gua(self, Name, Lower, Upper, baguaset):
        """adds hexagram from Lower and Upper gua from baguaset"""
        e = Element(Name, baguaset.elements[Lower].Y1,
        baguaset.elements[Lower].Y2,
        baguaset.elements[Lower].Y3,
        baguaset.elements[Upper].Y1,
        baguaset.elements[Upper].Y2,
        baguaset.elements[Upper].Y3)
        self.elements[Name]= e
        
    def add_from_duo(self, Name, Lower, Middle, Upper, duoset):
        """adds hexagram from Loer and Upper gua from baguaset"""
        e = Element(Name, duoset.elements[Lower].Y1,
        duoset.elements[Lower].Y2,
        duoset.elements[Middle].Y1,
        duoset.elements[Middle].Y2,
        duoset.elements[Upper].Y1,
        duoset.elements[Upper].Y2)
        self.elements[Name]= e
        
    def div_to_gua(self,Name, Lower, Upper):
        """divide element Name to upper and lower gua and
        adds the as separate elements to current group"""
        if self.elements[Name].if_hex() :
            l=Element(Lower, self.elements[Name].Y1,
                      self.elements[Name].Y2,
                      self.elements[Name].Y3)
            self.elements[Lower]= l
            u=Element(Upper, self.elements[Name].Y4,
                      self.elements[Name].Y5,
                      self.elements[Name].Y6)
            self.elements[Upper]= u
            
    def div_to_duo(self,Name,Lower,Middle,Upper):
        """divide element Name to upper ,middle and lower duo and
        adds the as separate elements to current group"""
        if self.elements[Name].if_hex() :
            l=Element(Lower, self.elements[Name].Y1,
                      self.elements[Name].Y2)
            self.elements[Lower]= l
            m=Element(Middle, self.elements[Name].Y3,
                      self.elements[Name].Y4)
            self.elements[Middle]= m
            u=Element(Upper, self.elements[Name].Y5,
                      self.elements[Name].Y6)
            self.elements[Upper]= u
        
            
        
    def add_byN_from_set(self, Name, N, set):
        """adds hexagram by number from set"""
        i = 0
        for p in set.elements:
            if N == set.elements[p].HNumber :
                self.basic_copy(Name, set.elements[p])
                print "one element added"
                i = i +1
        if i == 0 :
            print "Nothing corresponding found"
        elif i > 1 : print "More than one found"
        
    def add_all_from_set(self, set):
        """adds all elements from set to working set"""
        for p in set.elements:
            self.basic_copy(set.elements[p].Name, set.elements[p])
            self.copy_properties(set.elements[p].Name, set.elements[p])
            self.copy_yao_properties(set.elements[p].Name, set.elements[p])
        
    def plot_El_test(self,ax,Name,x0,y0,xS,yS,dm,lw1=None,lw2=None,ecolor=None):
        """ test for element plot ax-sublpot, Name - element name 
        x0 y0 -corrds for left lower corner(start point)
        xS yS - size x and y
        dm - margin space to the edges of xSyS square
        ecolor - color
        lw1 - line width
        lw2 - space width"""
        
        line= xS-4*dm
        dline = line/9
        d = (yS-2*dm)/6
        
        x = x0 + dm
        y = y0 + dm 
        
        if lw1 is None:
            lw1 = 4
        if lw2 is None:
            lw2 = 5
        
        
        
        kr = range(1,7)
        
        l={}
        if self.elements[Name].Y1 is not None :
            l[1] = self.elements[Name].Y1
        else : l[1] = -1
        if self.elements[Name].Y2 is not None :
            l[2] = self.elements[Name].Y2
        else : l[2] = -1
        if self.elements[Name].Y3 is not None :
            l[3] = self.elements[Name].Y3
        else : l[3] = -1
        if self.elements[Name].Y4 is not None :
            l[4] = self.elements[Name].Y4
        else : l[4] = -1
        if self.elements[Name].Y5 is not None :
            l[5] = self.elements[Name].Y5
        else : l[5] = -1
        if self.elements[Name].Y6 is not None :
            l[6] = self.elements[Name].Y6
        else : l[6] = -1
        
        if ecolor is None :
            ecolor = 'k'
        
        for k in kr :
            yw = y + (k-1)*d
            
            if l[k] != -1 :
                if l[k] == 1:
                    ax.plot([x,x+line],[yw,yw],color=ecolor,lw=lw1)
                else : 
                    ax.plot([x,x+line],[yw,yw],color=ecolor,lw=lw1)
                    ax.plot([x+4*dline,x+5*dline],[yw,yw],color='w',lw=lw2)
                    
    def plot_h_by_number(self,N,hset):  
        """plots hexagram by N and saves to N.png file"""  
        self.add_byN_from_set("h1",N,hset)


        ax=plt.subplot(111)
        ax.axis('equal')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)


        ax.plot([0,1.5],[0,0],color='w',lw=4)
        ax.plot([0,0],[0,1.5],color='w',lw=4)
        ax.plot([0,1.5],[1.5,1.5],color='w',lw=4)
        ax.plot([1.5,1.5],[0,1.5],color='w',lw=4)


        self.plot_El_test(ax,'h1',0,0,2,2,0.2,10,13,ecolor='k')

        plt.draw()
        fname = str(N)+'.png'
        plt.savefig(fname, bbox_inches='tight')
        
    def plot_square_test(self, Name1=None,Name2=None,ecolor=None):
        """plots square and 2 elements"""
        ax=plt.subplot(111)
        ax.axis('equal')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)



        ax.plot([2,8],[2,2],color='k',lw=4)
        ax.plot([2,2],[2,8],color='k',lw=4)
        ax.plot([2,8],[8,8],color='k',lw=4)
        ax.plot([8,8],[2,8],color='k',lw=4)

        ax.plot([0,10],[0,0],color='w',lw=4)
        ax.plot([0,0],[0,10],color='w',lw=4)
        ax.plot([0,10],[10,10],color='w',lw=4)
        ax.plot([10,10],[0,10],color='w',lw=4)
        
        if ecolor is None :
            ecolor = 'k'

        if Name1 is not None:
            self.plot_El_test(ax,Name1,4,2,2,2,0.2,ecolor)
        if Name2 is not None:
            self.plot_El_test(ax,Name2,6,6,2,2,0.2,ecolor)
        #self.plot_El_test(ax,Name2,4,2,2,2,0.2,ecolor)

        plt.draw()
        plt.show()
   
        
    
        
    def polar_plot_test(self,ax,Name,cc,d,Si,N=None,n=None):
        """test for polar plot"""
        w=np.pi/(2*N)
        
        #cc = np.pi - np.pi*(n-1)/N

        kr = range(1,7)
 
        q1 = cc +w 
        q2 = cc -w 
        
        l={}
        if self.elements[Name].Y1 is not None :
            l[1] = self.elements[Name].Y1
        else : l[1] = -1
        if self.elements[Name].Y2 is not None :
            l[2] = self.elements[Name].Y2
        else : l[2] = -1
        if self.elements[Name].Y3 is not None :
            l[3] = self.elements[Name].Y3
        else : l[3] = -1
        if self.elements[Name].Y4 is not None :
            l[4] = self.elements[Name].Y4
        else : l[4] = -1
        if self.elements[Name].Y5 is not None :
            l[5] = self.elements[Name].Y5
        else : l[5] = -1
        if self.elements[Name].Y6 is not None :
            l[6] = self.elements[Name].Y6
        else : l[6] = -1
        
 
        for k in kr :
            dr = d +k*Si
            q1 = cc +w  #-Si*np.sin(cc-w)*k/6
            q2 = cc -w  #+Si*np.sin(cc-w)*k/6
            if l[k] != -1 :
                if l[k] == 1:
                      ax.plot([q1,q2],[dr,dr],color='k',lw=4)
                else : 
                    
                    q3 = cc +w/12
                    q4 = cc -w/12
                    ax.plot([q1,q2],[dr,dr],color='k',lw=4)
                    ax.plot([q3,q4],[dr,dr],color='w',lw=12)
                    
            #print k
            #print dr
            #print q1
            #print q2

        ax.plot([q1,q2],[dr+dr*0.3,dr+dr*0.3],color='w',lw=4)
        
        s = self.elements[Name].Name
    
        ax.text(cc, dr+dr*0.3*np.sin(cc/2)*np.sign(np.sin(cc/2)), str(Name))
        #ax.text(cc, dr+dr*0.3*np.sin(cc/2)*np.sign(np.sin(cc/2)),  s ,size= 25, fontproperties = ChineseFont2)
        
        plt.draw()
        
    def plot_arrow_test(self,ax,q1,q2,r1,r2,dir=None):
        """plots arrow"""
        ax.plot([q1,q2],[r1,r2],color='k',lw=2)
        if dir  == None :
            dir =1 #arrows direction

        if dir == 1:
            
            ah1 = q2 + dir*np.abs(q2-q1)/10
            adr1 = r2 #+ dr/30

            ah2 = q2 + dir*np.abs(q2-q1)/10
            adr2 = r2

            ax.plot([ah1,q2],[adr1,r2],color='k',lw=3)
            #ax.plot([ah2,q2],[adr2,dr],color='k',lw=2)
        elif dir == -1 :
            ah1 = q1 + dir*np.abs(q2-q1)/10
            adr1 = r1 #+ dr/30

            ah2 = q1 + dir*np.abs(q2-q1)/10
            adr2 = r1

            ax.plot([ah1,q1],[adr1,r1],color='k',lw=3)
            #ax.plot([ah2,q2],[adr2,dr],color='k',lw=2)
            
        
    
        
        
        
        
    def dice(self, Name, octdice1, octdice2, hexdice, Bset, Hset):
        """forms a hexagram from dice - 1st -  octagonal (1-8) -lower trigramm,
         second -(1-8)-upper, hexagonal- (1-6) -moving line, 
         Bset - baguaset, Hset - hexagram set
         then basic info from Hset is added"""
        l = ["Qian","Zhen","Kan","Gen","Kun","Xun","Li","Dui"]
        Upper = l[octdice2-1]
        Lower = l[octdice1-1]
        self.add_from_gua(Name, Lower, Upper, Bset)
        #self.add_float_yao(Name, hexdice)
        self.find_in_set(Name, Name, Hset)
        self.add_float_yao(Name, hexdice) # floating dice should be added after the main info about hexagram is copied from set
    

        
    def sim_dice_st1(self, Name, Bset, Hset):
        """simulated dice using python random 
        - do not use  for research only
        fast version"""
        oct1 = random.randint(1,8)
        oct2 = random.randint(1,8)
        hex1 = random.randint(1,6)
        
        #print str(oct1)+" "+str(oct2)+ " "+str(hex)+" \n"
        self.dice(Name, int(oct1), int(oct2), int(hex1), Bset, Hset)
        self.update_stats_in_set(Name, Hset)
        
        
    
    def sim_coins_st(self, Name, Hset):
        """simulate Jing Fang's coins using python random 
        - do not use  for research only
        - fast version"""
        c = []
        #print "simulating coins... \n"  
        for i in range(18):
            e = random.randint(0,1)
            c.append(e)
            #if e == 0 :
            #    print "Tail"
            #else : print "Head"
        #print '\n'
        
        self.coins(Name, c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10], c[11], c[12], c[13], c[14], c[15], c[16], c[17], Hset)
        self.update_stats_in_set(Name, Hset)
        
    
    def sim_dice_fw(self, Name, Bset, Hset):
        
        """ simulated dice using python random - win version"""
        mseed = int((time.time()+os.getpid()*70000))
        random.seed(mseed)
        print "simulating dice... "
        oct1 = random.randint(1,8)
        oct2 = random.randint(1,8)
        hex = random.randint(1,6)
        
        print str(oct1)+" "+str(oct2)+ " "+str(hex)+" \n"
        self.dice(Name, int(oct1), int(oct2), int(hex), Bset, Hset)
        
        print "result : \n"
        
        print self.__call__(Name)
        
        
    def sim_coins_fw(self,  Name, Hset ):
        """simulate Jing Fang's coins using python ramdom - win resion"""
        mseed = int((time.time()+os.getpid()*70000))
        random.seed(mseed)
        
        c = []
        print "simulating coins... \n"  
        for i in range(18):
            e = random.randint(0,1)
            c.append(e)
            if e == 0 :
                print "Tail"
            else : print "Head"
        print '\n'
        
        self.coins(Name, c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10], c[11], c[12], c[13], c[14], c[15], c[16], c[17], Hset)

        print "result : \n"
        
        print self.__call__(Name)
               
        
             
        

   
        
        
        
        
        
    def coins(self, Name, c1,c2,c3, c4,c5,c6, c7,c8,c9, c10,c11,c12, c13,c14,c15, c16,c17,c18,Hset ): 
        """ forms a hexagram from coins - 3 coin tossed 6 times
        each time 1 for Head or 0 for tail is entered separated by comma , 
        18 numbers total, then the name of hexagram set
        then basic info from Hset is added"""
        s1 = 6 + c1 +c2 +c3 
        s2 = 6 + c4 + c5 +c6
        s3 = 6 + c7 + c8 + c9
        s4 = 6 + c10 +c11 +c12
        s5 = 6 + c13 + c14 + c15
        s6 = 6 + c16 + c17 + c18
        
        flo = None
        flo2 = None
        flo3 = None
        flo4 = None
        flo5 = None
        flo6 = None
        
        if s1 == 6 :
            Y1 = 0
            flo = 1
        elif s1 == 7 :
            Y1 = 1
        elif s1 == 8 :
            Y1 = 0
        elif s1 == 9 :
            Y1 = 1
            flo = 1
            
            
        if s2 == 6 :
            Y2 = 0
            if flo is None :
                flo = 2
            else : flo2 = 2
            
        elif s2 == 7 :
            Y2 = 1
        elif s2 == 8 :
            Y2 = 0
        elif s2 == 9 :
            Y2 = 1
            if flo is None :
                flo = 2
            else : flo2 = 2
        
        if s3 == 6 :
            Y3 = 0
            if flo is None :
                flo = 3
            elif flo2 is None :
                flo2 = 3
            else : flo3 = 3
            
        elif s3 == 7 :
            Y3 = 1
        elif s3 == 8 :
            Y3 = 0
        elif s3 == 9 :
            Y3 = 1
            if flo is None :
                flo = 3
            elif flo2 is None :
                flo2 = 3
            else : flo3 = 3
            
            
        if s4 == 6 :
            Y4 = 0
            if flo is None :
                flo = 4
            elif flo2 is None :
                flo2 = 4
            elif flo3 is None :
                flo3 = 4
            else : flo4 = 4
        elif s4 == 7 :
            Y4 = 1
        elif s4 == 8 :
            Y4 = 0
        elif s4 == 9 :
            Y4 = 1
            if flo is None :
                flo = 4
            elif flo2 is None :
                flo2 = 4
            elif flo3 is None :
                flo3 = 4
            else : flo4 = 4
        
        if s5 == 6 :
            Y5 = 0
            if flo is None :
                flo = 5
            elif flo2 is None :
                flo2 = 5
            elif flo3 is None :
                flo3 = 5
            elif flo4 is None :
                flo4 = 5
            else : flo5 = 5
        elif s5 == 7 :
            Y5 = 1
        elif s5 == 8 :
            Y5 = 0
        elif s5 == 9 :
            Y5 = 1
            if flo is None :
                flo = 5
            elif flo2 is None :
                flo2 = 5
            elif flo3 is None :
                flo3 = 5
            elif flo4 is None :
                flo4 = 5
            else : flo5 = 5
            
        if s6 == 6 :
            Y6 = 0
            if flo is None :
                flo = 6
            elif flo2 is None :
                flo2 = 6
            elif flo3 is None :
                flo3 = 6
            elif flo4 is None :
                flo4 = 6
            elif flo5 is None :
                flo5 = 6
            else : flo6 = 6
        elif s6 == 7 :
            Y6 = 1
        elif s6 == 8 :
            Y6 = 0
        elif s6 == 9 :
            Y6 = 1
            if flo is None :
                flo = 6
            elif flo2 is None :
                flo2 = 6
            elif flo3 is None :
                flo3 = 6
            elif flo4 is None :
                flo4 = 6
            elif flo5 is None :
                flo5 = 6
            else : flo6 = 6 
        
        self.add(Name,Y1,Y2,Y3,Y4,Y5,Y6)
        self.find_in_set(Name, Name, Hset)
        if flo is not None :
            self.add_float_yao(Name, flo, flo2, flo3, flo4, flo5, flo6)
            
        
         
    def HsienTien(self,Name,Year,Month,Day,Hour,bset,hset):
        """Hsien Tien devination method -Year -YYYY, Month 1-12, Day 1-31, Hour 1-24"""
        l=['Qian','Dui','Li','Zhen','Xun','Kan','Gen','Kun']
        ChYear = Year%12
        if ChYear == 0 :
            ChYear = 12
        print ' Year : '+str(Year)+', Month : '+str(Month)+', Day : '+str(Day)+', Hour : '+str(Hour)+'\n'
        up = (ChYear+Month+Day)%8
        if up == 0 :
            up = 8
        low = (ChYear+Month+Day+Hour)%8
        if low == 0 :
            low = 8
        fl = (ChYear+Month+Day+Hour)%6
        if fl == 0 :
            fl = 6
        Lower = l[low-1]
        Upper = l[up-1]
        self.add_from_gua(Name, Lower, Upper, bset)
        self.find_in_set(Name, Name, hset)
        self.add_float_yao(Name, fl)
        print "result : \n"
        
        print self.__call__(Name)
        
        
    def HuTien(self,Name,EventGua,DirectonGua,Hour,Dpos,bset,hset): 
        """Hu Tien devination method - consult bagua properties to 
        find EventGua and direction property to find Direction Gua, hour -(1-24),
         Dpos -position of deviner: 1-sitting, 2-standing,3-moving"""
        l=['Qian','Dui','Li','Zhen','Xun','Kan','Gen','Kun']
        NN = {'Qian':1,'Dui':2,'Li':3,'Zhen':4,'Xun':5,'Kan':6,'Gen':7,'Kun':8}
        Upper = EventGua
        Lower = DirectonGua
        up = NN[Upper]
        low = NN[Lower]
        fl = (up + low + Hour)%6
        if fl == 0 :
            fl = 6
            
        Rtime = up + low + Hour
        if Dpos == 1 :
            Rtime = Rtime*2
        elif Dpos == 3 :
            Rtime = Rtime/2
            
        self.add_from_gua(Name, Lower, Upper, bset)
        self.find_in_set(Name, Name, hset)
        self.add_float_yao(Name, fl)
        print "result : \n"
        
        print self.__call__(Name)
        
        print 'expectation time: '+str(Rtime)+' days.'
        
        
    def find_JFstems(self, Name, bagua):  
        """finds stems corresponding to lower and upper gua
        according to Jing Fann classification.
        returns lower upper pair of stems separated by space""" 
        #l=['Qian','Dui','Li','Zhen','Xun','Kan','Gen','Kun']
        #NN = {'Qian':1,'Dui':2,'Li':3,'Zhen':4,'Xun':5,'Kan':6,'Gen':7,'Kun':8}
        #stems = {1:'Jia', 2:'Yi', 3:'Bing', 4:'Ding', 5:'Wu', 6:'Ji', 7:'Geng', 8:'Xin', 9:'Ren', 10:'Gui'}
        #cstems = {1:'甲',2:'乙',3:'丙',4:'丁',5:'戊',6:'己',7:'庚',8:'辛',9:'壬',10:'癸'} 
        low = {'Qian':'Jia','Dui':'Ding','Li':'Ji','Zhen':'Geng','Xun':'Xin','Kan':'Wu','Gen':'Bing','Kun':'Yi'}
        up = {'Qian':'Ren','Dui':'Ding','Li':'Ji','Zhen':'Geng','Xun':'Xin','Kan':'Wu','Gen':'Bing','Kun':'Gui'}
        
        temp = Elements()
        temp.copy_El(Name, self.elements[Name])
        temp.div_to_gua(Name, 'L'+Name, 'U'+Name)
        for e in bagua.elements :
            if temp.compare_Els(temp.elements['L'+Name], bagua.elements[e]) :
                lstem = low[bagua.elements[e].Name]
            if temp.compare_Els(temp.elements['U'+Name], bagua.elements[e]) :
                ustem = up[bagua.elements[e].Name] 
        s = lstem+' '+ustem   
        return s
        
    def find_JFbranches(self,Name,bagua):
        """finds Jing Fann branch for each Yao, returns string branches names 
        devided by space""" 
        branches = {1:'Zi', 2:'Chou', 3:'Yin', 4:'Mao', 5:'Chen', 6:'Si', 7:'Wu', 8:'Wei', 9:'Shen', 10:'You', 11:'Xu', 12:'Hai', 13:'Zi'}
        low = {'Qian':'Zi Yin Chen','Dui':'Si Mao Chou','Li':'Mao Chou Hai','Zhen':'Zi Yin Chen','Xun':'Chou Hai You','Kan':'Yin Chen Wu','Gen':'Chen Wu Shen','Kun':'Wei Si Mao'}
        up = {'Qian':'Wu Shen Xu','Dui':'Hai You Wei','Li':'You Wei Si','Zhen':'Wu Shen Xu','Xun':'Wei Si Mao','Kan':'Shen Xu Zi','Gen':'Xu Zi Yin','Kun':'Chou Hai You'}
        
        temp = Elements()
        temp.copy_El(Name, self.elements[Name])
        temp.div_to_gua(Name, 'L'+Name, 'U'+Name)
        for e in bagua.elements :
            if temp.compare_Els(temp.elements['L'+Name], bagua.elements[e]) :
                lbranch = low[bagua.elements[e].Name]
            if temp.compare_Els(temp.elements['U'+Name], bagua.elements[e]) :
                ubranch = up[bagua.elements[e].Name] 
        s = lbranch+' '+ubranch   
        return s
    
    def add_JFstemsbaranches(self,Name,bagua):
        """adds Jing Fann stems and branches to hexagram Name yaos"""
        st = self.find_JFstems(Name, bagua)
        br = self.find_JFbranches(Name, bagua)
        s = st.split(' ')[0]+' '+br.split(' ')[0]
        cs = self.get_chnames(s)
        self.elements[Name].Y1com = s+' '+cs
        s = st.split(' ')[0]+' '+br.split(' ')[1]
        cs = self.get_chnames(s)
        self.elements[Name].Y2com = s+' '+cs
        s = st.split(' ')[0]+' '+br.split(' ')[2]
        cs = self.get_chnames(s)
        self.elements[Name].Y3com = s+' '+cs
        s = st.split(' ')[1]+' '+br.split(' ')[3]
        cs = self.get_chnames(s)
        self.elements[Name].Y4com = s+' '+cs
        s = st.split(' ')[1]+' '+br.split(' ')[4]
        cs = self.get_chnames(s)
        self.elements[Name].Y5com = s+' '+cs
        s = st.split(' ')[1]+' '+br.split(' ')[5] 
        cs = self.get_chnames(s)
        self.elements[Name].Y6com = s+' '+cs
    
    def add_to_all_JFstemsbranches(self,set,bagua):
        """adds Jing Fann stems and branches to all hexagrams in set"""
        for e in set.elements :
            set.add_JFstemsbaranches(set.elements[e].Name, bagua)
        
    def get_chnames(self,s):
        """returns ch names for stem and branch"""
        stems = {1:'Jia', 2:'Yi', 3:'Bing', 4:'Ding', 5:'Wu', 6:'Ji', 7:'Geng', 8:'Xin', 9:'Ren', 10:'Gui'}

        cstems = {1:'甲',2:'乙',3:'丙',4:'丁',5:'戊',6:'己',7:'庚',8:'辛',9:'壬',10:'癸'}

        branches = {1:'Zi', 2:'Chou', 3:'Yin', 4:'Mao', 5:'Chen', 6:'Si', 7:'Wu', 8:'Wei', 9:'Shen', 10:'You', 11:'Xu', 12:'Hai', 13:'Zi'}

        cbranches = {1:'子', 2:'丑', 3:'寅', 4:'卯',5:'辰',6:'巳',7:'午',8:'未',9:'申',10:'酉',11:'戌',12:'亥',13:'子'}

        st = s.split(' ')[0]
        br = s.split(' ')[1]
        for i in range(1,11) :
            #print i
            if stems[i]==st :
                cst = cstems[i]
        for i in range(1,13) :
            #print i
            if branches[i]==br :
                cbr = cbranches[i]
        cc = cst+cbr
        return cc
        
    def reload_set_and_save(self,set,newname):
        """reloads set and saves under new name ( technical ) """  
        temp = Elements()
        temp.add_all_from_set(set)
        for e in set.elements :
            temp.copy_properties(temp.elements[e].Name, set.elements[e])
            temp.copy_yao_properties(temp.elements[e].Name, set.elements[e])
        
        save_to_file(temp, newname)
               
            
    
    
    
    def nuclear(self, Name, NucName):
        """makes nuclear hexagram and adds under NucName"""
        e = Element(NucName, self.elements[Name].Y2,
        self.elements[Name].Y3,
        self.elements[Name].Y4,
        self.elements[Name].Y3,
        self.elements[Name].Y4,
        self.elements[Name].Y5)
        self.elements[NucName]= e
        
    def invert(self, Name, InvName):
        """inverts all yaos and adds under InvName"""
        e = Element(InvName, 1-self.elements[Name].Y1,
        1-self.elements[Name].Y2,
        1-self.elements[Name].Y3,
        1-self.elements[Name].Y4,
        1-self.elements[Name].Y5,
        1-self.elements[Name].Y6)
        self.elements[InvName]= e
        
    
    def inv_keep_float(self, Name, InvName):
        """inverts all yaos but keeps floating and adds under InvName""" 
        self.change_float_yaos(Name, InvName)
        self.invert(InvName, InvName)
           
        
        
        
        
        
    def change_yao(self,Name,CGName,Yao):
        """invertes yao and adds under CGName """
        if Yao == 1 :
            e = Element(CGName,1 - self.elements[Name].Y1,
                        self.elements[Name].Y2,
                        self.elements[Name].Y3,
                        self.elements[Name].Y4,
                        self.elements[Name].Y5,
                        self.elements[Name].Y6)
            self.elements[CGName]= e
        elif Yao == 2 :
            e = Element(CGName, self.elements[Name].Y1,
                        1 - self.elements[Name].Y2,
                        self.elements[Name].Y3,
                        self.elements[Name].Y4,
                        self.elements[Name].Y5,
                        self.elements[Name].Y6)
            self.elements[CGName]= e
        elif Yao == 3 :
            e = Element(CGName, self.elements[Name].Y1,
                        self.elements[Name].Y2,
                        1 - self.elements[Name].Y3,
                        self.elements[Name].Y4,
                        self.elements[Name].Y5,
                        self.elements[Name].Y6)
            self.elements[CGName]= e
        elif Yao == 4 :
            e = Element(CGName, self.elements[Name].Y1,
                        self.elements[Name].Y2,
                        self.elements[Name].Y3,
                        1 - self.elements[Name].Y4,
                        self.elements[Name].Y5,
                        self.elements[Name].Y6)
            self.elements[CGName]= e
        elif Yao == 5 :
            e = Element(CGName, self.elements[Name].Y1,
                        self.elements[Name].Y2,
                        self.elements[Name].Y3,
                        self.elements[Name].Y4,
                        1 - self.elements[Name].Y5,
                        self.elements[Name].Y6)
            self.elements[CGName]= e
        elif Yao == 6 :
            e = Element(CGName, self.elements[Name].Y1,
                        self.elements[Name].Y2,
                        self.elements[Name].Y3,
                        self.elements[Name].Y4,
                        self.elements[Name].Y5,
                        1 - self.elements[Name].Y6)
            self.elements[CGName]= e
        
    def change_yaos(self, Name,CGName,Yao, Yao2 = None,Yao3=None,Yao4=None,Yao5=None,Yao6=None):
        """changes up to 6 yaos and adds resulting hexagram  under CGName """
        self.change_yao(Name, CGName, Yao)
        if Yao2 is not None :
            self.change_yao(CGName, CGName, Yao2)
        if Yao3 is not None :
            self.change_yao(CGName, CGName, Yao3)
        if Yao4 is not None :
            self.change_yao(CGName, CGName, Yao4)
        if Yao5 is not None :
            self.change_yao(CGName, CGName, Yao5)
        if Yao6 is not None :
            self.change_yao(CGName, CGName, Yao6)
        
    def if_float_yaos(self, Name):
        """returns true if any floating yaos"""
        if self.elements[Name].flo is not None or self.elements[Name].flo2 is not None or self.elements[Name].flo3 is not None or self.elements[Name].flo4 is not None or self.elements[Name].flo5 is not None or self.elements[Name].flo6 is not None :
            return True
        else :
            return False
        
          
            
    def change_float_yaos(self, Name, CGName):
        """changes floating yaos in Name and saves under CGName"""
        if self.elements[Name].flo is not None :
            self.change_yao(Name, CGName, self.elements[Name].flo)
        if self.elements[Name].flo2 is not None :
            self.change_yao(CGName, CGName, self.elements[Name].flo2)
        if self.elements[Name].flo3 is not None :
            self.change_yao(CGName, CGName, self.elements[Name].flo3)
        if self.elements[Name].flo4 is not None :
            self.change_yao(CGName, CGName, self.elements[Name].flo4)
        if self.elements[Name].flo5 is not None :
            self.change_yao(CGName, CGName, self.elements[Name].flo5)
        if self.elements[Name].flo6 is not None :
            self.change_yao(CGName, CGName, self.elements[Name].flo6)
            
    def change_float_print(self,Name, CGName, hset):
        """changes floating yaos in Name gets info from hset and prints it"""
        self.change_float_yaos(Name, CGName)
        self.find_in_set(CGName, CGName, hset)
        print self.__call__(CGName)
            
    def changeYao_set(self,Name):
        """forms a set of 6 hexagram - each yao of Name is changed
        names :  Name + N yao changed"""
        if self.elements[Name].Y1 is not None:
            self.change_yao(Name, Name + " 1st yao changed", 1)
        if self.elements[Name].Y2 is not None:
            self.change_yao(Name, Name + " 2nd yao changed", 2)
        if self.elements[Name].Y3 is not None:
            self.change_yao(Name, Name + " 3d yao changed", 3)
        if self.elements[Name].Y4 is not None:
            self.change_yao(Name, Name + " 4th yao changed", 4)
        if self.elements[Name].Y5 is not None:
            self.change_yao(Name, Name + " 5th yao changed", 5)
        if self.elements[Name].Y1 is not None:
            self.change_yao(Name, Name + " top yao changed", 6)
            
    def all_add_info_from_set(self, SetName):
        """adds to all hexagram in the set info from SetName"""
        for p in self.elements:
            self.find_in_set(self.elements[p].Name, self.elements[p].Name, SetName)
            
    def show_hextable(self,Bset, Hset):
        """displays hexagram table """
        l = ["Qian","Zhen","Kan","Gen","Kun","Xun","Li","Dui"]
        temp=Elements()
        s=""
        s=s+"    upper->"
        for i in range(len(l)):
            s=s+"     "+Bset.elements[l[i]].Ucode+" "+Bset.elements[l[i]].Name
       
        s=s+'\n'
        s=s+'    lower\n'
        for k in range(len(l)):
            s=s+"    "+Bset.elements[l[k]].Ucode+" "+Bset.elements[l[k]].Name
            if Bset.elements[l[k]].Name == "Li" :
                s=s+"  "
            if len(Bset.elements[l[k]].Name) == 3 :
                s=s+" "
            for j in range(len(l)):
                temp.add_from_gua(l[k]+" "+l[j], l[k], l[j], Bset)
                temp.find_in_set(l[k]+" "+l[j],l[k]+" "+l[j], Hset)
                
                #print temp(l[k]+" "+l[j])
                #temp.add_from_gua(k+j, Bset.elements[l[k]].Name, Bset.elements[l[j]].Name, Bset)
                s=s+"  "+temp.elements[l[k]+" "+l[j]].print_n_ucode()
                if temp.elements[l[k]+" "+l[j]].HNumber // 10 == 0 :
                    s=s+" "
            s=s+'\n'
            s=s+'\n'
                
        
        print s
           
        
        
        
            
        
        
        
        

        
            
        
        
        
    def get_ElCrdatetime(self, Name):
        """Gives the time of the creation of the element. """
        s = self.elements[Name].get_crdatetime()
        return s
        
    def add_ElProperty(self, Name, PrName, PrValue):
        """Adds the property to the element.
        Element Name, Property name and Property value should be indicated.
        like add_ElProperty("Qian","Season","early October mid-December") """
        self.elements[Name].add_property(PrName, PrValue)
        
    def add_ElProperty_from_file(self, Name, PrName, fname):
        """adds property from file fname"""
        s = ''
        with open(fname) as f:
            for line in f:
                s += line
                
        self.add_ElProperty(Name, PrName, s)
        
    def batch_add_ElProperty(self,PrName,Dir=None):
        """(adds to current set property PrName from the files in current dir or directory Dir. 
        name of the file should correspond N of hexagram"""
        for e in self.elements :
            Name = self.elements[e].Name 
            HN = self.elements[e].HNumber
            fname = str(HN)
            if Dir is not None:
                fname = Dir + fname
            self.add_ElProperty_from_file(Name, PrName, fname)
    
    def batch_del_ElProperty(self,PrName):
        """deletes given property for current set""" 
        for e in self.elements :
            Name = self.elements[e].Name 
            self.del_ElProperty(Name, PrName)
            
    def batch_ren_ElProperty(self,PrName,PrNameN):
        """renames given property in current set"""
        for e in self.elements :
            Name = self.elements[e].Name 
            PrValue = self.elements[Name].ElProperties[PrName].PrValue            
            self.elements[Name].add_property(PrNameN, PrValue)
            self.del_ElProperty(Name, PrName)
        
            
  
        
    def del_ElProperty(self, Name, PrName):
        """Deletes prperty PrNmae of element Name """
        self.elements[Name].del_property(PrName)
        
    def edit_ElProperty(self, Name, PrName, PrNewValue):
        """Edit the Property - PrNewValue is assigned to the PrValue field"""
        self.elements[Name].edit_property(PrName, PrNewValue)
        
    def copy_ElProperty(self, Name, PrName, El):
        """copies the property PrName from element El to Name element"""
        PrValue = El.print_property(PrName)
        self.add_ElProperty(Name, PrName, PrValue)
    
    def get_ElProperty(self,Name,PrName): 
        """ returns value of element's Name property PrName"""
        PrValue = self.elements[Name].get_property(PrName)
        return PrValue
        
        
    
    def find_in_ElProperties(self, Name, SearchStr):
        """find searchstr in element Name properties"""
        return self.elements[Name].find_in_properties(SearchStr)
        
    
    def find_in_set_properties(self, SearchStr, FoundName, set):
        """finds searchstr in all elements properties in set
        if found printed and  added to the current set under FoundName + elementName"""
        for e in set.elements :
            l = set.find_in_ElProperties(set.elements[e].Name, SearchStr)
            if l is not None :
                for p in l :
                    prname = p
                    prvalue = l[p]
                    print "found in element: "+str(set.elements[e].Name)+"\n"
                    print "in property: "+str(prname)+"\n"
                    #print "value: "+str(prvalue) +"\n"
                    self.copy_El(set.elements[e].Name, set.elements[e])
                    self.find_in_set(self.elements[e].Name, FoundName+set.elements[e].Name, set)
                    self.delete(set.elements[e].Name)
                    #PrValue = set.elements[e].print_property(prname)
                    #self.add_ElProperty(FoundName+set.elements[e].Name, prname , PrValue)
                    print self.__call__(FoundName+set.elements[e].Name)
                
    def find_in_set_add_property(self, SearchStr, PrName, PrValue, set):
        """finds searchstr in all elements properties in set
        if found adds property Prname and value prvalue"""
        for e in set.elements :
            l = set.find_in_ElProperties(set.elements[e].Name, SearchStr)
            if l is not None : 
                for p in l :
                    set.add_ElProperty(set.elements[e].Name, PrName, PrValue)
                    print str(set.elements[e].Name)+"\n"    
                l = None
        
    def print_ElProperty(self, Name, PrName):
        """Gives Property for the Element"""
        s = str(self.elements[Name].print_property(PrName))
        return s
    
    
    def inflate_branches_group(self,branches,s):
        """inflates a group of elements for branches (technical)
        s - stemsbranches object"""
        for i in range(1,13):
            branches.add(s.branches[i])
            branches.add_ElChname(s.branches[i],s.cbranches[i])
            branches.add_ElHNumber(s.branches[i],i)
            
    def inflate_stems_group(self,stems,s):
        """inflates a group of elements for branches (technical)
        s - stemsbranches object"""
        for i in range(1,11):
            stems.add(s.stems[i])
            stems.add_ElChname(s.stems[i],s.cstems[i])
            stems.add_ElHNumber(s.stems[i],i)
    
    def change_gua_heaven(self,Name,CGName,bset):
        """principle of heaven -change upper line of a trigram"""
        self.change_yao(Name, CGName, 3)
        self.find_in_set(CGName, CGName, bset)
        
    def change_gua_heavenmen(self,Name,CGName,bset):
        """principle of heaven and men-change upper and middle line of a trigram"""
        self.change_yaos(Name, CGName, 2, 3)
        self.find_in_set(CGName, CGName, bset)
        
    def change_gua_hsiao(self,Name,CGName,bset):
        """principle of hsiao -change  of a trigram"""
        if self.compare_Els(self.elements[Name], bset.elements['Dui']) or self.compare_Els(self.elements[Name], bset.elements['Li']) or self.compare_Els(self.elements[Name], bset.elements['Xun']) or self.compare_Els(self.elements[Name], bset.elements['Kun']) :
            Y1 = 1
        elif self.compare_Els(self.elements[Name], bset.elements['Qian']) or self.compare_Els(self.elements[Name], bset.elements['Zhen']) or self.compare_Els(self.elements[Name], bset.elements['Kan']) or self.compare_Els(self.elements[Name], bset.elements['Gen']) :
            Y1 = 0
        Y2 = self.elements[Name].Y1
        Y3 = self.elements[Name].Y2
        e = Element(CGName, Y1, Y2, Y3)
        self.elements[CGName]= e
        self.find_in_set(CGName, CGName, bset)
        
    def change_gua_hsi(self,Name,CGName,bset):
        """principle of hsi -change  of a trigram"""
        if self.compare_Els(self.elements[Name], bset.elements['Dui']) or self.compare_Els(self.elements[Name], bset.elements['Li']) or self.compare_Els(self.elements[Name], bset.elements['Xun']) or self.compare_Els(self.elements[Name], bset.elements['Kun']) :
            Y3 = 1
        elif self.compare_Els(self.elements[Name], bset.elements['Qian']) or self.compare_Els(self.elements[Name], bset.elements['Zhen']) or self.compare_Els(self.elements[Name], bset.elements['Kan']) or self.compare_Els(self.elements[Name], bset.elements['Gen']) :
            Y3 = 0
        Y2 = self.elements[Name].Y3
        Y1 = self.elements[Name].Y2
        e = Element(CGName, Y1, Y2, Y3)
        self.elements[CGName]= e
        self.find_in_set(CGName, CGName, bset)
    
    def change_gua_earthman(self, Name,CGName,bset): 
        """principle of eath and men-change lower and middle line of a trigram"""
        self.change_yaos(Name, CGName, 1, 2)
        self.find_in_set(CGName, CGName, bset)
        
    def change_gua_earth(self,Name,CGName,bset):
        """principle of heaven -change lower line of a trigram"""
        self.change_yao(Name, CGName, 1)
        self.find_in_set(CGName, CGName, bset)
        
    def change_gua_heavenearth(self,Name,CGName,bset):
        """principle of heaven and eath -change lower and upper line of a trigram"""
        self.change_yaos(Name, CGName, 1, 3)
        self.find_in_set(CGName, CGName, bset)
        
    def change_gua_man(self,Name,CGName,bset):
        """principle of heaven -change lower line of a trigram"""
        self.change_yao(Name, CGName, 2)
        self.find_in_set(CGName, CGName, bset)
        
    def change_gua_threepowers(self,Name,CGName,bset):
        """principle of three powers -change all three lines of a trigram"""
        self.change_yaos(Name, CGName, 1, 2, 3)
        self.find_in_set(CGName, CGName, bset)
        
        
        
           
        
        
        

        
        
    def getstrE(self, Name): 
        """returns element printout as string"""  
        return self.elements[Name].__str__() 
        
        
    def __call__(self, Name):
        """Returns the Element"""
        return self.elements[Name]
    
    def __str__(self):
        """Returns all the elements in the group"""
        nmax = 0
        c=0                        # control if set is full
        for p in self.elements:
            c = c+1
            if self.elements[p].HNumber is not None:
                k = self.elements[p].HNumber
                if k>nmax :
                    nmax=k
        
        
        i = 0
        s = ''
        
        for p in sorted(self.elements):
            i = i+1
            if self.elements[p].HNumber is not None and nmax == c:
                k = self.elements[p].HNumber
                for e in self.elements :
                    if self.elements[e].HNumber == i :
                        s += str(self.elements[e]) + '\n'
                    
            else :
                s += str(self.elements[p]) + '\n'
            
            
        s = s+ "total elements:" +str(i) + '\n'
        
        
        return s
    
        
    
        
        
        

        
        
        
        
        
        

        
