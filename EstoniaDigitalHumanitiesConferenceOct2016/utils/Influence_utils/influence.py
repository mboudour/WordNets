__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

'''
This script computes and plots simulations of network infuence.
'''

import networkx as nx
import utils_attributes as utilat
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import itertools as it
import numpy as np
import random
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

np.seterr(all='ignore')

def influence_sim(nodes,p,sa,iterations,scale=1000,new_old=False,source = [0]):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)
    checklist={sou:(True,0) for sou in source }

    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    if new_old:
        F,asoc=utilat.create_random_scalar_attributes2(G,scale)
    else:
        F,asoc=utilat.create_random_scalar_attributes(G,scale)

    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]

    fig = plt.figure(figsize=(17,17))
    if not new_old:


        sstt="Initial distribution of scalar attributes over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
        plt.subplot(3,2,1).set_title(sstt)
        # plt.set_cmap('cool')
        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
        plt.axis('equal')
        plt.axis('off')
        
        # plt.figure(2)
        sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
        plt.subplot(3,2,5).set_title(sstt)
    else:
        sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
        plt.subplot(211).set_title(sstt)

    # for i in F.nodes(data=True):
        # print i
    # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
    iterat=[]
    assort=[]
    # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    nod5=[]
    for ii in range(iterations):
        # sa=0.05
        y={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
        nod5.append(y[5])
        checkin=True
        # nd=F.nodes()[0]
        for nd in source:
            # print nd
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            
            for nnei in nei:
                if nnei in checklist:
                    if checklist[nnei][0] and checklist[nnei][1]<ii:
                        uu+=y[nnei]

                # if checklist[nnei][0] and checklist[nnei][1]<ii:
                #     uu+=y[nnei]

                # uu+=y[nnei]#F.node[nnei]['scalar_attribute']
            Xnei=uu/len(nei)
            # X=F.node[nd]['scalar_attribute']
            X=y[nd]
            if new_old:
                uX=(sa*Xnei)+(2-sa)*X
            else:
                uX=(sa*Xnei)+(1-sa)*X
            insau=int(uX*scale)
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        sources=set(source)
        for nd in set(F.nodes())-sources:
            # sa=1-(1./nx.degree(F,nd))
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            for nnei in nei:
                if nnei in checklist:
                    if checklist[nnei][0] and checklist[nnei][1]<ii:
                        uu+=y[nnei]
                    # checklist[]
            if uu!=0 and nd not in checklist:
                checklist[nd]=(True,ii)
            X=y[nd]
            # X=F.node[nd]['scalar_attribute']
            if uu!=0:
                Xnei=uu/len(nei)
                if new_old:
                    uX=(sa*Xnei)+(2-sa)*X
                else:
                    uX=(sa*Xnei)+(1-sa)*X
                insau=int(uX*scale)
            else:
                uX=y[nd]
                insau=F.node[nd]['scalar_attribute_numeric']
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)

            
        # for i in F.nodes(data=True):
        #   print i
        # Checking for attributes equality
        # print ii
        # y1=y
        # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        # raw_input()
        if ii ==ckck and ii<10:
            # print ii
            if new_old:
                ckck+=5
                kckc+=1
                # plt.subplot(211)
                # print ckck
                # print kckc
            else:
            # col=['%.5f' %yy for yy in y]
                col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
                sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(ii+1)

                plt.subplot(3,2,kckc).set_title(sstt)
                nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
                plt.axis('equal')
                plt.axis('off')
                ckck+=5
                kckc+=1
                plt.subplot(3,2,5)

        # for yy in it.combinations(y,2):
        #   checkin=checkin and yy[0] -yy[1] <(1./scale)
        # for yy in range(len(y1)):
        #   # print y[yy]-y1[yy]<(1./scale)
        #   checkin=checkin and y[yy]-y1[yy]<(0.1/(scale))
        #   # print checkin
        # if checkin:
        #   break
        # print y
        # asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # if np.isnan(asss):
        #     asss=1.
        # # print 'Iteration %i ==> %f' %(ii,asss),y 
        # # print type(asss), asss<-1,asss>1
        # iterat.append(ii)

        # assort.append(asss)
        # print assort

        # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        yplot=[y[i] for i in F.nodes()]
        plt.plot(F.nodes(),yplot)
        


        # if asss==1. :
        #   break
    # raw_input()
    # if new_old:
        # plt.plot(F.nodes(),yplot,linewidth=3.)
        # sstt= "Time variation of scalar attribute assortativity coefficient"

        # plt.subplot(212).set_title(sstt)

        # # plt.figure(3)

        # plt.plot(iterat,assort)
        # plt.ylim(-1.1,1.1)
        # continue
    if not new_old:
        asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        if np.isnan(asss):
            asss=1.
        # print 'Iteration %i ==> %f' %(ii,asss),y 
        # print type(asss), asss<-1,asss>1
        iterat.append(ii)

        assort.append(asss)
        plt.plot(F.nodes(),yplot,linewidth=3.)
        sstt= "Time variation of scalar attribute assortativity coefficient"

        plt.subplot(3,2,6).set_title(sstt)

        # plt.figure(3)

        plt.plot(iterat,assort)
        plt.ylim(-1.1,1.1)
        # plt.figure(3)
        # plt.plot(F.nodes(),y)
        # col=['%.5f' %yy for yy in y]
        col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        sstt="Distribution of scalar attributes over graph nodes at %i iterations\n (consensual attribute = %s)" %(iterations,col[0])
        plt.subplot(3,2,4).set_title(sstt)

        # plt.figure(4)

        
        # print col
        # print [F.node[i]['scalar_attribute_numeric'] for i in F.nodes()]
        # pos=nx.spring_layout(G)
        ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    # plt.axis('equal')
    # plt.axis('off')
    plt.subplot(212)

    plt.plot(range(len(nod5)),nod5)

    plt.show()
    # return G



#     plt.subplot(2,2,1).set_title("Original distribution of scalar attributes over graph nodes")
#     # plt.set_cmap('cool')
#     nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
#     # nx.draw_networkx(G,pos=pos, node_color=col,cmap=plt.cm.Cool)
#     plt.axis('equal')
#     plt.axis('off')

#     # plt.figure(2)
#     plt.subplot(2,2,2).set_title("Time variation of scalar attributes over graph nodes")

#     # for i in F.nodes(data=True):
#         # print i
#     # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
#     iterat=[]
#     assort=[]
#     y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
#     for ii in range(iterations):
#         # sa=0.05
#         checkin=True

#         for nd in F.nodes():
#             # sa=1-(1./nx.degree(F,nd))
#             uu=0
#             nei=nx.neighbors(F,nd)
#             # print nei
#             for nnei in nei:
#                 uu+=F.node[nnei]['scalar_attribute']

#             sau=(sa*uu/len(nei))+(1-sa)*F.node[nd]['scalar_attribute']
#             insau=int(sau*scale)
#             F.add_node(nd,scalar_attribute=sau,scalar_attribute_numeric=insau)

#         # for i in F.nodes(data=True):
#         #   print i
#         # Checking for attributes equality
#         y1=y
#         y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
#         # for yy in it.combinations(y,2):
#         #   checkin=checkin and yy[0] -yy[1] <(1./scale)
#         # for yy in range(len(y1)):
#         #   # print y[yy]-y1[yy]<(1./scale)
#         #   checkin=checkin and y[yy]-y1[yy]<(0.1/(scale))
#         #   # print checkin
#         # if checkin:
#         #   break
#         asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
#         if np.isnan(asss):
#             asss=1.
#         # print 'Iteration %i ==> %f' %(ii,asss),y 
#         # print type(asss), asss<-1,asss>1
#         iterat.append(ii)

#         assort.append(asss)

#         # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
#         # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
#         plt.plot(F.nodes(),y)
#         # if asss==1. :
#         #   break
#     plt.plot(F.nodes(),y,linewidth=3.)


#     plt.subplot(2,2,3).set_title("Time variation of scalar attribute assortativity coefficient")

#     # plt.figure(3)

#     plt.plot(iterat,assort)
#     plt.ylim(-1.1,1.1)
#     # plt.figure(3)
#     # plt.plot(F.nodes(),y)

#     plt.subplot(2,2,4).set_title("Final distribution of scalar attributes over graph nodes")

#     # plt.figure(4)

#     col=['%.5f' %yy for yy in y]
#     # print col
#     # print [F.node[i]['scalar_attribute_numeric'] for i in F.nodes()]
#     # pos=nx.spring_layout(G)
#     ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
#     nx.draw_networkx(G,pos=pos, node_color=col)
#     plt.axis('equal')
#     plt.axis('off')

#     plt.show()
def influence_sim_v(iterations,G,u_all,insrplot=False,source=None,pos=None):
    # print G.nodes()
    # print G.edges(data=True)
    if pos == None:
        pos=nx.spring_layout(G)

    fig = plt.figure(figsize=(17,17))
    col=[v[0] for i,v in u_all.items()]
    sstt="Initial distribution of scalar attributes over graph nodes" 
    ax1=plt.subplot2grid((7,2),(0,0),colspan=1,rowspan=2)
    ax1.set_title(sstt)
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)
    plt.axis('equal')
    plt.axis('off')

    nu_all={}
    # print u_all.keys()
    for i,v in u_all.items():
        for j,u in enumerate(v):
            

            # if j>0:
            if j not in nu_all:
                if j==0:
                    nu_all[j]=[u]
                else:
                    w=nu_all[j-1][-1]
                    nu_all[j]=[(u)+w]
            else:
                # if i in source:
                #     nu_all[j].append(u)
                if j==0:
                    nu_all[j].append(u)
                else:
                    w=nu_all[j-1][-1]
                    nu_all[j].append((u)+w)
                    # print u+u_all[i][j],u,u_all[i][j],i,w
                    # if j>100:
                    #     print aaaa
            # else:
            #     if j not in nu_all:
            #         nu_all[j]=

    sstt = "Time variation of opinions (v) over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
    # plt.subplot(413).set_title(sstt)
    ax3=plt.subplot2grid((7,2),(2,0),colspan=2)
    # plt.subplot(3,2,1).set_title(sstt)
    ax3.set_title(sstt)
    for i,v in nu_all.items():
        plt.plot(G.nodes(),v)

    sstt = "Time variation of opinions (v) of each graph node" #%F.nodes()[0]#,starting_value_of_zero_node)
    # plt.subplot(414).set_title(sstt)
    ax4=plt.subplot2grid((7,2),(3,0),colspan=2,rowspan=3)
        # plt.subplot(3,2,1).set_title(sstt)
    ax4.set_title(sstt)
    final_d={}
    for vkkk,kvvv in u_all.items():
        nnnn=[]
        if vkkk in source:
            nnnn.append(kvvv[0])
        else:
            for i,vkvk in enumerate(kvvv):
                
                if i==0:
                    nnnn.append(vkvk)
                    # plt.plot(range(len(kvvv)),vkvk)
                else:
                    w=nnnn[-1]
            # if vkkk == source[0]:
            #     continue
            # final_d[vkkk]=kvvv[-1]
                    nnnn.append((vkvk+w))
            final_d[vkkk]=nnnn
        plt.plot(range(len(nnnn)),nnnn)
        y_pos=nnnn[-1]
        plt.text(iterations+(iterations/100.), y_pos, vkkk, fontsize=10)
    if insrplot:
        axins=zoomed_inset_axes(ax4,12,loc=4)
        for ivv,vkkk in enumerate(nodds):
            kvvv=nodds[vkkk]
            # if vkkk == source[0]:
            #     continue
            
            # final_d[vkkk]=kvvv[-1]
            # if ivv < 15:

            axins.plot(range(len(kvvv)),kvvv)
        # axins.plot()
        x1, x2, y1, y2 = 0.0,40.0, 0., 0.031
        axins.set_xlim(x1, x2)
        axins.set_ylim(y1, y2)
        plt.xticks(np.arange(x1,x2,2))
        plt.yticks(np.arange(y1,y2,.01))
        mark_inset(ax4, axins, loc1=2, loc2=4, fc="none", ec="0.5")

    # plt.axis('equal')
    # col=[G.node[i]['scalar_attribute'] for i in G.nodes()]
    # for i,v in u_all.items():
    #     print i,len(v)
    col=[v[iterations-1] for i,v in u_all.items()]
    sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(iterations) #,col[0]) #\n (consensual attribute = %s)
    # plt.subplot(4,1,2).set_title(sstt)
    ax2=plt.subplot2grid((7,2),(0,1),colspan=1,rowspan=2)
    # plt.subplot(3,2,1).set_title(sstt)
    ax2.set_title(sstt)

    plt.axis('equal')
    plt.axis('off')

    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)

    plt.show()
    return final_d

# F,y_all,source,y_orig,final_d,snodds=
def influence_sim_dh_F_J_multi(k,nodes,p,ssas_ds,iterations,G,dic_of_Graphs_final,new_old=None,source=[0],source_u=[1],su=.9,h=1.,funcion='',insrplot=False,no_change=False,scale=1000,):
# def influence_sim_dh_F_J(nodes,p,sa,iterations,G=None,scale=1000,new_old=False,source = [0],source_u=[1],su=0.9,h=0.3,funcion='',insrplot=False,no_change=False):
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)
    checklist={sou:(True,0) for sou in source }
    # print checklist
    # print aaa
    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    print no_change,new_old
    print G.nodes()
    if new_old or new_old==None:
        if no_change:
            print 'aaaa'
            F=nx.Graph(G)
        else:
            F=utilat.create_random_scalar_attributes_dh(G,scale,source=source,source_u=source_u)
    # elif no_change:
        
    else:
        F,asoc=utilat.create_random_scalar_attributes(G,scale)

    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    # print col
    # print [i for i in F.nodes(data=True)]
    # print aaa
    if new_old != None:
        print col,lineno()
    initial_val={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    ##### NOT for this
    if new_old!=None and not new_old:
        fig = plt.figure(figsize=(17,17))

        sstt="Initial distribution of opinions over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
        # ax1=plt.subplot2grid((3,2),(0,0),colspan=1)
        plt.subplot(3,2,1).set_title(sstt)
        # ax1.set_title(sstt)
        # plt.set_cmap('cool')
        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
        plt.axis('equal')
        plt.axis('off')
        
        # plt.figure(2)
        sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
        plt.subplot(3,2,5).set_title(sstt)
        # ax2=plt.subplot2grid((3,2),(2,0),colspan=2)
        # # plt.subplot(3,2,1).set_title(sstt)
        # ax2.set_title(sstt)
        
    # elif new_old==None:
    #     continue
    elif new_old !=None and new_old:
        fig = plt.figure(figsize=(17,17))
        sstt="Initial distribution of scalar attributes over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
        # plt.subplot(411).set_title(sstt)
        ax1=plt.subplot2grid((7,2),(0,0),colspan=1,rowspan=2)
        ax1.set_title(sstt)
        # plt.set_cmap('cool')
        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)
        plt.axis('equal')
        plt.axis('off')
        sstt = "Time variation of opinions over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
        # plt.subplot(413).set_title(sstt)
        ax3=plt.subplot2grid((7,2),(2,0),colspan=2)
        # plt.subplot(3,2,1).set_title(sstt)
        ax3.set_title(sstt)
    ####### NOT for multi

    iterat=[]
    assort=[]
    # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    # nod5=[]
    nodds={}
    snodds={}
    # ssas_d={i:},
    if new_old!= None:
        print source,source_u,ssas_d, lineno()
    # nod4=random.choice(G.nodes())
    # print nod4,F.node[nod4]['scalar_attribute']
    # print F.edges()

    y_orig={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    if new_old!= None:

        print y_orig , lineno()
    # for kkk,vvv in y_orig.items():
    #     if kkk not in nodds:
    #         nodds[kkk]=[vvv]
    #         snodds[kkk]=[vvv]
    #     else:
    #         nodds[kkk].append(vvv)
    #         if ii <40:
    #             snodds[kkk].append(vvv)
    # nod5.append(y[5])
    checkin=True
    # nd=F.nodes()[0]
    print funcion
    # print ssas_ds
    # 
    # print aaaaa
    for ii in range(1,iterations):
        y={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
        for kkk,vvv in y.items():
            if kkk not in nodds:
                nodds[kkk]=[vvv]
                snodds[kkk]=[vvv]
            else:
                nodds[kkk].append(vvv)
                if ii <400:
                    snodds[kkk].append(vvv)
        checkin=True
        for nd in G.nodes():
            uX=0
            xnei={}
            deg=G.degree(nd)
            snd=0
            for iij in range(k):
                for jji in range(iij,k):
                    gg=dic_of_Graphs_final[(iij,jji)]
                    if nd not in gg.nodes():
                        continue
                    xnei[(iij,jji)]={}
                    uu=0
                    snd+=ssas_ds[(iij,jji)][nd]
                    nei=nx.neighbors(gg,nd)
                    if len(nei)==0:
                        continue
                    # print nei,nd
                    for nnei in nei:
                        if nnei in checklist:
                            if checklist[nnei][0] and checklist[nnei][1]<ii:
                                uu+=y[nnei]
                    if uu!=0:
                        xnei[(iij,jji)][nd]=uu/deg
                    if uu!=0 and nd not in checklist:
                        checklist[nd]=(True,ii)
            # print xnei
            # print ssas_ds[(iij,jji)][nd]
            # print xnei[(iij,jji)][nd]
            # for iij in range(k):
            #     for jji in range(iij,k):
            for iij,jji in xnei:
                # print iij,jji
                if nd not in xnei[(iij,jji)]:
                    continue
                # print xnei[(iij,jji)]
                uX+=eval(funcion)
            F.add_node(nd,scalar_attribute=uX)

        # for nd in source:

        #     ssa=ssas_d[nd]
        #     uu=0
        #     nei=nx.neighbors(F,nd)
        #     # print nei
            
        #     for nnei in nei:
        #         if nnei in checklist:
        #             if checklist[nnei][0] and checklist[nnei][1]<ii:
        #                 uu+=y[nnei]
        #     Xnei=uu/len(nei)
        #     # X=F.node[nd]['scalar_attribute']
        #     X=y[nd]
        #     if new_old or new_old==None:
        #         uX=eval(funcion)
        #     else:
        #         uX=(ssa*Xnei)+(1-ssa)*X
        #     insau=int(uX*scale)
        #     F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        # sources=set(source)
        # # print source,F.nodes()
        # # print aaa
        # for nd in set(F.nodes())-sources:
        #     # sa=1-(1./nx.degree(F,nd))
        #     # if nd==nod4:
        #     #     ssa=0
        #     # else:
        #     #     ssa=sa
        #     uu=0
        #     nei=nx.neighbors(F,nd)
        #     # print nei
        #     for nnei in nei:
        #         # print nd,nnei,checklist,nei,ii
        #         if nnei in checklist:
        #             # print 'a',checklist[nnei][0] ,checklist[nnei][1]<ii,checklist[nnei][0] and checklist[nnei][1]<ii,ii,y[nnei]
        #             if checklist[nnei][0] and checklist[nnei][1]<ii:
        #                 uu+=y[nnei]
        #         # print uu
        #             # checklist[]
        #     # if nd not in checklist:
        #     #     print nd,uu,nei
        #     if uu!=0 and nd not in checklist:
        #         checklist[nd]=(True,ii)
        #     X=y[nd]
        #     # X=F.node[nd]['scalar_attribute']
        #     # if uu!=0:
        #     Xnei=uu/len(nei)
        #     if new_old or new_old==None:
        #         # ssa=sa
        #         ssa=ssas_d[nd]
        #         # if ii == 0:
        #         #     uX=(ssa*(Xnei-X))
        #         # else:
        #             # uX=X+h/(ssa*Xnei)
        #         # uX=X+(h*ssa*Xnei)
        #         # uX= X+h*(X-Xnei)
        #         # elif nd== nod4:
        #         #     uX=X
        #         # else:
        #         if Xnei==0:
        #             continue
        #         else:
        #             uX=eval(funcion)
        #             # uX=eval(funcion)
                    
        #             # uX=(ssa*Xnei)+(2-ssa)*X
        #     else:
        #         uX=(ssa*Xnei)+(1-ssa)*X
        #     insau=int(uX*scale)
        #     # else:
        #     #     uX=y[nd]
        #     #     insau=F.node[nd]['scalar_attribute_numeric']
        #     # print '0000000000000000000000',ii,'0000000000000000000'
        #     # print X,uX
        #     # print nd
        #     F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        if ii ==ckck and ii<10:
            # print ii
            if new_old or new_old==None:
                ckck+=5
                kckc+=1
                # plt.subplot(211)
                # print ckck
                # print kckc
            else:
            # col=['%.5f' %yy for yy in y]
                col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
                sstt="Distribution of opinions over graph nodes at %i iterations" %(ii+1)

                plt.subplot(3,2,kckc).set_title(sstt)
                nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
                plt.axis('equal')
                plt.axis('off')
                ckck+=5
                kckc+=1
                plt.subplot(3,2,5)

        yplot=[y[i] for i in F.nodes()]
        if new_old!=None:
            plt.plot(F.nodes(),yplot)
        # print yplot
        # print checklist
    if new_old:
        sstt = "Time variation of opinions of each graph node" #%F.nodes()[0]#,starting_value_of_zero_node)
        # plt.subplot(414).set_title(sstt)
        ax4=plt.subplot2grid((7,2),(3,0),colspan=2,rowspan=3)
            # plt.subplot(3,2,1).set_title(sstt)
        ax4.set_title(sstt)

    elif new_old!=None and not new_old:
        asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        if np.isnan(asss):
            asss=1.
        # print 'Iteration %i ==> %f' %(ii,asss),y 
        # print type(asss), asss<-1,asss>1
        iterat.append(ii)

        assort.append(asss)
        plt.plot(F.nodes(),yplot,linewidth=3.)
        sstt= "Time variation of scalar attribute assortativity coefficient"

        plt.subplot(3,2,6).set_title(sstt)

        # plt.figure(3)

        plt.plot(iterat,assort)
        plt.ylim(-1.1,1.1)
        col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        sstt="Distribution of opinions over graph nodes at %i iterations" %(iterations,col[0]) #\n (consensual attribute = %s)
        plt.subplot(3,2,4).set_title(sstt)  #   

        # ,figsize=(15,15)

        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    # plt.axis('equal')
    # plt.axis('off')
    # elif new_old==None:
    #     continue


    
    # try:
    #     print 'Boundary node %i = %f' %(nod4,y[nod4])
    # except:
    #     print 'not'

    # plt.plot(range(len(nod5)),nod5)
    final_d={}
    for vkkk,kvvv in nodds.items():
        # if vkkk == source[0]:
        #     continue
        final_d[vkkk]=kvvv[-1]
        y_pos=kvvv[-1]
        if new_old!= None:
            # continue
            plt.plot(range(len(kvvv)),kvvv)
            plt.text(iterations+(iterations/100.), y_pos, vkkk, fontsize=10)
    if insrplot:
        axins=zoomed_inset_axes(ax4,12,loc=4)
        for ivv,vkkk in enumerate(nodds):
            kvvv=nodds[vkkk]
            # if vkkk == source[0]:
            #     continue
            
            # final_d[vkkk]=kvvv[-1]
            # if ivv < 15:

            axins.plot(range(len(kvvv)),kvvv)
        # axins.plot()
        x1, x2, y1, y2 = 0.0,40.0, 0., 0.2531
        axins.set_xlim(x1, x2)
        axins.set_ylim(y1, y2)
        plt.xticks(np.arange(x1,x2,2))
        plt.yticks(np.arange(y1,y2,.01))
        mark_inset(ax4, axins, loc1=2, loc2=4, fc="none", ec="0.5")

    # plt.axis('equal')
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    if new_old !=None:
        sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(iterations) #,col[0]) #\n (consensual attribute = %s)
        # plt.subplot(4,1,2).set_title(sstt)
        ax2=plt.subplot2grid((7,2),(0,1),colspan=1,rowspan=2)
        # plt.subplot(3,2,1).set_title(sstt)
        ax2.set_title(sstt)

        plt.axis('equal')
        plt.axis('off')

        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)
    if new_old!= None:

        print 'Final ', final_d
        print 'Until the 40'
    # degge=c
    no_zeros={}
    for ikk,vkk in snodds.items():
        # print ikk,vkk
        for kkkk,kkvv in enumerate(vkk):
            # print kkkk

            if isinstance(kkvv,float):
                no_zeros[ikk]=(kkkk,kkvv)
                if new_old!= None:
                    print 'Node %i left 0 at %i iterations becoming %.4f and deg^-1 %.4f' %(ikk, kkkk, kkvv,1./closs[ikk])
                break

    if new_old !=None:
        plt.show()
    return F,nodds,source,y_orig,final_d,no_zeros

def influence_sim_dh_F_J_mu(nodes,p,iterations,G=None,scale=1000,new_old=False,source = [0],source_u=[1],su=0.9,h=0.3,funcion='',insrplot=False,no_change=False,ssas_d={}):
    if G==None:
        while  True:
            # print 'creating erdos_renyi_graph'
            # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
            G=nx.erdos_renyi_graph(nodes,p)
            if nx.is_connected(G) :
                # if 4 not in nx.isolates(G):
                break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)
    # closs=nx.closeness_centrality(G)
    closs=nx.degree(G)
    closse=[v for v in sorted(closs,key=closs.get,reverse=True)]
    if new_old!=None:
        print closse[-1],nx.neighbors(G,closse[-1]), lineno()

    # print closse,closs
    # print aaa
    
    # print ssas_d
    # ssas_d={}
    # if len(source)==0:
    #     source = [closse[-1]]
    #     source_u=[su]
    #     if len(ssas_d)==0:
    #         ssas_d[closse[-1]]=0
    # else:
    #     for nd  in source:
    #         if len(ssas_d)==0:
    #             ssas_d[nd]=0
    # if len(ssas_d)==0:
    #     for nd in set(G.nodes())-set(source):
    #         ssas_d[nd]=sa
    checklist={sou:(True,0) for sou in source }
    # print checklist
    # print ssas_d
    # print aaaa
    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    if new_old or new_old==None:
        if no_change:
            print 'aaaa'
            F=nx.Graph(G)
        else:
            F=utilat.create_random_scalar_attributes_dh(G,scale,source=source,source_u=source_u)
    # elif no_change:
        
    else:
        F,asoc=utilat.create_random_scalar_attributes(G,scale)

    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    if new_old != None:
        print source,sa,nx.neighbors(F,source[0])
        print col,lineno()
    initial_val={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    
    if new_old!=None and not new_old:
        fig = plt.figure(figsize=(17,17))

        sstt="Initial distribution of opinions over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
        # ax1=plt.subplot2grid((3,2),(0,0),colspan=1)
        plt.subplot(3,2,1).set_title(sstt)
        # ax1.set_title(sstt)
        # plt.set_cmap('cool')
        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
        plt.axis('equal')
        plt.axis('off')
        
        # plt.figure(2)
        sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
        plt.subplot(3,2,5).set_title(sstt)
        # ax2=plt.subplot2grid((3,2),(2,0),colspan=2)
        # # plt.subplot(3,2,1).set_title(sstt)
        # ax2.set_title(sstt)
        
    # elif new_old==None:
    #     continue
    elif new_old !=None and new_old:
        fig = plt.figure(figsize=(17,17))
        sstt="Initial distribution of scalar attributes over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
        # plt.subplot(411).set_title(sstt)
        ax1=plt.subplot2grid((7,2),(0,0),colspan=1,rowspan=2)
        ax1.set_title(sstt)
        # plt.set_cmap('cool')
        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)
        plt.axis('equal')
        plt.axis('off')
        sstt = "Time variation of opinions over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
        # plt.subplot(413).set_title(sstt)
        ax3=plt.subplot2grid((7,2),(2,0),colspan=2)
        # plt.subplot(3,2,1).set_title(sstt)
        ax3.set_title(sstt)

    iterat=[]
    assort=[]
    # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    # nod5=[]
    nodds={}
    snodds={}
    # ssas_d={i:},
    if new_old!= None:
        print source,source_u,ssas_d, lineno()
    # nod4=random.choice(G.nodes())
    # print nod4,F.node[nod4]['scalar_attribute']
    # print F.edges()

    y_orig={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    if new_old!= None:

        print y_orig , lineno()
        # print aaa
    # for kkk,vvv in y_orig.items():
    #     if kkk not in nodds:
    #         nodds[kkk]=[vvv]
    #         snodds[kkk]=[vvv]
    #     else:
    #         nodds[kkk].append(vvv)
    #         if ii <40:
    #             snodds[kkk].append(vvv)
    # nod5.append(y[5])
    checkin=True
    # nd=F.nodes()[0]
    
    for ii in range(1,iterations):
        # print ii,ssas_d
        # sa=0.05
        y={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
        # print ii, y
        for kkk,vvv in y.items():
            if kkk not in nodds:
                nodds[kkk]=[vvv]
                snodds[kkk]=[vvv]
            else:
                nodds[kkk].append(vvv)
                if ii <400:
                    snodds[kkk].append(vvv)
        # nod5.append(y[5])
        # print ii, nodds
        # raw_input()
        checkin=True
        # nd=F.nodes()[0]
        
        for nd in source:
            ssa=ssas_d[nd]
            # print nd,'heeey'
            # if nd==nod4:
            #     ssa=0
            # else:
            #     ssa=sa

            # print nd
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            
            for nnei in nei:
                if nnei in checklist:
                    if checklist[nnei][0] and checklist[nnei][1]<ii:
                        uu+=y[nnei]
            Xnei=uu/len(nei)
            # X=F.node[nd]['scalar_attribute']
            X=y[nd]
            if new_old or new_old==None:
                # ssa=0
                # if ii == 0:
                #     uX=(ssa*(Xnei-X))
                # else:
                    # uX=X+h/(ssa*Xnei)
                # if nd !=4:
                # uX=X+(h*ssa*Xnei)
                # elif nd== nod4:
                #     uX=X
                # else:
                uX=eval(funcion)
                # uX=0
                # uX= X+h*(X-Xnei)
            # uX=(ssa*Xnei)+(2-ssa)*X
            else:
                uX=(ssa*Xnei)+(1-ssa)*X
            insau=int(uX*scale)
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        sources=set(source)
        # print source,F.nodes()
        # print aaa
        for nd in set(F.nodes())-sources:

            # sa=1-(1./nx.degree(F,nd))
            # if nd==nod4:
            #     ssa=0
            # else:
            #     ssa=sa
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei,lineno()
            for nnei in nei:
                # print nd,nnei,checklist,nei,ii
                if nnei in checklist:
                    # print 'a',checklist[nnei][0] ,checklist[nnei][1]<ii,checklist[nnei][0] and checklist[nnei][1]<ii,ii,y[nnei]
                    if checklist[nnei][0] and checklist[nnei][1]<ii:
                        uu+=y[nnei]
                # print uu,lineno()
                    # checklist[]
            # if nd not in checklist:
            #     print nd,uu,nei
            # print ii,checklist,uu
            if uu!=0 and nd not in checklist:
                checklist[nd]=(True,ii)
            X=y[nd]
            # X=F.node[nd]['scalar_attribute']
            if uu!=0:
                Xnei=uu/(len(nei)*1.)
            else:
                Xnei=0
            # print Xnei,lineno()
            if new_old or new_old==None:
                # ssa=sa
                # try:
                ssa=ssas_d[nd]
                # except Exception ,e:
                #     print e
                #     print nd
                #     print ssas_d
                #     print F.nodes()
                #     print G.nodes()


                # if ii == 0:
                #     uX=(ssa*(Xnei-X))
                # else:
                    # uX=X+h/(ssa*Xnei)
                # uX=X+(h*ssa*Xnei)
                # uX= X+h*(X-Xnei)
                # elif nd== nod4:
                #     uX=X
                # else:
                if Xnei==0:
                    continue
                else:
                    uX=eval(funcion)
                    # uX=eval(funcion)
                    
                    # uX=(ssa*Xnei)+(2-ssa)*X
            else:
                uX=(ssa*Xnei)+(1-ssa)*X
            insau=int(uX*scale)
            # else:
            #     uX=y[nd]
            #     insau=F.node[nd]['scalar_attribute_numeric']
            # print '0000000000000000000000',ii,'0000000000000000000'
            # print X,uX,lineno()
            # print nd
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        if ii ==ckck and ii<10:
            # print ii
            if new_old or new_old==None:
                ckck+=5
                kckc+=1
                # plt.subplot(211)
                # print ckck
                # print kckc
            else:
            # col=['%.5f' %yy for yy in y]
                col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
                sstt="Distribution of opinions over graph nodes at %i iterations" %(ii+1)

                plt.subplot(3,2,kckc).set_title(sstt)
                nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
                plt.axis('equal')
                plt.axis('off')
                ckck+=5
                kckc+=1
                plt.subplot(3,2,5)

        yplot=[y[i] for i in F.nodes()]
        if new_old!=None:
            plt.plot(F.nodes(),yplot)
        # print yplot
        # print checklist
    if new_old:
        sstt = "Time variation of opinions of each graph node" #%F.nodes()[0]#,starting_value_of_zero_node)
        # plt.subplot(414).set_title(sstt)
        ax4=plt.subplot2grid((7,2),(3,0),colspan=2,rowspan=3)
            # plt.subplot(3,2,1).set_title(sstt)
        ax4.set_title(sstt)

    elif new_old!=None and not new_old:
        asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        if np.isnan(asss):
            asss=1.
        # print 'Iteration %i ==> %f' %(ii,asss),y 
        # print type(asss), asss<-1,asss>1
        iterat.append(ii)

        assort.append(asss)
        plt.plot(F.nodes(),yplot,linewidth=3.)
        sstt= "Time variation of scalar attribute assortativity coefficient"

        plt.subplot(3,2,6).set_title(sstt)

        # plt.figure(3)

        plt.plot(iterat,assort)
        plt.ylim(-1.1,1.1)
        col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        sstt="Distribution of opinions over graph nodes at %i iterations" %(iterations,col[0]) #\n (consensual attribute = %s)
        plt.subplot(3,2,4).set_title(sstt)  #   

        # ,figsize=(15,15)

        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    # plt.axis('equal')
    # plt.axis('off')
    # elif new_old==None:
    #     continue


    
    # try:
    #     print 'Boundary node %i = %f' %(nod4,y[nod4])
    # except:
    #     print 'not'

    # plt.plot(range(len(nod5)),nod5)
    final_d={}
    for vkkk,kvvv in nodds.items():
        # if vkkk == source[0]:
        #     continue
        final_d[vkkk]=kvvv[-1]
        y_pos=kvvv[-1]
        if new_old!= None:
            # continue
            plt.plot(range(len(kvvv)),kvvv)
            plt.text(iterations+(iterations/100.), y_pos, vkkk, fontsize=10)
    if insrplot:
        axins=zoomed_inset_axes(ax4,12,loc=4)
        for ivv,vkkk in enumerate(nodds):
            kvvv=nodds[vkkk]
            # if vkkk == source[0]:
            #     continue
            
            # final_d[vkkk]=kvvv[-1]
            # if ivv < 15:

            axins.plot(range(len(kvvv)),kvvv)
        # axins.plot()
        x1, x2, y1, y2 = 0.0,40.0, 0., 0.2531
        axins.set_xlim(x1, x2)
        axins.set_ylim(y1, y2)
        plt.xticks(np.arange(x1,x2,2))
        plt.yticks(np.arange(y1,y2,.01))
        mark_inset(ax4, axins, loc1=2, loc2=4, fc="none", ec="0.5")

    # plt.axis('equal')
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    if new_old !=None:
        sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(iterations) #,col[0]) #\n (consensual attribute = %s)
        # plt.subplot(4,1,2).set_title(sstt)
        ax2=plt.subplot2grid((7,2),(0,1),colspan=1,rowspan=2)
        # plt.subplot(3,2,1).set_title(sstt)
        ax2.set_title(sstt)

        plt.axis('equal')
        plt.axis('off')

        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)
    if new_old!= None:

        print 'Final ', final_d
        print 'Until the 40'
    # degge=c
    no_zeros={}
    for ikk,vkk in snodds.items():
        # print ikk,vkk
        for kkkk,kkvv in enumerate(vkk):
            # print kkkk

            if isinstance(kkvv,float):
                no_zeros[ikk]=(kkkk,kkvv)
                if new_old!= None:
                    print 'Node %i left 0 at %i iterations becoming %.4f and deg^-1 %.4f' %(ikk, kkkk, kkvv,1./closs[ikk])
                break

    if new_old !=None:
        plt.show()
    return F,nodds,source,y_orig,final_d,no_zeros

def influence_sim_dh_F_J(nodes,p,sa,iterations,G=None,scale=1000,new_old=False,source = [0],source_u=[1],su=0.9,h=0.3,funcion='',insrplot=False,no_change=False,ssas_d={}):
    if G==None:
        while  True:
            # print 'creating erdos_renyi_graph'
            # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
            G=nx.erdos_renyi_graph(nodes,p)
            if nx.is_connected(G) :
                # if 4 not in nx.isolates(G):
                break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)
    # closs=nx.closeness_centrality(G)
    closs=nx.degree(G)
    closse=[v for v in sorted(closs,key=closs.get,reverse=True)]
    if new_old!=None:
        print closse[-1],nx.neighbors(G,closse[-1]), lineno()

    # print closse,closs
    # print aaa
    
    # print ssas_d
    # ssas_d={}
    if len(source)==0:
        source = [closse[-1]]
        source_u=[su]
        if len(ssas_d)==0:
            ssas_d[closse[-1]]=0
    else:
        for nd  in source:
            if len(ssas_d)==0:
                ssas_d[nd]=0
    if len(ssas_d)==0:
        for nd in set(G.nodes())-set(source):
            ssas_d[nd]=sa
    checklist={sou:(True,0) for sou in source }
    # print checklist
    # print ssas_d
    # print aaaa
    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    if new_old or new_old==None:
        if no_change:
            print 'aaaa'
            F=nx.Graph(G)
        else:
            F=utilat.create_random_scalar_attributes_dh(G,scale,source=source,source_u=source_u)
    # elif no_change:
        
    else:
        F,asoc=utilat.create_random_scalar_attributes(G,scale)

    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    if new_old != None:
        print source,sa,nx.neighbors(F,source[0])
        print col,lineno()
    initial_val={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    
    if new_old!=None and not new_old:
        fig = plt.figure(figsize=(17,17))

        sstt="Initial distribution of opinions over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
        # ax1=plt.subplot2grid((3,2),(0,0),colspan=1)
        plt.subplot(3,2,1).set_title(sstt)
        # ax1.set_title(sstt)
        # plt.set_cmap('cool')
        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
        plt.axis('equal')
        plt.axis('off')
        
        # plt.figure(2)
        sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
        plt.subplot(3,2,5).set_title(sstt)
        # ax2=plt.subplot2grid((3,2),(2,0),colspan=2)
        # # plt.subplot(3,2,1).set_title(sstt)
        # ax2.set_title(sstt)
        
    # elif new_old==None:
    #     continue
    elif new_old !=None and new_old:
        fig = plt.figure(figsize=(17,17))
        sstt="Initial distribution of scalar attributes over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
        # plt.subplot(411).set_title(sstt)
        ax1=plt.subplot2grid((7,2),(0,0),colspan=1,rowspan=2)
        ax1.set_title(sstt)
        # plt.set_cmap('cool')
        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)
        plt.axis('equal')
        plt.axis('off')
        sstt = "Time variation of opinions over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
        # plt.subplot(413).set_title(sstt)
        ax3=plt.subplot2grid((7,2),(2,0),colspan=2)
        # plt.subplot(3,2,1).set_title(sstt)
        ax3.set_title(sstt)

    iterat=[]
    assort=[]
    # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    # nod5=[]
    nodds={}
    snodds={}
    # ssas_d={i:},
    if new_old!= None:
        print source,source_u,ssas_d, lineno()
    # nod4=random.choice(G.nodes())
    # print nod4,F.node[nod4]['scalar_attribute']
    # print F.edges()

    y_orig={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    if new_old!= None:

        print y_orig , lineno()
        # print aaa
    # for kkk,vvv in y_orig.items():
    #     if kkk not in nodds:
    #         nodds[kkk]=[vvv]
    #         snodds[kkk]=[vvv]
    #     else:
    #         nodds[kkk].append(vvv)
    #         if ii <40:
    #             snodds[kkk].append(vvv)
    # nod5.append(y[5])
    checkin=True
    # nd=F.nodes()[0]
    
    for ii in range(1,iterations):
        # print ii,ssas_d
        # sa=0.05
        y={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
        # print ii, y
        for kkk,vvv in y.items():
            if kkk not in nodds:
                nodds[kkk]=[vvv]
                snodds[kkk]=[vvv]
            else:
                nodds[kkk].append(vvv)
                if ii <400:
                    snodds[kkk].append(vvv)
        # nod5.append(y[5])
        # print ii, nodds
        # raw_input()
        checkin=True
        # nd=F.nodes()[0]
        
        for nd in source:
            ssa=ssas_d[nd]
            # print nd,'heeey'
            # if nd==nod4:
            #     ssa=0
            # else:
            #     ssa=sa

            # print nd
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            
            for nnei in nei:
                if nnei in checklist:
                    if checklist[nnei][0] and checklist[nnei][1]<ii:
                        uu+=y[nnei]
            Xnei=uu/len(nei)
            # X=F.node[nd]['scalar_attribute']
            X=y[nd]
            if new_old or new_old==None:
                # ssa=0
                # if ii == 0:
                #     uX=(ssa*(Xnei-X))
                # else:
                    # uX=X+h/(ssa*Xnei)
                # if nd !=4:
                # uX=X+(h*ssa*Xnei)
                # elif nd== nod4:
                #     uX=X
                # else:
                uX=eval(funcion)
                # uX=0
                # uX= X+h*(X-Xnei)
            # uX=(ssa*Xnei)+(2-ssa)*X
            else:
                uX=(ssa*Xnei)+(1-ssa)*X
            insau=int(uX*scale)
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        sources=set(source)
        # print source,F.nodes()
        # print aaa
        for nd in set(F.nodes())-sources:
            # sa=1-(1./nx.degree(F,nd))
            # if nd==nod4:
            #     ssa=0
            # else:
            #     ssa=sa
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei,lineno()
            for nnei in nei:
                # print nd,nnei,checklist,nei,ii
                if nnei in checklist:
                    # print 'a',checklist[nnei][0] ,checklist[nnei][1]<ii,checklist[nnei][0] and checklist[nnei][1]<ii,ii,y[nnei]
                    if checklist[nnei][0] and checklist[nnei][1]<ii:
                        uu+=y[nnei]
                # print uu,lineno()
                    # checklist[]
            # if nd not in checklist:
            #     print nd,uu,nei
            # print ii,checklist,uu
            if uu!=0 and nd not in checklist:
                checklist[nd]=(True,ii)
            X=y[nd]
            # X=F.node[nd]['scalar_attribute']
            if uu!=0:
                Xnei=uu/(len(nei)*1.)
            else:
                Xnei=0
            # print Xnei,lineno()
            if new_old or new_old==None:
                # ssa=sa
                ssa=ssas_d[nd]
                # if ii == 0:
                #     uX=(ssa*(Xnei-X))
                # else:
                    # uX=X+h/(ssa*Xnei)
                # uX=X+(h*ssa*Xnei)
                # uX= X+h*(X-Xnei)
                # elif nd== nod4:
                #     uX=X
                # else:
                if Xnei==0:
                    continue
                else:
                    uX=eval(funcion)
                    # uX=eval(funcion)
                    
                    # uX=(ssa*Xnei)+(2-ssa)*X
            else:
                uX=(ssa*Xnei)+(1-ssa)*X
            insau=int(uX*scale)
            # else:
            #     uX=y[nd]
            #     insau=F.node[nd]['scalar_attribute_numeric']
            # print '0000000000000000000000',ii,'0000000000000000000'
            # print X,uX,lineno()
            # print nd
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        if ii ==ckck and ii<10:
            # print ii
            if new_old or new_old==None:
                ckck+=5
                kckc+=1
                # plt.subplot(211)
                # print ckck
                # print kckc
            else:
            # col=['%.5f' %yy for yy in y]
                col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
                sstt="Distribution of opinions over graph nodes at %i iterations" %(ii+1)

                plt.subplot(3,2,kckc).set_title(sstt)
                nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
                plt.axis('equal')
                plt.axis('off')
                ckck+=5
                kckc+=1
                plt.subplot(3,2,5)

        yplot=[y[i] for i in F.nodes()]
        if new_old!=None:
            plt.plot(F.nodes(),yplot)
        # print yplot
        # print checklist
    if new_old:
        sstt = "Time variation of opinions of each graph node" #%F.nodes()[0]#,starting_value_of_zero_node)
        # plt.subplot(414).set_title(sstt)
        ax4=plt.subplot2grid((7,2),(3,0),colspan=2,rowspan=3)
            # plt.subplot(3,2,1).set_title(sstt)
        ax4.set_title(sstt)

    elif new_old!=None and not new_old:
        asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        if np.isnan(asss):
            asss=1.
        # print 'Iteration %i ==> %f' %(ii,asss),y 
        # print type(asss), asss<-1,asss>1
        iterat.append(ii)

        assort.append(asss)
        plt.plot(F.nodes(),yplot,linewidth=3.)
        sstt= "Time variation of scalar attribute assortativity coefficient"

        plt.subplot(3,2,6).set_title(sstt)

        # plt.figure(3)

        plt.plot(iterat,assort)
        plt.ylim(-1.1,1.1)
        col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        sstt="Distribution of opinions over graph nodes at %i iterations" %(iterations,col[0]) #\n (consensual attribute = %s)
        plt.subplot(3,2,4).set_title(sstt)  #   

        # ,figsize=(15,15)

        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    # plt.axis('equal')
    # plt.axis('off')
    # elif new_old==None:
    #     continue


    
    # try:
    #     print 'Boundary node %i = %f' %(nod4,y[nod4])
    # except:
    #     print 'not'

    # plt.plot(range(len(nod5)),nod5)
    final_d={}
    for vkkk,kvvv in nodds.items():
        # if vkkk == source[0]:
        #     continue
        final_d[vkkk]=kvvv[-1]
        y_pos=kvvv[-1]
        if new_old!= None:
            # continue
            plt.plot(range(len(kvvv)),kvvv)
            plt.text(iterations+(iterations/100.), y_pos, vkkk, fontsize=10)
    if insrplot:
        axins=zoomed_inset_axes(ax4,12,loc=4)
        for ivv,vkkk in enumerate(nodds):
            kvvv=nodds[vkkk]
            # if vkkk == source[0]:
            #     continue
            
            # final_d[vkkk]=kvvv[-1]
            # if ivv < 15:

            axins.plot(range(len(kvvv)),kvvv)
        # axins.plot()
        x1, x2, y1, y2 = 0.0,40.0, 0., 0.2531
        axins.set_xlim(x1, x2)
        axins.set_ylim(y1, y2)
        plt.xticks(np.arange(x1,x2,2))
        plt.yticks(np.arange(y1,y2,.01))
        mark_inset(ax4, axins, loc1=2, loc2=4, fc="none", ec="0.5")

    # plt.axis('equal')
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    if new_old !=None:
        sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(iterations) #,col[0]) #\n (consensual attribute = %s)
        # plt.subplot(4,1,2).set_title(sstt)
        ax2=plt.subplot2grid((7,2),(0,1),colspan=1,rowspan=2)
        # plt.subplot(3,2,1).set_title(sstt)
        ax2.set_title(sstt)

        plt.axis('equal')
        plt.axis('off')

        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)
    if new_old!= None:

        print 'Final ', final_d
        print 'Until the 40'
    # degge=c
    no_zeros={}
    for ikk,vkk in snodds.items():
        # print ikk,vkk
        for kkkk,kkvv in enumerate(vkk):
            # print kkkk

            if isinstance(kkvv,float):
                no_zeros[ikk]=(kkkk,kkvv)
                if new_old!= None:
                    print 'Node %i left 0 at %i iterations becoming %.4f and deg^-1 %.4f' %(ikk, kkkk, kkvv,1./closs[ikk])
                break

    if new_old !=None:
        plt.show()
    return F,nodds,source,y_orig,final_d,no_zeros



def influence_sim_dh_t(nodes,p,sa,iterations,G=None,scale=1000,new_old=False,source = [0],source_u=[1],su=0.9,h=0.3,funcion='',insrplot=False,yes_plot=True):
    if G==None:
        while  True:
            # print 'creating erdos_renyi_graph'
            # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
            G=nx.erdos_renyi_graph(nodes,p)
            if nx.is_connected(G) :
                # if 4 not in nx.isolates(G):
                break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)
    # closs=nx.closeness_centrality(G)
    closs=nx.degree(G)
    closse=[v for v in sorted(closs,key=closs.get,reverse=True)]
    # print 
    # print closse[-1],nx.neighbors(G,closse[-1])

    # print closse,closs
    # print aaa
    ssas_d={}
    if len(source)==0:
        source = [closse[-1]]
        source_u=[su]
        ssas_d[closse[-1]]=0
    else:
        for nd  in source:
            ssas_d[nd]=0
    for nd in set(G.nodes())-set(source):
        ssas_d[nd]=sa
    checklist={sou:(True,0) for sou in source }
    # print checklist

    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    if new_old:
        F=utilat.create_random_scalar_attributes_dh(G,scale,source=source,source_u=source_u)
    else:
        F,asoc=utilat.create_random_scalar_attributes(G,scale)

    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    initial_val={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    if yes_plot:
        fig = plt.figure(figsize=(17,17))
    # else:

        if new_old!=None and not new_old:


            sstt="Initial distribution of opinions over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
            # ax1=plt.subplot2grid((3,2),(0,0),colspan=1)
            plt.subplot(3,2,1).set_title(sstt)
            # ax1.set_title(sstt)
            # plt.set_cmap('cool')
            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
            plt.axis('equal')
            plt.axis('off')
            
            # plt.figure(2)
            sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
            plt.subplot(3,2,5).set_title(sstt)
            # ax2=plt.subplot2grid((3,2),(2,0),colspan=2)
            # # plt.subplot(3,2,1).set_title(sstt)
            # ax2.set_title(sstt)
        elif new_old and new_old!=None:
            sstt="Initial distribution of scalar attributes over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
            # plt.subplot(411).set_title(sstt)
            ax1=plt.subplot2grid((7,2),(0,0),colspan=1,rowspan=2)
            ax1.set_title(sstt)
            # plt.set_cmap('cool')
            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)
            plt.axis('equal')
            plt.axis('off')
            sstt = "Time variation of opinions over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
            # plt.subplot(413).set_title(sstt)
            ax3=plt.subplot2grid((7,2),(2,0),colspan=2)
            # plt.subplot(3,2,1).set_title(sstt)
            ax3.set_title(sstt)

    iterat=[]
    assort=[]
    # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    # nod5=[]
    nodds={}
    snodds={}
    # ssas_d={i:},
    # print source,source_u,ssas_d,
    # nod4=random.choice(G.nodes())
    # print nod4,F.node[nod4]['scalar_attribute']
    # print F.edges()

    y={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    for kkk,vvv in y.items():
        if kkk not in nodds:
            nodds[kkk]=[vvv]
            snodds[kkk]=[vvv]
        else:
            nodds[kkk].append(vvv)
            if ii <40:
                snodds[kkk].append(vvv)
    # nod5.append(y[5])
    checkin=True
    # nd=F.nodes()[0]
    
    # for nd in source:
    #     ssa=ssas_d[nd]
    #     uu=0
    #     nei=nx.neighbors(F,nd)
    #     for nnei in nei:
    #         if nnei in checklist:
    #             if checklist[nnei][0] and checklist[nnei][1]<ii:
    #                 uu+=y[nnei]
    #     Xnei=uu/len(nei)
    #     X=y[nd]
    #     if new_old:
    #         uX=0
    #     else:
    #         uX=(ssa*Xnei)+(1-ssa)*X
    #     insau=int(uX*scale)
    #     # checklist[nnd]=(True,0)
    #     F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
    #     for nnd in nx.neighbors(F,nd):
    # # sources=set(source)
    # # for nnd in set(F.nodes())-sources:
    #         uu=0
    #         nei=nx.neighbors(F,nnd)
    #         # print nei
    #         for nnei in nei:
    #             if nnei in checklist:
    #                 if checklist[nnei][0] :#and checklist[nnei][1]<ii:
    #                     uu+=y[nnei]
    #         if uu!=0 and nnd not in checklist:
    #             checklist[nnd]=(True,0)
    #         X=y[nnd]
    #         if uu!=0:
    #             Xnei=uu/len(nei)
    #             if new_old:
    #                 ssa=ssas_d[nnd]
    #                 uX=eval(funcion)
    #             else:
    #                 uX=(ssa*Xnei)+(1-ssa)*X
    #             insau=int(uX*scale)
    #         else:
    #             uX=y[nnd]
    #             insau=F.node[nnd]['scalar_attribute_numeric']
    #         F.add_node(nnd,scalar_attribute=uX,scalar_attribute_numeric=insau)
    # y={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    # print y


    # for i,nd in enumerate(source):
    #     attr_dic=G.node[nd]
    #     rand=0.
    #     irand=int(rand*scale)
    #     F.add_node(nd,attr_dict=attr_dic,scalar_attribute=rand,scalar_attribute_numeric=irand)
    #     for nnd in nx.neighbors(F,nd):
    #         attr_dic=F.node[nnd]
    #         rand=cal
    #         irand=int(rand*scale)
    #         F.add_node(nd,attr_dict=attr_dic,scalar_attribute=rand,scalar_attribute_numeric=irand)
    # for nd in set(G.nodes())-set(source):

    #     attr_dic=G.node[nd]
    #     rand=0
    #     # rand=random.uniform(-1,1)
    #     # rand=random.random()
    #     irand=int(rand*scale)
    #     F.add_node(nd,attr_dict=attr_dic,scalar_attribute=rand,scalar_attribute_numeric=irand)
    for ii in range(1,iterations):
        # print ii,ssas_d
        # sa=0.05
        y={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
        for kkk,vvv in y.items():
            if kkk not in nodds:
                nodds[kkk]=[vvv]
                snodds[kkk]=[vvv]
            else:
                nodds[kkk].append(vvv)
                if ii <40:
                    snodds[kkk].append(vvv)
        # nod5.append(y[5])
        # print ii, nodds
        # raw_input()
        checkin=True
        # nd=F.nodes()[0]
        
        for nd in source:
            ssa=ssas_d[nd]
            # print nd,'heeey'
            # if nd==nod4:
            #     ssa=0
            # else:
            #     ssa=sa

            # print nd
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            
            for nnei in nei:
                if nnei in checklist:
                    if checklist[nnei][0] and checklist[nnei][1]<ii:
                        uu+=y[nnei]
            Xnei=uu/len(nei)
            # X=F.node[nd]['scalar_attribute']
            X=y[nd]
            if new_old:
                # ssa=0
                # if ii == 0:
                #     uX=(ssa*(Xnei-X))
                # else:
                    # uX=X+h/(ssa*Xnei)
                # if nd !=4:
                # uX=X+(h*ssa*Xnei)
                # elif nd== nod4:
                #     uX=X
                # else:
                uX=eval(funcion)
                # uX=0
                # uX= X+h*(X-Xnei)
            # uX=(ssa*Xnei)+(2-ssa)*X
            else:
                uX=(ssa*Xnei)+(1-ssa)*X
            insau=int(uX*scale)
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        sources=set(source)
        # print source,F.nodes()
        # print aaa
        for nd in set(F.nodes())-sources:
            # sa=1-(1./nx.degree(F,nd))
            # if nd==nod4:
            #     ssa=0
            # else:
            #     ssa=sa
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            for nnei in nei:
                # print nd,nnei,checklist,nei,ii
                if nnei in checklist:
                    # print 'a',checklist[nnei][0] ,checklist[nnei][1]<ii,checklist[nnei][0] and checklist[nnei][1]<ii,ii,y[nnei]
                    if checklist[nnei][0] and checklist[nnei][1]<ii:
                        uu+=y[nnei]
                # print uu
                    # checklist[]
            # if nd not in checklist:
            #     print nd,uu,nei
            if uu!=0 and nd not in checklist:
                checklist[nd]=(True,ii)
            X=y[nd]
            # X=F.node[nd]['scalar_attribute']
            # if uu!=0:
            Xnei=uu/len(nei)
            if new_old:
                # ssa=sa
                ssa=ssas_d[nd]
                # if ii == 0:
                #     uX=(ssa*(Xnei-X))
                # else:
                    # uX=X+h/(ssa*Xnei)
                # uX=X+(h*ssa*Xnei)
                # uX= X+h*(X-Xnei)
                # elif nd== nod4:
                #     uX=X
                # else:
                uX=eval(funcion)
                    # uX=eval(funcion)
                    
                    # uX=(ssa*Xnei)+(2-ssa)*X
            else:
                uX=(ssa*Xnei)+(1-ssa)*X
            insau=int(uX*scale)
            # else:
            #     uX=y[nd]
            #     insau=F.node[nd]['scalar_attribute_numeric']
            # print '0000000000000000000000',ii,'0000000000000000000'
            # print X,uX
            # print nd
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        if ii ==ckck and ii<10:
            # print ii
            if new_old:
                ckck+=5
                kckc+=1
                # plt.subplot(211)
                # print ckck
                # print kckc
            else:
            # col=['%.5f' %yy for yy in y]
                col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
                sstt="Distribution of opinions over graph nodes at %i iterations" %(ii+1)

                plt.subplot(3,2,kckc).set_title(sstt)
                nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
                plt.axis('equal')
                plt.axis('off')
                ckck+=5
                kckc+=1
                plt.subplot(3,2,5)
        if yes_plot:
            yplot=[y[i] for i in F.nodes()]
            plt.plot(F.nodes(),yplot)
        # print yplot
        # print checklist
    if yes_plot:
        if not new_old:
            asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
            if np.isnan(asss):
                asss=1.
            # print 'Iteration %i ==> %f' %(ii,asss),y 
            # print type(asss), asss<-1,asss>1
            iterat.append(ii)

            assort.append(asss)
            plt.plot(F.nodes(),yplot,linewidth=3.)
            sstt= "Time variation of scalar attribute assortativity coefficient"

            plt.subplot(3,2,6).set_title(sstt)

            # plt.figure(3)

            plt.plot(iterat,assort)
            plt.ylim(-1.1,1.1)
            col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
            sstt="Distribution of opinions over graph nodes at %i iterations" %(iterations,col[0]) #\n (consensual attribute = %s)
            plt.subplot(3,2,4).set_title(sstt)  #   

            # ,figsize=(15,15)

            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
        # plt.axis('equal')
        # plt.axis('off')

        sstt = "Time variation of opinions of each graph node" #%F.nodes()[0]#,starting_value_of_zero_node)
        # plt.subplot(414).set_title(sstt)
        ax4=plt.subplot2grid((7,2),(3,0),colspan=2,rowspan=3)
            # plt.subplot(3,2,1).set_title(sstt)
        ax4.set_title(sstt)


    
    # try:
    #     print 'Boundary node %i = %f' %(nod4,y[nod4])
    # except:
    #     print 'not'

    # plt.plot(range(len(nod5)),nod5)
        final_d={}
        for vkkk,kvvv in nodds.items():
            # if vkkk == source[0]:
            #     continue
            final_d[vkkk]=kvvv[-1]
            plt.plot(range(len(kvvv)),kvvv)
        if insrplot:
            axins=zoomed_inset_axes(ax4,12,loc=4)
            for ivv,vkkk in enumerate(nodds):
                kvvv=nodds[vkkk]
                # if vkkk == source[0]:
                #     continue
                
                # final_d[vkkk]=kvvv[-1]
                # if ivv < 15:

                axins.plot(range(len(kvvv)),kvvv)
            # axins.plot()
            x1, x2, y1, y2 = 0.0,40.0, 0., 0.2531
            axins.set_xlim(x1, x2)
            axins.set_ylim(y1, y2)
            plt.xticks(np.arange(x1,x2,2))
            plt.yticks(np.arange(y1,y2,.01))
            mark_inset(ax4, axins, loc1=2, loc2=4, fc="none", ec="0.5")

        # plt.axis('equal')
        col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(iterations) #,col[0]) #\n (consensual attribute = %s)
        # plt.subplot(4,1,2).set_title(sstt)
        ax2=plt.subplot2grid((7,2),(0,1),colspan=1,rowspan=2)
        # plt.subplot(3,2,1).set_title(sstt)
        ax2.set_title(sstt)

        plt.axis('equal')
        plt.axis('off')

        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)
        print 'Final ', final_d
        print 'Until the 40'
        # degge=c
        if new_old !=None:
            for ikk,vkk in snodds.items():
                # print ikk,vkk
                for kkkk,kkvv in enumerate(vkk):
                    

                    if isinstance(kkvv,float):
                        print 'Node %i left 0 at %i iterations becoming %.4f and deg^-1 %.4f' %(ikk, kkkk, kkvv,1./closs[ikk])
                        break

    plt.show()
    return F,nodds,source

def influence_sim_dh(nodes,p,sa,iterations,G=None,scale=1000,new_old=False,source = [0],source_u=[1],su=0.9,h=0.3,funcion='',insrplot=False,yes_plot=True):
    if G==None:
        while  True:
            # print 'creating erdos_renyi_graph'
            # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
            G=nx.erdos_renyi_graph(nodes,p)
            if nx.is_connected(G) :
                # if 4 not in nx.isolates(G):
                break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)
    # closs=nx.closeness_centrality(G)
    closs=nx.degree(G)
    closse=[v for v in sorted(closs,key=closs.get,reverse=True)]
    # print 
    # print closse[-1],nx.neighbors(G,closse[-1])

    # print closse,closs
    # print aaa
    ssas_d={}
    if len(source)==0:
        source = [closse[-1]]
        source_u=[su]
        ssas_d[closse[-1]]=0
    else:
        for nd  in source:
            ssas_d[nd]=0
    for nd in set(G.nodes())-set(source):
        ssas_d[nd]=sa
    checklist={sou:(True,0) for sou in source }
    # print checklist

    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    if new_old:
        F=utilat.create_random_scalar_attributes_dh(G,scale,source=source,source_u=source_u)
    else:
        F,asoc=utilat.create_random_scalar_attributes(G,scale)

    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    initial_val={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    if yes_plot:
        fig = plt.figure(figsize=(17,17))
    # else:

        if not new_old:


            sstt="Initial distribution of opinions over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
            # ax1=plt.subplot2grid((3,2),(0,0),colspan=1)
            plt.subplot(3,2,1).set_title(sstt)
            # ax1.set_title(sstt)
            # plt.set_cmap('cool')
            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
            plt.axis('equal')
            plt.axis('off')
            
            # plt.figure(2)
            sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
            plt.subplot(3,2,5).set_title(sstt)
            # ax2=plt.subplot2grid((3,2),(2,0),colspan=2)
            # # plt.subplot(3,2,1).set_title(sstt)
            # ax2.set_title(sstt)
        else:
            sstt="Initial distribution of scalar attributes over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
            # plt.subplot(411).set_title(sstt)
            ax1=plt.subplot2grid((7,2),(0,0),colspan=1,rowspan=2)
            ax1.set_title(sstt)
            # plt.set_cmap('cool')
            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)
            plt.axis('equal')
            plt.axis('off')
            sstt = "Time variation of opinions over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
            # plt.subplot(413).set_title(sstt)
            ax3=plt.subplot2grid((7,2),(2,0),colspan=2)
            # plt.subplot(3,2,1).set_title(sstt)
            ax3.set_title(sstt)

    iterat=[]
    assort=[]
    # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    # nod5=[]
    nodds={}
    snodds={}
    # ssas_d={i:},
    # print source,source_u,ssas_d,
    # nod4=random.choice(G.nodes())
    # print nod4,F.node[nod4]['scalar_attribute']
    # print F.edges()

    y={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    for kkk,vvv in y.items():
        if kkk not in nodds:
            nodds[kkk]=[vvv]
            snodds[kkk]=[vvv]
        else:
            nodds[kkk].append(vvv)
            if ii <40:
                snodds[kkk].append(vvv)
    # nod5.append(y[5])
    checkin=True
    # nd=F.nodes()[0]
    
    for nd in source:
        ssa=ssas_d[nd]
        uu=0
        nei=nx.neighbors(F,nd)
        for nnei in nei:
            if nnei in checklist:
                if checklist[nnei][0] and checklist[nnei][1]<ii:
                    uu+=y[nnei]
        Xnei=uu/len(nei)
        X=y[nd]
        if new_old:
            uX=0
        else:
            uX=(ssa*Xnei)+(1-ssa)*X
        insau=int(uX*scale)
        # checklist[nnd]=(True,0)
        F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        for nnd in nx.neighbors(F,nd):
    # sources=set(source)
    # for nnd in set(F.nodes())-sources:
            uu=0
            nei=nx.neighbors(F,nnd)
            # print nei
            for nnei in nei:
                if nnei in checklist:
                    if checklist[nnei][0] :#and checklist[nnei][1]<ii:
                        uu+=y[nnei]
            if uu!=0 and nnd not in checklist:
                checklist[nnd]=(True,0)
            X=y[nnd]
            if uu!=0:
                Xnei=uu/len(nei)
                if new_old:
                    ssa=ssas_d[nnd]
                    uX=eval(funcion)
                else:
                    uX=(ssa*Xnei)+(1-ssa)*X
                insau=int(uX*scale)
            else:
                uX=y[nnd]
                insau=F.node[nnd]['scalar_attribute_numeric']
            F.add_node(nnd,scalar_attribute=uX,scalar_attribute_numeric=insau)
    # y={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
    # print y


    # for i,nd in enumerate(source):
    #     attr_dic=G.node[nd]
    #     rand=0.
    #     irand=int(rand*scale)
    #     F.add_node(nd,attr_dict=attr_dic,scalar_attribute=rand,scalar_attribute_numeric=irand)
    #     for nnd in nx.neighbors(F,nd):
    #         attr_dic=F.node[nnd]
    #         rand=cal
    #         irand=int(rand*scale)
    #         F.add_node(nd,attr_dict=attr_dic,scalar_attribute=rand,scalar_attribute_numeric=irand)
    # for nd in set(G.nodes())-set(source):

    #     attr_dic=G.node[nd]
    #     rand=0
    #     # rand=random.uniform(-1,1)
    #     # rand=random.random()
    #     irand=int(rand*scale)
    #     F.add_node(nd,attr_dict=attr_dic,scalar_attribute=rand,scalar_attribute_numeric=irand)
    for ii in range(1,iterations):
        # print ii,ssas_d
        # sa=0.05
        y={i:F.node[i]['scalar_attribute'] for i in F.nodes()}
        for kkk,vvv in y.items():
            if kkk not in nodds:
                nodds[kkk]=[vvv]
                snodds[kkk]=[vvv]
            else:
                nodds[kkk].append(vvv)
                if ii <40:
                    snodds[kkk].append(vvv)
        # nod5.append(y[5])
        # print ii, nodds
        # raw_input()
        checkin=True
        # nd=F.nodes()[0]
        
        for nd in source:
            ssa=ssas_d[nd]
            # print nd,'heeey'
            # if nd==nod4:
            #     ssa=0
            # else:
            #     ssa=sa

            # print nd
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            
            for nnei in nei:
                if nnei in checklist:
                    if checklist[nnei][0] and checklist[nnei][1]<ii:
                        uu+=y[nnei]
            Xnei=uu/len(nei)
            # X=F.node[nd]['scalar_attribute']
            X=y[nd]
            if new_old:
                # ssa=0
                # if ii == 0:
                #     uX=(ssa*(Xnei-X))
                # else:
                    # uX=X+h/(ssa*Xnei)
                # if nd !=4:
                # uX=X+(h*ssa*Xnei)
                # elif nd== nod4:
                #     uX=X
                # else:
                # uX=eval(funcion)
                uX=0
                # uX= X+h*(X-Xnei)
            # uX=(ssa*Xnei)+(2-ssa)*X
            else:
                uX=(ssa*Xnei)+(1-ssa)*X
            insau=int(uX*scale)
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        sources=set(source)
        # print source,F.nodes()
        # print aaa
        for nd in set(F.nodes())-sources:
            # sa=1-(1./nx.degree(F,nd))
            # if nd==nod4:
            #     ssa=0
            # else:
            #     ssa=sa
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            for nnei in nei:
                # print nd,nnei,checklist,nei,ii
                if nnei in checklist:
                    # print 'a',checklist[nnei][0] ,checklist[nnei][1]<ii,checklist[nnei][0] and checklist[nnei][1]<ii,ii,y[nnei]
                    if checklist[nnei][0] and checklist[nnei][1]<ii:
                        uu+=y[nnei]
                # print uu
                    # checklist[]
            # if nd not in checklist:
            #     print nd,uu,nei
            if uu!=0 and nd not in checklist:
                checklist[nd]=(True,ii)
            X=y[nd]
            # X=F.node[nd]['scalar_attribute']
            # if uu!=0:
            Xnei=uu/len(nei)
            if new_old:
                # ssa=sa
                ssa=ssas_d[nd]
                # if ii == 0:
                #     uX=(ssa*(Xnei-X))
                # else:
                    # uX=X+h/(ssa*Xnei)
                # uX=X+(h*ssa*Xnei)
                # uX= X+h*(X-Xnei)
                # elif nd== nod4:
                #     uX=X
                # else:
                uX=eval(funcion)
                    # uX=eval(funcion)
                    
                    # uX=(ssa*Xnei)+(2-ssa)*X
            else:
                uX=(ssa*Xnei)+(1-ssa)*X
            insau=int(uX*scale)
            # else:
            #     uX=y[nd]
            #     insau=F.node[nd]['scalar_attribute_numeric']
            # print '0000000000000000000000',ii,'0000000000000000000'
            # print X,uX
            # print nd
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)
        if ii ==ckck and ii<10:
            # print ii
            if new_old:
                ckck+=5
                kckc+=1
                # plt.subplot(211)
                # print ckck
                # print kckc
            else:
            # col=['%.5f' %yy for yy in y]
                col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
                sstt="Distribution of opinions over graph nodes at %i iterations" %(ii+1)

                plt.subplot(3,2,kckc).set_title(sstt)
                nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
                plt.axis('equal')
                plt.axis('off')
                ckck+=5
                kckc+=1
                plt.subplot(3,2,5)
        if yes_plot:
            yplot=[y[i] for i in F.nodes()]
            plt.plot(F.nodes(),yplot)
        # print yplot
        # print checklist
    if yes_plot:
        if not new_old:
            asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
            if np.isnan(asss):
                asss=1.
            # print 'Iteration %i ==> %f' %(ii,asss),y 
            # print type(asss), asss<-1,asss>1
            iterat.append(ii)

            assort.append(asss)
            plt.plot(F.nodes(),yplot,linewidth=3.)
            sstt= "Time variation of scalar attribute assortativity coefficient"

            plt.subplot(3,2,6).set_title(sstt)

            # plt.figure(3)

            plt.plot(iterat,assort)
            plt.ylim(-1.1,1.1)
            col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
            sstt="Distribution of opinions over graph nodes at %i iterations" %(iterations,col[0]) #\n (consensual attribute = %s)
            plt.subplot(3,2,4).set_title(sstt)  #   

            # ,figsize=(15,15)

            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
        # plt.axis('equal')
        # plt.axis('off')

        sstt = "Time variation of opinions of each graph node" #%F.nodes()[0]#,starting_value_of_zero_node)
        # plt.subplot(414).set_title(sstt)
        ax4=plt.subplot2grid((7,2),(3,0),colspan=2,rowspan=3)
            # plt.subplot(3,2,1).set_title(sstt)
        ax4.set_title(sstt)


    
    # try:
    #     print 'Boundary node %i = %f' %(nod4,y[nod4])
    # except:
    #     print 'not'

    # plt.plot(range(len(nod5)),nod5)
        final_d={}
        for vkkk,kvvv in nodds.items():
            # if vkkk == source[0]:
            #     continue
            final_d[vkkk]=kvvv[-1]
            plt.plot(range(len(kvvv)),kvvv)
        if insrplot:
            axins=zoomed_inset_axes(ax4,12,loc=4)
            for ivv,vkkk in enumerate(nodds):
                kvvv=nodds[vkkk]
                # if vkkk == source[0]:
                #     continue
                
                # final_d[vkkk]=kvvv[-1]
                # if ivv < 15:

                axins.plot(range(len(kvvv)),kvvv)
            # axins.plot()
            x1, x2, y1, y2 = 0.0,40.0, 0., 0.2531
            axins.set_xlim(x1, x2)
            axins.set_ylim(y1, y2)
            plt.xticks(np.arange(x1,x2,2))
            plt.yticks(np.arange(y1,y2,.01))
            mark_inset(ax4, axins, loc1=2, loc2=4, fc="none", ec="0.5")

        # plt.axis('equal')
        col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(iterations) #,col[0]) #\n (consensual attribute = %s)
        # plt.subplot(4,1,2).set_title(sstt)
        ax2=plt.subplot2grid((7,2),(0,1),colspan=1,rowspan=2)
        # plt.subplot(3,2,1).set_title(sstt)
        ax2.set_title(sstt)

        plt.axis('equal')
        plt.axis('off')

        nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.,alpha=.1)
        print 'Final ', final_d
        print 'Until the 40'
        # degge=c
        for ikk,vkk in snodds.items():
            # print ikk,vkk
            for kkkk,kkvv in enumerate(vkk):
                

                if isinstance(kkvv,float):
                    print 'Node %i left 0 at %i iterations becoming %.4f and deg^-1 %.4f' %(ikk, kkkk, kkvv,1./closs[ikk])
                    break

    plt.show()
    return F,nodds,source,ssas_d



def influence_sim_dh_old(nodes,p,sa,iterations,scale=1000,h=0.3):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)

    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    F,asoc=utilat.create_random_scalar_attributes_dh(G,scale)
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]

    fig = plt.figure(figsize=(17,17)) #figsize=(17,17)


    sstt="Initial distribution of scalar attributes over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
    plt.subplot(3,2,1).set_title(sstt)
    # plt.set_cmap('cool')
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')
    
    # plt.figure(2)
    sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
    plt.subplot(3,2,5).set_title(sstt)

    # for i in F.nodes(data=True):
        # print i
    # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
    iterat=[]
    assort=[]
    y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    for ii in range(iterations):
        # sa=0.05
        checkin=True
        nd=F.nodes()[0]
        # print nd
        uu=0
        nei=nx.neighbors(F,nd)
        # print nei
        for nnei in nei:
            uu+=F.node[nnei]['scalar_attribute']
        Xnei=uu/len(nei)
        X=F.node[nd]['scalar_attribute']
        # uX=(sa*Xnei)+(1 + (1-sa))*X
        uX=X+(h*sa*Xnei)
        insau=int(uX*scale)
        F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)

        for nd in F.nodes()[1:]:
            # sa=1-(1./nx.degree(F,nd))
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            for nnei in nei:
                uu+=F.node[nnei]['scalar_attribute']
            X=F.node[nd]['scalar_attribute']
            Xnei=uu/len(nei)
            # uX=(sa*Xnei)+(1-sa)*X
            uX=X+(h*sa*Xnei)
            insau=int(uX*scale)
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)

            
        # for i in F.nodes(data=True):
        #   print i
        # Checking for attributes equality
        y1=y
        y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        if ii ==ckck and ii<10:
            # col=['%.5f' %yy for yy in y]
            col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
            sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(ii+1)

            plt.subplot(3,2,kckc).set_title(sstt)
            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
            plt.axis('equal')
            plt.axis('off')
            ckck+=5
            kckc+=1
            plt.subplot(3,2,5)
        # for yy in it.combinations(y,2):
        #   checkin=checkin and yy[0] -yy[1] <(1./scale)
        # for yy in range(len(y1)):
        #   # print y[yy]-y1[yy]<(1./scale)
        #   checkin=checkin and y[yy]-y1[yy]<(0.1/(scale))
        #   # print checkin
        # if checkin:
        #   break
        
        # asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # if np.isnan(asss):
        #     asss=1.
        # # print 'Iteration %i ==> %f' %(ii,asss),y 
        # # print type(asss), asss<-1,asss>1
        # iterat.append(ii)

        # assort.append(asss)

        # # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        # plt.plot(F.nodes(),y)
        # # if asss==1. :
        # #   break
    
    plt.plot(F.nodes(),y,linewidth=3.)
    sstt= "Time variation of scalar attribute assortativity coefficient"

    plt.subplot(3,2,6).set_title(sstt)

    # plt.figure(3)

    plt.plot(iterat,assort)
    plt.ylim(-1.1,1.1)
    # plt.figure(3)
    # plt.plot(F.nodes(),y)
    # col=['%.5f' %yy for yy in y]
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    sstt="Distribution of scalar attributes over graph nodes at %i iterations\n (consensual attribute = %s)" %(iterations,col[0])
    plt.subplot(3,2,4).set_title(sstt)

    # plt.figure(4)

    
    # print col
    # print [F.node[i]['scalar_attribute_numeric'] for i in F.nodes()]
    # pos=nx.spring_layout(G)
    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')

    plt.show()










def influence_sim_d(nodes,p,sa,iterations,scale=1000):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)

    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    F,asoc=utilat.create_random_scalar_attributes(G,scale)
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]

    fig = plt.figure(figsize=(17,17))


    sstt="Initial distribution of scalar attributes over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
    plt.subplot(3,2,1).set_title(sstt)
    # plt.set_cmap('cool')
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')
    
    # plt.figure(2)
    sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
    plt.subplot(3,2,5).set_title(sstt)

    # for i in F.nodes(data=True):
        # print i
    # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
    iterat=[]
    assort=[]
    y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    for ii in range(iterations):
        # sa=0.05
        checkin=True
        nd=F.nodes()[0]
        # print nd
        uu=0
        nei=nx.neighbors(F,nd)
        # print nei
        for nnei in nei:
            uu+=F.node[nnei]['scalar_attribute']
        Xnei=uu/len(nei)
        X=F.node[nd]['scalar_attribute']
        # uX=(sa*Xnei)+(1 + (1-sa))*X
        uX=(sa*Xnei)-(sa*X)
        insau=int(uX*scale)
        F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)

        for nd in F.nodes()[1:]:
            # sa=1-(1./nx.degree(F,nd))
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            for nnei in nei:
                uu+=F.node[nnei]['scalar_attribute']
            X=F.node[nd]['scalar_attribute']
            Xnei=uu/len(nei)
            # uX=(sa*Xnei)+(1-sa)*X
            uX=(sa*Xnei)-(sa*X)
            insau=int(uX*scale)
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)

            
        # for i in F.nodes(data=True):
        #   print i
        # Checking for attributes equality
        y1=y
        y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        if ii ==ckck and ii<10:
            # col=['%.5f' %yy for yy in y]
            col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
            sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(ii+1)

            plt.subplot(3,2,kckc).set_title(sstt)
            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
            plt.axis('equal')
            plt.axis('off')
            ckck+=5
            kckc+=1
            plt.subplot(3,2,5)
        # for yy in it.combinations(y,2):
        #   checkin=checkin and yy[0] -yy[1] <(1./scale)
        # for yy in range(len(y1)):
        #   # print y[yy]-y1[yy]<(1./scale)
        #   checkin=checkin and y[yy]-y1[yy]<(0.1/(scale))
        #   # print checkin
        # if checkin:
        #   break
        
        # asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # if np.isnan(asss):
        #     asss=1.
        # # print 'Iteration %i ==> %f' %(ii,asss),y 
        # # print type(asss), asss<-1,asss>1
        # iterat.append(ii)

        # assort.append(asss)

        # # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        # plt.plot(F.nodes(),y)
        # # if asss==1. :
        # #   break
    
    plt.plot(F.nodes(),y,linewidth=3.)
    sstt= "Time variation of scalar attribute assortativity coefficient"

    plt.subplot(3,2,6).set_title(sstt)

    # plt.figure(3)

    plt.plot(iterat,assort)
    plt.ylim(-1.1,1.1)
    # plt.figure(3)
    # plt.plot(F.nodes(),y)
    # col=['%.5f' %yy for yy in y]
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    sstt="Distribution of scalar attributes over graph nodes at %i iterations\n (consensual attribute = %s)" %(iterations,col[0])
    plt.subplot(3,2,4).set_title(sstt)

    # plt.figure(4)

    
    # print col
    # print [F.node[i]['scalar_attribute_numeric'] for i in F.nodes()]
    # pos=nx.spring_layout(G)
    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')

    plt.show()






def infdif_sim(nodes,p,sa,sb,iterations,scale=1000):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)

    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    F,asoc=utilat.create_random_scalar_attributes(G,scale)
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]

    fig = plt.figure(figsize=(17,17))

    starting_value_of_zero_node=F.node[0]['scalar_attribute']
    sstt="Initial distribution of scalar attributes over graph nodes\n (diffusion source at node %s with initial attribute = %f)" %(F.nodes()[0],starting_value_of_zero_node)
    plt.subplot(3,2,1).set_title(sstt)
    # plt.set_cmap('cool')
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')
    
    # plt.figure(2)
    sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
    plt.subplot(3,2,5).set_title(sstt)

    # for i in F.nodes(data=True):
        # print i
    # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
    iterat=[]
    assort=[]
    y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    for ii in range(iterations):
        # sa=0.05
        checkin=True
        nd=F.nodes()[0]
        # print nd
        uu=0
        nei=nx.neighbors(F,nd)
        # print nei
        for nnei in nei:
            uu+=F.node[nnei]['scalar_attribute']
        Xnei=uu/len(nei)
        X=F.node[nd]['scalar_attribute']
        uX=(sa*Xnei)+(1-sa)*X
        insau=int(uX*scale)
        F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)

        for nd in F.nodes()[1:]:
            # sa=1-(1./nx.degree(F,nd))
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            for nnei in nei:
                uu+=F.node[nnei]['scalar_attribute']
            Xnei=uu/len(nei)
            X=F.node[nd]['scalar_attribute']
            uX=(sb*Xnei)+(1-sb)*X
            insau=int(uX*scale)
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)

        # for i in F.nodes(data=True):
        #   print i
        # Checking for attributes equality
        y1=y
        y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        if ii ==ckck and ii<10:
            # col=['%.5f' %yy for yy in y]
            col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
            sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(ii+1)

            plt.subplot(3,2,kckc).set_title(sstt)
            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
            plt.axis('equal')
            plt.axis('off')
            ckck+=5
            kckc+=1
            plt.subplot(3,2,5)
        # for yy in it.combinations(y,2):
        #   checkin=checkin and yy[0] -yy[1] <(1./scale)
        # for yy in range(len(y1)):
        #   # print y[yy]-y1[yy]<(1./scale)
        #   checkin=checkin and y[yy]-y1[yy]<(0.1/(scale))
        #   # print checkin
        # if checkin:
        #   break
        asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        if np.isnan(asss):
            asss=1.
        # print 'Iteration %i ==> %f' %(ii,asss),y 
        # print type(asss), asss<-1,asss>1
        iterat.append(ii)

        assort.append(asss)

        # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        plt.plot(F.nodes(),y)
        # if asss==1. :
        #   break
    plt.plot(F.nodes(),y,linewidth=3.)
    sstt= "Time variation of scalar attribute assortativity coefficient"

    plt.subplot(3,2,6).set_title(sstt)

    # plt.figure(3)

    plt.plot(iterat,assort)
    plt.ylim(-1.1,1.1)
    # plt.figure(3)
    # plt.plot(F.nodes(),y)
    # col=['%.5f' %yy for yy in y]
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    sstt="Distribution of scalar attributes over graph nodes at %i iterations\n (consensual attribute = %s)" %(iterations,col[0])
    plt.subplot(3,2,4).set_title(sstt)

    # plt.figure(4)

    
    # print col
    # print [F.node[i]['scalar_attribute_numeric'] for i in F.nodes()]
    # pos=nx.spring_layout(G)
    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')

    plt.show()



def polinf_sim(nodes,p,iterations,scale=1000):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)

    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    F,asoc=utilat.create_random_scalar_attributes(G,scale)
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]

    fig = plt.figure(figsize=(17,17))

    starting_value_of_zero_node=F.node[0]['scalar_attribute']
    sstt="Initial distribution of scalar attributes over graph nodes"#\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
    plt.subplot(3,2,1).set_title(sstt)
    # plt.set_cmap('cool')
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')
    
    # plt.figure(2)
    sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
    plt.subplot(3,2,5).set_title(sstt)

    # for i in F.nodes(data=True):
        # print i
    # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
    iterat=[]
    assort=[]
    y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    for ii in range(iterations):
        # sa=0.05
        checkin=True
        # nd=F.nodes()[0]
        # # print nd
        # uu=0
        # nei=nx.neighbors(F,nd)
        # # print nei
        # for nnei in nei:
        #     uu+=F.node[nnei]['scalar_attribute']
        # if 
        # sau=(sa*uu/len(nei))+(1-sa)*F.node[nd]['scalar_attribute']
        # insau=int(sau*scale)
        # F.add_node(nd,scalar_attribute=sau,scalar_attribute_numeric=insau)

        for nd in F.nodes():
            # sa=1-(1./nx.degree(F,nd))
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            for nnei in nei:
                uu+=F.node[nnei]['scalar_attribute']
            X=F.node[nd]['scalar_attribute']
            if X<0.5 and uu<0.5:
                F.add_node(nd,scalar_attribute=min(X,uu),scalar_attribute_numeric=int(min(X,uu)*scale))
            elif X>=0.5 and uu>=0.5:
                F.add_node(nd,scalar_attribute=max(X,uu),scalar_attribute_numeric=int(max(X,uu)*scale))
            
            # sau=(sb*uu/len(nei))+(1-sb)*F.node[nd]['scalar_attribute']
            # insau=int(sau*scale)
            # F.add_node(nd,scalar_attribute=sau,scalar_attribute_numeric=insau)

        # for i in F.nodes(data=True):
        #   print i
        # Checking for attributes equality
        y1=y
        y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        if ii ==ckck and ii<10:
            # col=['%.5f' %yy for yy in y]
            col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
            sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(ii+1)

            plt.subplot(3,2,kckc).set_title(sstt)
            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
            plt.axis('equal')
            plt.axis('off')
            ckck+=5
            kckc+=1
            plt.subplot(3,2,5)
        # for yy in it.combinations(y,2):
        #   checkin=checkin and yy[0] -yy[1] <(1./scale)
        # for yy in range(len(y1)):
        #   # print y[yy]-y1[yy]<(1./scale)
        #   checkin=checkin and y[yy]-y1[yy]<(0.1/(scale))
        #   # print checkin
        # if checkin:
        #   break
        asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        if np.isnan(asss):
            asss=1.
        # print 'Iteration %i ==> %f' %(ii,asss),y 
        # print type(asss), asss<-1,asss>1
        iterat.append(ii)

        assort.append(asss)

        # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        plt.plot(F.nodes(),y)
        # if asss==1. :
        #   break
    plt.plot(F.nodes(),y,linewidth=3.)
    sstt= "Time variation of scalar attribute assortativity coefficient"

    plt.subplot(3,2,6).set_title(sstt)

    # plt.figure(3)

    plt.plot(iterat,assort)
    plt.ylim(-1.1,1.1)
    # plt.figure(3)
    # plt.plot(F.nodes(),y)
    # col=['%.5f' %yy for yy in y]
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    sstt="Distribution of scalar attributes over graph nodes at %i iterations"#\n (consensual attribute = %s)" %(iterations,col[0])
    plt.subplot(3,2,4).set_title(sstt)

    # plt.figure(4)

    
    # print col
    # print [F.node[i]['scalar_attribute_numeric'] for i in F.nodes()]
    # pos=nx.spring_layout(G)
    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')

    plt.show()




def sidif_sim(nodes,p,b,iterations,scale=1000):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)

    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    F,asoc=utilat.create_random_scalar_attributes(G,scale)
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]

    fig = plt.figure(figsize=(17,17))

    starting_value_of_zero_node=F.node[0]['scalar_attribute']
    sstt="Initial distribution of scalar attributes over graph nodes\n (diffusion source at node %s with initial attribute = %f)" %(F.nodes()[0],starting_value_of_zero_node)
    plt.subplot(3,2,1).set_title(sstt)
    # plt.set_cmap('cool')
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')
    
    # plt.figure(2)
    sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
    plt.subplot(3,2,5).set_title(sstt)

    # for i in F.nodes(data=True):
        # print i
    # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
    iterat=[]
    assort=[]
    y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    for ii in range(iterations):
        # sa=0.05
        checkin=True
        # nd=F.nodes()[0]
        # # print nd
        # uu=0
        # nei=nx.neighbors(F,nd)
        # # print nei
        # for nnei in nei:
        #     uu+=F.node[nnei]['scalar_attribute']

        # sau=F.node[nd]['scalar_attribute'] + b*(1. - F.node[nd]['scalar_attribute'])*(uu/len(nei))
        # # sau=(sa*uu/len(nei))+(1-sa)*F.node[nd]['scalar_attribute']
        # insau=int(sau*scale)
        # F.add_node(nd,scalar_attribute=sau,scalar_attribute_numeric=insau)

        for nd in F.nodes():
            # sa=1-(1./nx.degree(F,nd))
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            for nnei in nei:
                uu+=F.node[nnei]['scalar_attribute']
            X=F.node[nd]['scalar_attribute']
            Xnei=uu/len(nei)
            # uX= len(nei)*(1-Xnei)
            uX= b*(1. - X)*Xnei+X**2
            # uX= b*(1. - Xnei)*X

            # sau=(sb*uu/len(nei))+(1-sb)*F.node[nd]['scalar_attribute']
            insau=int(uX*scale)
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)

        # for i in F.nodes(data=True):
        #   print i
        # Checking for attributes equality
        y1=y
        y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        if ii ==ckck and ii<10:
            # col=['%.5f' %yy for yy in y]
            col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
            sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(ii+1)

            plt.subplot(3,2,kckc).set_title(sstt)
            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
            plt.axis('equal')
            plt.axis('off')
            ckck+=5
            kckc+=1
            plt.subplot(3,2,5)
        # for yy in it.combinations(y,2):
        #   checkin=checkin and yy[0] -yy[1] <(1./scale)
        # for yy in range(len(y1)):
        #   # print y[yy]-y1[yy]<(1./scale)
        #   checkin=checkin and y[yy]-y1[yy]<(0.1/(scale))
        #   # print checkin
        # if checkin:
        #   break
        asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        if np.isnan(asss):
            asss=1.
        # print 'Iteration %i ==> %f' %(ii,asss),y 
        # print type(asss), asss<-1,asss>1
        iterat.append(ii)

        assort.append(asss)

        # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        plt.plot(F.nodes(),y)
        # if asss==1. :
        #   break
    plt.plot(F.nodes(),y,linewidth=3.)
    sstt= "Time variation of scalar attribute assortativity coefficient"

    plt.subplot(3,2,6).set_title(sstt)

    # plt.figure(3)

    plt.plot(iterat,assort)
    plt.ylim(-1.1,1.1)
    # plt.figure(3)
    # plt.plot(F.nodes(),y)
    # col=['%.5f' %yy for yy in y]
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    sstt="Distribution of scalar attributes over graph nodes at %i iterations\n (consensual attribute = %s)" %(iterations,col[0])
    plt.subplot(3,2,4).set_title(sstt)

    # plt.figure(4)

    
    # print col
    print [F.node[i]['scalar_attribute_numeric'] for i in F.nodes()]
    # pos=nx.spring_layout(G)
    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')

    plt.show()



def polinfluence_sim(nodes,p,sa,iterations,scale=1000):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)

    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    F,asoc=utilat.create_random_scalar_attributes(G,scale)
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]

    fig = plt.figure(figsize=(17,17))


    sstt="Initial distribution of scalar attributes over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
    plt.subplot(3,2,1).set_title(sstt)
    # plt.set_cmap('cool')
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')
    
    # plt.figure(2)
    sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
    plt.subplot(3,2,5).set_title(sstt)
    plt.ylim(-0.01,1.01)
    # for i in F.nodes(data=True):
        # print i
    # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
    iterat=[]

    assort=[]
    y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    for ii in range(iterations):
        # sa=0.05
        checkin=True
        # nd=F.nodes()[0]
        # # # print nd
        # uu=0

        # nei=nx.neighbors(F,nd)
        # # # print nei
        # for nnei in nei:
        #     uu+=F.node[nnei]['scalar_attribute']
        
        # if F.node[nd]['scalar_attribute'] < uu/len(nei):
        #     sau=sa*max(2.*F.node[nd]['scalar_attribute'] - uu/len(nei),0.)+(1-sa)*F.node[nd]['scalar_attribute']
        # if F.node[nd]['scalar_attribute'] > uu/len(nei):
        #     sau=sa*min(2.*F.node[nd]['scalar_attribute'] - uu/len(nei),1.)+(1-sa)*F.node[nd]['scalar_attribute']

        # # sau=(sa*uu/len(nei))+(1-sa)*F.node[nd]['scalar_attribute']
        # insau=int(sau*scale)
        # F.add_node(nd,scalar_attribute=sau,scalar_attribute_numeric=insau)

        # nd=F.nodes()[-1]
        # # # print nd
        # uu=0

        # nei=nx.neighbors(F,nd)
        # # # print nei
        # for nnei in nei:
        #     uu+=F.node[nnei]['scalar_attribute']
        
        # if F.node[nd]['scalar_attribute'] < uu/len(nei):
        #     sau=sa*max(2.*F.node[nd]['scalar_attribute'] - uu/len(nei),0.)+(1-sa)*F.node[nd]['scalar_attribute']
        # if F.node[nd]['scalar_attribute'] > uu/len(nei):
        #     sau=sa*min(2.*F.node[nd]['scalar_attribute'] - uu/len(nei),1.)+(1-sa)*F.node[nd]['scalar_attribute']

        # # sau=(sa*uu/len(nei))+(1-sa)*F.node[nd]['scalar_attribute']
        # insau=int(sau*scale)
        # F.add_node(nd,scalar_attribute=sau,scalar_attribute_numeric=insau)


        # if F.node[nd]['scalar_attribute'] < (uu/len(nei)):

        #     sau=(sa*max(2.*F.node[nd]['scalar_attribute'] - (uu/len(nei)),0.)+(1-sa)*F.node[nd]['scalar_attribute']
        # if F.node[nd]['scalar_attribute'] > (uu/len(nei)):

        # # else:
        #     sau=(sa*min(2.*F.node[nd]['scalar_attribute'] - (uu/len(nei)),1.)+(1-sa)*F.node[nd]['scalar_attribute']

        # # sau=(sa*uu/len(nei))+(1-sa)*F.node[nd]['scalar_attribute']
        
        # insau=int(sau*scale)
        # F.add_node(nd,scalar_attribute=sau,scalar_attribute_numeric=insau)
        # for nd in F.nodes()[1:-1]:
        #     # sa=1-(1./nx.degree(F,nd))
        #     uu=0
        #     nei=nx.neighbors(F,nd)
        #     # print nei
        #     for nnei in nei:
        #         uu+=F.node[nnei]['scalar_attribute']

        #     sau=(sa*uu/len(nei))+(1-sa)*F.node[nd]['scalar_attribute']
        #     insau=int(sau*scale)
        #     F.add_node(nd,scalar_attribute=sau,scalar_attribute_numeric=insau)


        for nd in F.nodes():
            # sa=1-(1./nx.degree(F,nd))
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            for nnei in nei:
                uu+=F.node[nnei]['scalar_attribute']
            X=F.node[nd]['scalar_attribute']
            Xnei=uu/len(nei)

            if X < Xnei:
                uX=sa*max(2.*X - Xnei,0.)+(1-sa)*X
            if X > Xnei:
                uX=sa*min(2.*X - Xnei,1.)+(1-sa)*X

            # uX=(sa*uu/len(nei))+(1-sa)*F.node[nd]['scalar_attribute']
            insau=int(uX*scale)
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)

            
        # for i in F.nodes(data=True):
        #   print i
        # Checking for attributes equality
        y1=y
        y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        if ii ==ckck and ii<10:
            # col=['%.5f' %yy for yy in y]
            col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
            sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(ii+1)

            plt.subplot(3,2,kckc).set_title(sstt)
            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
            plt.axis('equal')
            plt.axis('off')
            ckck+=5
            kckc+=1
            plt.subplot(3,2,5)
        # for yy in it.combinations(y,2):
        #   checkin=checkin and yy[0] -yy[1] <(1./scale)
        # for yy in range(len(y1)):
        #   # print y[yy]-y1[yy]<(1./scale)
        #   checkin=checkin and y[yy]-y1[yy]<(0.1/(scale))
        #   # print checkin
        # if checkin:
        #   break
        asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # if np.isnan(asss):
        #     asss=1.
        # print 'Iteration %i ==> %f' %(ii,asss),y 
        # print type(asss), asss<-1,asss>1
        iterat.append(ii)

        assort.append(asss)

        # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        plt.plot(F.nodes(),y)
        # if asss==1. :
        #   break
    plt.plot(F.nodes(),y,linewidth=3.)
    sstt= "Time variation of scalar attribute assortativity coefficient"

    plt.subplot(3,2,6).set_title(sstt)

    # plt.figure(3)

    plt.plot(iterat,assort)
    plt.ylim(-1.1,1.1)
    # plt.figure(3)
    # plt.plot(F.nodes(),y)
    # col=['%.5f' %yy for yy in y]
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    sstt="Distribution of scalar attributes over graph nodes at %i iterations\n (polarized attributes = (%.2f, %.2f))" %(iterations,min(col),max(col))#col[0])
    plt.subplot(3,2,4).set_title(sstt)

    # plt.figure(4)

    
    # print col
    # print [F.node[i]['scalar_attribute_numeric'] for i in F.nodes()]
    # pos=nx.spring_layout(G)
    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')

    plt.show()





def cl_influence_sim(nodes,p,sa1,sa2,iterations,scale=1000):  # b1,b2,
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    # col=y
    pos=nx.spring_layout(G)

    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    # scale=1000
    F,asoc=utilat.create_random_scalar_attributes(G,scale)
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]

    fig = plt.figure(figsize=(17,17))


    sstt="Initial distribution of scalar attributes over graph nodes" #\n (diffusion source at node %s with initial attribute =%f)" %(F.nodes()[0],starting_value_of_zero_node)
    plt.subplot(3,2,1).set_title(sstt)
    # plt.set_cmap('cool')
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')
    
    # plt.figure(2)
    sstt = "Time variation of scalar attributes over graph nodes" #%F.nodes()[0]#,starting_value_of_zero_node)
    plt.subplot(3,2,5).set_title(sstt)

    # for i in F.nodes(data=True):
        # print i
    # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
    iterat=[]
    assort=[]
    y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    ckck=4
    kckc=2
    for ii in range(iterations):
        # sa=0.05
        checkin=True
        # nd=F.nodes()[0]
        # # print nd
        # uu=0
        # nei=nx.neighbors(F,nd)
        # # print nei
        # for nnei in nei:
        #     uu+=F.node[nnei]['scalar_attribute']
        # Xnei=uu/len(nei)
        # X=F.node[nd]['scalar_attribute']

        # if X <= 1/3. and Xnei <= 1/2.:  #1/3.
        #     uX=(sa1*Xnei)+(1-sa1)*X
        # elif 1/3. < X <= 2/3.:  #and 1/3. < Xnei <= 2/3.: 
        #     uX=(sa1*Xnei)+(1-sa1)*X
        # elif X > 2/3. and Xnei > 1/2.:  #2/3.
        #     uX=(sa1*Xnei)+(1-sa1)*X

        # elif X <= 1/3. and 1/3. < Xnei <= 2/3.:
        #     uX=(sa2*Xnei)+(1-sa2)*X
        # elif 1/3. < X <= 2/3. and Xnei <= 1/3.:
        #     uX=(sa2*Xnei)+(1-sa2)*X
        # elif 1/3. < X <= 2/3. and 2/3. < Xnei:
        #     uX=(sa2*Xnei)+(1-sa2)*X
        # elif 1/3. < Xnei <= 2/3. and 2/3. < X:
        #     uX=(sa2*Xnei)+(1-sa2)*X

        # elif X <= 1/3. and 1/3. < Xnei <= 2/3.:
        #     uX=(sa2*Xnei)+(1-sa2)*X
        # elif 1/3. < X <= 2/3. and Xnei <= 1/3.:
        #     uX=(sa2*Xnei)+(1-sa2)*X
        # elif 1/3. < X <= 2/3. and 2/3. < Xnei:
        #     uX=(sa2*Xnei)+(1-sa2)*X
        # elif 1/3. < Xnei <= 2/3. and 2/3. < X:
        #     uX=(sa2*Xnei)+(1-sa2)*X

        # else:
        #     uX = X

        # if b1 <= abs(X - Xnei) <= b2:
        #     uX=(sa*Xnei)+(1-sa)*X
        # # else:
        # #     uX = X
        # # elif X < Xnei:
        # #     uX=0
        # # elif X > Xnei:
        # #     uX=1
        # elif X < Xnei:
        #     uX=sa*max(2.*X - Xnei,0.)+(1-sa)*X
        # elif X > Xnei:
        #     uX=sa*min(2.*X - Xnei,1.)+(1-sa)*X
        # insau=int(uX*scale)
        # F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)

        for nd in F.nodes():
            # sa=1-(1./nx.degree(F,nd))
            uu=0
            nei=nx.neighbors(F,nd)
            # print nei
            for nnei in nei:
                uu+=F.node[nnei]['scalar_attribute']
            X=F.node[nd]['scalar_attribute']
            Xnei=uu/len(nei)

            if X <= 1/3. and Xnei <= 1/2.:  #1/3.
                uX=(sa1*Xnei)+(1-sa1)*X
            elif 1/3. < X <= 2/3.:  #and 1/3. < Xnei <= 2/3.: 
                uX=(sa1*Xnei)+(1-sa1)*X
            elif X > 2/3. and Xnei > 1/2.:  #2/3.
                uX=(sa1*Xnei)+(1-sa1)*X

            # elif X <= 1/3. and 1/3. < Xnei <= 2/3.:
            #     uX=(sa2*Xnei)+(1-sa2)*X
            # elif 1/3. < X <= 2/3. and Xnei <= 1/3.:
            #     uX=(sa2*Xnei)+(1-sa2)*X
            # elif 1/3. < X <= 2/3. and 2/3. < Xnei:
            #     uX=(sa2*Xnei)+(1-sa2)*X
            # elif 1/3. < Xnei <= 2/3. and 2/3. < X:
            #     uX=(sa2*Xnei)+(1-sa2)*X

            else:
                uX = X
            # print uX
            # if b1 <= abs(X - Xnei) <= b2:
            #     uX=(sa*Xnei)+(1-sa)*X
            # # else:
            # #     uX = X
            # # elif X < Xnei:
            # #     uX=0
            # # elif X > Xnei:
            # #     uX=1
            # elif X < Xnei:
            #     uX=sa*max(2.*X - Xnei,0.)+(1-sa)*X
            # elif X > Xnei:
            #     uX=sa*min(2.*X - Xnei,1.)+(1-sa)*X
            # # uX=(sa*Xnei)+(1-sa)*X
            insau=int(uX*scale)
            F.add_node(nd,scalar_attribute=uX,scalar_attribute_numeric=insau)

            
        # for i in F.nodes(data=True):
        #   print i
        # Checking for attributes equality
        y1=y
        y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        if ii ==ckck and ii<10:
            # col=['%.5f' %yy for yy in y]
            col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
            sstt="Distribution of scalar attributes over graph nodes at %i iterations" %(ii+1)

            plt.subplot(3,2,kckc).set_title(sstt)
            nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
            plt.axis('equal')
            plt.axis('off')
            ckck+=5
            kckc+=1
            plt.subplot(3,2,5)
        # for yy in it.combinations(y,2):
        #   checkin=checkin and yy[0] -yy[1] <(1./scale)
        # for yy in range(len(y1)):
        #   # print y[yy]-y1[yy]<(1./scale)
        #   checkin=checkin and y[yy]-y1[yy]<(0.1/(scale))
        #   # print checkin
        # if checkin:
        #   break
        asss=nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        if np.isnan(asss):
            asss=1.
        # print 'Iteration %i ==> %f' %(ii,asss),y 
        # print type(asss), asss<-1,asss>1
        iterat.append(ii)

        assort.append(asss)

        # print nx.numeric_assortativity_coefficient(F,'scalar_attribute_numeric')
        # y=[F.node[i]['scalar_attribute'] for i in F.nodes()]
        plt.plot(F.nodes(),y,'-o')
        # if asss==1. :
        #   break
    momo1=[1./3 for nd in F.nodes()]
    momo2=[2./3 for nd in F.nodes()]
    plt.plot(F.nodes(),y,linewidth=3.)
    plt.plot(F.nodes(),momo1,linewidth=2.,color='r')
    plt.plot(F.nodes(),momo2,linewidth=2.,color='r')
    sstt= "Time variation of scalar attribute assortativity coefficient"

    plt.subplot(3,2,6).set_title(sstt)

    # plt.figure(3)

    plt.plot(iterat,assort)
    plt.ylim(-1.1,1.1)
    # plt.figure(3)
    # plt.plot(F.nodes(),y)
    # col=['%.5f' %yy for yy in y]
    col=[F.node[i]['scalar_attribute'] for i in F.nodes()]
    sstt="Distribution of scalar attributes over graph nodes at iterations" #%i  ss\n (consensual attribute = %s)" %(iterations,col[0])
    plt.subplot(3,2,4).set_title(sstt)

    # plt.figure(4)

    
    # print col
    # print [F.node[i]['scalar_attribute_numeric'] for i in F.nodes()]
    # pos=nx.spring_layout(G)
    ##nx.draw_networkx(g,pos=pos, node_color=col,cmap=plot.cm.Reds)
    nx.draw_networkx(G,pos=pos, node_color=col,vmin=0.,vmax=1.)
    plt.axis('equal')
    plt.axis('off')

    plt.show()






# influence_sim(25,0.2,.1,500)
# infdif_sim(25,.2,0.,.1,500)
# polinf_sim(25,.2,500)
# sidif_sim(25,.2,1.,500)
# polinfluence_sim(25,0.2,.041,500)
# cl_influence_sim(25,0.2,0.9,0.1,500)
# 
# nodes = 25
# p = 0.2
# iterations = 500
# sa = 0.1
# # %autoreload 2
# influence_sim(nodes,p,sa,iterations,new_old=True)nodes = 14
# p = 0.2
# sa =1
# nodes=14
# # %autoreload 2
# iterations = 10
# h=1
# su=1.
# ffun='(1-h)*X+h*ssa*Xnei'
# ffun='h*ssa*Xnei'
# F,u_all,source=influence_sim_dh(nodes,p,sa,iterations,G=None,new_old=True,source=[],source_u=[.5],su=su,h=h,funcion=ffun,insrplot=False) #,new_old=False
# print u_all