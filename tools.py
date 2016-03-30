__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2016 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

'''
This script computes (and plots) networks, centralities and communities.
'''

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import matplotlib
import random
import math
import numpy
import community as comm
from nltk.tokenize import sent_tokenize, word_tokenize
import itertools
import os
import re

def draw_network(G,sstt,pos={},with_edgewidth=False,withLabels=True,pernode_dict={},labfs=10,valpha=0.4,ealpha=0.4,labelfont=20,with_node_weight=False,node_size_fixer=300.):
    plt.figure(figsize=(12,12))
    if len(pos)==0:
        pos=nx.spring_layout(G,scale=50)
    if with_edgewidth:
        edgewidth=[]
        for (u,v,d) in G.edges(data=True):
            edgewidth.append(d['weight'])
    else:
        edgewidth=[1 for i in G.edges()]
    if with_node_weight:
        node_weights=[node_size_fixer* math.log(nd[1]['weight']) for nd in G.nodes(data=True)]
        # print node_weights
        nx.draw_networkx_nodes(G,pos=pos,with_labels=False,alpha=valpha,node_size=node_weights)
    else:
        nx.draw_networkx_nodes(G,pos=pos,with_labels=False,alpha=valpha)
    if withLabels:
        if len(pernode_dict)>0:
            labels={i:v for v,i in pernode_dict.items() if i in G.nodes()}
            labe=nx.draw_networkx_labels(G,pos=pos,labels=labels,font_size=labelfont)
        else:
            labe=nx.draw_networkx_labels(G,pos=pos,font_size=labfs)
    nx.draw_networkx_edges(G,pos=pos,edge_color='b',width=edgewidth, alpha=ealpha)#,edge_labels=weights,label_pos=0.2)
    plt.title(sstt,fontsize=20)
    kk=plt.axis('off')
    return pos

def draw_centralities(G,centr,pos,with_edgewidth=False,withLabels=True,pernode_dict={},title_st='', labfs=10,valpha=0.4,ealpha=0.4):
    plt.figure(figsize=(12,12))
    if centr=='degree_centrality':
        cent=nx.degree_centrality(G)
        sstt='Degree Centralities'
        ssttt='degree centrality'
    elif centr=='closeness_centrality':
        cent=nx.closeness_centrality(G)
        sstt='Closeness Centralities'
        ssttt='closeness centrality'
    elif centr=='betweenness_centrality':
        cent=nx.betweenness_centrality(G)
        sstt='Betweenness Centralities'
        ssttt='betweenness centrality'
    elif centr=='eigenvector_centrality':
        cent=nx.eigenvector_centrality(G,max_iter=2000)
        sstt='Eigenvector Centralities'
        ssttt='eigenvector centrality'
    elif centr=='katz_centrality':
        phi = (1+math.sqrt(5))/2.0 # largest eigenvalue of adj matrix
        cent=nx.katz_centrality_numpy(G,1/phi-0.01)
        sstt='Katz Centralities'
        ssttt='Katz centrality'
    elif centr=='page_rank':
        cent=nx.pagerank(G)
        sstt='PageRank'
        ssttt='pagerank'
    cs={}
    nods_dici={v:k for k,v in pernode_dict.items()}
    for k,v in cent.items():
        if v not in cs:
            cs[v]=[k]
        else:
            cs[v].append(k)
    for k in sorted(cs,reverse=True):
        for v in cs[k]:
            print 'Node %s has %s = %.4f' %(nods_dici[v],ssttt,k)
    if withLabels:
        if len(pernode_dict)>1:
            labels={i:v for v,i in pernode_dict.items() if i in G.nodes()}
            labe=nx.draw_networkx_labels(G,pos=pos,labels=labels,font_size=20)
        else:
            labe=nx.draw_networkx_labels(G,pos=pos,font_size=labfs)
    nx.draw_networkx_nodes(G,pos=pos,nodelist=cent.keys(), #with_labels=withLabels,
                           node_size = [d*4000 for d in cent.values()],node_color=cent.values(),
                           cmap=plt.cm.Reds,alpha=valpha)
    if with_edgewidth:
        edgewidth=[]
        for (u,v,d) in G.edges(data=True):
            edgewidth.append(d['weight'])
    else:
        edgewidth=[1 for i in G.edges()]
    nx.draw_networkx_edges(G,pos=pos,edge_color='b',width=edgewidth, alpha=ealpha)
    plt.title(title_st+' '+ sstt,fontsize=20)
    kk=plt.axis('off')

def draw_centralities_subplots(G,pos,withLabels=True,labfs=10,valpha=0.4,ealpha=0.4,figsi=(12,12),vals=False):
    centList=['degree_centrality','closeness_centrality','betweenness_centrality',
    'eigenvector_centrality','katz_centrality','page_rank']
    cenLen=len(centList)
    valus={}
    plt.figure(figsize=figsi)
    for uu,centr in enumerate(centList):
        if centr=='degree_centrality':
            cent=nx.degree_centrality(G)
            sstt='Degree Centralities'
            ssttt='degree centrality'
            valus[centr]=cent
        elif centr=='closeness_centrality':
            cent=nx.closeness_centrality(G)
            sstt='Closeness Centralities'
            ssttt='closeness centrality'
            valus[centr]=cent

        elif centr=='betweenness_centrality':
            cent=nx.betweenness_centrality(G)
            sstt='Betweenness Centralities'
            ssttt='betweenness centrality'
            valus[centr]=cent

        elif centr=='eigenvector_centrality':
            try:
                cent=nx.eigenvector_centrality(G,max_iter=2000)
                sstt='Eigenvector Centralities'
                ssttt='eigenvector centrality'
                valus[centr]=cent

            except:
                valus[centr]=None

                continue
        elif centr=='katz_centrality':
            phi = (1+math.sqrt(5))/2.0 # largest eigenvalue of adj matrix
            cent=nx.katz_centrality_numpy(G,1/phi-0.01)
            sstt='Katz Centralities'
            ssttt='Katz centrality'
            valus[centr]=cent

        elif centr=='page_rank':
            try:
                cent=nx.pagerank(G)
                sstt='PageRank'
                ssttt='pagerank'
                valus[centr]=cent

            except:
                valus[centr]=None

                continue
        cs={}
        for k,v in cent.items():
            if v not in cs:
                cs[v]=[k]
            else:
                cs[v].append(k)
        nodrank=[]
        uui=0
        for k in sorted(cs,reverse=True):
            for v in cs[k]:
                if uui<5:
                    nodrank.append(v)
                    uui+=1
        nodeclo=[]
        for k,v in cent.items():
            if k in  nodrank :
                nodeclo.append(v)
            else:
                nodeclo.append(0.)
        plt.subplot(1+cenLen/2.,2,uu+1).set_title(sstt)
        if withLabels:
            labe=nx.draw_networkx_labels(G,pos=pos,font_size=labfs)
        nx.draw_networkx_nodes(G,pos=pos,nodelist=cent.keys(),
                               node_color=nodeclo,
                               cmap=plt.cm.Reds,alpha=valpha)
        nx.draw_networkx_edges(G,pos=pos,edge_color='b', alpha=ealpha)
        plt.title(sstt,fontsize=20)
        kk=plt.axis('off')
    if vals:
        return valus

def draw_comms(G,dom,idom,doml,nodoml ,par,cpar,d,dd,c,cc,alpha,ealpha,nodper,sstt,titlefont=20,labelfont=20,valpha=0.2):
    import community 
    import matplotlib
    invpar={}
    for i,v in par.items():
        if v not in invpar:
            invpar[v]=[i]
        else:
            invpar[v].append(i)
    ninvpar={}
    for i,v in invpar.items():
        if i not in ninvpar:
            ninvpar[i]=nx.spring_layout(G.subgraph(v))
    pos=nx.spring_layout(G,scale=70,k=0.8,iterations=20)        
    ells=[]
    ellc=[]
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green','m','c']))
    col_dic={}
    for i,v in ninvpar.items():
        xp=[xx[0] for x,xx in v.items()]
        yp=[yy[1] for y,yy in v.items()]
        ells.append(Ellipse(xy=(((-1)**i)*dd+max(xp)/2.,d*i+max(yp)/2.),width=cc*max(xp)/dd,height=c*max(yp)/d))
        colll=random.choice(colors)
        ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll
        for j in v:
            npos=v[j]
            pos[j]=[((-1)**par[j])*dd+npos[0],npos[1]+d*par[j]]
    col=[]
    if dom==G.nodes():
        for nd in G.nodes():
            col.append(col_dic[par[nd]])
    else:
        for nd in G.nodes():
            if nd in dom:
                col.append('r')
            elif nd in doml:
                col.append('m')
            elif nd in nodoml:
                col.append('c')
            else:
                col.append('b')
    fig = plt.figure(figsize=(12,12))
    ncomm=max(cpar.values())+1
    plt.subplot(1,1,1).set_title(sstt,fontsize=titlefont)
    ax = fig.add_subplot(1,1,1)
    labelsn={v:i for v,i in nodper.items() if v in G.nodes()}
    edgewidth=[]
    for (u,v,d) in G.edges(data=True):
        edgewidth.append(d['weight'])
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col,alpha=valpha)  
    nx.draw_networkx_labels(G,pos,labels=labelsn,font_size=labelfont)#,font_color='w')
    nx.draw_networkx_edges(G,pos,edge_color='b',width=edgewidth, alpha=ealpha)
    plt.axis('equal')
    plt.axis('off')
    plt.show()
    
def modul_arity(G,attribute):
    from correlationss import attribute_mixing_matrix
    M = attribute_mixing_matrix(G,attribute)
    return attribute_ac(M)

def print_communities(G,sstt):
    part=comm.best_partition(G) 
    print 'Number of communities of %s = %i' %(sstt, max(part.values())+1)
    print 'Community partition of %s:' %(sstt)
    parLis=[]
    partdi={}
    for i,k in part.items():
        if k not in partdi:
            partdi[k]=[i]
        else:
            partdi[k].append(i)
    for i,k in partdi.items():
        parLis.append(k)
    print parLis
    nodper={i:i for i in G.nodes()}
    print 'Community modularity of %s = %.4f' %(sstt, comm.modularity(part,G))
    return part,nodper

def occurrences(source,terms):
    ALL_sentences=sent_tokenize(source)
    combinations_terms = list(itertools.combinations(terms,2))
    n = len(combinations_terms)
    occurlist =[]
    for i in range(n):
        for j in ALL_sentences:
            temp= list(combinations_terms[i])            
            out  = re.compile(str(temp[0])+'(.*?)'+str(temp[1]), re.DOTALL |  re.IGNORECASE).findall(j)
            if out :
                occurlist.append(tuple(temp))
            out2  = re.compile(str(temp[1])+'(.*?)'+str(temp[0]), re.DOTALL |  re.IGNORECASE).findall(j)
            if out2 :
                occurlist.append(tuple(temp))
    occurdict={}
    for i in occurlist:
        if i not in occurdict:
            occurdict[i] = 1
        else:
            occurdict[i] = occurdict[i]+1
    return occurdict

def makegraph(occurrences):
    G = nx.Graph()
    for ed,wei in occurrences.items():   
        if ed[0] not in G:
            wei=1
        else:
            wei=G.node[ed[0]]['weight']+1
        if ed[1] not in G:
            weib=1
        else:
            weib=G.node[ed[1]]['weight']+1
        G.add_edge(ed[0],ed[1],weight=wei)
        G.add_node(ed[0],label=ed[0],weight=wei)
        G.add_node(ed[1],label=ed[1],weight=weib)
    return G

def dhist(G,sstth,pos={},pla=[0.47,0.47,0.47,0.47],a=0.3):
	degree_sequence=sorted(G.degree().values(),reverse=True)
	dmax=max(degree_sequence)
	plt.figure(figsize=(16,10))
	plt.plot(degree_sequence,'g-',marker='o')
	plt.ylabel("Degree")
	plt.xlabel("Number of nodes")
	plt.axes(pla)
	nx.draw_networkx_nodes(G,pos=pos,node_size=20,node_color='g',alpha=a)
	nx.draw_networkx_edges(G,pos=pos,alpha=a)
	plt.title(sstth,fontsize=17)
	kk=plt.axis('off')

