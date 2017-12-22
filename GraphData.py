# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 11:13:08 2017

@author: bit_lxy
"""
import numpy as np

class GraphData ():
    def __init__(self,v,e):
        self.vertexArray=  np.zeros(v).astype(np.int32)
        self.vertexcount=v
        self.edgeArray=np.zeros(e*2).astype(np.int32)
        self.edgecount=e
        self.weightArray=np.zeros(e*2).astype(np.float32)
    def show(self):
        print "g.vertexArray:",self.vertexArray
        print "g.edgeArray:",self.edgeArray
        print "g.weightArray",self.weightArray
    
def generateAGraph(v,e):
    return GraphData(v,e)

