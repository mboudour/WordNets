__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

'''
This script implements the trajectory analysis (cf. Borgatti & Halgin) of temporal graphs.
'''

import networkx as nx
from networkx.algorithms import bipartite as bip
import os
import itertools as it
from collections import Counter
import xlsxwriter #sudo pip install xlsxwriter
import pickle

# import create_gexf_year as cgy
import pyinter #as interval sudo pip install  pyinter
import matplotlib.pylab as plt
import matplotlib.pyplot as mp
import igraph as ig
import pandas as pd
from prettytable import PrettyTable #sudo pip install prettytable
# from IPython.display import *
# from IPython.display import HTML

def meanstdvs(x):
    from math import sqrt
    n, mean, std = len(x), 0, 0
    for a in x:
        mean = mean + a
    if n==0:
        mean=0
    else:
        mean = mean / float(n)
    for a in x:
       std = std + (a - mean)**2
    std = sqrt(std / float(n-1))
    return mean, std

def meanstdv(x):
    from math import sqrt
    n, mean, std = len(x), 0, 0
    for a in x:
        mean = mean + a
    if n==0:
        mean=0
    else:
        mean = mean / float(n)
##    for a in x:
##        std = std + (a - mean)**2
##    std = sqrt(std / float(n-1))
    return mean#, std
def modeS(data_list):
    c=Counter(data_list)
    return c.most_common(1),c.most_common()
def maxMin(myList):

    return max(myList),min(myList),max(myList)-min(myList)

def newInterPlus(inter,q):
    return pyinter.interval.closed(inter.lower_value,inter.upper_value+q)
def newInterMinus(inter,q):
    return pyinter.interval.closed(inter.lower_value-q,inter.upper_value)
def normInter(inter):
    return inter.upper_value-inter.lower_value

def lisEqual(list1,list2):
    if len(list1)!=len(list2):
        return False
    for i in range(len(list1)):
        if list1[i]!=list2[i]:
            return False
    return True
# def int_equal(ll,mm):
#     if 
def dicIs_empty(any_structure):
    if any_structure:
        # print('Structure is not empty.')
        return False
    else:
        # print('Structure is empty.')
        return True

def create_interv(G,nodelist=[],time_to_add=0):
    intervals=dict()
    lintervals=dict()
    # udatc=pyinter.interval.closed(0,0)
    if len(nodelist)==0:
        nodelist=G.nodes()
    coun=0
    for nd in nodelist:
        # print nd,'dddddddddddddddddddd',coun
        poin=dict()
        # udat=pyinter.interval.closed(0,0)
        # udat=pyinter.interval_set(udate)
        # print nd,G[nd],'aaaaa'
        for ed in G[nd]:
            udat=pyinter.interval.closed(0,0)
            # if not isinstance(G,nx.MultiGraph):
            #     date_start=G[nd][ed]['date_start']
            #     date_end=G[nd][ed]['date_end']+time_to_add

            #     date=pyinter.interval.closed(date_start,date_end)
            #     # print type(udat),isinstance(udat,pyinter.interval.Interval)
            #     # print udatc,'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk'
            #     if isinstance(udat,pyinter.interval.Interval)  and normInter(udat)==0:
            #         udat=date
            #     # date=pyinter.interval_set(dates)
            #     # print date,udat
            #     try:
            #         udat=udat.union(date)
            #     except:
            #         udat.add(date)
            #     # if isinstance(udatc,pyinter.interval.Interval)  and normInter(udatc)==0:
            #     #     udatc=date
            #     if coun==0:
            #         udatc=date
            #         coun+=1
            #     try:
            #         udatc=udatc.union(date)
            #     except Exception,e:
            #         # print e,date,udatc
            #         udatc.add(date)
            # # print G[nd]
            # # print ed
            # # print G[nd][ed]
            # elif isinstance(G[nd][ed],list):
            for edin in G[nd][ed]:
                date_start=G[nd][ed][edin]['date_start']
                date_end=G[nd][ed][edin]['date_end']+time_to_add

                date=pyinter.interval.closed(date_start,date_end)
                # print type(udat),isinstance(udat,pyinter.interval.Interval)
                # print udatc,'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk'
                if isinstance(udat,pyinter.interval.Interval)  and normInter(udat)==0:
                    udat=date
                # date=pyinter.interval_set(dates)
                # print date,udat
                try:
                    udat=udat.union(date)
                except:
                    udat.add(date)
                # if isinstance(udatc,pyinter.interval.Interval)  and normInter(udatc)==0:
                #     udatc=date
                if coun==0:
                    udatc=date
                    coun+=1
                try:
                    udatc=udatc.union(date)
                except Exception,e:
                    # print e,date,udatc
                    udatc.add(date)
            # print udat,ed,nd
            # print sorted((nd,ed))
            soso=sorted((nd,ed))
            # print soso
            poin[(soso[0],soso[1])]=udat
            # poin[str(sorted((nd,ed)))]=udat
        intervals[nd]=poin
        # if isinstance(intervals[i][j],pyinter.interval.Interval):
    return intervals,udatc

def plot_total_traject_ig(traj_list,F,u_node,uu,nam_v=dict(),colors=True):
    # nam_v=dict()
    # uu=0
    # print traj_list,'88888888888888888888888888888888888888888'
    for kk in traj_list:
        lldic,cldic=clear_traj_d(kk)
        if len(cldic)>1:
            for kj in lldic:
                jj=lldic[kj][0]
                ll=lldic[kj][1]
                # print kk,jj,ll
                if jj not in nam_v:
                    nam_v[jj]=uu
                    uu+=1
                    if colors:
                        if jj=='v':
                            vcolor='green'
                        elif jj=='w':
                            vcolor='cyan' 
                        elif jj=='z':
                            vcolor='#FFD700'
                        elif jj =='u':
                            vcolor='#B22222'
                    F.add_vertex(name=jj,color=vcolor,shape='circle',vlabel=jj)
            # for kj in ldicc:
            for kjj in range(len(kk)-1):
                kj = kk[kjj]
                jk = kk[kjj+1]
                # print lldic[kj][0],lldic[jk][0],'lllll',nam_v

                if lldic[kj][0]!=lldic[jk][0]:
                    if (nam_v[lldic[kj][0]],nam_v[lldic[jk][0]]) not in nam_v:
                        nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])]=uu
                        uu+=1
                        momo=set()
                        momo.add(u_node+str(lldic[kj][1]))
                        F.add_vertex(name=(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]]),color='grey',shape='hidden',\
                            vlabel=momo)
                        # F.add_edge(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]],ed_label=momo)#,ecolor=ecolor)
                        F.add_edge(nam_v[lldic[kj][0]],nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])])
                        F.add_edge(nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])],nam_v[lldic[jk][0]])
                    else:
                        F.vs[nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])]]['vlabel'].add(u_node+str(lldic[kj][1]))
                    # continue
                # print kjj , kj,jk,'dddd',nam_v
                # print nam_v[lldic[kj][0]],nam_v[lldic[jk][0]],'lllll'
                    # print lldic[kj][0],lldic[jk][0],'llllldfasdfasdfa'
                    # if u_node=='u':
                    #     ecolor='#FF00FF'
                    # elif u_node == 'v':
                    #     ecolor='#7FFF00'
                    # elif u_node== 'w':
                    #     ecolor='#6495ED'
                    # elif u_node=='z':
                    #     ecolor='#DAA520'
                    # try:
                    #     ver=F.vs.find(_name_eq=(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]]))
                    #     ver['vlabel'].add(u_node+str(lldic[kj][1]))
                    #     # F.add_edge(nam_v[lldic[kj][0]],nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])])
                    #     # F.add_edge(nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])],nam_v[lldic[kj][0]])
                    #     # edg=F.es.find(_source_eq=nam_v[lldic[kj][0]],_target_eq=nam_v[lldic[jk][0]])
                    #     # edg['ed_label'].add(u_node+str(lldic[kj][1]))
                    # except Exception,e:
                        # print e,nam_v
                    #     momo=set()
                    #     momo.add(u_node+str(lldic[kj][1]))
                    #     nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])]=uu
                    #     uu+=1
                    #     F.add_vertex(name=(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]]),color='grey',shape='rectangle',\
                    #         vlabel=momo)
                    #     # F.add_edge(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]],ed_label=momo)#,ecolor=ecolor)
                    #     F.add_edge(nam_v[lldic[kj][0]],nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])])
                    #     F.add_edge(nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])],nam_v[lldic[kj][0]])
                        
                        
    # print F
    # print '5555555555555555555555555555555555555555555555555555555555'
    return F,nam,uu
def plot_total_traject(traj_list,F,u_node,uu,nam_v=dict(),colors=False):
    # nam_v=dict()
    # uu=0
    # print traj_list,'88888888888888888888888888888888888888888'
    for kk in traj_list:
        lldic,cldic=clear_traj_d(kk)
        if len(cldic.keys())>1:
            for kj in lldic:
                jj=lldic[kj][0]
                ll=lldic[kj][1]
                # print kk,jj,ll
                if jj not in nam_v:
                    nam_v[jj]=uu
                    uu+=1
                    if colors:
                        if jj=='v':
                            vcolor='green'
                        elif jj=='w':
                            vcolor='cyan' 
                        elif jj=='z':
                            vcolor='#FFD700'
                        elif jj =='u':
                            vcolor='#B22222'
                    else:
                        vcolor='grey'
                    F.add_vertex(name=jj,color=vcolor,shape='circle',vlabel=jj)
            # for kj in ldicc:
            for kjj in range(len(kk)-1):
                kj = kk[kjj]
                jk = kk[kjj+1]
                # print lldic[kj][0],lldic[jk][0],'lllll',nam_v

                if lldic[kj][0]!=lldic[jk][0]:
                    # if (nam_v[lldic[kj][0]],nam_v[lldic[jk][0]]) not in nam_v:
                    #     nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])]=uu
                    #     uu+=1
                    #     momo=set()
                    #     momo.add(u_node+str(lldic[kj][1]))
                    #     F.add_vertex(name=(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]]),color='grey',shape='hidden',\
                    #         vlabel=momo)
                    #     # F.add_edge(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]],ed_label=momo)#,ecolor=ecolor)
                    #     F.add_edge(nam_v[lldic[kj][0]],nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])])
                    #     F.add_edge(nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])],nam_v[lldic[jk][0]])
                    # else:
                    #     F.vs[nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])]]['vlabel'].add(u_node+str(lldic[kj][1]))
                    # continue
                # print kjj , kj,jk,'dddd',nam_v
                # print nam_v[lldic[kj][0]],nam_v[lldic[jk][0]],'lllll'
                    # print lldic[kj][0],lldic[jk][0],'llllldfasdfasdfa'
                    # if u_node=='u':
                    #     ecolor='#FF00FF'
                    # elif u_node == 'v':
                    #     ecolor='#7FFF00'
                    # elif u_node== 'w':
                    #     ecolor='#6495ED'
                    # elif u_node=='z':
                    #     ecolor='#DAA520'
                    try:
                        ver=F.es.find(_source_eq=nam_v[lldic[kj][0]],_target_eq= nam_v[lldic[jk][0]])
                        # ver=F.vs.find(_name_eq=(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]]))
                        ver['vlabel'].add(u_node+str(lldic[kj][1]))
                        # F.add_edge(nam_v[lldic[kj][0]],nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])])
                        # F.add_edge(nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])],nam_v[lldic[kj][0]])
                        # edg=F.es.find(_source_eq=nam_v[lldic[kj][0]],_target_eq=nam_v[lldic[jk][0]])
                        # edg['ed_label'].add(u_node+str(lldic[kj][1]))
                    except Exception,e:
                        # print e#,nam_v
                        # print nam_v

                        # print nam_v[lldic[kj][0]],nam_v[lldic[jk][0]]
                        momo=set()
                        momo.add(u_node+str(lldic[kj][1]))
                        # nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])]=uu
                        # uu+=1
                        # F.add_vertex(name=(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]]),color='grey',shape='rectangle',\
                        #     vlabel=momo)
                        F.add_edge(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]],ed_label=momo)#,ecolor=ecolor)
                        # F.add_edge(nam_v[lldic[kj][0]],nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])])
                        # F.add_edge(nam_v[(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]])],nam_v[lldic[kj][0]])
                        
                        
    # print F
    # print '5555555555555555555555555555555555555555555555555555555555'
    # return F,nam,uu
    return F,uu

    
def plot_transit_igraph(F,infile_name,bot_t,u_nd,write_to_file=False): 

    bobo_t=dict()
    # bobo_t['mama']='loli'
    # print bot_t,'bbbbbbbbbbbbbbbb'
    for i in bot_t:
        # print i,bot_t
        # bobo_t[i]=bot_t[i]
        # nod_st=i[2]
        # nod_en=i[7]
        nod_st=i[0]
        nod_en=i[1]
        # print i,nod_st,nod_en,'bboboobbbboooooooooo',bot_t[i],bobo_t,u_nd
        if nod_st==u_nd:
            bobo_t[nod_en]=bot_t[i]
        else:

            bobo_t[nod_st]=bot_t[i]  
    g = ig.read(infile_name)
    filedir='S_out_figs'
    try:
        os.stat(filedir)
    except:
        os.mkdir(filedir)
    filf='%s_graph_trans.png' %u_nd
    outfile_name = os.path.join('%s' % filedir,filf)
    g.vs["label"] = F.nodes()
    # print g.vs['label']
    iii=0
    # print bobo_t
    for v in  g.vs:
        # print v,v['id'].split('__')[1]
        # print bobo_t[v['id'].split('__')[0]]
        # print bobo_t
        # g.vs[iii]['layout']=(int(v['id'][1:]),bobo_t[v['id'][0]])
        g.vs[iii]['layout']=(int(v['id'].split('__')[1]),bobo_t[v['id'].split('__')[0]])

        iii+=1
    if write_to_file:
        ig.plot(g,outfile_name,layout=g.vs['layout'],vertex_size=30, vertex_color='grey', vertex_label_size=12,edge_curved=0.05,
     bbox=(0, 0, 800, 600))#,
    else:
        ig.draw(g)
     #    ig.plot(g,layout=g.vs['layout'],vertex_size=30, vertex_color='grey', vertex_label_size=12,edge_curved=0.05,
     # bbox=(0, 0, 800, 600))
    return outfile_name

def aNala(traj_list,traj_counter,filf):

    so='current'
    from prettytable import PrettyTable
    x=PrettyTable(['Vertices','fOriginator','fTransmitter','fTerminator','fBlackHole','fInvolvement',
        'pOriginator','pTransmitter'])
    x.padding_width=1
    y=PrettyTable(['Vertices','pTerminator','pBlackHole','lOriginator','lTransmitter','lTerminator',
        'lBlackHole'])
    y.padding_width=1
    z=PrettyTable(['Vertices','lInvolvement','Position','RelPosition','Betweenness'])
    z.padding_width=1
    # y=PrettyTable(['Vertices','lOriginator','lTransmitter',
    #     'lTerminator','lBlackHole','lInvolvement','Position','RelPosition','Betweenness'])
    # y.padding_width=1


    # outfile_name = os.path.join('%s' % filedir,filenam)
    fil=open(filf[:-4]+'txt','w')

    workbook = xlsxwriter.Workbook(filf)#+'_current.xlsx')
    worksheet = workbook.add_worksheet('Trajectories')
    worksheet.write('A6', 'Vertices')
    worksheet.write('B6','fOriginator')
    worksheet.write('C6','fTransmitter')
    worksheet.write('D6','fTerminator')
    worksheet.write('E6','fBlackHole')
    worksheet.write('F6','fInvolvement')
    worksheet.write('G6','pOriginator')
    worksheet.write('H6','pTransmitter')
    worksheet.write('I6','pTerminator')
    worksheet.write('J6','pBlackHole')
    worksheet.write('K6','lOriginator')
    worksheet.write('L6','lTransmitter')
    worksheet.write('M6', 'lTerminator')
    worksheet.write('N6','lBlackHole')
    worksheet.write('O6','lInvolvement')
    worksheet.write('P6','Position')
    worksheet.write('Q6','RelPosition')
    worksheet.write('R6','Betweenness')
##        worksheet.write('S1','fOriginator')
##        worksheet.write('T1','fTransmitter')
##        worksheet.write('U1','fTerminator')
##        worksheet.write('V1','fBlackHole')
##        worksheet.write('W1','fInvolvement')
##        worksheet.write('X1','Weight')
    
    all_nodes,fOriginator, fTransmitter,fTerminator, fBlackHole,fInvolvement,lOriginator,\
    lTransmitter,lTerminator,lBlackHole, lInvolvement,Position,RelPosition ,bet,llength\
    =trajectoriesProp(traj_list,traj_counter)
    pOriginator=dict()
    pTransmitter =dict()
    pTerminator=dict()
    pBlackHole  =dict()

        
    u=6
    for kk in all_nodes:
        # print kk
        pOriginator[kk]=float(fOriginator[kk])/fInvolvement[kk]
        pTransmitter[kk] =float(fTransmitter[kk])/fInvolvement[kk]
        pTerminator[kk]=float(fTerminator[kk])/fInvolvement[kk]
        pBlackHole[kk]=float(fBlackHole[kk])/fInvolvement[kk]
        u+=1
        a='A%i' %u
        b='B%i' %u
        c='C%i' %u
        d='D%i' %u
        e='E%i' %u
        f='F%i' %u
        g='G%i' %u
        h='H%i' %u
        i='I%i' %u
        j='J%i' %u
        k='K%i' %u
        l='L%i' %u
        m='M%i' %u
        n='N%i' %u
        o='O%i' %u
        p='P%i' %u
        q='Q%i' %u
        r='R%i' %u
        worksheet.write(a,kk )
        worksheet.write(b,fOriginator [kk])
        worksheet.write(c,fTransmitter[kk])
        worksheet.write(d,fTerminator[kk])
        worksheet.write(e, fBlackHole[kk])
        worksheet.write(f,fInvolvement[kk])
        worksheet.write(g,pOriginator[kk])
        worksheet.write(h,pTransmitter [kk])
        worksheet.write(i,pTerminator[kk])
        worksheet.write(j,pBlackHole[kk])
        worksheet.write(k, lOriginator[kk])
        worksheet.write(l,lTransmitter[kk])
        worksheet.write(m,lTerminator[kk])

        worksheet.write(n,lBlackHole[kk])
        worksheet.write(o,lInvolvement [kk])
        worksheet.write(p,Position[kk])
        worksheet.write(q,RelPosition[kk])
        worksheet.write(r, bet[kk])
        x.add_row([kk,fOriginator [kk],fTransmitter[kk],fTerminator[kk],fBlackHole[kk],
            fInvolvement[kk],pOriginator[kk],pTransmitter [kk]])#,pTerminator[kk],pBlackHole[kk]])

        y.add_row([kk,pTerminator[kk],pBlackHole[kk],lOriginator[kk],lTransmitter[kk],lTerminator[kk],lBlackHole[kk]])#,
             # Position[kk],RelPosition[kk],bet[kk]])
        z.add_row([kk,lInvolvement [kk],Position[kk],RelPosition[kk],bet[kk]])
# x=PrettyTable(['Vertices','fOriginator','fTransmitter','fTerminator','fBlackHole','fInvolvement',
#         'pOriginator','pTransmitter'])
#     x.padding_width=1
#     y=PrettyTable(['Vertices','pTerminator','pBlackHole','lOriginator','lTransmitter','lTerminator',
#         'lBlackHole','lInvolvement'])
#     y.padding_width=1
#     z=PrettyTable(['Vertices','Position','RelPosition','Betweenness'])


    mena,stad=meanstdvs(llength)
    fil.write('%s trajectories analyzed.\n' %str(len(traj_list)))
    print '%s trajectories analyzed.' %str(len(traj_list))

    worksheet.write('A1', '%s trajectories analyzed.' %str(len(traj_list)))#str(sum(traj_counter.values())))
    # print '%s trajectories analyzed.' %str(len(traj_list))# str(sum(traj_counter.values()))
    ccou=1
    for i in traj_counter:
        e='E%i' %ccou
        fil.write('Trajectories of %s: %i\n' %(i,traj_counter[i]))
        print 'Trajectories of %s: %i' %(i,traj_counter[i])
        worksheet.write(e, 'Trajectories of %s: %i' %(i,traj_counter[i]))
        ccou+=1
    fil.write('Average length = %s\n' %str(mena))
    print
    print 'Average length = %s' %str(mena)
    worksheet.write('A2', 'Average length = %s' %str(mena))
    # print 'Average length = %s' %str(mena)
    print 'Std. dev. of length = %.4f\n' %stad
    fil.write('Std. dev. of length = %.4f\n' %stad)
    worksheet.write('A3', 'Std. dev. of length = %.4f' %stad)
    # x.float_format['fOriginator','fTransmitter','fTerminator','fBlackHole','fInvolvement',
    #     'pOriginator','pTransmitter','pTerminator','pBlackHole','lOriginator','lTransmitter',
    #     'lTerminator','lBlackHole','lInvolvement','Position','RelPosition','Betweenness']='%.4f'
    print x#.get_html_string()
    print 
    print 
    print 
    print y
    print
    print 
    print 
    print z
    fil.write(x.get_string())
    fil.close()
    # print 'Std. dev. of length = %.4f' %stad
    # print llength
    # worksheet.write('A4', 'Maximum length = %.4f' %max(llength))
    # print 'Maximum length = %.4f' %max(llength)
    # print traj_list,len(traj_list)
    workbook.close()
def aNala_pandas(traj_list,traj_counter,filf,plot_first_mode=True):

    so='current'
    pdf=pd.DataFrame(columns=['Vertices','fOriginator','fTransmitter','fTerminator','fBlackHole','fInvolvement',
        'pOriginator','pTransmitter','pTerminator','pBlackHole','lOriginator','lTransmitter','lTerminator',
        'lBlackHole','lInvolvement','Position','RelPosition','Betweenness'])

    #     'pOriginator','pTransmitter'])
    from prettytable import PrettyTable
    x=PrettyTable(['Vertices','fOriginator','fTransmitter','fTerminator','fBlackHole','fInvolvement',
        'pOriginator','pTransmitter'])
    x.padding_width=1
    y=PrettyTable(['Vertices','pTerminator','pBlackHole','lOriginator','lTransmitter','lTerminator',
        'lBlackHole'])
    y.padding_width=1
    z=PrettyTable(['Vertices','lInvolvement','Position','RelPosition','Betweenness'])
    z.padding_width=1
    # y=PrettyTable(['Vertices','lOriginator','lTransmitter',
    #     'lTerminator','lBlackHole','lInvolvement','Position','RelPosition','Betweenness'])
    # y.padding_width=1


    # outfile_name = os.path.join('%s' % filedir,filenam)
    fil=open(filf[:-4]+'txt','w')

    workbook = xlsxwriter.Workbook(filf)#+'_current.xlsx')
    worksheet = workbook.add_worksheet('Trajectories')
    worksheet.write('A6', 'Vertices')
    worksheet.write('B6','fOriginator')
    worksheet.write('C6','fTransmitter')
    worksheet.write('D6','fTerminator')
    worksheet.write('E6','fBlackHole')
    worksheet.write('F6','fInvolvement')
    worksheet.write('G6','pOriginator')
    worksheet.write('H6','pTransmitter')
    worksheet.write('I6','pTerminator')
    worksheet.write('J6','pBlackHole')
    worksheet.write('K6','lOriginator')
    worksheet.write('L6','lTransmitter')
    worksheet.write('M6', 'lTerminator')
    worksheet.write('N6','lBlackHole')
    worksheet.write('O6','lInvolvement')
    worksheet.write('P6','Position')
    worksheet.write('Q6','RelPosition')
    worksheet.write('R6','Betweenness')
##        worksheet.write('S1','fOriginator')
##        worksheet.write('T1','fTransmitter')
##        worksheet.write('U1','fTerminator')
##        worksheet.write('V1','fBlackHole')
##        worksheet.write('W1','fInvolvement')
##        worksheet.write('X1','Weight')
    
    all_nodes,fOriginator, fTransmitter,fTerminator, fBlackHole,fInvolvement,lOriginator,\
    lTransmitter,lTerminator,lBlackHole, lInvolvement,Position,RelPosition ,bet,llength\
    =trajectoriesProp(traj_list,traj_counter)
    pOriginator=dict()
    pTransmitter =dict()
    pTerminator=dict()
    pBlackHole  =dict()

        
    u=6
    uuk=0
    for kk in all_nodes:
        # print kk
        pOriginator[kk]=float(fOriginator[kk])/fInvolvement[kk]
        pTransmitter[kk] =float(fTransmitter[kk])/fInvolvement[kk]
        pTerminator[kk]=float(fTerminator[kk])/fInvolvement[kk]
        pBlackHole[kk]=float(fBlackHole[kk])/fInvolvement[kk]
        u+=1
        a='A%i' %u
        b='B%i' %u
        c='C%i' %u
        d='D%i' %u
        e='E%i' %u
        f='F%i' %u
        g='G%i' %u
        h='H%i' %u
        i='I%i' %u
        j='J%i' %u
        k='K%i' %u
        l='L%i' %u
        m='M%i' %u
        n='N%i' %u
        o='O%i' %u
        p='P%i' %u
        q='Q%i' %u
        r='R%i' %u
        worksheet.write(a,kk )
        worksheet.write(b,fOriginator [kk])
        worksheet.write(c,fTransmitter[kk])
        worksheet.write(d,fTerminator[kk])
        worksheet.write(e, fBlackHole[kk])
        worksheet.write(f,fInvolvement[kk])
        worksheet.write(g,pOriginator[kk])
        worksheet.write(h,pTransmitter [kk])
        worksheet.write(i,pTerminator[kk])
        worksheet.write(j,pBlackHole[kk])
        worksheet.write(k, lOriginator[kk])
        worksheet.write(l,lTransmitter[kk])
        worksheet.write(m,lTerminator[kk])

        worksheet.write(n,lBlackHole[kk])
        worksheet.write(o,lInvolvement [kk])
        worksheet.write(p,Position[kk])
        worksheet.write(q,RelPosition[kk])
        worksheet.write(r, bet[kk])
        # x.add_row([kk,fOriginator [kk],fTransmitter[kk],fTerminator[kk],fBlackHole[kk],
        #     fInvolvement[kk],pOriginator[kk],pTransmitter [kk]])#,pTerminator[kk],pBlackHole[kk]])

        # y.add_row([kk,pTerminator[kk],pBlackHole[kk],lOriginator[kk],lTransmitter[kk],lTerminator[kk],lBlackHole[kk]])#,
        #      # Position[kk],RelPosition[kk],bet[kk]])
        # z.add_row([kk,lInvolvement [kk],Position[kk],RelPosition[kk],bet[kk]])
# x=PrettyTable(['Vertices','fOriginator','fTransmitter','fTerminator','fBlackHole','fInvolvement',
#         'pOriginator','pTransmitter'])
#     x.padding_width=1
#     y=PrettyTable(['Vertices','pTerminator','pBlackHole','lOriginator','lTransmitter','lTerminator',
#         'lBlackHole','lInvolvement'])
#     y.padding_width=1
#     z=PrettyTable(['Vertices','Position','RelPosition','Betweenness'])
        pdf.loc[uuk]=[kk,fOriginator [kk],fTransmitter[kk],fTerminator[kk],fBlackHole[kk],
            fInvolvement[kk],pOriginator[kk],pTransmitter [kk],pTerminator[kk],pBlackHole[kk],
            lOriginator[kk],lTransmitter[kk],lTerminator[kk],lBlackHole[kk],lInvolvement [kk],
            Position[kk],RelPosition[kk],bet[kk] ]
        uuk+=1

    mena,stad=meanstdvs(llength)
    fil.write('%s trajectories analyzed.\n' %str(len(traj_list)))
    print '%s trajectories analyzed.' %str(len(traj_list))

    worksheet.write('A1', '%s trajectories analyzed.' %str(len(traj_list)))#str(sum(traj_counter.values())))
    # print '%s trajectories analyzed.' %str(len(traj_list))# str(sum(traj_counter.values()))
    ccou=1
    for i in traj_counter:
        e='E%i' %ccou
        fil.write('Trajectories of %s: %i\n' %(i,traj_counter[i]))
        print 'Trajectories of %s: %i' %(i,traj_counter[i])
        worksheet.write(e, 'Trajectories of %s: %i' %(i,traj_counter[i]))
        ccou+=1
    fil.write('Average length = %s\n' %str(mena))
    if plot_first_mode:
        print
        print 'Average length = %s' %str(mena)
        print 'Std. dev. of length = %.4f\n' %stad
        print pdf

    worksheet.write('A2', 'Average length = %s' %str(mena))
    # print 'Average length = %s' %str(mena)
    fil.write('Std. dev. of length = %.4f\n' %stad)
    worksheet.write('A3', 'Std. dev. of length = %.4f' %stad)
    # x.float_format['fOriginator','fTransmitter','fTerminator','fBlackHole','fInvolvement',
    #     'pOriginator','pTransmitter','pTerminator','pBlackHole','lOriginator','lTransmitter',
    #     'lTerminator','lBlackHole','lInvolvement','Position','RelPosition','Betweenness']='%.4f'
    # print x#.get_html_string()
    # print 
    # print 
    # print 
    # print y
    # print
    # print 
    # print 
    # print z
    fil.write(x.get_string())
    fil.close()
    # print 'Std. dev. of length = %.4f' %stad
    # print llength
    # worksheet.write('A4', 'Maximum length = %.4f' %max(llength))
    # print 'Maximum length = %.4f' %max(llength)
    # print traj_list,len(traj_list)
    workbook.close()
    return pdf

def bEtweennes(traj,bet=Counter()):

    # bet=Counter()
    # print traj.keys()
    # print aaa
    # print traj,'dddddddkjkjkj'
    for kk in traj:
        # print kk
        # print traj[kk]
        # print aa
        # yearst=sorted(kk)
        # print kk,yearst
        st=traj.index(kk)
        # ma=traj[:st]
        # mb=traj[st:]
        # print ma
        # print mb
        # bb=len(ma)*len(mb) #### or this
        bb=(st)*(len(traj)-st-1)

        # print bb
        # print aaaa
        bet[kk]+=bb
#         for yy in range(len(yearst)):
#             bb=(yy)*(len(yearst)-1-yy)
#            print yy,len(yearst),traj[kk],kk,bb
#             y =yearst[yy]
            # print y

#             bet[kk]+=bb
    # print bet
    # print aaaaa

    return bet
def clear_traj(ld):

    ldic=[]
    # print ld,'+++++++++++++++++'
    for k in range(len((ld))):
        na=ld[k].split('__')[0]
        # nb=ld[k][0]
        if len(ldic)==0:
            ldic.append(na)
        elif na!=ldic[-1]:
            ldic.append(na)
    # print ldic,'==============='
    return ldic
def clear_traj_d(ld):

    ldic=dict()
    cldic=dict()
    # print ld,'+++++++++++++++++'
    for k in range(len((ld))):
        # na=ld[k][0]
        # nb=ld[k][1:]
        kk=ld[k]

        lsd=kk.split('__')
        # print kk,lsd
        na=lsd[0]
        nb=lsd[1]
        
        # print na,nb,kk,lsd
        # nb=ld[k][0]
        # if k not in ldic:
        try:
            ldic[kk]=(na,int(nb))
        except :
            ldic[kk]=(na,int(float(nb)))
        if na not in cldic:
            cldic[na]=[kk]
        else:
            cldic[na].append(kk)
        # if nb not in cldic:
        #     cldic[nb]=[kk]
        # else:
        #     cldic[nb].append(kk)

    #     else:
    #         ldic
    #     if len(ldic)==0:
    #         ldic.append(na)
    #     elif na!=ldic[-1]:
    #         ldic.append(na)
    # print ldic,'==============='
    return ldic,cldic


def trajectoriesProp(ldicc,traj):
    '''
    fOriginator = No. of trajectories in which "job" is first node
    fTransmitter = No. of trajectories in which "job" is an interior node
    fTerminator = No. of trajectories in which "job" is last node
    fBlackHole = No. of trajectories in which "job" is first and last node
    fInvolvement = No. of trajectories in which "job" is involved
    pOriginator = Prop. of trajectories in which "job" is first node
    pTransmitter = Prop. of trajectories in which "job" is an interior node
    pTerminator = Prop. of trajectories in which "job" is last node
    pBlackHole = Prop. of trajectories in which "job" is first and last node
    lOriginator = Length of trajectories in which "job" is first node
    lTransmitter = Length of trajectories in which "job" is an interior node
    lTerminator = Length of trajectories in which "job" is last node
    lBlackHole = Length of trajectories in which "job" is first and last node
    lInvolvement = Length of trajectories in which "job" is involved
    Position = Avg. position of job in trajectories that involve it
    RelPosition = Avg. relative position of job in trajectories that involve it (if trajectory has n nodes,
     relative position is 100*(position-1)/(n-1)
    Betweenness = Total betweenness
    '''

    fOriginator=Counter()
    fTransmitter=Counter()
    fTerminator=Counter()
    fBlackHole=Counter()
    fInvolvement=Counter() #len(ldicc)#osa deixnoun afto
    lOriginator=Counter()
    lTransmitter=Counter()
    lTerminator=Counter()
    lBlackHole=Counter()
    lInvolvement =Counter()
    bet=Counter()
    lisPos=dict()
    alisPos=dict()
    lisInv=dict()
    lisOr=dict()
    lisTran=dict()
    lisTer=dict()
    lisBl=dict()
    all_nodes=set()
    position=dict()
    Position=dict()
    APosition=dict()
    lInvolvement=Counter()
    lTransmitter=Counter()
    lTerminator=Counter()
    lBlackHole=Counter()
    lOriginator=Counter()
    llength=[]


    # print ldicc,len(ldicc)
    # print aaaa
    # print traj
    # print 
    # print aaa
    # lldic=clear_traj(ldicc)
    for kk in ldicc:
        # if len(traj[kk[0]])==1:
        #     continue

        # print kk,kk[0],kk[0][0],kk[-1][0]
        lldic=clear_traj(kk)
        # print lldic,'PPPPPPPPPPPPPPPPPPPPPPPPPPPP'
        llength.append(len(lldic))
        bet=bEtweennes(lldic,bet)
        # print bet,'bbeett'
        # for kj,jv in bEtweennes(lldic):
            # print kj,jv
        #     bet[kj]+=jv
        fOriginator[lldic[0]]+=1
        if lldic[0] not in lisOr:
            lisOr[lldic[0]]=[len(lldic)]
        else:
            lisOr[lldic[0]].append(len(lldic))

        fTerminator[lldic[-1]]+=1
        if lldic[-1] not in lisTer:
            lisTer[lldic[-1]]=[len(lldic)]
        else:
            lisTer[lldic[-1]].append(len(lldic))

        if lldic[0]==lldic[-1]:
            fBlackHole[lldic[0]]+=1
            if lldic[0] not in lisBl:
                lisBl[lldic[0]]=[len(lldic[0])]
            else:
                lisBl[lldic[0]].append(len(lldic[0]))

        for k in range(1,len(lldic)-1):
            in_node=lldic[k]
            fTransmitter[lldic[k]]+=1
            if in_node not in lisTran:
                lisTran[in_node]=[len(lldic)]
            else:
                lisTran[in_node].append(len(lldic))


        linv=set()
        for i in lldic:
            linv.add(i)
        # print linv
        for i in linv:
            fInvolvement[i]+=1
            if i not in lisInv:
                lisInv[i]=[len(lldic)]
            else:
                lisInv[i].append(len(lldic))
        for j in range(len(lldic)):
            all_nodes.add(lldic[j])
            if lldic[j] not in lisPos:
                lisPos[lldic[j]]=[j+1]
            else:
                lisPos[lldic[j]].append(j+1)
            if len(lldic)-1==0:
                alili=0
            else:
                alili=(100.0*(j))/(len(lldic)-1)
            if lldic[j] not in alisPos:
                alisPos[lldic[j]]=[alili]
                
            else:
                alisPos[lldic[j]].append(alili)



        # print aaaa
#         fOriginator[kk[0][0]]+=1
#         fTerminator[kk[-1][0]]+=1
#         if kk[0][0]==kk[-1][0]:
#             fBlackHole+=1
#         # lisInv[]

#        print sorted(traj[kk[0]]),'aaa',kk,traj[kk[0]].keys()
#         lisInv.append(len(traj[kk[0]].keys()))
#         lisPos.append(sorted(traj[kk[0]]).index(kk[1])+1)
#        print sorted(traj[kk[0]]).index(kk[1]),len(traj[kk[0]])-1
#         alisPos.append(100.0*((sorted(traj[kk[0]]).index(kk[1])+1)-1)/(len(traj[kk[0]])-1))
#         if sorted(traj[kk[0]])[0]==kk[1]:
#             fOriginator+=1
#             lisOr.append(len(traj[kk[0]].keys()))

#         if sorted(traj[kk[0]])[-1]==kk[1]:
#             fTerminator+=1

#             lisTer.append(len(traj[kk[0]].keys()))

#         if sorted(traj[kk[0]])[0]==kk[1] and sorted(traj[kk[0]])[-1]==kk[1]:
#             fBlackHole+=1
#             lisBl.append(len(traj[kk[0]].keys()))
#         if sorted(traj[kk[0]])[0]!=kk[1] and sorted(traj[kk[0]])[-1]!=kk[1]:
#             fTransmitter+=1
#             lisTran.append(len(traj[kk[0]].keys()))
   # print lisPos
   # print lisOr
    for i in lisPos:

        Position[i]=meanstdv(lisPos[i])
    for i in alisPos:
        APosition[i]=meanstdv(alisPos[i])
    # print lisInv
    for i in lisInv:
        lInvolvement[i]=meanstdv(lisInv[i])
    for i in lisTran:
        lTransmitter[i]=meanstdv(lisTran[i])
    for i in lisTer:
        lTerminator[i]=meanstdv(lisTer[i])
    for i in lisBl:
        lBlackHole[i]=meanstdv(lisBl[i])
    for i in lisOr:
        lOriginator[i]=meanstdv(lisOr[i])
    return (all_nodes, fOriginator, fTransmitter,    fTerminator, fBlackHole,fInvolvement,lOriginator,lTransmitter,
    lTerminator,lBlackHole,lInvolvement,Position ,APosition,bet,llength)
def plot_transit_n(intervals,transit,tot_interv,ved_trans,npo,u_node,counter,write_to_file=False):

    bott=[]
    botti=[]
    wid=[]
    topp=[]
    lef=[]
    bot=0.
    top=.1
    # print type(tot_interv)
    if isinstance(tot_interv,pyinter.interval_set.IntervalSet):
        for i in tot_interv:
            mm=i
    else:
        mm=tot_interv
    # for i in tot_interv:
    #     mm=i
        # print i
    # print mm,type(mm),mm.lower_value,mm.upper_value
    # print dir(tot_interv)
    # print tot_interv.__sizeof
    # mm=tot_interv
    # print mm.lower_value,mm.upper_value
    pos=range(mm.lower_value,mm.upper_value+1)
    bot_di=dict()
    # print ved_trans,'ddddkdjdkjdkjdkdjdkjdkdjkdj'
    # print 
    # print ved_trans[u_node],'================================='
    # print ved_trans[u_node],']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]'
    for i in ved_trans[u_node]:
        # for k in ved_trans[i]:
        bot+=1

        for j in sorted(ved_trans[u_node][i]):
            # print i,j,bot,lef
            
            bott.append(bot)
            bot_di[i]=bot
            wid.append(j.upper_value-j.lower_value)
            topp.append(top)
            lef.append(j.lower_value)
            if bot not in botti:
                botti.append(bot)
# to plot     uncomment
    # fig=plt.figure(figsize=(10,10))
    subslines=len(intervals)
    if subslines%3 !=0:
        subb=subslines/3 +1
    else:
        subb=subslines/3    
    plt.subplot(subb,3,counter)
    plt.barh(bott,wid,topp,lef)
    # pos=range(minn,maxx+1)

    plt.xticks(pos)
    ylabes=[]
    for i in ved_trans[u_node]:
        # print i,'mmmmlllleeee'
        # for j in ved_trans[u_node][i]:
        # li=list(i)
        # print li
        ylabes.append('(%s,%s)' %(i[0],i[1]))
    # ylabes=ved_trans.keys()#['(u,v)','(u,w)','(u,z)']#,'(v,w)','(z,w)']
    # print bott
    plt.yticks(botti,ylabes)
    # plt.title('Transitions of node %s' %u_node)
    plt.ylim(0,bot+.5)
    xl=[]
    yl=[]
    for i in sorted(npo):
        xl=[i,i]
        yl=[0,bot+.5]
        plt.plot(xl,yl,'k--')
    bobo=dict()
    done=[]
    # F=nx.DiGraph()
    # print bot_di,'bot_di'
    counn=0
    for i in transit:
        # print transit

        if i[5]==u_node :
            # print i,'uuuuuuuuuuppppppppppppppppppppppppp',outfile_name,i[5],'hhhse',u_node,i[5]==u_node
            if i[1] not in bot_di or i[2] not in bot_di:
                continue
            if i[0] in bobo:
                bobo[i[0]]+=.1
            else:
                bobo[i[0]]=i[0]

            if (i[0],bot_di[i[1]],bot_di[i[2]]-bot_di[i[1]]) not in done:
            # print i,bot_di
                mp.arrow(bobo[i[0]],bot_di[i[1]],0,bot_di[i[2]]-bot_di[i[1]],shape='full',color='r',width=0.05,length_includes_head=True,head_width=0.3,head_length=.4)
                done.append((i[0],bot_di[i[1]],bot_di[i[2]]-bot_di[i[1]]))
                counn+=1
    plt.title('%i Transitions of node %s' %(counn,u_node))
    # if write_to_file:
    #     plt.savefig(outfile_name, bbox_inches='tight')
    # else:
    #     continue
        # plt.show()
    # plt.show()
    return bot_di#,outfile_name

def plot_transit(intervals,transit,tot_interv,ved_trans,npo,u_node,counter,write_to_file=False):

    filedir='S_out_figs'
    try:
        os.stat(filedir)
    except:
        os.mkdir(filedir)
    filf='%s_trans.png' %u_node
    outfile_name = os.path.join('%s' % filedir,filf)
    # print tot_interv

    bott=[]
    botti=[]
    wid=[]
    topp=[]
    lef=[]
    bot=0.
    top=.1
    # print type(tot_interv)
    if isinstance(tot_interv,pyinter.interval_set.IntervalSet):
        for i in tot_interv:
            mm=i
    else:
        mm=tot_interv
    # for i in tot_interv:
    #     mm=i
        # print i
    # print mm,type(mm),mm.lower_value,mm.upper_value
    # print dir(tot_interv)
    # print tot_interv.__sizeof
    # mm=tot_interv
    pos=range(mm.lower_value,mm.upper_value+1)
    bot_di=dict()
    # print ved_trans,'ddddkdjdkjdkjdkdjdkjdkdjkdj'
    # print 
    # print ved_trans[u_node],'================================='
    # print ved_trans[u_node],']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]'
    for i in ved_trans[u_node]:
        # for k in ved_trans[i]:
        bot+=1

        for j in sorted(ved_trans[u_node][i]):
            # print i,j,bot,lef
            
            bott.append(bot)
            bot_di[i]=bot
            wid.append(j.upper_value-j.lower_value)
            topp.append(top)
            lef.append(j.lower_value)
            if bot not in botti:
                botti.append(bot)
# to plot     uncomment
    fig=plt.figure(figsize=(10,10))
    # plt.subplot(len(intervals)/2,2,counter)
    plt.barh(bott,wid,topp,lef)
    # pos=range(minn,maxx+1)

    plt.xticks(pos)
    ylabes=[]
    for i in ved_trans[u_node]:
        # print i,'mmmmlllleeee'
        # for j in ved_trans[u_node][i]:
        # li=list(i)
        # print li
        ylabes.append('(%s,%s)' %(i[0],i[1]))
    # ylabes=ved_trans#['(u,v)','(u,w)','(u,z)']#,'(v,w)','(z,w)']
    # print bott
    plt.yticks(botti,ylabes)
    plt.title('Transitions of %s' %u_node)
    plt.ylim(0,bot+.5)
    xl=[]
    yl=[]
    for i in sorted(npo):
        xl=[i,i]
        yl=[0,bot+.5]
        plt.plot(xl,yl,'k--')
    bobo=dict()
    done=[]
    # F=nx.DiGraph()
    # print bot_di,'bot_di'
    for i in transit:
        

        if i[5]==u_node :
            # print i,'uuuuuuuuuuppppppppppppppppppppppppp',outfile_name,i[5],'hhhse',u_node,i[5]==u_node
            if i[1] not in bot_di or i[2] not in bot_di:
                continue
            if i[0] in bobo:
                bobo[i[0]]+=.1
            else:
                bobo[i[0]]=i[0]

            if (i[0],bot_di[i[1]],bot_di[i[2]]-bot_di[i[1]]) not in done:
            # print i,bot_di
                mp.arrow(bobo[i[0]],bot_di[i[1]],0,bot_di[i[2]]-bot_di[i[1]],shape='full',color='r',width=0.05,length_includes_head=True,head_width=0.3,head_length=.4)
                done.append((i[0],bot_di[i[1]],bot_di[i[2]]-bot_di[i[1]]))
    if write_to_file:
        plt.savefig(outfile_name, bbox_inches='tight')
    # else:
    #     continue
        # plt.show()
    # plt.show()
    return bot_di,outfile_name
def plot_transit_timeline(intervals,transit,tot_interv, ved_trans,npo,ndls,write_to_file=False,plot_first_mode=True):
    filedir='S_out_figs'
    try:
        os.stat(filedir)
    except:
        os.mkdir(filedir)
    filf='Activity_timeline.png' 
    outfile_name = os.path.join('%s' % filedir,filf)
    # print tot_interv

    bott=[]
    botti=[]
    wid=[]
    topp=[]
    lef=[]
    bot=0.
    top=.1
    # for i in tot_interv:
    #     mm=i
        # print i
    # print mm
    # print dir(tot_interv)
    # print tot_interv.__sizeof
    if isinstance(tot_interv,pyinter.interval_set.IntervalSet):
        for i in tot_interv:
            mm=i
    else:
        mm=tot_interv
    pos=range(mm.lower_value,mm.upper_value+1)
    bot_di=dict()
    # print ved_trans,'ddddkdjdkjdkjdkdjdkjdkdjkdj'
    # print 
    # print ved_trans[u_node],'================================='
    # print ved_trans[u_node],']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]'
    done=[]
    for u_node in ndls:
        for i in ved_trans[u_node]:
            # for k in ved_trans[i]:
            if sorted(i) not in done:
                done.append(sorted(i))
                bot+=1

                for j in sorted(ved_trans[u_node][i]):
                
                    bott.append(bot)
                    bot_di[i]=bot
                    wid.append(j.upper_value-j.lower_value)
                    topp.append(top)
                    lef.append(j.lower_value)
                    if bot not in botti:
                        botti.append(bot)
            
    # plt.figure(figsize=(20,20))
    plt.barh(bott,wid,topp,lef)
    # pos=range(minn,maxx+1)

    plt.xticks(pos)
    ylabes=[]
    done=[]
    for u_node in ndls:
        for i in ved_trans[u_node]:
            if sorted(i) not in done:
                done.append(sorted(i))
                # print i,'mmmmlllleeeerrrrrrrrrrrrrrrrr'
                # for j in ved_trans[u_node][i]:
                # li=list(i)
                # print li
                ylabes.append('(%s,%s)' %(i[0],i[1]))
    # ylabes=ved_trans.keys()#['(u,v)','(u,w)','(u,z)']#,'(v,w)','(z,w)']
    # print bott
    plt.yticks(botti,ylabes)
    plt.title('Activity Timeline Diagram',{'size': '20'})
    plt.ylim(0,bot+.5)
    xl=[]
    yl=[]
    for i in sorted(npo):
        xl=[i,i]
        yl=[0,bot+.5]
        plt.plot(xl,yl,'k--')
    bobo=dict()
    done=[]
    # F=nx.DiGraph()
    # print bot_di,'bot_di'
    # for i in transit:
        

    #     if i[5]==u_node :
    #         print i,'uuuuuuuuuuppppppppppppppppppppppppp',outfile_name,i[5],'hhhse',u_node,i[5]==u_node
    # #         if i[1] not in bot_di.keys() or i[2] not in bot_di.keys():
    #             continue
    #         if i[0] in bobo:
    #             bobo[i[0]]+=.1
    #         else:
    #             bobo[i[0]]=i[0]

    #         if (i[0],bot_di[i[1]],bot_di[i[2]]-bot_di[i[1]]) not in done:
            # print i,bot_di
    #             mp.arrow(bobo[i[0]],bot_di[i[1]],0,bot_di[i[2]]-bot_di[i[1]],shape='full',color='r',width=0.05,length_includes_head=True,head_width=0.3,head_length=.4)
    #             done.append((i[0],bot_di[i[1]],bot_di[i[2]]-bot_di[i[1]]))
    if write_to_file:
        plt.savefig(outfile_name, bbox_inches='tight')
    elif plot_first_mode :
        plt.show()
        # continue
    # else:
    # #     continue
    #     plt.show()
    return bot_di,outfile_name
def create_points(intervals):
    points=dict()
    transit=dict()
    for i in intervals:
        points[i]=set()
        # transit[i]=dict()
        for j in intervals[i]:

            if isinstance(intervals[i][j],pyinter.interval.Interval):
                points[i].add(intervals[i][j].lower_value)
                points[i].add(intervals[i][j].upper_value)

            else:
                for k in intervals[i][j]:
                    points[i].add(k.lower_value)
                    points[i].add(k.upper_value)
        npo=set()
        for i in points:
            inters=intervals[i]
            help_inter=dict()
            npo=npo.union(points[i])
            for j in sorted(list(points[i])):

                
                help_inter[j]=dict()
                for k in inters:
                    # print i,j,k,inters[k]
                    if isinstance(inters[k],pyinter.interval.Interval):
                        if j in inters[k]:
                            help_inter[j][k]=inters[k]
                    else:
                        for kk in inters[k]:
                            # print i,j,k,kk,'aaaaa',j in kk
                            if j in kk:
                                help_inter[j][k]=kk
                        # print   help_inter,'==========================='
            transit[i]=help_inter
    return npo,transit,points
def create_transitions(transit):
    transitions=set()
    for i in transit:
        for j in transit[i]:
            # print i,j,transit[i][j],'aaaaaaaaaaaaaaaaaaaa'
            if len(transit[i][j].keys())>=2:
                tranpoint=transit[i][j]
                for ii in it.permutations(tranpoint.keys(),2):
                    ia=ii[0]
                    ib=ii[1]
                    ma=tranpoint[ia]
                    mb=tranpoint[ib]
                    if j ==ma.lower_value and j!=mb.lower_value:
                        transitions.add((j,ib,ia,ma,mb,i))
                    elif j ==ma.upper_value and j!=mb.upper_value :
                        transitions.add((j,ia,ib,ma,mb,i))  
    return transitions   
def create_paths(points):
    path_dic=dict()
    mma=0
    mmi=1000000000000
    for i in points:
        # print i,points
        ma=max(points[i])
        mi=min(points[i])
        path_dic[i]=(i+ '__'+str(mi),i+ '__'+str(ma),mi,ma)
        if ma>mma:
            mma=ma
        if mi < mmi:
            mmi=mi          
    return path_dic,mma,mmi
def create_edge_nedge_tran(intervals,points):#,u_node):
    ved_trans=dict()
    orizd_trans=dict()
    for i in intervals:
        # if i=='u':
        #     continue
        # print intervals[i],'=====================',i,intervals.keys()
        ved_trans[i]=dict()
        orizd_trans[i]=dict()
        for j in intervals[i]:
            # print j,'neeee'
            if j not in ved_trans[i]:
                ved_trans[i][j]=set()
            if j not in orizd_trans[i].keys():
                orizd_trans[i][j]=set()
            # print i,'i',j,'j',intervals[i][j]
            # if j[2]==i:
            #     ii=j[7]
            #     jj=j[2]
            # else:
            #     ii=j[2]
            #     jj=j[7]
            if j[0]==i:
                ii=j[1]
                jj=j[0]
            else:
                ii=j[0]
                jj=j[1]
            # print ii,jj
            if  isinstance(intervals[i][j],pyinter.interval.Interval):
                ini=intervals[i][j]
                ved_trans[i][j].add(ini)
                for kkj  in range(0,len(points[jj])):
                    # print kkj,sorted(points),'ddddddddddddddddddddddddddddddddddddddddddd'
                        # print kkj,len(points[i])
                    if kkj<len(points[i])-1: 
                        kk=sorted(points[jj])[kkj]
                        kn=sorted(points[jj])[kkj+1]
                        # print kk,kn
                        if kk !=ini.upper_value and kn in ini and kk in ini:
                            orizd_trans[i][j].add((ii+ '__'+ str(kk),ii+ '__'+str(kn)))
                    # print orizd_trans[i],'kkkkk'
            else:
                for ini in intervals[i][j]:
                    ved_trans[i][j].add(ini)
                    # print sorted(points[i])
                    for kkj  in range(0,len(points[jj])):
                        # print kkj,sorted(points[jj]),'djjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj'
                        # print kkj,sorted(points[i])[kkj]
                        # print kkj,len(points[i])
                        if kkj<len(points[jj])-1: 
                            kk=sorted(points[jj])[kkj]
                            kn=sorted(points[jj])[kkj+1]
                            # print kk,kn
                            # if kk==0 and kn==4:
                                # print ini,j,ii,'===================================================',kk,kn
                            if kk !=ini.upper_value and kn in ini and kk in ini :
                                    orizd_trans[i][j].add((ii+ '__'+str(kk),ii+ '__'+str(kn)))
    return ved_trans,orizd_trans

def create_start_end_path(jed_trans,ned_transj,path_dic,mma,mmi,u_node):
    start_pa=[]
    end_pa=[]
    # print path_dic,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
    # print aaa
    # for i in path_dic:

    # if i=='u':
    #     continue
    # print path_dic,'papa'
    # print mma,mmi
    # print u_node
    # print jed_trans,'uuuuuuuuuuu'
    # for i in jed_trans:

    # mina=path_dic[u_node][2]
    # maxa=path_dic[u_node][3]
    # print mina,maxa,'mmmmmm'
    udat=None
    for jj in jed_trans:
        for ii in jed_trans[jj]:
            # print ii,'<------------',type(ii)
            try:
                if udat==None:
                    udat=ii
            except:

                if isinstance(udat,pyinter.interval.Interval):
                    udat=udat.union(ii)
                else:
                    udat.add(ii)
            # print udat,dir(udat)
    # print udat,len(udat)
    # print type(udat)
    start_s=[]
    end_s=[]
    if isinstance(udat,pyinter.interval_set.IntervalSet):
        for i in udat:
            start_s.append(i.lower_value)
            end_s.append(i.upper_value)
    else:
        start_s.append(udat.lower_value)
        end_s.append(udat.upper_value)
    # print start_s,end_s,'======' 

    for j in jed_trans:
        if j[0]==u_node:
            nno=j[1]
        else:
            nno=j[0]
        jjed=jed_trans[j]
        # print jjed,type(jjed)
        if isinstance(jjed,pyinter.interval.Interval):
            # print 'ppppppp',jjed,jjed.lower_value,jjed.upper_value
            if jjed.lower_value in start_s:
                start_pa.append((u_node,nno+ '__'+str(jjed.lower_value)))
            if jjed.upper_value in end_s:
                end_pa.append((u_node,nno+ '__'+str(jjed.upper_value)))
        else:

        # if isinstance(jjed,pyinter.interval_set.IntervalSet):
            for jj in jjed:
                # print 'oooo',jj,jj.lower_value,jj.upper_value
                if jj.lower_value in start_s:
                    start_pa.append((u_node,nno+ '__'+str(jj.lower_value)))
                if jj.upper_value in end_s:
                    end_pa.append((u_node,nno+ '__'+str(jj.upper_value)))
        # print start_pa,end_pa,j,jjed,'+++++++++++++'
        # else:
        #     if jjed.lower_value in start_s:
        #         start_pa.append((u_node,nno+ '__'+str(jjed.lower_value)))
        #     elif jjed.upper_value in end_pa:
        #         end_pa.append((u_node,nno+ '__'+str(jjed.upper_value)))

            # if 

        # if 
    #     start_pa.append((u_node,nno+ '__'+str(udat.lower_value)))
    #     end_pa.append((u_node,nno+ '__'+str(udat.upper_value)))
    # else:
    #     for i in udat:
    #         start_pa.append((u_node,nno+ '__'+str(udat.lower_value)))
    # #         end_pa.append((u_node,nno+ '__'+str(udat.upper_value)))
    # print start_pa,end_pa
    # print aaaa
    # for j in jed_trans:

    #     if j[0]==u_node:
    #         nno=j[1]
    #     else:
    #         nno=j[0]
    #     if isinstance(jed_trans[j],pyinter.interval.Interval):
    #         start_pa.append((u_node,nno+ '__'+str(jed_trans[j].lower_value)))
    #         end_pa.append((u_node,nno+ '__'+str(jed_trans[j].upper_value)))
    #     else:
    #         for i in jed_trans[j]:
    #             start_pa.append((u_node,nno+ '__'+str(i.lower_value)))
    #             end_pa.append((u_node,nno+ '__'+str(i.upper_value)))
        # mina=path_dic[nno][2]
        # maxa=path_dic[nno][3]
        # minU_node=path_dic[u_node][2]
        # maxU_node=path_dic[u_node][3]
        # if minU_node> mina:
        #     mina=minU_node
        # if maxU_node<maxa:
        #     maxa=maxU_node
        
        # start_pa.append((u_node,nno+str(mina)))
        # end_pa.append((u_node,nno+str(maxa)))

    # for i in path_dic:
        # print i,path_dic[i],'path'
    #     if i==u_node:
    #         continue
    #     if path_dic[i][2]==mmi :
    #         start_pa.append((i,path_dic[i][0]))
    #     if path_dic[i][3]== mma:
    #         end_pa.append((i,path_dic[i][1]))
    
    return start_pa, end_pa
def create_start_end_path_davis(jed_trans,ned_transj,path_dic,mma,mmi,u_node):
    start_pa=[('aa','ddd__500000')]
    end_pa=[('aa','ddd__0')]
    # print path_dic,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
    # print aaa
    # for i in path_dic:

    # if i=='u':
    #     continue
    # print path_dic,'papa'
    # print mma,mmi
    # print u_node
    # print jed_trans,'uuuuuuuuuuu'
    # for i in jed_trans:

    # mina=path_dic[u_node][2]
    # maxa=path_dic[u_node][3]
    # print mina,maxa,'mmmmmm'

    for j in jed_trans:

        if j[0]==u_node:
            nno=j[1]
        else:
            nno=j[0]
        if isinstance(jed_trans[j],pyinter.interval.Interval):

            if jed_trans[j].lower_value<int(start_pa[0][1].split('__')[1]):
                start_pa=[(u_node,nno+ '__'+str(jed_trans[j].lower_value))]
            if jed_trans[j].upper_value>int(end_pa[0][1].split('__')[1]):
                end_pa=[(u_node,nno+ '__'+str(jed_trans[j].upper_value))]
        else:
            for i in jed_trans[j]:
                # print i.lower_value,type(i.lower_value),start_pa[0][1].split('__')[1]
                if i.lower_value<int(start_pa[0][1].split('__')[1]):
                    start_pa=[(u_node,nno+ '__'+str(i.lower_value))]
                if i.upper_value>int(end_pa[0][1].split('__')[1]):
                    end_pa=[(u_node,nno+ '__'+str(i.upper_value))]
        # mina=path_dic[nno][2]
        # maxa=path_dic[nno][3]
        # minU_node=path_dic[u_node][2]
        # maxU_node=path_dic[u_node][3]
        # if minU_node> mina:
        #     mina=minU_node
        # if maxU_node<maxa:
        #     maxa=maxU_node
        
        # start_pa[0].append((u_node,nno+str(mina)))
        # end_pa.append((u_node,nno+str(maxa)))

    # for i in path_dic:
        # print i,path_dic[i],'path'
    #     if i==u_node:
    #         continue
    #     if path_dic[i][2]==mmi :
    #         start_pa.append((i,path_dic[i][0]))
    #     if path_dic[i][3]== mma:
    #         end_pa.append((i,path_dic[i][1]))
    
    return start_pa, end_pa
def create_graph_trans(ned_transj,transitions,u_node):
    F=nx.DiGraph() 
    donel=[]  
    # print
    # print ned_transj,'ddddddddddddddddddddd'
    # print 
    # print ned_transj[u_node],'aaaaaaaaaaaaaaaaaaaaaaaaaaa'
    # print aaaaaa
    # print ned_transj,'nej'
    # print ned_transj[u_node]
    for i in ned_transj:
        for j in ned_transj[i]:
            # print j
            F.add_edge(j[0],j[1])
    # print F.nodes()
    # print '======================================================'


    for i in sorted(transitions):
        # print i,'++++++++++++++++++++++++++++++++++++++++++'
        if (i[0],i[1],i[2]) not in donel:
            donel.append((i[0],i[1],i[2]))
            # nna=list(i[1])
            # nnda=nna[2]
            # nndb=nna[7]
            nnda=i[1][0]
            nndb=i[1][1]
            if nnda==u_node or nndb==u_node:

                if nnda==i[5] and nndb!=i[5]:
                    nda=nndb
                elif nndb==i[5] and nnda!=i[5]:
                    nda=nnda
                # else:
                    # print '============================',i,nndb,nnda
            else:
                continue
            # nnb=list(i[2])
            # nnda=nnb[2]
            # nndb=nnb[7]

            nnda=i[2][0]
            nndb=i[2][1]
            if nnda==u_node or nndb==u_node:
                if nnda==i[5] and nndb!=i[5]:
                    ndb=nndb
                elif nndb==i[5] and nnda!=i[5]:
                    ndb=nnda
                # else:
                    # print '***********************',i,nndb,nnda
            else:
                continue
            # nono=i[0]+1
            # F.add_edge(nda+ '__'+str(nono),ndb+ '__'+str(nono))
            F.add_edge(nda+ '__'+str(i[0]),ndb+ '__'+str(i[0]))

            # print nda+str(i[0]),ndb+str(i[0]),'ppppppppppppppppppppppppp'
    return F#,start_pa,end_pa
# def create_trans_graphtool(nw,ff,u_node,uu,namv=dict()):
#     for kk in traj_list:
#         lldic,cldic=clear_traj_d(kk)
#         if len(cldic)>1:
#             for kj in lldic:
#                 jj=lldic[kj][0]
#                 ll=lldic[kj][1]
                # print kk,jj,ll
#                 if jj not in nam_v.keys():
#                     nam_v[jj]=uu
#                     uu+=1
#                     if colors:
#                         if jj=='v':
#                             vcolor='green'
#                         elif jj=='w':
#                             vcolor='cyan' 
#                         elif jj=='z':
#                             vcolor='#FFD700'
#                         elif jj =='u':
#                             vcolor='#B22222'
#                     F.add_vertex()
#                     vprop_label[F.vertex(uu)] = jj
#             # for kj in ldicc:
#             for kjj in range(len(kk)-1):
#                 kj = kk[kjj]
#                 jk = kk[kjj+1]
                # print lldic[kj][0],lldic[jk][0],'lllll',nam_v

#                 if lldic[kj][0]!=lldic[jk][0]:
#                     # continue
                # print kjj , kj,jk,'dddd',nam_v
                # print nam_v[lldic[kj][0]],nam_v[lldic[jk][0]],'lllll'
                    # print lldic[kj][0],lldic[jk][0],'llllldfasdfasdfa'
#                     # if u_node=='u':
#                     #     ecolor='#FF00FF'
#                     # elif u_node == 'v':
#                     #     ecolor='#7FFF00'
#                     # elif u_node== 'w':
#                     #     ecolor='#6495ED'
#                     # elif u_node=='z':
#                     #     ecolor='#DAA520'
#                     try:
#                         edg=F.es.find(_source_eq=nam_v[lldic[kj][0]],_target_eq=nam_v[lldic[jk][0]])
#                         edg['ed_label'].add(u_node+str(lldic[kj][1]))
#                     except Exception,e:
                        # print e
#                         momo=set()
#                         momo.add(u_node+str(lldic[kj][1]))
#                         F.add_edge(nam_v[lldic[kj][0]],nam_v[lldic[jk][0]],ed_label=momo)#,ecolor=ecolor)
    # print F
    # print '5555555555555555555555555555555555555555555555555555555555'
#     return F,nam,uu
def create_tex(outfile_name,Ff):
    # print outfile_name
    lat=r'''\documentclass{beamer}

%\usepackage{amsmath}
%\usepackage{amsfonts,amssymb,wasysym}

\usepackage{tikz}
\usepackage{pgf}
\usetikzlibrary{arrows,shapes,trees,topaths}
%\usetikzlibrary{automata,positioning}
%\usetikzlibrary[automata]
%\usepackage{verbatim}
%\usepackage{varwidth}
%\usepackage{pgfplots, pgfplotstable}



\begin{document}


\begin{frame}

\begin{figure}[h!]
\centering
\begin{tikzpicture}[->, >=stealth, shorten >=1pt,auto,node distance=7 cm, semithick, scale = 1.1,transform shape]'''.decode('utf-8')


    fop=open(outfile_name,'w')
    fop.write(lat)
    fop.write('\n')
    # g=ig.Graph.Full(len(Ff.vs))
    lay=Ff.layout_circle()
    # for vv in Ff.vs:
    Ff.vs['layout']=lay

    for vv in Ff.vs:
        nam=vv['name']
        la=vv['layout']

        lattv=r'\node[draw,shape=circle,line width=1pt]'+ ' (%s) at (%s,%s) {$%s$};\n' %(nam,(la[0]+1)*2.5,(la[1]+1)*1.5,nam)
        # print j
        fop.write(lattv)

        # print (j[0]+1)*5,(j[1]+1)*3.5
    ed_dici=dict()
    for ee in Ff.es:

        # print ee
        aa= Ff.vs[ee.source]['name']
        bb= Ff.vs[ee.target]['name']
        lab=ee['ed_label']
        if (aa,bb) not in ed_dici:
            ed_dici[(aa,bb)]=set()
            ed_dici[(aa,bb)].add(lab)
        else:
            ed_dici[(aa,bb)].add(lab)
    for ab in ed_dici:
        lab=''
        for ll in ed_dici[ab]:
            if len(ll[1:])>1:
                lab+=ll[0]+'_{'+ll[1:]+'}, '
            else:
                lab+=ll[0]+'_'+ll[1:]+', '
        lab=lab[:-2]
        # print lab,ab[0],ab[1]
        late=r'\path'+' (%s) edge [bend right,line width=1pt] node [pos=0.5,sloped,below] {' %ab[0]
        late+=r'\tiny'+'{$%s$}} (%s);\n' %(lab,ab[1])
        fop.write(late)
    fop.write(r'''\end{tikzpicture}
\end{figure}

\end{frame}

\end{document}'''.decode('utf-8'))
    fop.close()


def creatTestGraph():
    ndls=[]
    Gg=nx.davis_southern_women_graph()
    G=nx.MultiGraph()
    for n in Gg.nodes(data=True):
        if n[1]['bipartite']==0:
               # print n,'dir'
            ndls.append(n[0])
            # G.add_node(n[0],attribute='director')
        # else:

               # print n,'com'
    #         G.add_node(n[0],attribute='company')
    # print aaaaa
    elist=['E12','E11','E10','E9','E8','E7','E6','E5','E4','E3','E2','E1']
    for ed in Gg.edges(data=True):
        ee=ed[0]
        dd=ed[1]
        # print ed[0]
        if ee in elist:
            ee=ed[1]
            dd=ed[0]
        ##    if G.node[dd]['attribute']=='company':
        ##        ee=ed[1]
        ##        dd=ed[0]
        if dd=='E1' or ee=='E1':
            G.add_edge(ee,dd,date_start=2000,date_end=2001)
        elif dd=='E2' or ee=='E2':
            G.add_edge(ee,dd,date_start=2001,date_end=2002)
        elif dd=='E3' or ee=='E3':
            G.add_edge(ee,dd,date_start=2002,date_end=2003)
        elif dd=='E4' or ee=='E4':
            G.add_edge(ee,dd,date_start=2003,date_end=2004)
        elif dd=='E5' or ee=='E5':
            G.add_edge(ee,dd,date_start=2004,date_end=2005)
        elif dd=='E6' or ee=='E6':
            G.add_edge(ee,dd,date_start=2005,date_end=2006)
        elif dd=='E7' or ee=='E7':
            G.add_edge(ee,dd,date_start=2006,date_end=2007)
        elif dd=='E8' or ee=='E8':
            G.add_edge(ee,dd,date_start=2007,date_end=2008)
        elif dd=='E9' or ee=='E9':
            G.add_edge(ee,dd,date_start=2008,date_end=2009)
        elif dd=='E10' or ee=='E10':
            G.add_edge(ee,dd,date_start=2009,date_end=2010)
        elif dd=='E11' or ee=='E11':
            G.add_edge(ee,dd,date_start=2010,date_end=2011)
        elif dd=='E12' or ee=='E12':
            G.add_edge(ee,dd,date_start=2011,date_end=2012)
        elif dd=='E13' or ee=='E13':
            G.add_edge(ee,dd,date_start=2012,date_end=2013)
        elif dd=='E14' or ee=='E14':
            G.add_edge(ee,dd,date_start=2013,date_end=2014)
    return G,ndls

##for edd in G.edges(data=True):
   # print edd
# G,ndls=creatTestGraph()
def create_graph_number1(time_to_add=0):
    
    davisw=False#True
    # print ndls
    # print aaa
    # uv=[(0,4),(6,8),(10,12)]
    # uw=[(2,4),(6,10)]
    # uz=[(3,12)]
    # vw=[(2,7),(10,12)]
    # wz=[(0,3),(7,11)]
    uv=[(0,3),(4,6),(7,9)]
    uw=[(1,3),(4,7)]
    uz=[(2,9)]
    vw=[(1,5),(7,9)]
    wz=[(0,2),(5,8)]
    G=nx.MultiGraph()
    for i in uv:
        G.add_edge('u','v',date_start=i[0],date_end=i[1])
    for i in uw:
        G.add_edge('u','w',date_start=i[0],date_end=i[1])
    for i in uz:
        G.add_edge('u','z',date_start=i[0],date_end=i[1])
    for i in vw:
        G.add_edge('v','w',date_start=i[0],date_end=i[1])
    for i in wz:
        G.add_edge('w','z',date_start=i[0],date_end=i[1])
    ndls=['u','v','w','z']
    return G,ndls,time_to_add,davisw
def create_synthetic3lgB(k,n,m,pp,timetoadd=0):    
    import syntheticThreeLayerGraph_time as s3l
    # k=5
    # n=10
    # pp=[0.21,.31,.21,.31,.4]
    # G, list_of_Graphs_final, Gagr, edgeList,nmap,mapping =s3l.synthetic_multi_level(k,n,p=pp,No_isolates=True)
    G, list_of_Graphs_final, Gagr, edgeList,nmap,mapping =s3l.synthetic_multi_bipartite(k,n,m,p=pp)
    pos,fig1=s3l.plot_graph_k_nm(k,n,m,G,list_of_Graphs_final, Gagr,1,colors_grey='bipartite', nodesize=50,withlabels=True,edgelist=edgeList,layout=True,b_alpha=0.5)
    # pos,fig2=s3l.plot_graph_k_nm(k,n,m,G,list_of_Graphs_final, Gagr,2,colors_grey='bipartite', nodesize=50,withlabels=True,edgelist=edgeList,layout=True,b_alpha=0.5)
    dic_of_edges,dict_of_edges_time=s3l.make_dict_of_edge_timesB(k,nmap,mapping,list_of_Graphs_final)
    Gg=nx.MultiGraph()
    # print dic_of_edges
    # print aaa
    ppld=0
    for i in dic_of_edges.values():
        for ii in i:
            ppld+=1
    print 'Total number of edges: %i' %ppld#len(dic_of_edges.keys())
    for i in sorted(dict_of_edges_time.keys()):
        print 'Number of edges in time interval %s: %i' %(str(i),dict_of_edges_time[i])

    for i,v in dic_of_edges.items():
        # print i,v
        # print 'Number of edges during time interval %i : %i' %(i[0],len(v))
        # print i,v
        for jj in v:
            # print jj
            Gg.add_edge(str(i[0]),str(i[1]),date_start=jj[0],date_end=jj[1])
    # print nx.is_bipartite(Gg)
    ndlss=bip.sets(Gg)
    ndls=[list(i) for i in ndlss]
    # print ndls
    # ndls=Gg.nodes()
    # print aaaaa
    return Gg,ndls,timetoadd,fig1
def create_synthetic3lg(k,n,pp,timetoadd=0):    
    import syntheticThreeLayerGraph_time as s3l
    # k=5
    # n=10 
    # pp=[0.21,.31,.21,.31,.4]
    G, list_of_Graphs_final, Gagr, edgeList,nmap,mapping =s3l.synthetic_multi_level(k,n,p=pp,No_isolates=True)
    # print edgeList
    pos,figi=s3l.plot_graph_k_n(k,n,G,list_of_Graphs_final, Gagr,nodesize=50,withlabels=False,edgelist=edgeList,layout=True,b_alpha=1)
    # G, list_of_Graphs_final, Gagr, edgeList,nmap,mapping =s3l.synthetic_multi_bipartite(k,n,m,p=pp)
    dic_of_edges,dict_of_edges_time=s3l.make_dict_of_edge_times(k,nmap,mapping,list_of_Graphs_final)
    # print dic_of_edges
    # print aaa
    ppld=0
    for i in dic_of_edges.values():
        for ii in i:
            ppld+=1
    # print dict_of_edges_time
    # print dic_of_edges
    # print aaa
    Gg=nx.MultiGraph()
    print 'Total number of edges: %i' %ppld#len(dic_of_edges.keys())
    for i in sorted(dict_of_edges_time.keys()):
        print 'Number of edges for the time interval %s: %i' %(str(i),dict_of_edges_time[i])
    for i,v in dic_of_edges.items():
        # print i,v
        # print 'Number of edges during time interval %i : %i' %(i[0],len(v))
        # print i,v
        for jj in v:
            # print jj
            Gg.add_edge(str(i[0]),str(i[1]),date_start=jj[0],date_end=jj[1])

    ndls=Gg.nodes()
    return Gg,ndls,timetoadd,figi
def creatTestGraph_pandas(start,end,characters,character,quak=600):
    import datetime
    
    # G=nx.davis_southern_women_graph()
    G=nx.Graph()
    for i,v in enumerate(characters):
        # ide=v.index(character)
        for nc in v:

            if nc!=character:
                dats=datetime.datetime.fromtimestamp(start[i]*quak)
                dae=datetime.datetime.fromtimestamp(end[i]*quak)
                G.add_edge(nc,character,date_start=dats.strftime('%d-%m-%y'),date_end=dae.strftime('%d-%m-%y'))

                G.add_node(nc,attribute='director')
    G.add_node(character,attribute='company')
    # ndlss=bip.sets(Gg)
    # ndls=[list(i) for i in ndlss]
    return G#,ndls
def creatTestGraph_pandas_bip(start,end,characters,character,pols,subj,quak=600):
    import datetime
    pold={}
    subjd={}
    # G=nx.davis_southern_women_graph()
    G=nx.MultiGraph()
    for i,v in enumerate(characters):
        # ide=v.index(character)
        for nc in v:
            pold[nc+'__'+str(start[i])]=pols[i]
            pold[nc+'__'+str(end[i])]=pols[i]
            subjd[nc+'__'+str(start[i])]=subj[i]

            subjd[nc+'__'+str(end[i])]=subj[i]
            if nc!=character:
                # dats=datetime.datetime.fromtimestamp(start[i]*quak)
                # dae=datetime.datetime.fromtimestamp(end[i]*quak)
                # G.add_edge(nc,character,date_start=dats.strftime('%d-%m-%y'),date_end=dae.strftime('%d-%m-%y'))
                # 
                G.add_edge(nc,character,date_start=int(start[i]),date_end=int(end[i]))
                G.add_node(nc,attribute='director',bipartite=0)
    G.add_node(character,attribute='company',bipartite=1)
    ndlss=bip.sets(G)
    ndls=[list(i) for i in ndlss]
    return G,ndls,pold,subjd
def main_work(G,ndll,timetoadd,figi,davisw=False,verb=False,plot_first_mode=True):
    pdfs={}
    if isinstance(ndll[0],list):

        fig_u=1
        for ndls in ndll:
            # print ndls,'aaaaaaaaaaaaaaaa'
            intervals,tot_interval=create_interv(G,nodelist=ndls,time_to_add=timetoadd)
            if verb:
                print ndls,'done intervals'

            #     for jj in v:
            #         print i,v,jj
            #         # print jj

            #         Gg.add_edge(str(i[0]),str(i[1]),date_start=jj[0],date_end=jj[1])
            # ndls=Gg.nodes()
            # print Gg.edges(data=True)

            # intervals,tot_interval=create_interv(Gg,nodelist=ndls,time_to_add=time_to_add)


            # for i in intervals:
            #     # print i,' ',intervals[i]
            # print tot_interval,'--------'
            # print aaaa

            npo,transit,points=create_points(intervals)
            if verb:
                print ndls,'done transits'
            # print points
            # for i in points:
            #     print i,points[i]
            # for i in transit:
            #     print i,transit[i]
            #     print 
            # print transit
            # print npo
            # print aaa
            transitions=create_transitions(transit)
            if verb:
                print ndls,'done transitions'
            # for i in transitions:
                # print i#,transitions[i]
                # print '++++++++++++++++++++++++++++++++++++'

            # print len(transitions)
            # print aaa
            # print transitions
            ved_trans,orizd_trans=create_edge_nedge_tran(intervals,points)#,u_node)
            if verb:
                print ndls,'done edge_trans'
            # print ved_trans,'amama'
            # print
            # print orizd_trans,'orizd_trans'
            # print aaaa
            # for i in orizd_trans:
                # print i,orizd_trans[i]
            # print 
            # print '<<'
            path_dic,mma,mmi=create_paths(points)
            if verb:
                print ndls,'done paths'
            # print path_dic,mma,mmi
            # for i in path_dic:
            #     print i, path_dic[i]
            # print aaaa
            traj_counter_C=Counter()
            traj_list=[]
            Ff=ig.Graph().as_directed()
            # import graph-tool as gt
            # F=Graph()
            # eprop=F.new_edge_property('string')
            # F.edge_properties['elabel']=eprop
            # vprop=F.new_vertex_property('string')
            # vcol=F.new_vertex_property('string')
            # F.vertex_properties['vlabel']=vprop
            # F.vertex_properties['vcolor']=vcol
            # filedir='Example_DavisWomen'
            #     try:
            #         os.stat(filedir)
            #     except:
            #         os.mkdir(filedir)
            # filedir=
            nam=dict()
            uu=0
            outfile_names=[]
            outfile_namestr=[]
            counter=0
            # fig1=plt.figure(num=1,figsize=(12,12))
            # fig1=figi
            # if fig_u!=1:
            #     # fig=plt.figure(figsize=(10,10))
            #     fig1 =plt.figure(num=fig_u,figsize=(14,16))
            # fig=plt.figure(num=1,figsize=(24,12))
            # ax.set_title('Diagrams of vertex transitions')
            for u_node in intervals:
                # u_node='u'
                # print u_node,'dflskdjalskdjflkasjdflkasjdfljasldfjalsdkjflaksjdflaksjdflkajsdflkjasldfkj'
                nw_traj=[]
                lolo=0
                for j in orizd_trans[u_node]:
                    # print j, orizd_trans[u_node][j],'dddddddddddddddddddddddddddddddddddkkkkkkkkkkkkkkkkkkkkkkk'
                    if len(orizd_trans[u_node][j])==0:
                        continue
                    else:
                        lolo=1
                if lolo==0:
                    continue
                start_pa,end_pa=create_start_end_path(ved_trans[u_node],orizd_trans[u_node],path_dic,mma,mmi,u_node)
                # start_pa,end_pa=create_start_end_path_davis(ved_trans[u_node],orizd_trans[u_node],path_dic,mma,mmi,u_node)
                # print start_pa,end_pa,'sted'
                # print aaaa
                F=create_graph_trans(orizd_trans[u_node],transitions,u_node)
                # print start_pa,end_pa,'aaaa'
                filedir='S_out_graphs'
                try:
                    os.stat(filedir)
                except:
                    os.mkdir(filedir)
                filf='%s_graph.graphml' %u_node
                outfile_name = os.path.join('%s' % filedir,filf)
                nx.write_graphml(F,outfile_name)
                # print start_pa
                # print end_pa
                # print F.nodes()
                starters=[]
                
                traj_counter=0
                
                # print u_node
                # print start_pa,end_pa
                for i in start_pa:
                    starters.append(i[1])
                    trajjj=set()
                    # print 'Trajectories of %s starting with %s' %(u_node, i[1])
                    if davisw:
                        for j in intervals[u_node]:
                            # print j,u_node
                            if j[0]==u_node:
                                jj=j[1]
                            else:
                                jj=j[0]
                            # print jj,j,u_node,'ssssssssssssssss',jj[1:]+jj
                            trajjj.add((int(jj[1:]),jj))
                        # print sorted(trajjj, key=lambda traj: traj[0])
                        nw=[]
                        for i in sorted(trajjj, key=lambda traj: traj[0]):
                            ii=i[1]
                            # print ii
                            nw.append(ii)
                        # print nw
                        traj_list.append(nw)
                    else:

                        for j in end_pa:
                    # for i in path_dic:
                    #     if i=='u':
                    #         continue
                            # print i,j,'aaaaaaaaaaaaaaaaaa'
                            # print F.nodes()
                            # print F.edges()
                            try:
                                uup=nx.all_simple_paths(F,i[1],j[1])

                                un=0
                                for ii in uup:
                                    # print ii
                                    traj_list.append(ii)
                                    nw_traj.append(ii)
                                    un+=1
                                    traj_counter+=1
                                    traj_counter_C[u_node]+=1
                                # print un
                            except Exception,e:
                                pass
                                # print e
                       
                    
                    # print
                # print nam,u_node,'ddddddddddddddddddddddddddddddddddddd'
                # print Ff
                # create_trans_graphtool
                # print aaaa
                # if not davisw:
                # Ff,nam,uu=plot_total_traject(nw_traj,Ff,u_node,uu,nam_v=nam)  
                Ff,uu=plot_total_traject(nw_traj,Ff,u_node,uu,nam_v=nam)
                if verb:
                    print ndls,'done plot traj'  

                # print Ff
                # print aaaa
                # print traj_counter   
                # print traj_counter_C
                counter+=1
                if plot_first_mode:

                    bot_t=plot_transit_n(intervals,transitions,tot_interval,ved_trans,npo,u_node,counter,write_to_file=True)
                else:
                    if u_node==search_name:
                        bot_t=plot_transit_n(intervals,transitions,tot_interval,ved_trans,npo,u_node,counter,write_to_file=True)


                if verb:
                    print ndls,i,'done plot ntrans'
                # bot_t,outfile_name=plot_transit(intervals,transitions,tot_interval,ved_trans,npo,u_node,counter,write_to_file=True)
                # outfile_namestr.append(outfile_name)
                # outfile_name=plot_transit_igraph(F,outfile_name, bot_t,u_node,write_to_file=True)
                # outfile_names.append(outfile_name)
                # display(Image(filename=outfile_name))
                # print aaaa
            # if write_to_file:
            
            filedir='S_out_figs'
            try:
                os.stat(filedir)
            except:
                os.mkdir(filedir)
            filf='Sub_trans.png' #%u_node
            outfile_name = os.path.join('%s' % filedir,filf)
            # plt.savefig(outfile_name, bbox_inches='tight')
            if fig_u!=1:
                # fig=plt.figure(figsize=(10,10))
                fig =plt.figure(num=fig_u)
            else:
                fig=plt.figure(num=fig_u)
                # fig=figi[fig_u]
                
                fig.add_subplot(111)#,figsize=(12,12))


            # fig=plt.figure(num=fig_u)
            # # fig=figi[fig_u]
            # fig_u+=1
            # fig.add_subplot(122)#,figsize=(12,12))
            # if plot_first_mode:
            # bot_ti,outFig_transit=plot_transit_timeline(intervals,transit,tot_interval,ved_trans,npo,ndls,write_to_file=False,plot_first_mode=plot_first_mode)
            # plt.show()
            # 
            if fig_u!=1:
                print 
                print 'Statistics of trajectories of second mode vertices'
                print 
            else:
                print 
                print 'Statistics of trajectories of first mode vertices'
                print 
                fig_u+=1

            
            # display(Image(filename=outFig))
            filedir='S_out_traject'
            try:
                os.stat(filedir)
            except:
                os.mkdir(filedir)
            filf='trajectories.xlsx'
            outfile_name_xls = os.path.join('%s' % filedir,filf)
            # aNala(traj_list,traj_counter_C,outfile_name_xls)
            pdfs[str(ndls)]=aNala_pandas(traj_list,traj_counter_C,outfile_name_xls,plot_first_mode=plot_first_mode)
            if verb:
                print ndls,'done anala'
            # print traj_counter_C

            ul=5
            for ee in Ff.es:
                ll=ul
                
                # print ee
                momo=ee['ed_label']
                # print momo
                mmmm=''
                for i in momo:
                    if len(mmmm)>ll:
                        mmmm+='\n'
                        ll+=ul
                    mmmm+=i+' , '
                mmmm=mmmm[:-3]
                ee['ed_label']=mmmm

            filedir='S_out_figs'
            try:
                os.stat(filedir)
            except:
                os.mkdir(filedir)
            filf='Total_graph_trans.tex' 
            outfile_name_tex = os.path.join('%s' % filedir,filf)
            create_tex(outfile_name_tex,Ff)
            # return pdf
            # return outfile_namestr,outfile_names,outFig_transit,outfile_name_xls,outfile_name_tex

    else:
        if verb:
            print 'else'
        ndls=ndll

        intervals,tot_interval=create_interv(G,nodelist=ndls,time_to_add=timetoadd)


        #     for jj in v:
        #         print i,v,jj
        #         # print jj

        #         Gg.add_edge(str(i[0]),str(i[1]),date_start=jj[0],date_end=jj[1])
        # ndls=Gg.nodes()
        # print Gg.edges(data=True)

        # intervals,tot_interval=create_interv(Gg,nodelist=ndls,time_to_add=time_to_add)


        # for i in intervals:
        #     # print i,' ',intervals[i]
        # print tot_interval,'--------'
        # print aaaa

        npo,transit,points=create_points(intervals)
        # print points
        # for i in points:
        #     print i,points[i]
        # for i in transit:
        #     print i,transit[i]
        #     print 
        # print transit
        # print npo
        # print aaa
        transitions=create_transitions(transit)
        # for i in transitions:
            # print i#,transitions[i]
            # print '++++++++++++++++++++++++++++++++++++'

        # print len(transitions)
        # print aaa
        # print transitions
        ved_trans,orizd_trans=create_edge_nedge_tran(intervals,points)#,u_node)
        # print ved_trans,'amama'
        # print
        # print orizd_trans,'orizd_trans'
        # print aaaa
        # for i in orizd_trans:
            # print i,orizd_trans[i]
        # print 
        # print '<<'
        path_dic,mma,mmi=create_paths(points)
        # print path_dic,mma,mmi
        # for i in path_dic:
        #     print i, path_dic[i]
        # print aaaa
        traj_counter_C=Counter()
        traj_list=[]
        Ff=ig.Graph().as_directed()
        # import graph-tool as gt
        # F=Graph()
        # eprop=F.new_edge_property('string')
        # F.edge_properties['elabel']=eprop
        # vprop=F.new_vertex_property('string')
        # vcol=F.new_vertex_property('string')
        # F.vertex_properties['vlabel']=vprop
        # F.vertex_properties['vcolor']=vcol
        # filedir='Example_DavisWomen'
        #     try:
        #         os.stat(filedir)
        #     except:
        #         os.mkdir(filedir)
        # filedir=
        nam=dict()
        uu=0
        outfile_names=[]
        outfile_namestr=[]
        counter=0
        # fig1=plt.figure(num=1,figsize=(12,12))
        fig=plt.figure(num=2,figsize=(24,12))
        # plt.title('Diagrams of vertex transitions')
        # fig.set_title('Diagrams of vertex transitions')

        for u_node in intervals:
            # u_node='u'
            # print u_node,'dflskdjalskdjflkasjdflkasjdfljasldfjalsdkjflaksjdflaksjdflkajsdflkjasldfkj'
            nw_traj=[]
            lolo=0
            for j in orizd_trans[u_node]:
                # print j, orizd_trans[u_node][j],'dddddddddddddddddddddddddddddddddddkkkkkkkkkkkkkkkkkkkkkkk'
                if len(orizd_trans[u_node][j])==0:
                    continue
                else:
                    lolo=1
            if lolo==0:
                continue
            start_pa,end_pa=create_start_end_path(ved_trans[u_node],orizd_trans[u_node],path_dic,mma,mmi,u_node)
            # start_pa,end_pa=create_start_end_path_davis(ved_trans[u_node],orizd_trans[u_node],path_dic,mma,mmi,u_node)
            # print start_pa,end_pa,'sted'
            # print aaaa
            F=create_graph_trans(orizd_trans[u_node],transitions,u_node)
            # print start_pa,end_pa,'aaaa'
            filedir='S_out_graphs'
            try:
                os.stat(filedir)
            except:
                os.mkdir(filedir)
            filf='%s_graph.graphml' %u_node
            outfile_name = os.path.join('%s' % filedir,filf)
            nx.write_graphml(F,outfile_name)
            # print start_pa
            # print end_pa
            # print F.nodes()
            starters=[]
            
            traj_counter=0
            
            # print u_node
            # print start_pa,end_pa
            for i in start_pa:
                starters.append(i[1])
                trajjj=set()
                # print 'Trajectories of %s starting with %s' %(u_node, i[1])
                if davisw:
                    for j in intervals[u_node]:
                        # print j,u_node
                        if j[0]==u_node:
                            jj=j[1]
                        else:
                            jj=j[0]
                        # print jj,j,u_node,'ssssssssssssssss',jj[1:]+jj
                        trajjj.add((int(jj[1:]),jj))
                    # print sorted(trajjj, key=lambda traj: traj[0])
                    nw=[]
                    for i in sorted(trajjj, key=lambda traj: traj[0]):
                        ii=i[1]
                        # print ii
                        nw.append(ii)
                    # print nw
                    traj_list.append(nw)
                else:

                    for j in end_pa:
                # for i in path_dic:
                #     if i=='u':
                #         continue
                        # print i,j,'aaaaaaaaaaaaaaaaaa'
                        # print F.nodes()
                        # print F.edges()
                        try:
                            uup=nx.all_simple_paths(F,i[1],j[1])

                            un=0
                            for ii in uup:
                                # print ii
                                traj_list.append(ii)
                                nw_traj.append(ii)
                                un+=1
                                traj_counter+=1
                                traj_counter_C[u_node]+=1
                            # print un
                        except Exception,e:
                            pass
                            # print e
                   
                
                # print
            # print nam,u_node,'ddddddddddddddddddddddddddddddddddddd'
            # print Ff
            # create_trans_graphtool
            # print aaaa
            # if not davisw:
            # Ff,nam,uu=plot_total_traject(nw_traj,Ff,u_node,uu,nam_v=nam)  
            Ff,uu=plot_total_traject(nw_traj,Ff,u_node,uu,nam_v=nam)  

            # print Ff
            # print aaaa
            # print traj_counter   
            # print traj_counter_C
            counter+=1

            bot_t=plot_transit_n(intervals,transitions,tot_interval,ved_trans,npo,u_node,counter,write_to_file=True)
            # bot_t,outfile_name=plot_transit(intervals,transitions,tot_interval,ved_trans,npo,u_node,counter,write_to_file=True)
            # outfile_namestr.append(outfile_name)
            outfile_name=plot_transit_igraph(F,outfile_name, bot_t,u_node,write_to_file=True)
            # outfile_names.append(outfile_name)
            # display(Image(filename=outfile_name))
            # print aaaa
        # if write_to_file:
        
        filedir='S_out_figs'
        try:
            os.stat(filedir)
        except:
            os.mkdir(filedir)
        filf='Sub_trans.png' #%u_node
        outfile_name = os.path.join('%s' % filedir,filf)
        # plt.savefig(outfile_name, bbox_inches='tight')
        fig=plt.figure(num=1)
        fig.add_subplot(122)
        # fig=plt.figure(num=1)
        bot_ti,outFig_transit=plot_transit_timeline(intervals,transit,tot_interval,ved_trans,npo,ndls,write_to_file=False)
        plt.show()
        print 
        print 'Statistics of trajectories'
        print 
        
        # display(Image(filename=outFig))
        filedir='S_out_traject'
        try:
            os.stat(filedir)
        except:
            os.mkdir(filedir)
        filf='trajectories.xlsx'
        outfile_name_xls = os.path.join('%s' % filedir,filf)
        # aNala(traj_list,traj_counter_C,outfile_name_xls)
        pdfs=aNala_pandas(traj_list,traj_counter_C,outfile_name_xls)
        
        # print traj_counter_C

        ul=5
        for ee in Ff.es:
            ll=ul
            
            # print ee
            momo=ee['ed_label']
            # print momo
            mmmm=''
            for i in momo:
                if len(mmmm)>ll:
                    mmmm+='\n'
                    ll+=ul
                mmmm+=i+' , '
            mmmm=mmmm[:-3]
            ee['ed_label']=mmmm

        filedir='S_out_figs'
        try:
            os.stat(filedir)
        except:
            os.mkdir(filedir)
        filf='Total_graph_trans.tex' 
        outfile_name_tex = os.path.join('%s' % filedir,filf)
        create_tex(outfile_name_tex,Ff)
        # print pdf
        # return outfile_namestr,outfile_names,outFig_transit,outfile_name_xls,outfile_name_tex
    return pdfs

    # uv=[(0,4),(4,8),(10,12)]
    # uz=[(3,12)]
    # vw=[(2,7),(10,12)]
    # wz=[(0,3),(7,11)]
    # wy=[(2,4),(6,10)]
    # G=nx.MultiGraph()
    # for i in uv:
    #     G.add_edge('u','A',date_start=i[0],date_end=i[1])
    # for i in wy:
    #     G.add_edge('w','C',date_start=i[0],date_end=i[1])
    # for i in uz:
    #     G.add_edge('u','B',date_start=i[0],date_end=i[1])
    # for i in vw:
    #     G.add_edge('w','A',date_start=i[0],date_end=i[1])
    # for i in wz:
    #     G.add_edge('w','B',date_start=i[0],date_end=i[1])
    # ndls=['u','w']
    # for ed in G.edges():
    #     print ed,G[ed[0]][ed[1]]
    #     for att ,v in G[ed[0]][ed[1]].items():
    #         print att , v
    # print aaaa
    # # print G.edges(dat)
    # def create_graph_number1(time_to_add=0):
    # G,ndls,timetoadd,davisw=create_graph_number1()
    # k=5
    # n=10
    # pp=[0.21,.31,.21,.31,.4]
    # davisw=False
    # G,ndls,timetoadd,davisw=create_synthetic3lg(k,n,pp,davisw)
    # outfile_names,outFig_transit,outfile_name_xls,outfile_name_tex= main_work(G,ndls,timetoadd,davisw)
        # ig.plot(Ff,outfile_name, vertex_size=30, vertex_color='grey', vertex_label_size=12,vertex_label=Ff.vs['vlabel'],
        #     edge_curved=0.15,
        #      # edge_color=Ff.es['ecolor'],
        #      edge_label_dist=12,edge_label_halign='right',edge_label_valign='top',edge_label=Ff.es['ed_label'], 
        #      bbox=(0, 0, 1000, 1000))#,Ff.vs['color']

# k=10
# n=7
# m=6
# pp=[0.19,.31,.31,.31,.24,.28,.32,.35,.33,.32]
# G,ndls,timetoadd=create_synthetic3lgB(k,n,m,pp)

# k=10
# n=8
# pp=[0.19,.11,.11,.11,.14,.18,.12,.15,.13,.12]
# G,ndls,timetoadd=create_synthetic3lg(k,n,pp)
# outfile_namestr,outfile_names,outFig_transit,outfile_name_xls,outfile_name_tex= main_work(G,ndls,timetoadd)


# k=10
# n=7
# m=6
# pp=[0.19,.11,.11,.11,.14,.18,.12,.15,.13,.12]
# G,ndls,timetoadd=create_synthetic3lgB(k,n,m,pp)
# #outfile_namestr,outfile_names,outFig_transit,outfile_name_xls,outfile_name_tex= 
# main_work(G,ndls,timetoadd)
def main_work_search_name(G,ndll,timetoadd,figi,search_name,davisw=False,verb=False,plot_first_mode=True):
    pdfs={}
    if isinstance(ndll[0],list):

        fig_u=1
        for ndls in ndll:
            # print ndls,'aaaaaaaaaaaaaaaa'
            intervals,tot_interval=create_interv(G,nodelist=ndls,time_to_add=timetoadd)
            if verb:
                print ndls,'done intervals'

            #     for jj in v:
            #         print i,v,jj
            #         # print jj

            #         Gg.add_edge(str(i[0]),str(i[1]),date_start=jj[0],date_end=jj[1])
            # ndls=Gg.nodes()
            # print Gg.edges(data=True)

            # intervals,tot_interval=create_interv(Gg,nodelist=ndls,time_to_add=time_to_add)


            # for i in intervals:
            #     # print i,' ',intervals[i]
            # print tot_interval,'--------'
            # print aaaa

            npo,transit,points=create_points(intervals)
            if verb:
                print ndls,'done transits'
            # print points
            # for i in points:
            #     print i,points[i]
            # for i in transit:
            #     print i,transit[i]
            #     print 
            # print transit
            # print npo
            # print aaa
            transitions=create_transitions(transit)
            if verb:
                print ndls,'done transitions'
            # for i in transitions:
                # print i#,transitions[i]
                # print '++++++++++++++++++++++++++++++++++++'

            # print len(transitions)
            # print aaa
            # print transitions
            ved_trans,orizd_trans=create_edge_nedge_tran(intervals,points)#,u_node)
            if verb:
                print ndls,'done edge_trans'
            # print ved_trans,'amama'
            # print
            # print orizd_trans,'orizd_trans'
            # print aaaa
            # for i in orizd_trans:
                # print i,orizd_trans[i]
            # print 
            # print '<<'
            path_dic,mma,mmi=create_paths(points)
            if verb:
                print ndls,'done paths'
            # print path_dic,mma,mmi
            # for i in path_dic:
            #     print i, path_dic[i]
            # print aaaa
            traj_counter_C=Counter()
            traj_list=[]
            Ff=ig.Graph().as_directed()
            # import graph-tool as gt
            # F=Graph()
            # eprop=F.new_edge_property('string')
            # F.edge_properties['elabel']=eprop
            # vprop=F.new_vertex_property('string')
            # vcol=F.new_vertex_property('string')
            # F.vertex_properties['vlabel']=vprop
            # F.vertex_properties['vcolor']=vcol
            # filedir='Example_DavisWomen'
            #     try:
            #         os.stat(filedir)
            #     except:
            #         os.mkdir(filedir)
            # filedir=
            nam=dict()
            uu=0
            outfile_names=[]
            outfile_namestr=[]
            counter=0
            # fig1=plt.figure(num=1,figsize=(12,12))
            # fig1=figi
            # if fig_u!=1:
            #     # fig=plt.figure(figsize=(10,10))
            #     fig1 =plt.figure(num=fig_u,figsize=(14,16))
            fig=plt.figure(num=1,figsize=(24,12))
            # ax.set_title('Diagrams of vertex transitions')
            for u_node in intervals:
                # u_node='u'
                # print u_node,'dflskdjalskdjflkasjdflkasjdfljasldfjalsdkjflaksjdflaksjdflkajsdflkjasldfkj'
                nw_traj=[]
                lolo=0
                for j in orizd_trans[u_node]:
                    # print j, orizd_trans[u_node][j],'dddddddddddddddddddddddddddddddddddkkkkkkkkkkkkkkkkkkkkkkk'
                    if len(orizd_trans[u_node][j])==0:
                        continue
                    else:
                        lolo=1
                if lolo==0:
                    continue
                start_pa,end_pa=create_start_end_path(ved_trans[u_node],orizd_trans[u_node],path_dic,mma,mmi,u_node)
                # start_pa,end_pa=create_start_end_path_davis(ved_trans[u_node],orizd_trans[u_node],path_dic,mma,mmi,u_node)
                # print start_pa,end_pa,'sted'
                # print aaaa
                F=create_graph_trans(orizd_trans[u_node],transitions,u_node)
                # print start_pa,end_pa,'aaaa'
                filedir='S_out_graphs'
                try:
                    os.stat(filedir)
                except:
                    os.mkdir(filedir)
                filf='%s_graph.graphml' %u_node
                outfile_name = os.path.join('%s' % filedir,filf)
                nx.write_graphml(F,outfile_name)
                # print start_pa
                # print end_pa
                # print F.nodes()
                starters=[]
                
                traj_counter=0
                
                # print u_node
                # print start_pa,end_pa
                for i in start_pa:
                    starters.append(i[1])
                    trajjj=set()
                    # print 'Trajectories of %s starting with %s' %(u_node, i[1])
                    if davisw:
                        for j in intervals[u_node]:
                            # print j,u_node
                            if j[0]==u_node:
                                jj=j[1]
                            else:
                                jj=j[0]
                            # print jj,j,u_node,'ssssssssssssssss',jj[1:]+jj
                            trajjj.add((int(jj[1:]),jj))
                        # print sorted(trajjj, key=lambda traj: traj[0])
                        nw=[]
                        for i in sorted(trajjj, key=lambda traj: traj[0]):
                            ii=i[1]
                            # print ii
                            nw.append(ii)
                        # print nw
                        traj_list.append(nw)
                    else:

                        for j in end_pa:
                    # for i in path_dic:
                    #     if i=='u':
                    #         continue
                            # print i,j,'aaaaaaaaaaaaaaaaaa'
                            # print F.nodes()
                            # print F.edges()
                            try:
                                uup=nx.all_simple_paths(F,i[1],j[1])

                                un=0
                                for ii in uup:
                                    # print ii
                                    traj_list.append(ii)
                                    nw_traj.append(ii)
                                    un+=1
                                    traj_counter+=1
                                    traj_counter_C[u_node]+=1
                                # print un
                            except Exception,e:
                                pass
                                # print e
                       
                    
                    # print
                # print nam,u_node,'ddddddddddddddddddddddddddddddddddddd'
                # print Ff
                # create_trans_graphtool
                # print aaaa
                # if not davisw:
                # Ff,nam,uu=plot_total_traject(nw_traj,Ff,u_node,uu,nam_v=nam)  
                Ff,uu=plot_total_traject(nw_traj,Ff,u_node,uu,nam_v=nam)
                if verb:
                    print ndls,'done plot traj'  

                # print Ff
                # print aaaa
                # print traj_counter   
                # print traj_counter_C
                counter+=1
                if plot_first_mode:

                    bot_t=plot_transit_n(intervals,transitions,tot_interval,ved_trans,npo,u_node,counter,write_to_file=True)
                else:
                    if u_node==search_name:
                        bot_t=plot_transit_n(intervals,transitions,tot_interval,ved_trans,npo,u_node,counter,write_to_file=True)
                        

                if verb:
                    print ndls,i,'done plot ntrans'
                # bot_t,outfile_name=plot_transit(intervals,transitions,tot_interval,ved_trans,npo,u_node,counter,write_to_file=True)
                # outfile_namestr.append(outfile_name)
                # outfile_name=plot_transit_igraph(F,outfile_name, bot_t,u_node,write_to_file=True)
                # outfile_names.append(outfile_name)
                # display(Image(filename=outfile_name))
                # print aaaa
            # if write_to_file:
            
            filedir='S_out_figs'
            try:
                os.stat(filedir)
            except:
                os.mkdir(filedir)
            filf='Sub_trans.png' #%u_node
            outfile_name = os.path.join('%s' % filedir,filf)
            # plt.savefig(outfile_name, bbox_inches='tight')
            # if fig_u!=1:
            #     # fig=plt.figure(figsize=(10,10))
            #     fig =plt.figure(num=fig_u)
            # else:
            #     fig=plt.figure(num=fig_u)
                # fig=figi[fig_u]
                
                # fig.add_subplot(122)#,figsize=(12,12))


            # fig=plt.figure(num=fig_u)
            # # fig=figi[fig_u]
            # fig_u+=1
            # fig.add_subplot(122)#,figsize=(12,12))
            # if plot_first_mode:
            # bot_ti,outFig_transit=plot_transit_timeline(intervals,transit,tot_interval,ved_trans,npo,ndls,write_to_file=False,plot_first_mode=plot_first_mode)
            # plt.show()
            # 
            if fig_u!=1:
                print 
                print 'Statistics of trajectories of second mode vertices'
                print 
            else:
                print 
                print 'Statistics of trajectories of first mode vertices'
                print 
                fig_u+=1

            
            # display(Image(filename=outFig))
            filedir='S_out_traject'
            try:
                os.stat(filedir)
            except:
                os.mkdir(filedir)
            filf='trajectories.xlsx'
            outfile_name_xls = os.path.join('%s' % filedir,filf)
            # aNala(traj_list,traj_counter_C,outfile_name_xls)
            pdfs[str(ndls)]=aNala_pandas(traj_list,traj_counter_C,outfile_name_xls,plot_first_mode=plot_first_mode)
            if verb:
                print ndls,'done anala'
            # print traj_counter_C

            ul=5
            for ee in Ff.es:
                ll=ul
                
                # print ee
                momo=ee['ed_label']
                # print momo
                mmmm=''
                for i in momo:
                    if len(mmmm)>ll:
                        mmmm+='\n'
                        ll+=ul
                    mmmm+=i+' , '
                mmmm=mmmm[:-3]
                ee['ed_label']=mmmm

            filedir='S_out_figs'
            try:
                os.stat(filedir)
            except:
                os.mkdir(filedir)
            filf='Total_graph_trans.tex' 
            outfile_name_tex = os.path.join('%s' % filedir,filf)
            create_tex(outfile_name_tex,Ff)
            # return pdf
            # return outfile_namestr,outfile_names,outFig_transit,outfile_name_xls,outfile_name_tex

    else:
        if verb:
            print 'else'
        ndls=ndll

        intervals,tot_interval=create_interv(G,nodelist=ndls,time_to_add=timetoadd)


        #     for jj in v:
        #         print i,v,jj
        #         # print jj

        #         Gg.add_edge(str(i[0]),str(i[1]),date_start=jj[0],date_end=jj[1])
        # ndls=Gg.nodes()
        # print Gg.edges(data=True)

        # intervals,tot_interval=create_interv(Gg,nodelist=ndls,time_to_add=time_to_add)


        # for i in intervals:
        #     # print i,' ',intervals[i]
        # print tot_interval,'--------'
        # print aaaa

        npo,transit,points=create_points(intervals)
        # print points
        # for i in points:
        #     print i,points[i]
        # for i in transit:
        #     print i,transit[i]
        #     print 
        # print transit
        # print npo
        # print aaa
        transitions=create_transitions(transit)
        # for i in transitions:
            # print i#,transitions[i]
            # print '++++++++++++++++++++++++++++++++++++'

        # print len(transitions)
        # print aaa
        # print transitions
        ved_trans,orizd_trans=create_edge_nedge_tran(intervals,points)#,u_node)
        # print ved_trans,'amama'
        # print
        # print orizd_trans,'orizd_trans'
        # print aaaa
        # for i in orizd_trans:
            # print i,orizd_trans[i]
        # print 
        # print '<<'
        path_dic,mma,mmi=create_paths(points)
        # print path_dic,mma,mmi
        # for i in path_dic:
        #     print i, path_dic[i]
        # print aaaa
        traj_counter_C=Counter()
        traj_list=[]
        Ff=ig.Graph().as_directed()
        # import graph-tool as gt
        # F=Graph()
        # eprop=F.new_edge_property('string')
        # F.edge_properties['elabel']=eprop
        # vprop=F.new_vertex_property('string')
        # vcol=F.new_vertex_property('string')
        # F.vertex_properties['vlabel']=vprop
        # F.vertex_properties['vcolor']=vcol
        # filedir='Example_DavisWomen'
        #     try:
        #         os.stat(filedir)
        #     except:
        #         os.mkdir(filedir)
        # filedir=
        nam=dict()
        uu=0
        outfile_names=[]
        outfile_namestr=[]
        counter=0
        # fig1=plt.figure(num=1,figsize=(12,12))
        fig=plt.figure(num=2,figsize=(24,12))
        # plt.title('Diagrams of vertex transitions')
        # fig.set_title('Diagrams of vertex transitions')

        for u_node in intervals:
            # u_node='u'
            # print u_node,'dflskdjalskdjflkasjdflkasjdfljasldfjalsdkjflaksjdflaksjdflkajsdflkjasldfkj'
            nw_traj=[]
            lolo=0
            for j in orizd_trans[u_node]:
                # print j, orizd_trans[u_node][j],'dddddddddddddddddddddddddddddddddddkkkkkkkkkkkkkkkkkkkkkkk'
                if len(orizd_trans[u_node][j])==0:
                    continue
                else:
                    lolo=1
            if lolo==0:
                continue
            start_pa,end_pa=create_start_end_path(ved_trans[u_node],orizd_trans[u_node],path_dic,mma,mmi,u_node)
            # start_pa,end_pa=create_start_end_path_davis(ved_trans[u_node],orizd_trans[u_node],path_dic,mma,mmi,u_node)
            # print start_pa,end_pa,'sted'
            # print aaaa
            F=create_graph_trans(orizd_trans[u_node],transitions,u_node)
            # print start_pa,end_pa,'aaaa'
            filedir='S_out_graphs'
            try:
                os.stat(filedir)
            except:
                os.mkdir(filedir)
            filf='%s_graph.graphml' %u_node
            outfile_name = os.path.join('%s' % filedir,filf)
            nx.write_graphml(F,outfile_name)
            # print start_pa
            # print end_pa
            # print F.nodes()
            starters=[]
            
            traj_counter=0
            
            # print u_node
            # print start_pa,end_pa
            for i in start_pa:
                starters.append(i[1])
                trajjj=set()
                # print 'Trajectories of %s starting with %s' %(u_node, i[1])
                if davisw:
                    for j in intervals[u_node]:
                        # print j,u_node
                        if j[0]==u_node:
                            jj=j[1]
                        else:
                            jj=j[0]
                        # print jj,j,u_node,'ssssssssssssssss',jj[1:]+jj
                        trajjj.add((int(jj[1:]),jj))
                    # print sorted(trajjj, key=lambda traj: traj[0])
                    nw=[]
                    for i in sorted(trajjj, key=lambda traj: traj[0]):
                        ii=i[1]
                        # print ii
                        nw.append(ii)
                    # print nw
                    traj_list.append(nw)
                else:

                    for j in end_pa:
                # for i in path_dic:
                #     if i=='u':
                #         continue
                        # print i,j,'aaaaaaaaaaaaaaaaaa'
                        # print F.nodes()
                        # print F.edges()
                        try:
                            uup=nx.all_simple_paths(F,i[1],j[1])

                            un=0
                            for ii in uup:
                                # print ii
                                traj_list.append(ii)
                                nw_traj.append(ii)
                                un+=1
                                traj_counter+=1
                                traj_counter_C[u_node]+=1
                            # print un
                        except Exception,e:
                            pass
                            # print e
                   
                
                # print
            # print nam,u_node,'ddddddddddddddddddddddddddddddddddddd'
            # print Ff
            # create_trans_graphtool
            # print aaaa
            # if not davisw:
            # Ff,nam,uu=plot_total_traject(nw_traj,Ff,u_node,uu,nam_v=nam)  
            Ff,uu=plot_total_traject(nw_traj,Ff,u_node,uu,nam_v=nam)  

            # print Ff
            # print aaaa
            # print traj_counter   
            # print traj_counter_C
            counter+=1

            bot_t=plot_transit_n(intervals,transitions,tot_interval,ved_trans,npo,u_node,counter,write_to_file=True)
            # bot_t,outfile_name=plot_transit(intervals,transitions,tot_interval,ved_trans,npo,u_node,counter,write_to_file=True)
            # outfile_namestr.append(outfile_name)
            outfile_name=plot_transit_igraph(F,outfile_name, bot_t,u_node,write_to_file=True)
            # outfile_names.append(outfile_name)
            # display(Image(filename=outfile_name))
            # print aaaa
        # if write_to_file:
        
        filedir='S_out_figs'
        try:
            os.stat(filedir)
        except:
            os.mkdir(filedir)
        filf='Sub_trans.png' #%u_node
        outfile_name = os.path.join('%s' % filedir,filf)
        # plt.savefig(outfile_name, bbox_inches='tight')
        fig=plt.figure(num=1)
        fig.add_subplot(122)
        # fig=plt.figure(num=1)
        bot_ti,outFig_transit=plot_transit_timeline(intervals,transit,tot_interval,ved_trans,npo,ndls,write_to_file=False)
        # plt.show()
        print 
        print 'Statistics of trajectories'
        print 
        
        # display(Image(filename=outFig))
        filedir='S_out_traject'
        try:
            os.stat(filedir)
        except:
            os.mkdir(filedir)
        filf='trajectories.xlsx'
        outfile_name_xls = os.path.join('%s' % filedir,filf)
        # aNala(traj_list,traj_counter_C,outfile_name_xls)
        pdfs=aNala_pandas(traj_list,traj_counter_C,outfile_name_xls)
        
        # print traj_counter_C

        ul=5
        for ee in Ff.es:
            ll=ul
            
            # print ee
            momo=ee['ed_label']
            # print momo
            mmmm=''
            for i in momo:
                if len(mmmm)>ll:
                    mmmm+='\n'
                    ll+=ul
                mmmm+=i+' , '
            mmmm=mmmm[:-3]
            ee['ed_label']=mmmm

        filedir='S_out_figs'
        try:
            os.stat(filedir)
        except:
            os.mkdir(filedir)
        filf='Total_graph_trans.tex' 
        outfile_name_tex = os.path.join('%s' % filedir,filf)
        create_tex(outfile_name_tex,Ff)
        # print pdf
        # return outfile_namestr,outfile_names,outFig_transit,outfile_name_xls,outfile_name_tex
    return pdfs

    # uv=[(0,4),(4,8),(10,12)]
    # uz=[(3,12)]
    # vw=[(2,7),(10,12)]
    # wz=[(0,3),(7,11)]
    # wy=[(2,4),(6,10)]
    # G=nx.MultiGraph()
    # for i in uv:
    #     G.add_edge('u','A',date_start=i[0],date_end=i[1])
    # for i in wy:
    #     G.add_edge('w','C',date_start=i[0],date_end=i[1])
    # for i in uz:
    #     G.add_edge('u','B',date_start=i[0],date_end=i[1])
    # for i in vw:
    #     G.add_edge('w','A',date_start=i[0],date_end=i[1])
    # for i in wz:
    #     G.add_edge('w','B',date_start=i[0],date_end=i[1])
    # ndls=['u','w']
    # for ed in G.edges():
    #     print ed,G[ed[0]][ed[1]]
    #     for att ,v in G[ed[0]][ed[1]].items():
    #         print att , v
    # print aaaa
    # # print G.edges(dat)
    # def create_graph_number1(time_to_add=0):
    # G,ndls,timetoadd,davisw=create_graph_number1()
    # k=5
    # n=10
    # pp=[0.21,.31,.21,.31,.4]
    # davisw=False
    # G,ndls,timetoadd,davisw=create_synthetic3lg(k,n,pp,davisw)
    # outfile_names,outFig_transit,outfile_name_xls,outfile_name_tex= main_work(G,ndls,timetoadd,davisw)
        # ig.plot(Ff,outfile_name, vertex_size=30, vertex_color='grey', vertex_label_size=12,vertex_label=Ff.vs['vlabel'],
        #     edge_curved=0.15,
        #      # edge_color=Ff.es['ecolor'],
        #      edge_label_dist=12,edge_label_halign='right',edge_label_valign='top',edge_label=Ff.es['ed_label'], 
        #      bbox=(0, 0, 1000, 1000))#,Ff.vs['color']

# k=10
# n=7
# m=6
# pp=[0.19,.31,.31,.31,.24,.28,.32,.35,.33,.32]
# G,ndls,timetoadd=create_synthetic3lgB(k,n,m,pp)

# k=10
# n=8
# pp=[0.19,.11,.11,.11,.14,.18,.12,.15,.13,.12]
# G,ndls,timetoadd=create_synthetic3lg(k,n,pp)
# outfile_namestr,outfile_names,outFig_transit,outfile_name_xls,outfile_name_tex= main_work(G,ndls,timetoadd)


# k=10
# n=7
# m=6
# pp=[0.19,.11,.11,.11,.14,.18,.12,.15,.13,.12]
# G,ndls,timetoadd=create_synthetic3lgB(k,n,m,pp)
# #outfile_namestr,outfile_names,outFig_transit,outfile_name_xls,outfile_name_tex= 
# main_work(G,ndls,timetoadd)
