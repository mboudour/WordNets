__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

'''
This script computes and plots dominating sets and communities.
'''

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import matplotlib
import random

# import community as community

def create_conn_random_graph(nodes,p):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    return G

def create_conn_random_graph_chrom(nodes,p,x):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            g=Graph(G)
            cn=vertex_coloring(g, value_only=True)
            if cn==x:
                break
    G.remove_nodes_from(nx.isolates(G))
    return G

def synthetic_multi_level_path_dic(k,n=[20,20],p=[.05,.06,.05],No_isolates=True,maxTries=1000):
    # from networkx.algorithms import bipartite

    list_of_Graphs=[]
    list_of_isolates={}
    dic_of_Graphs_final={}
    list_of_Graphs_final=[]
    uucount=0
    dic_of_nodes={}
    counters={}
    for ij in range(k):
        for ji in range(ij,k):
            tries=0
            # print ij,ji,uucount
            if ij==ji:
                dic_of_nodes[(ij,ji)]=(n[ij],n[ij])
                while tries<maxTries:
                    fgf=nx.path_graph(n[ij])
                    # fgf=nx.erdos_renyi_graph(n[ij],p[uucount])
                    if No_isolates:
                        fgf.remove_nodes_from(nx.isolates(fgf))
                    if len(fgf.nodes())==n[ij]:
                        # print fgf.nodes()
                        break
                    else:
                        tries+=1
                if tries==maxTries:
                    print 'Cannot find graph %i,%i' %(n[ij],p[uucount])
                    print aaaaaaaaaaa

                list_of_Graphs.append(fgf)
                list_of_isolates[ij]=nx.isolates(list_of_Graphs[ij])
                # print len(list_of_Graphs),ij,ji,uucount
                counters[(ij,ji)]=(len(list_of_Graphs)-1,uucount)
            uucount+=1
    uucount=0

    G=nx.Graph()  #The synthetic two-layer graph
    mapping={}
    sumnodes=0
    uucount=0
    for i in range(k):
        for j in range(i,k):
            mapping[(i,j)]={}
            if i==j:
                # print i,j,sumnodes,uucount,'ddddddddddddd'
                for ij in list_of_Graphs[counters[(i,j)][0]].nodes():# range(n[uucount]):
                    mapping[(i,j)][ij]=ij+sumnodes
                # print i,j,mapping[(i,j)],uucount
                dic_of_Graphs_final[(i,j)]=nx.relabel_nodes(list_of_Graphs[counters[(i,j)][0]],
            mapping[(i,j)],copy=True)
                sumnodes+=len(list_of_Graphs[uucount].nodes())
                uucount+=1
    uucount=0
    # print counters
    # print mapping
    # print list_of_Graphs
    # print aaa
    for ij in range(k):
        for ji in range(ij,k):

            # print ij,ji,uucount
            if ij!=ji:
                # print counters[(ji,ji)]
                # print counters[(ij,ij)]
                dic_of_nodes[(ij,ji)]=(n[ij],n[ji])
                counters[(ij,ji)]=(len(list_of_Graphs)-1, uucount)
                # upp=len(list_of_Graphs[counters[(ij,ij)][0]].nodes())
                # dodd=len(list_of_Graphs[counters[(ji,ji)][0]].nodes())
                # upp=dic_of_Graphs_final[(ij,ij)].nodes()
                # dodd=dic_of_Graphs_final[(ji,ji)].nodes()
                upp=list_of_Graphs[counters[(ij,ij)][0]].nodes()
                dodd=list_of_Graphs[counters[(ji,ji)][0]].nodes()
                # print upp
                # print dodd
                midG=nx.Graph()
                # print uucount,p[uucount]
                for nid in upp:
                    # for nod in dodd:
                    if random.random() <= p[uucount]:
                        ndn=mapping[(ij,ij)][nid]
                        nod=mapping[(ji,ji)][nid]
                            # print nid,p[uucount],uucount
                        midG.add_edge(ndn,nod)
                # print ij,ji,'kkkkkkkk',n[ij],n[ji],p[uucount]
                dic_of_Graphs_final[(ij,ji)]=midG
                
            uucount+=1
    # print aaaa
    nuf=set()
    luf=set()
    edgelist=set()
    for j,i in dic_of_Graphs_final.items():
        # print j
        # if No_isolates:
        #     if j in list_of_isolates:
        #         i.remove_nodes_from(list_of_isolates[j])
        luf=luf.union(set(i.edges()))
        # if not No_isolates:
        nuf=nuf.union(set(i.nodes()))
        if j[0]!=j[1]:
            # print i.edges(),'aaaaaaaaaaaaaaa'
            edgelist.update(set(i.edges()))
    luf=list(luf)
    # print luf
    G.add_edges_from(luf)
    # if not No_isolates:
    G.add_nodes_from(nuf)
    nmap={}
    for i  in mapping:
        for j in mapping[i]:
            nmap[mapping[i][j]]=j

    return G, dic_of_Graphs_final,  edgelist ,nmap ,mapping#F



def synthetic_multi_level_bip_dic(k,n=[20,20],p=[.05,.06,.05],No_isolates=True,maxTries=1000):
    # from networkx.algorithms import bipartite

    list_of_Graphs=[]
    list_of_isolates={}
    dic_of_Graphs_final={}
    list_of_Graphs_final=[]
    uucount=0
    dic_of_nodes={}
    counters={}
    for ij in range(k):
        for ji in range(ij,k):
            tries=0
            # print ij,ji,uucount
            if ij==ji:
                dic_of_nodes[(ij,ji)]=(n[ij],n[ij])
                while tries<maxTries:
                    fgf=nx.erdos_renyi_graph(n[ij],p[uucount])
                    # if No_isolates:
                    fgf.remove_nodes_from(nx.isolates(fgf))
                    if len(fgf.nodes())==n[ij]:
                        # print fgf.nodes()
                        # print fgf.edges()
                        break
                    else:
                        tries+=1
                if tries==maxTries:
                    print 'Cannot find graph %i,%i' %(n[ij],p[uucount])
                    print aaaaaaaaaaa

                list_of_Graphs.append(fgf)
                list_of_isolates[ij]=nx.isolates(list_of_Graphs[ij])
                # print len(list_of_Graphs),ij,ji,uucount
                counters[(ij,ji)]=(len(list_of_Graphs)-1,uucount)
            uucount+=1
    uucount=0
    # print counters
    # for ij in range(k):
    #     for ji in range(ij,k):

    #         # print ij,ji,uucount
    #         if ij!=ji:
    #             # print counters[(ij,ij)]
    #             # print counters[(ji,ji)]
    #             dic_of_nodes[(ij,ji)]=(n[ij],n[ji])
    #             counters[(ij,ji)]=(len(list_of_Graphs)-1, uucount)
    #             # upp=len(list_of_Graphs[counters[(ij,ij)][0]].nodes())
    #             # dodd=len(list_of_Graphs[counters[(ji,ji)][0]].nodes())
    #             upp=len(list_of_Graphs[counters[(ij,ij)][0]].nodes())
    #             dodd=len(list_of_Graphs[counters[(ji,ji)][0]].nodes())

    #             # print upp,dodd
    #             # fgf=nx.bipartite_random_graph(n[ij],n[ji],p[uucount])
    #             # fgf=nx.bipartite_random_graph(upp,dodd,p[uucount])

    #             # if No_isolates:
    #             #     fgf.remove_nodes_from(nx.isolates(fgf))
    #             list_of_Graphs.append(fgf)
    #             # print ij,ji,'kkkkkkkk',n[ij],n[ji],p[uucount]
    #         uucount+=1
    # print list_of_Graphs
    # print aaaa
        # list_of_Graphs.append(nx.erdos_renyi_graph(n[ij],p[ij]))
        # list_of_isolates.append(nx.isolates(list_of_Graphs[ij]))

    # Gagr=nx.Graph()
    # for i in list_of_Graphs:
    #     Gagr.add_edges_from(i.edges())
    #     Gagr.add_nodes_from(i.nodes())

    G=nx.Graph()  #The synthetic two-layer graph
    # for kk,vv in enumerate(list_of_Graphs):
    #     print kk,vv
    # print counters
    # Relabing nodes maps
    mapping={}
    sumnodes=0
    uucount=0
    for i in range(k):
        for j in range(i,k):
            mapping[(i,j)]={}
            if i==j:
                # print i,j,sumnodes,uucount,'ddddddddddddd'
                for ij in list_of_Graphs[counters[(i,j)][0]].nodes():# range(n[uucount]):
                    mapping[(i,j)][ij]=ij+sumnodes
                # print i,j,mapping[(i,j)],uucount
                dic_of_Graphs_final[(i,j)]=nx.relabel_nodes(list_of_Graphs[counters[(i,j)][0]],
            mapping[(i,j)],copy=True)
                # print i,j
                # print list_of_Graphs[(uucount)].nodes()
                # print list_of_Graphs[(uucount)].edges()
                # print dic_of_Graphs_final[(i,j)].edges()
                # print uucount
                # print '==============='
                sumnodes+=len(list_of_Graphs[uucount].nodes())
                uucount+=1
                # print i,j,sumnodes,uucount
            # else:
            #     # print 'sssssssssssssss'
            #     # print i,j,dic_of_nodes[i,j]
            #     mpot=0
            #     npot=0
            #     if i>0:
            #         ii=i
            #         while ii!=0:
            #             ii-=1
            #             mpot+=dic_of_nodes[(ii,j)][0]
            #     if j>0:
            #         jj=j
            #         while jj!=0:
            #             jj-=1
            #             # print jj,dic_of_nodes[jj,j][0],npot
            #             npot+=dic_of_nodes[(jj,j)][0]
            #             # print npot

            #     # print i,j ,mpot,npot,dic_of_nodes[(i,j)]
            #     # print dic_of_nodes[j]
            #     # print list_of_Graphs[(uucount)].nodes()
            #     # print 'ttttttttttttttt'
            #     # for iijj in list_of_Graphs[uucount].nodes():
            #     #     if iijj
            #     for iijj in range(dic_of_nodes[i,j][0]):
            #         mapping[(i,j)][iijj]=mpot+iijj
            #     for iijj in range(dic_of_nodes[(i,j)][1]):
            #         mapping[(i,j)][iijj+dic_of_nodes[(i,j)][0]]=npot+iijj
            #     # print i,j,mapping[(i,j)],mpot,npot,'<<<<<<<<<<<'
            #     dic_of_Graphs_final[(i,j)]=nx.relabel_nodes(list_of_Graphs[uucount],
            # mapping[(i,j)],copy=True)
            #     # print list_of_Graphs[(uucount)].edges()
            #     # print uucount
            #     # sumnodes+=n[uucount]
            #     uucount+=1
    # print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
    # print sumnodes,uucount,mapping
    # print dic_of_Graphs_final
    uucount=0
    for ij in range(k):
        for ji in range(ij,k):

            # print ij,ji,uucount
            if ij!=ji:
                # print counters[(ij,ij)]
                # print counters[(ji,ji)]
                dic_of_nodes[(ij,ji)]=(n[ij],n[ji])
                counters[(ij,ji)]=(len(list_of_Graphs)-1, uucount)
                # upp=len(list_of_Graphs[counters[(ij,ij)][0]].nodes())
                # dodd=len(list_of_Graphs[counters[(ji,ji)][0]].nodes())
                upp=dic_of_Graphs_final[(ij,ij)].nodes()
                dodd=dic_of_Graphs_final[(ji,ji)].nodes()
                midG=nx.Graph()
                # print uucount,p[uucount]
                for nid in upp:
                    for nod in dodd:
                        if random.random() <= p[uucount]:
                            # print nid,p[uucount],uucount,nod
                            midG.add_edge(nid,nod)
                # print upp,dodd,'mmmpppp'
                # fgf=nx.bipartite_random_graph(n[ij],n[ji],p[uucount])
                # fgf=nx.bipartite_random_graph(upp,dodd,p[uucount])

                # if No_isolates:
                #     fgf.remove_nodes_from(nx.isolates(fgf))
                # list_of_Graphs.append(fgf)
                # print ij,ji,'kkkkkkkk',n[ij],n[ji],p[uucount]
                dic_of_Graphs_final[(ij,ji)]=midG
                
            uucount+=1
    # print dic_of_Graphs_final
    # print aaa

    # for i,k in dic_of_Graphs_final.items():
    #     print i,k.nodes()
    # for i in range(k):
    #     for j in range(i,k):
    #         if i==j:

    # print dic_of_Graphs_final
        # mapping[i]={}
        
        # for ij in range(n[i]):
        #     mapping[i][ij]=ij+sumnodes
        # sumnodes+=i*n[i]
        # list_of_Graphs_final.append(nx.relabel_nodes(list_of_Graphs[i],mapping[i],copy=True))
    # ################
    # list_of_translation_graphs=[]
    # for ij in range(k-1):
    #     H1=nx.Graph()
    #     #### A small fix to pain in the ass
    #     g1=sorted(list_of_Graphs_final[ij].nodes())
    #     g2=sorted(list_of_Graphs_final[ij+1].nodes())
    #     #######

    #     for ji in range(n):

    #         H1.add_edge(g1[ji],g2[ji]) #a small fix

    #     list_of_translation_graphs.append(H1)
    #     #####################
        

    # print aaaa
    # if No_isolates:
    # print mapping
    nuf=set()
    luf=set()
    edgelist=set()
    for j,i in dic_of_Graphs_final.items():
        # print j
        # if No_isolates:
        #     if j in list_of_isolates:
        #         i.remove_nodes_from(list_of_isolates[j])
        luf=luf.union(set(i.edges()))
        # if not No_isolates:
        nuf=nuf.union(set(i.nodes()))
        if j[0]!=j[1]:
            # print i.edges(),'aaaaaaaaaaaaaaa'
            edgelist.update(set(i.edges()))
    luf=list(luf)
    # print luf
    G.add_edges_from(luf)
    # if not No_isolates:
    G.add_nodes_from(nuf)
    # luf=set()
    # for i in list_of_translation_graphs:
    #     luf=luf.union(set(i.edges()))
    # edgeList=list(luf)
    # G.add_edges_from(luf)
    nmap={}
    for i  in mapping:
        for j in mapping[i]:
            nmap[mapping[i][j]]=j

    return G, dic_of_Graphs_final,  edgelist ,nmap ,mapping#F

def plot_graph(G,J,FF,DD,n1,n2,n3,d1=0.8,d2=3.,d3=0.8,nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):
    '''
    Plotting the synthetic graph after increasing the distance among layers by a parameter d1
def plot_graph_k_nm(k,G,list_of_Graphs_final, uuu,d1=0,d2=2,d3=0,d4=.3,d5=1,d6=.4,d7=.2,d8=1,d9=0.3,colors_grey='gray',nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):  
def plot_graph_k_nm(k,G,list_of_Graphs_final, uuu,d1=0,d2=2,d3=0,d4=.3,d5=1,d6=.4,d7=.2,d8=1,d9=0.3,colors_grey='gray',nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):  

    and dilating each layer by a parameter d1 
    '''

    if layout:
        # pos=nx.circular_layout(G)
        pos=nx.spring_layout(G)
    else:
        pos=nx.random_layout(G)
        # pos =nx.circular_layout(G)
    
    top_set=set()
    bottom_set=set()
    middle_set=set()
    down=[]
    right=[]
    left=[]
    for i in pos:
        npos=pos[i]
        if i < n1:
            pos[i]=[d2*(npos[0]-d1),d2*(npos[1]+d1)] 
            top_set.add(i)
            left.append(pos[i])
        elif i>=n1+n2:
            pos[i]=[d2*(npos[0]+d1),d2*(npos[1]+d1)] 
            bottom_set.add(i)
            right.append(pos[i])
        else:
            pos[i]=[d2*npos[0],d2*(npos[1]-d1)] 
            middle_set.add(i)
            down.append(pos[i])
    
    xleft=[i[0] for i in left]
    yleft=[i[1] for i in left]

    aleft = [min(xleft)-d1/2.,max(yleft)+d1/2.+d3]
    bleft = [max(xleft)+d1/2.,max(yleft)+d1/2.+3*d3]
    cleft = [max(xleft)+d1/2.,min(yleft)-d1/2.-3*d3]
    dleft = [min(xleft)-d1/2.,min(yleft)-d1/2.-d3]

    xright=[i[0] for i in right]
    yright=[i[1] for i in right]

    aright = [min(xright)-d1/2.,max(yright)+d1/2.+d3]
    bright = [max(xright)+d1/2.,max(yright)+d1/2.+3*d3]
    cright = [max(xright)+d1/2.,min(yright)-d1/2.-3*d3]
    dright = [min(xright)-d1/2.,min(yright)-d1/2.-d3]

    xdown=[i[0] for i in down]
    ydown=[i[1] for i in down]

    adown = [min(xdown)-d1/2.,max(ydown)+d1/2.+d3]
    bdown = [max(xdown)+d1/2.,max(ydown)+d1/2.+3*d3]
    cdown = [max(xdown)+d1/2.,min(ydown)-d1/2.-3*d3]
    ddown = [min(xdown)-d1/2.,min(ydown)-d1/2.-d3]

    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(111)

    ax.add_patch(Polygon([aleft,bleft,cleft,dleft],color='r',alpha=0.1)) 
    plt.plot([aleft[0],bleft[0],cleft[0],dleft[0],aleft[0]],[aleft[1],bleft[1],cleft[1],dleft[1],aleft[1]],'-r')

    ax.add_patch(Polygon([aright,bright,cright,dright],color='b',alpha=0.1)) 
    plt.plot([aright[0],bright[0],cright[0],dright[0],aright[0]],[aright[1],bright[1],cright[1],dright[1],aright[1]],'-b')

    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='g',alpha=0.1)) 
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-g')

    # nx.draw(G,pos, with_labels=withlabels,nodelist=list(top_set),node_color='r',alpha=0.2,node_size=nodesize)
    # nx.draw(G,pos, with_labels=withlabels,nodelist=list(middle_set),node_color='g',alpha=0.2,node_size=nodesize)
    # nx.draw(G,pos, with_labels=withlabels,nodelist=list(bottom_set),node_color='b',alpha=0.2,node_size=nodesize)

    nx.draw(J,pos, with_labels=withlabels,nodelist=list(top_set),node_color='r',node_size=nodesize,edge_color='r',alpha=0.2)
    nx.draw(FF,pos, with_labels=withlabels,nodelist=list(middle_set),node_color='g',node_size=nodesize,edge_color='g',alpha=0.2)
    nx.draw(DD,pos, with_labels=withlabels,nodelist=list(bottom_set),node_color='b',node_size=nodesize,edge_color='b',alpha=0.2)
    # ,alpha=0.2
    nx.draw_networkx_edges(G,pos,edgelist=edgelist,edge_color='k',alpha=b_alpha)
    # partition = comm.best_partition(G)
    # npartition = list(nx.connected_components(G))
    # for i in G.nodes():
    #     # attr=G.node[i]
    #     # print attr
    #     G.add_node(i,attr_dict=G.node[i],best_partition=partition[i])
    #     if i in J.nodes():
    #         G.add_node(i,attr_dict=G.node[i],layers_3='1')
    #     elif i in DD.nodes():
    #         G.add_node(i,attr_dict=G.node[i],layers_3='2')
    #     else:
    #         G.add_node(i,attr_dict=G.node[i],layers_3='3')
def plot_graph_k_nm(k,n,G,list_of_Graphs_final, uuu,d1=0,d2=2,d3=0,d4=.3,d5=1,d6=.4,d7=.2,d8=1,d9=0.3,colors_grey='gray',nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):  
    '''
    Plotting the synthetic graph after increasing the distance among layers by a parameter d1
    and dilating each layer by a parameter d1 
    '''
    # print k,n,G.nodes(),Gagr.nodes()
    if layout:
        pos=nx.spring_layout(G)
        # pos=nx.graphviz_layout(G)
    else:
        pos=nx.graphviz_layout(G)
        # pos=nx.random_layout(G)

    minPos=min(pos.keys())
    top_set=set()
    bottom_set=set()
    middle_set=set()
    levels=dict()
    created_pos={}
    if colors_grey=='gray':
        colors=['gray' for i in range (2*n)]

    elif colors_grey=='bipartite':
        colors=[]
        aset=[i[0] for i in G.nodes(data=True) if i[1]['bipartite']==0 ]
        bset=[i[0] for i in G.nodes(data=True) if i[1]['bipartite']==1 ]

        bipsets=(aset,bset)#bipartite.sets(G)
        for i in G.nodes():

            if i in bipsets[0]:
                colors.append('m')
            else:
                colors.append('g')
    else:
        colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]

    for j,keyd in enumerate(list_of_Graphs_final):# range(k):

        sset=set()
        pos_lis=[]
        col_li=[]
        # print keyd
        if keyd[0]!=keyd[1]:
            continue
        # print 'aaa'
        # print list_of_Graphs_final[keyd].nodes()
        # print pos
        for i,v in enumerate(list_of_Graphs_final[keyd].nodes()):
            # print i,v,j,keyd

            npos=pos[v]


            created_pos[v]=[d2*npos[0],d8*(npos[1]+j*(n)*d6)] 
            sset.add(v)
            pos_lis.append(created_pos[v])
            # if v[0]=='A':
            if i<n:
            # if v in bipsets[0]:
                col_li.append('m')
            else:
                col_li.append('g')

        levels[j]=(sset,pos_lis,col_li)
    xylevels={}

    for i,keyd in enumerate(list_of_Graphs_final):#i in range(k):
        # print i,keyd
        if keyd[0]!=keyd[1]:
            continue
        # print 'cooo'
        xlevel2=[ij[0] for ij in levels[i][1]]
        ylevel2=[ij[1] for ij in levels[i][1]]
        alevel2 = [min(xlevel2)-d1,max(ylevel2)+d7/2.-d3+d5]
        blevel2 = [max(xlevel2)+d9,max(ylevel2)+d7/2.+d3+d5]
        clevel2 = [max(xlevel2)+d9-d4,min(ylevel2)-d7/2.+d3-d5]
        dlevel2 = [min(xlevel2)-d1-d4,min(ylevel2)-d7/2.-d3-d5]
        xylevels[i]=[alevel2,blevel2,clevel2,dlevel2]

    fig=plt.figure(num=uuu,figsize=(8,11))
    ax=fig.add_subplot(111)
    # fig=plt.figure(figsize=(10,10))
    # ax=fig.add_subplot(111)
    for i,keyd in enumerate(list_of_Graphs_final):#i in range(k):
        # print i,keyd
        if keyd[0]!=keyd[1]:
            continue
        # print 'moooo'#i in range(k):
        ax.add_patch(Polygon(xylevels[i],color='gray',alpha=0.1))
        xa=[j[0] for j in xylevels[i]]
        xa.append(xylevels[i][0][0])
        ya=[j[1] for j in xylevels[i]]
        ya.append(xylevels[i][0][1])
        plt.plot(xa,ya,'-',color='gray')
        nx.draw_networkx_nodes(list_of_Graphs_final[keyd],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.3)
        nx.draw_networkx_edges(list_of_Graphs_final[keyd],created_pos,alpha=0.4)
        # nx.draw(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)
    nx.draw_networkx_edges(G,created_pos,edgelist=edgelist,edge_color='k',alpha=0.4)
    sstt='%i-Layer Random Graph' %k  
    plt.title(sstt,{'size': '20'})
    plt.axis('off')
    plt.show()

    return created_pos,fig



def draw_domcomms(G,dom,idom,doml,nodoml ,par,cpar,d,dd,c,cc,alpha,ealpha):
    import community 
    from matplotlib.patches import Ellipse
    
    import matplotlib
    
    # par= community.best_partition(G)
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
    pos=nx.spring_layout(G)
    
    
        
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


    fig = plt.figure(figsize=(16,8))
    ncomm=max(par.values())+1
    sstt="Chromatic Partition in %s Groups" %ncomm
    plt.subplot(121).set_title(sstt)
    ax = fig.add_subplot(121)
    ax.set_title(sstt)
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col) 
    nx.draw_networkx_labels(G,pos,font_color='k')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=ealpha)
    plt.axis('equal')
    plt.axis('off')

    # pos=nx.spring_layout(G)

    # col=[]
    # for nd in G.nodes():
    #     if nd in idom:
    #         col.append('g')
    #     elif nd in doml:
    #         col.append('m')
    #     elif nd in nodoml:
    #         col.append('c')
    #     else:
    #         col.append('b')
    cinvpar={}

    for i,v in cpar.items():
        if v not in cinvpar:
            cinvpar[v]=[i]
        else:
            cinvpar[v].append(i)
    cninvpar={}
    for i,v in cinvpar.items():
        if i not in cninvpar:
            cninvpar[i]=nx.spring_layout(G.subgraph(v))
            # gg=Graph(G.subgraph(v))
            # print i,vertex_coloring(gg, value_only=False)
    ells=[]
    # colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    # colors=list(set(colors)-set(['red','blue','green','m','c']))
    for i,v in cninvpar.items():
        xp=[xx[0] for x,xx in v.items()]
        yp=[yy[1] for y,yy in v.items()]

        ells.append(Ellipse(xy=(((-1)**i)*dd+max(xp)/2.,d*i+max(yp)/2.),width=cc*max(xp)/dd,height=c*max(yp)/d))
        colll=random.choice(colors)
        ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll
        for j in v:
            npos=v[j]
            pos[j]=[((-1)**cpar[j])*dd+npos[0],npos[1]+d*cpar[j]]

    ncomm=max(cpar.values())+1
    sstt="Community Partition in %s Groups" %ncomm
    plt.subplot(1,2,2).set_title(sstt)
    ax = fig.add_subplot(1,2,2)

    ax.set_title(sstt)
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col)  
    nx.draw_networkx_labels(G,pos)#,font_color='w')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=ealpha)
    plt.axis('equal')
    plt.axis('off')
    plt.show()

def draw_domcomms_sr(G,layer1,layer2,dom,idom,doml,nodoml ,par,cpar,d,dd,c,cc,alpha,ealpha,labels=False,nodesize=10):
    import community 
    from matplotlib.patches import Ellipse
    import random

    
    # par= community.best_partition(G)
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
    pos=nx.spring_layout(G)
    
    
        
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

    col1=[]
    col2=[]
    if dom==G.nodes():
        for nd in G.nodes():
            if nd in layer1:
                col1.append(col_dic[par[nd]])
            if nd in layer2:
                col2.append(col_dic[par[nd]])
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


    fig = plt.figure(figsize=(16,8))
    ncomm=max(par.values())+1
    sstt="Chromatic Partition in %s Groups" %ncomm
    plt.subplot(121).set_title(sstt)
    ax = fig.add_subplot(121)
    ax.set_title(sstt)
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col1,nodelist=layer1,node_size=nodesize) 
    nx.draw_networkx_nodes(G,pos=pos, node_color=col2,nodelist=layer2,node_shape='s',node_size=nodesize)  
    if labels:
        nx.draw_networkx_labels(G,pos,font_color='k')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=ealpha)
    plt.axis('equal')
    plt.axis('off')

    # pos=nx.spring_layout(G)

    # col=[]
    # for nd in G.nodes():
    #     if nd in idom:
    #         col.append('g')
    #     elif nd in doml:
    #         col.append('m')
    #     elif nd in nodoml:
    #         col.append('c')
    #     else:
    #         col.append('b')
    cinvpar={}

    for i,v in cpar.items():
        if v not in cinvpar:
            cinvpar[v]=[i]
        else:
            cinvpar[v].append(i)
    cninvpar={}
    for i,v in cinvpar.items():
        if i not in cninvpar:
            cninvpar[i]=nx.spring_layout(G.subgraph(v))
            # gg=Graph(G.subgraph(v))
            # print i,vertex_coloring(gg, value_only=False)
    ells=[]
    # colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    # colors=list(set(colors)-set(['red','blue','green','m','c']))
    for i,v in cninvpar.items():
        xp=[xx[0] for x,xx in v.items()]
        yp=[yy[1] for y,yy in v.items()]

        ells.append(Ellipse(xy=(((-1)**i)*dd+max(xp)/2.,d*i+max(yp)/2.),width=cc*max(xp)/dd,height=c*max(yp)/d))
        colll=random.choice(colors)
        ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll
        for j in v:
            npos=v[j]
            pos[j]=[((-1)**cpar[j])*dd+npos[0],npos[1]+d*cpar[j]]

    ncomm=max(cpar.values())+1
    sstt="Community Partition in %s Groups" %ncomm
    plt.subplot(1,2,2).set_title(sstt)
    ax = fig.add_subplot(1,2,2)

    ax.set_title(sstt)
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col1,nodelist=layer1,node_size=nodesize) 
    nx.draw_networkx_nodes(G,pos=pos, node_color=col2,nodelist=layer2,node_shape='s',node_size=nodesize) 
    if labels:

        nx.draw_networkx_labels(G,pos)#,font_color='w')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=ealpha)
    plt.axis('equal')
    plt.axis('off')
    plt.show()


def attribute_ac(M):
    
    try:
        import numpy
    except ImportError:
        raise ImportError(
          "attribute_assortativity requires NumPy: http://scipy.org/ ")
    if M.sum() != 1.0:
        M=M/float(M.sum())
    M=numpy.asmatrix(M)
    s=(M*M).sum()
    t=M.trace()
    r=(t-s)
    return float(r)

def modul_arity(G,attribute):
    from correlationss import attribute_mixing_matrix
    M = attribute_mixing_matrix(G,attribute)
    return attribute_ac(M)

def sim_for_ch(G,start,stop,iterations,k,x,chromAttrassor,commAttrassor,commNumber,stringTitle=''):
    import random
    # import matplotlib.cbook as cbook
    ll={}
    llm=[]
    lln=[]
    ppn=[]
    ppm=[]
    pp={}
    plt.figure(figsize=(12,8))  
    for i in range(start,stop):
        ll[i]=[]
        pp[i]=[]
        for j in range(iterations):
            while True:
                checki=set()
                for nd in G.nodes():
                    kk=range(i)
                    kkll=random.choice(kk)
                    checki.add(kkll)
                    G.add_node(nd,vertex_colors=kkll)
    #             print len(checki),i
                if len(checki)==i:
                    break
            mm=modul_arity(G,'vertex_colors')
            ll[i].append(mm)
            # plt.plot(i,mm,'.k')
            # for mm in ll[i]:
            #     plt.plot(i,mm,'.k')
    #         ll[i].append(nx.attribute_assortativity_coefficient(G,'vertex_colors'))
    #         pp[i].append(nx.attribute_assortativity_coefficient(G,'comm_coll'))
        llm.append(max(ll[i]))
        lln.append(min(ll[i]))
    #     ppm.append(max(pp[i]))
    #     ppn.append(min(pp[i]))
    
    plt.plot(range(start,stop),llm,'ro',label='Sim-Max Modularity')
    plt.plot(range(start,stop),lln,'b*',label='Sim-Min Modularity')
    for kk,vv in enumerate(llm):
        plt.plot([kk+1,kk+1],[llm[kk],lln[kk]],'--k')
    # plt.plot([start,stop-1],[0,0],'-k')

    plt.xlim(start-0.1, stop-1+0.1)
    # plt.plot(range(start,stop),ppm,'-ms')
    # plt.plot(range(start,stop),ppn,'-c^')
    # plt.plot([x,x],[-1.,1.],'-g',label='Chromatic Number')
    # # chromAttrassor=modul_arity(G,)

    # plt.plot([start,stop-1],[chromAttrassor,chromAttrassor],'-c',label='Chromatic Modularity')
    # plt.plot([start,stop-1],[commAttrassor,commAttrassor],'-m',label='Community Modularity')
    # plt.plot([commNumber,commNumber],[-1,1],'-y',label='Community Number')
    # plt.legend(numpoints=1)
    plt.legend(loc=1)
    plt.plot(x, chromAttrassor, 'bD', markersize=12)  # ,label='(Chromatic Number, Chrommatic Modularity)')
    plt.annotate('(Chromatic Number, Chrommatic Modularity)', xy=(x, chromAttrassor), xytext=(x-1, chromAttrassor-0.015))
    plt.plot(commNumber, commAttrassor, 'rs', markersize=12)  # ,label='(Community Number, Community Modularity)')
    plt.annotate('(Community Number, Community Modularity)', xy=(commNumber, commAttrassor), xytext=(commNumber-1, commAttrassor-0.015))
    plt.xlabel('Number of Colors (Partition Cardinality)')
    plt.ylabel('Modularity')
    stil='%s simulations of colored partitions of graph G for %s - %s colors\n %s' %(iterations,start,stop-1,stringTitle)
    plt.title(stil)
    plt.legend()
        
    pass
def sim_for_ch1(G,start,stop,iterations,k,x,chromAttrassor,commAttrassor,commNumber,stringTitle=''):
    import random
    # import matplotlib.cbook as cbook
    ll={}
    llm=[]
    lln=[]
    ppn=[]
    ppm=[]
    pp={}
    plt.figure(figsize=(12,8))  
    for i in range(start,stop):
        ll[i]=[]
        pp[i]=[]
        for j in range(iterations):
            while True:
                checki=set()
                for nd in G.nodes():
                    kk=range(i)
                    kkll=random.choice(kk)
                    checki.add(kkll)
                    G.add_node(nd,vertex_colors=kkll)
    #             print len(checki),i
                if len(checki)==i:
                    break
            mm=modul_arity(G,'vertex_colors')
            ll[i].append(mm)
            plt.plot(i,mm,'.k')
            # for mm in ll[i]:
            #     plt.plot(i,mm,'.k')
    #         ll[i].append(nx.attribute_assortativity_coefficient(G,'vertex_colors'))
    #         pp[i].append(nx.attribute_assortativity_coefficient(G,'comm_coll'))
        llm.append(max(ll[i]))
        lln.append(min(ll[i]))
    #     ppm.append(max(pp[i]))
    #     ppn.append(min(pp[i]))
    
    plt.plot(range(start,stop),llm,'ro',label='Sim-Max Modularity')
    plt.plot(range(start,stop),lln,'b*',label='Sim-Min Modularity')
    for kk,vv in enumerate(llm):
        plt.plot([kk+1,kk+1],[llm[kk],lln[kk]],'--k')
    # plt.plot([start,stop-1],[0,0],'-k')

    plt.xlim(start-0.1, stop-1+0.1)
    # plt.plot(range(start,stop),ppm,'-ms')
    # plt.plot(range(start,stop),ppn,'-c^')
    # plt.plot([x,x],[-1.,1.],'-g',label='Chromatic Number')
    # # chromAttrassor=modul_arity(G,)

    # plt.plot([start,stop-1],[chromAttrassor,chromAttrassor],'-c',label='Chromatic Modularity')
    # plt.plot([start,stop-1],[commAttrassor,commAttrassor],'-m',label='Community Modularity')
    # plt.plot([commNumber,commNumber],[-1,1],'-y',label='Community Number')
    # plt.legend(numpoints=1)
    plt.legend(loc=1)
    plt.plot(x, chromAttrassor, 'bD', markersize=12)  # ,label='(Chromatic Number, Chrommatic Modularity)')
    # plt.annotate('(Chromatic Number, Chrommatic Modularity)', xy=(x, chromAttrassor), xytext=(x-1, chromAttrassor-0.015))
    plt.plot(commNumber, commAttrassor, 'rs', markersize=12)  # ,label='(Community Number, Community Modularity)')
    # plt.annotate('(Community Number, Community Modularity)', xy=(commNumber, commAttrassor), xytext=(commNumber-1, commAttrassor-0.015))
    plt.xlabel('Number of Colors (Partition Cardinality)')
    plt.ylabel('Modularity')
    stil='%s simulations of colored partitions of graph G for %s - %s colors\n %s' %(iterations,start,stop-1,stringTitle)
    plt.title(stil)
    plt.legend()
        
    pass


# def twolevel_plot(G,layer1,layer2,layer3,d1=1.5,d2=5.,d3=0.8,nodesize=1000,withlabels=True,edgelist=[],layout=True,alpha=0.5):

def plot_paral(G,layer1,layer2,d1=1.5,d2=5.,d3=0.8,d4=0,d5=0,d6=0,nodesize=1000,withlabels=True,edgelist=[],layout=True,alpha=0.5):
    
    edgeList =[]
    for e in G.edges():
        if (e[0] in layer1 and e[1] in layer2) or (e[0] in layer2 and e[1] in layer1):
            edgeList.append(e)
            
    pos=nx.spring_layout(G)
    # pos=nx.graphviz_layout(G)
    # d1=0.6 #1.5
    # d2=15. # 5.
    # d3=0.3 #0.8
    nodesize=200
    withlabels=False
    edgelist=[]
    layout=True
    alpha=0.25

    top_set=set()
    bottom_set=set()
    top=[]
    down=[]

    for i in pos:
        npos=pos[i]
        if i in layer1:
            pos[i]=[d2*(npos[0]),d2*(npos[1]+d1)] 
    #         pos[i]=[d2*(npos[0]-d1),d2*(npos[1]+d1)] 
            top_set.add(i)
            top.append(pos[i])
        else:
            pos[i]=[d6*(npos[0]),d6*(npos[1]-d1)] 
    #         pos[i]=[d2*(npos[0]+d1),d2*(npos[1]+d1)] 
            bottom_set.add(i)
            down.append(pos[i])

    xtop=[i[0] for i in top]
    ytop=[i[1] for i in top]

    atop = [min(xtop)-d4/2.+d5,max(ytop)+d4/2.+d3]
    btop = [max(xtop)+d4/2.+d5,max(ytop)+d4/2.+d3]   
    ctop = [max(xtop)+d4/2.-d5,min(ytop)-d4/2.-d3]
    dtop = [min(xtop)-d4/2.-d5,min(ytop)-d4/2.-d3]

    xdown=[i[0] for i in down]
    ydown=[i[1] for i in down]

    adown = [min(xdown)-d4/2+d5,max(ydown)+d4/2.+d3]
    bdown = [max(xdown)+d4/2.+d5,max(ydown)+d4/2.+d3]
    cdown = [max(xdown)+d4/2.-d5,min(ydown)-d4/2.-d3]
    ddown = [min(xdown)-d4/2.-d5,min(ydown)-d4/2.-d3]

    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(111)
    ax.add_patch(Polygon([atop,btop,ctop,dtop],color='r',alpha=0.1)) 
    plt.plot([atop[0],btop[0],ctop[0],dtop[0],atop[0]],[atop[1],btop[1],ctop[1],dtop[1],atop[1]],'-r')
    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='b',alpha=0.1)) 
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-b')
    nx.draw_networkx_nodes(G,pos, nodelist=top_set,node_color='r',alpha=0.2,node_size=nodesize,node_shape='s')
    nx.draw_networkx_nodes(G,pos,nodelist=bottom_set,node_color='b',alpha=0.2,node_size=nodesize)
    if withlabels:
        nx.draw_networkx_labels(G,pos)
    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    nx.draw_networkx_edges(G,pos,edgelist=lay1_edges,edge_color='r',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=lay2_edges,edge_color='b',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=edgeList,edge_color='k',alpha=alpha)
    plt.axis('off')
    plt.show()

def plot_paral_chr_comm(G,layer1,layer2,ccv,par,d1=1.5,d2=5.,d3=0.8,d4=0,d5=0,d6=0,nodesize=1000,withlabels=True,edgelist=[],layout=True,nodal=1,alpha=0.5):
    
    edgeList =[]
    for e in G.edges():
        if (e[0] in layer1 and e[1] in layer2) or (e[0] in layer2 and e[1] in layer1):
            edgeList.append(e)
            
    pos=nx.spring_layout(G)
    # pos=nx.graphviz_layout(G)
    # d1=0.6 #1.5
    # d2=15. # 5.
    # d3=0.3 #0.8
    # nodesize=200
    # withlabels=False
    # edgelist=[]
    # layout=True
    # alpha=0.25

    top_set=set()
    bottom_set=set()
    top=[]
    down=[]

    for i in pos:
        npos=pos[i]
        if i in layer1:
            pos[i]=[d2*(npos[0]),d2*(npos[1]+d1)] 
    #         pos[i]=[d2*(npos[0]-d1),d2*(npos[1]+d1)] 
            top_set.add(i)
            top.append(pos[i])
        else:
            pos[i]=[d6*(npos[0]),d6*(npos[1]-d1)] 
    #         pos[i]=[d2*(npos[0]+d1),d2*(npos[1]+d1)] 
            bottom_set.add(i)
            down.append(pos[i])

    xtop=[i[0] for i in top]
    ytop=[i[1] for i in top]

    atop = [min(xtop)-d4/2.+d5,max(ytop)+d4/2.+d3]
    btop = [max(xtop)+d4/2.+d5,max(ytop)+d4/2.+d3]   
    ctop = [max(xtop)+d4/2.-d5,min(ytop)-d4/2.-d3]
    dtop = [min(xtop)-d4/2.-d5,min(ytop)-d4/2.-d3]

    xdown=[i[0] for i in down]
    ydown=[i[1] for i in down]

    adown = [min(xdown)-d4/2+d5,max(ydown)+d4/2.+d3]
    bdown = [max(xdown)+d4/2.+d5,max(ydown)+d4/2.+d3]
    cdown = [max(xdown)+d4/2.-d5,min(ydown)-d4/2.-d3]
    ddown = [min(xdown)-d4/2.-d5,min(ydown)-d4/2.-d3]

    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(121)

    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green','m','c']))
    ccpar={}
    # print ccv
    for i,v in enumerate(ccv):
        for vv in v:
            # print i,v 
            if i not in ccpar:
                ccpar[i]=[vv]
            else:
                ccpar[i].append(vv)
    # print ccpar
    rccv={}
    for i,v in ccpar.items():
        # print i,v
        for ii in v:
            # print i,v,ii
            rccv[ii]=i
    # print len(ccpar)
    # print len(ccpar.keys())
    # print rccv.keys()
    col_dic={}
    for i,v in ccpar.items():
        # print i,v
        # for nd in v:
        colll=random.choice(colors)
        # ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll
    colors_a=[]
    colors_b=[]
    for nd in top_set:
        colors_a.append(col_dic[rccv[nd]])
    for nd in bottom_set:
        colors_b.append(col_dic[rccv[nd]])

    sst='Chromatic coloring in %i groups distributed over layers' %(len(ccpar.keys()))
    plt.title(sst)

    ax.add_patch(Polygon([atop,btop,ctop,dtop],color='r',alpha=0.1)) 
    plt.plot([atop[0],btop[0],ctop[0],dtop[0],atop[0]],[atop[1],btop[1],ctop[1],dtop[1],atop[1]],'-r')
    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='b',alpha=0.1)) 
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-b')
    nx.draw_networkx_nodes(G,pos, nodelist=top_set,node_color=colors_a,alpha=nodal,node_size=nodesize,node_shape='s')
    nx.draw_networkx_nodes(G,pos,nodelist=bottom_set,node_color=colors_b,alpha=nodal,node_size=nodesize)
    if withlabels:
        nx.draw_networkx_labels(G,pos)
    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    nx.draw_networkx_edges(G,pos,edgelist=lay1_edges,edge_color='r',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=lay2_edges,edge_color='b',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=edgeList,edge_color='k',alpha=alpha)
    plt.axis('off')

    ax=fig.add_subplot(122)
    # colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    # colors=list(set(colors)-set(['red','blue','green','m','c']))
    ccpar={}

    for i,v in enumerate(par):
        for vv in v:
            # print i,v 
            if i not in ccpar:
                ccpar[i]=[vv]
            else:
                ccpar[i].append(vv)
    # print ccpar
    rccv={}
    for i,v in ccpar.items():
        # print i,v
        for ii in v:
            # print i,v,ii
            rccv[ii]=i
    # print len(ccpar)
    # print len(ccpar.keys())
    # print rccv.keys()
    col_dic={}
    for i,v in ccpar.items():
        # print i,v
        # for nd in v:
        colll=random.choice(colors)
        # ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll

    # for i in par:
    #     for v in i:
    #         if v not in ccpar:
    #             ccpar[v]=[i]
    #         else:
    #             ccpar[v].append(i)
    # rccv={}
    # for i,v in ccpar.items():
    #     for ii in v:
    #         rccv[ii]=i

    # col_dic={}
    # for i,v in ccpar.items():
    #     # for nd in v:
    #     colll=random.choice(colors)
    #     # ellc.append(colll)
    #     colors.remove(colll)
    #     col_dic[i]=colll
    colors_a=[]
    colors_b=[]
    for nd in top_set:
        colors_a.append(col_dic[rccv[nd]])
    for nd in bottom_set:
        colors_b.append(col_dic[rccv[nd]])
    ax.add_patch(Polygon([atop,btop,ctop,dtop],color='r',alpha=0.1)) 
    plt.plot([atop[0],btop[0],ctop[0],dtop[0],atop[0]],[atop[1],btop[1],ctop[1],dtop[1],atop[1]],'-r')
    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='b',alpha=0.1)) 

    sst='Community coloring in %i groups distributed over layers' %(len(ccpar.keys()))
    plt.title(sst)
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-b')
    nx.draw_networkx_nodes(G,pos, nodelist=top_set,node_color=colors_a,alpha=nodal,node_size=nodesize,node_shape='s')
    nx.draw_networkx_nodes(G,pos,nodelist=bottom_set,node_color=colors_b,alpha=nodal,node_size=nodesize)
    if withlabels:
        nx.draw_networkx_labels(G,pos)
    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    nx.draw_networkx_edges(G,pos,edgelist=lay1_edges,edge_color='r',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=lay2_edges,edge_color='b',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=edgeList,edge_color='k',alpha=alpha)
    plt.axis('off')

    plt.show()
# k=3
# G, dic_of_Graphs_final,  edgelist ,nmap ,mapping=synthetic_multi_level_bip_dic(k,n=[10,5,30],p=[.11,.12,.13,.22,.23,.33])
# print G.nodes(data=True)
# print G.edges()
# print
# print  dic_of_Graphs_final
# print
# print   edgelist 
# print
# print nmap 
# print
# print mapping
# n1=n2=n3=50
# p1=p2=p3=0.01
# q1=q2=q3=0.01
# plot_graph(G,J,FF,DD,n1,n2,n3,d1=1,d2=10.,d3=0.8,nodesize=50,withlabels=False,edgelist=edgeList,layout=False,b_alpha=0.25)
# plot_graph_k_nm(k,len(G.nodes()),G,dic_of_Graphs_final, 111,d1=0,d2=2,d3=0,d4=.3,d5=1,d6=.4,d7=.2,d8=1,d9=0.3,colors_grey='gray',nodesize=100,withlabels=True,edgelist=edgelist,layout=True,b_alpha=0.5)
