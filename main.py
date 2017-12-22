# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 14:30:35 2017

@author: bit_lxy
"""
from GraphData import generateAGraph
import numpy as np
import random as rd
import pyopencl as cl
mf=cl.mem_flags
# source presents the begining of the graph to search.
def runDijkstra(graph,source,costArray):
    context = cl.create_some_context()
    with open("Kernel.cl", 'r') as fin:
        program = cl.Program(context, fin.read()).build()
    maskArray = np.zeros(graph.vertexcount).astype(np.int32)
    maskArray[source]=1
    updateCostArray = np.zeros(graph.vertexcount).astype(np.float32)
    for i in range(0,graph.vertexcount):
        updateCostArray[i]=np.Inf
    updateCostArray[source] =0
    costArray[source]=0
    queue = cl.CommandQueue(context)

    
    dijkstra_first = program.Dijkstra_first
    dijkstra_second=program.Dijkstra_second
    
    vertex = cl.Buffer(context,mf.READ_ONLY | mf.COPY_HOST_PTR,hostbuf=graph.vertexArray)
    edge = cl.Buffer(context,mf.READ_ONLY | mf.COPY_HOST_PTR,hostbuf=graph.edgeArray)
    weight = cl.Buffer(context,mf.READ_ONLY | mf.COPY_HOST_PTR,hostbuf=graph.weightArray)
    mask = cl.Buffer(context,mf.READ_WRITE | mf.COPY_HOST_PTR,hostbuf=maskArray)
    cost = cl.Buffer(context,mf.READ_WRITE | mf.COPY_HOST_PTR,hostbuf=costArray)
    updateCost = cl.Buffer(context,mf.READ_WRITE | mf.COPY_HOST_PTR,hostbuf=costArray)      
    
    while(maskArrayEmpty(maskArray,graph.vertexcount) is False):
     
        dijkstra_first(queue,(graph.vertexcount,),(1,),vertex,edge,weight,mask,cost,updateCost,np.int32(graph.vertexcount),np.int32(graph.edgecount))
        dijkstra_second(queue,(graph.vertexcount,),(1,),vertex,edge,weight,mask,cost,updateCost,np.int32(graph.vertexcount))
        
        cl.enqueue_barrier(queue)
        e =cl.enqueue_copy(queue,maskArray,mask)
        e.wait()
    cl.enqueue_barrier(queue)
    e =cl.enqueue_copy(queue,costArray,cost)
    e.wait()
    return costArray#return the shortest path weights from the source to each vertex
def maskArrayEmpty(maskArray, count):
    for i in range(0,count):
        if maskArray[i] == 1:
            return False
    return True

v=5
e=10
#random generating a graph
graph = generateAGraph(v,e)
costArray = np.zeros(v).astype(np.float32)
for i in range(0,v):
    costArray[i] = np.Inf
m = np.zeros((v,v)).astype(np.int32)
for i in range(0,v):
    graph.vertexArray[i]=-1
for i in range(0,e):
    s = rd.randint(0,v)
    p = rd.randint(0,v)
    while p == s:
        p = rd.randint(0,v)
    w= rd.random()*100
    if m[s-1][p-1]==0:
        m[s-1][p-1]=w
        m[p-1][s-1]=w
    elif w<m[s-1][p-1]:
        m[s-1][p-1]=w
        m[p-1][s-1]=w
count=0
for i in range(0,v):
    for j in range(0,v):
        if m[i][j]!=0:
            graph.edgeArray[count]=j;
            graph.weightArray[count]=m[i][j]
            if graph.vertexArray[i] == -1:
                graph.vertexArray[i] =count
            count+=1
graph.edgecount=count 

updateCostArray = np.zeros(graph.vertexcount)
# run Dijkstra Algorithm to find the shortest way
result = runDijkstra(graph,0,costArray )

