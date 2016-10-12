import numpy as np
import networkx as nx
from numpy import linalg
from numpy.linalg import inv
from scipy.linalg import eigvalsh
from prettytable import PrettyTable
from influence import influence_sim_dh_F_J,influence_sim_dh_F_J_multi,influence_sim_dh_F_J_mu
from tabulate import tabulate
import create_imgtex as crim
import random
import pickle
# from IPython.core.display import HTML

def steady_sol_calc(G,source,ssas_d,iterations,ijij=None):
    gg=nx.Graph(G)
    # print gg.nodes()
    # print gg.edges()
    nene=set()
    # print source
    for i in source:
        # print i
        if i not in G:
            ch=True
            continue
        if i in gg:
            ch=False
            gg.remove_node(i)
        for nne in G.neighbors(i):
            nene.add(nne)
    if ch:
        return np.zeros(len(gg))
    # aa= nx.adjacency_matrix(G)
    deg=nx.degree(G)
    aa= nx.adjacency_matrix(gg)
    deggh=nx.degree(gg)
    # print deg
    # print nene,'nnnn'
    # print deg.values()
    dim=len(deggh)
    # dim=len(deg)

    deg_fin=[]
    deg_lis=[]
    # nei = gg.neighbors(gg)
    for nd in gg.nodes():
        deg_lis.append(deg[nd])
        if nd in nene:
            deg_fin.append(-1./deg[nd])
        else:
            deg_fin.append(0)
    # print deg_fin
    # print nene
    # print aaaa
    deg_mat=[]
    s_k={}
    s_k_d={}
    so_k=0
    ddmm=[]
    proses_l=[]
    for k,v in enumerate(deg.keys()):
        proses_l.append(v)
        if v in source:
            s_k[v]= k
            so_k+=1
            s_k_d[v]=ddmm
            ddmm=[]
            continue
        ddmm.append(v)
        val=deg[v]
        nl=[]
        for i in range(dim):
    #         if so_k >0:
    #             for jj,prpr in enumerate(proses_l):
    #                 if prpr in source:
    #                     if i==jj:
    #                         continue
    #                     else if i 
    #                 nl.append(0)
                    
    #         else:
            if i == k:
                nl.append(val)
            else:
                nl.append(0)
    #     print v,nl
        deg_mat.append(nl)

    # deg_mat=np.matrix(deg_mat)
    deg_mat = np.diag(deg_lis) ######<<<<<<<<<<<<<<<<<<<<<< yparxei thema me kombous pou exoun bathmo 0...
    # print deg_lis
    # print 
    # print deg_mat
    # print nene, 'nene'
    # print deg_fin,'deg_fin'
    bba=inv(deg_mat)
    # for i in source
    if ijij == None:
        ssa_l=[ssas_d[i] for i in G.nodes() if i not in source]
    else:
        ssa_l=[ssas_d[ijij][i] for i in G.nodes() if i not in source]
    # ssa_l=[ssas_d[i] for i in G.nodes() ]

    # ssa_l=[ssa for i in nodes]
    ssa_all=np.array(ssa_l)
    # print np.eye(len(G.nodes())).shape
    # print ssa_all.transpose().shape
    # ss =np.eye(nodes)*ssa_all.transpose()
    ss= np.diag(ssa_all)
    bb=ss.dot(bba)
    # print ss
    ngn= []
    for i in G.nodes():
        if i not in source:
            ngn.append(i)
    sn=np.matrix(ngn)
    # sn=np.matrix(G.nodes())
    da=bb.dot(aa)
    # print da
    # dav=da.dot(sn.transpose())
    # print dav
    dap=da-np.identity(len(gg.nodes()))#.dot(deg_mat)
    # print dap, 'dap'
    # dap=dap.dot(aa)
    # dav=dap.dot(sn.transpose())
    # print sn.transpose()
    degss=np.matrix(deg_fin)
    # print degss,'degss'
    ndegss=ss.dot(degss.transpose())
    # print ndegss,'ndeg'
    # print np.linalg.inv(dap),'inv'
    # print degss.shape

    dav= np.linalg.inv(dap) *ndegss#.transpose()
    # sba=s_i_s_n.dot(i_s)
    # print sba.shape,np.linalg.det(sba)
    # print sn.shape , np.linalg.det(sn)
    # print dav,'ddddav'
    return dav

def steady_sols_calc(G,iterations,fjfun,precision=.3,sa=0,sb=.7,source_u=[1.],su=1.,h=1.,form_float_val=6,form_float_val_stead=6,cutting_num=None ):
    nodes=len(G.nodes())
    stt= '%i' %form_float_val
    # print stt
    ffv='%.' + stt+'f'
    stt= '%i' %form_float_val_stead
    ffvs='%.' + stt+'f'
    p=0.1
    lenghts=nx.all_pairs_shortest_path_length(G)
    list_ofNod=['Node/Node']
    for i in G.nodes():
        list_ofNod.append(i)
    table_of_no_zero_time = PrettyTable(list_ofNod)
    table_of_no_zero_val = PrettyTable(list_ofNod)
    table_of_no_iterations = PrettyTable(list_ofNod)
    table_of_comparison=PrettyTable(list_ofNod)
    table_of_steady_sols=PrettyTable(list_ofNod)
    row_ndl=[]
    row_vall=[]
    row_endl=[]
    row_compl=[]
    row_steadyl=[]
    for nd in G.nodes():
        ssas_ds={}
        source=[nd]
        if len(source)==0:
            source = [closse[-1]]
            source_u=[su]
            ssas_ds[closse[-1]]=0
        else:
            for nod  in source:
                ssas_ds[nod]=0
        if cutting_num!=None:
            for jjj,nod in enumerate(set(G.nodes())-set(source)):
                if jjj<cutting_num:
                    ssas_ds[nod]=sa
                else:
                    ssas_ds[nod]=sb
        else:
            for nod in set(G.nodes())-set(source):
                ssas_ds[nod]=sa
        F,y_all,source,y_orig,final_d,snodds=influence_sim_dh_F_J(nodes,p,sa,iterations,
            G=G,new_old=None,source=source,source_u=source_u,su=su,h=h,
            funcion=fjfun,insrplot=False,ssas_d=ssas_ds)
        # print source
        # print ssas_ds
        dav=steady_sol_calc(G,source,ssas_ds,iterations)
        row_nd=[nd]
        row_val=[nd]
        row_end=[nd]
        row_comp=[nd]
        row_steady=[nd]
        # print snodds
        # print aaaa
        # print dav
        for ii,jj in snodds.items():
            row_nd.append(jj[0])
            row_comp.append(jj[0]-lenghts[nd][ii])
            vals=ffv %jj[1]
            # print vals,'llllllllll',ffv
            row_val.append(vals)
        print 'Iterations %i and source %i with sa= %.4f' %(iterations,nd,sa)
        # print len(row_nd),len(row_nd)
        table_of_no_zero_time.add_row(row_nd)
        table_of_comparison.add_row(row_comp)
        table_of_no_zero_val.add_row(row_val)
        row_ndl.append(row_nd)#=[nd]
        row_vall.append(row_val)#=[nd]
        
        row_comp.append(row_comp)#=[nd]

        ch=True

        for ii,jj in enumerate(G.nodes()):
            if ch:
                iii=ii
            else:
                iii=ii-1
            if jj in source:
                ch=False
                iii=ii+1
                row_end.append(0)
                row_steady.append(ffvs %1.)
                continue
            row_steady.append(ffvs %dav.item(iii))
            # print ffvs %dav.item(iii)

            kk = y_all[jj]
            for ll,hh in enumerate(kk):
                # print ll,hh
                if abs(hh-dav.item(iii)) <= precision:
                    row_end.append(ll)
                    break
        table_of_no_iterations.add_row(row_end)
        table_of_steady_sols.add_row(row_steady)
        row_steadyl.append(row_steady)
        row_endl.append(row_end)
    # print 'Table of first no zero value time'
    # print table_of_no_zero_time.get_html_string(format=True)
    # print 
    # print 'Table of first no zero value value'
    # print table_of_no_zero_val.get_html_string(format=True)
    # print
    # print 'Table of iterations with precision %f ' %precision
    # print table_of_no_iterations
    # print 'Table of diffs shortest path' 
    # print table_of_comparison
    # print tabulate(row_steadyl,list_ofNod,tablefmt="latex")
    return (table_of_no_zero_time.get_html_string(format=True),table_of_no_zero_val.get_html_string(format=True),
            table_of_no_iterations.get_html_string(format=True),table_of_comparison.get_html_string(format=True),
            table_of_steady_sols.get_html_string(format=True))

def steady_sols_calc_multi_one(k,G,dic_of_Graphs_final,n,p,sas,edgelist,iterations,fjfun,precision=.3,sa_u=0,source_u=[1.],su=1.,h=1.,form_float_val=6,form_float_val_stead=6):
    nodes=len(G.nodes())
    dic_of_nodes_multi={}
    for i in range(k):
        for j in range(i,k):
            # print i,j,uucount
            # ssas_ds[(i,j)]={}
            if i==j:
                dic_of_nodes_multi[i]=dic_of_Graphs_final[(i,j)].nodes()
    # dic_of_nodes_multi_r={}
    # for i,v in dic_of_nodes_multi:

    G.remove_nodes_from(nx.isolates(G))
    stt= '%i' %form_float_val
    # print stt
    ffv='%.' + stt+'f'
    stt= '%i' %form_float_val_stead
    ffvs='%.' + stt+'f'
    p=0.1
    lenghts=nx.all_pairs_shortest_path_length(G)
    list_ofNod=['Node/Node']
    # print len(G.nodes())
    # print G.nodes()
    for i in G.nodes():
        list_ofNod.append(i)
    table_of_no_zero_time = PrettyTable(list_ofNod)
    table_of_no_zero_val = PrettyTable(list_ofNod)
    table_of_no_iterations = PrettyTable(list_ofNod)
    table_of_comparison=PrettyTable(list_ofNod)
    table_of_steady_sols=PrettyTable(list_ofNod)
    steady_sols_dict={}
    steady_sols_dict_t={}
    no_zero_time_dict={}
    no_zero_val_dict={}
    no_iterations_dict={}
    comparison_dict={}

    for nd in G.nodes():
        ssas_ds={}
        source=[nd]
        if len(source)==0:
            source = [closse[-1]]
            source_u=[su]
            ssas_ds[closse[-1]]=0
        else:
            for nod  in source:
                for i in range(k):
                    for j in range(i,k):
                        # ssas_ds[(i,j)]={}
                        ssas_ds[nod]=sa_u
        # print ssas_ds
        # print aaa
        uucount=0
        # dic_of_nodes_multi={}
        for i in range(k):
            for j in range(i,k):
                # print i,j,uucount
                # ssas_ds[(i,j)]={}
                if i==j:
                    gg=dic_of_Graphs_final[(i,j)].nodes()
                    # print gg,i,j
                    for nod in gg:
                        if nod not in source:
                            if sas!='rand':
                                ssas_ds[nod]=sas[uucount]
                            elif sas=='rand':
                                ssas_ds[nod]=random.random()
                    uucount+=1
        # print ssas_ds
        # print aaa
        # for nod in set(G.nodes())-set(source):
        #     ssas_ds[nod]=sa
        # print len(G.nodes())
        # print ssas_ds,'sasi'
        # print G.nodes()

        
        F,y_all,source,y_orig,final_d,snodds=influence_sim_dh_F_J_mu(nodes,p,iterations,
            G=G,new_old=None,source=source,source_u=source_u,su=su,h=h,
            funcion=fjfun,insrplot=False,ssas_d=ssas_ds)   
        # F,y_all,source,y_orig,final_d,snodds=influence_sim_dh_F_J_multi(k,nodes,p,ssas_ds,iterations,
        #     G,dic_of_Graphs_final,new_old=None,source=source,source_u=source_u,su=su,h=h,
        #     funcion=fjfun,insrplot=False)
        # print y_all
        # print source
        # print y_orig
        # print final_d
        # print snodds
        # print aaa
        # dav_di={}
        # for ii in range(k):
        #     for jj in range(ii,k):
        #         if ii==jj:
        #             print ii,jj
        #             dav_di[(ii,jj)]=steady_sol_calc(dic_of_Graphs_final[(ii,jj)],source,ssas_ds,iterations,ijij=(ii,jj))
                    # G,source,ssas_d,iterations
        # print len(G.nodes())
        dav=steady_sol_calc(G,source,ssas_ds,iterations)
        # NGr=nx.Graph()
        # NGr.add_edges_from(G.edges())

        # for iif,jjf in dav_di.items():
        #     ch=True
        #     for ii,jj in enumerate(dic_of_Graphs_final[iif].nodes()):
        #         print iif,ii,jj,ch
        #         if ch:
        #             iii=ii
        #         else:
        #             iii=ii-1
        #         if jj in source:
        #             ch=False
        #             iii=ii+1
        #             # row_end.append(0)
        #             # row_steady.append(ffvs %1.)
        #             NGr.add_node(jj,scalar_attribute=1)
        #             continue
        #         NGr.add_node(jj,scalar_attribute=jjf.item(iii))
        # print NGr.nodes(data=True)
        # # print aaa
        # Fr,y_allr,sourcer,y_origr,final_dr,snoddsr=influence_sim_dh_F_J_multi(k,nodes,p,ssas_ds,iterations,
        #     NGr,dic_of_Graphs_final,new_old=None,source=source,source_u=source_u,su=su,h=h,
        #     funcion=fjfun,insrplot=False,no_change=True)
        # print sourcer
        # print y_origr
        # print final_dr
        # print snoddsr
        # print aaa

                # row_steady.append(ffvs %dav.item(iii))
            # for nd in dic_of_Graphs_final[ii].nodes():
            #     attr_dic=G.node[nd]
            #     NGr.add_node(nd,scalar_attribute=)
        row_nd=[nd]
        row_val=[nd]
        row_end=[nd]
        row_comp=[nd]
        row_steady=[nd]
        row_steady_sols=[]
        # print G.nodes()
        # print list_ofNod
        # print len(G.nodes()),len(snodds),len(list_ofNod),'dddddddddd'
        for ii,jj in snodds.items():
            # print ii,jj
            row_nd.append(jj[0])
            row_comp.append(jj[0]-lenghts[nd][ii])
            vals=ffv %jj[1]
            # print vals,'llllllllll',ffv
            row_val.append(vals)
        # print iterations,nd,sas
        if sas!='rand':
            print 'Iterations %i and source %i with sa= [%.4f, %.4f]' %(iterations,nd,sas[0],sas[1])
        elif sas=='rand':
            print 'Iterations %i and source %i with sa= random' %(iterations,nd)#,sas[0],sas[1])
        # print len(row_nd),len(list_ofNod)
        # table_of_no_zero_time.add_row(row_nd)
        # table_of_comparison.add_row(row_comp)
        # table_of_no_zero_val.add_row(row_val)
        no_zero_time_dict[nd]=row_nd
        no_zero_val_dict[nd]=row_val
    
        comparison_dict[nd]=row_comp
        ch=True

        for ii,jj in enumerate(G.nodes()):
            if ch:
                iii=ii
            else:
                iii=ii-1
            if jj in source:
                ch=False
                iii=ii+1
                row_end.append(0)
                row_steady.append(ffvs %1.)
                row_steady_sols.append(1.)
                continue
            row_steady.append(ffvs %dav.item(iii))
            row_steady_sols.append(dav.item(iii))
            # print ffvs %dav.item(iii)

            kk = y_all[jj]
            for ll,hh in enumerate(kk):
                # print ll,hh
                # 
                if abs(hh-dav.item(iii)) <= precision:
                    row_end.append(ll)
                    break
        table_of_no_iterations.add_row(row_end)
        table_of_steady_sols.add_row(row_steady)
        steady_sols_dict[nd]=row_steady
        steady_sols_dict_t[nd]=row_steady_sols
        no_iterations_dict[nd]=row_end
# steady_sols_dict={}
    # no_zero_time_dict={}
    # no_zero_val_dict={}
    # no_iterations_dict={}
    # comparison_dict={}
    # for kkv,vvk in steady_sols_dict.items():
    #     print kkv,vvk
    # print steady_sols_dict
    # for 
    # import pickle
    # dic_of_Graphs_final,  edgelist ,nmap ,mapping
    fop=open('ssas_ds.dmp','w')
    pickle.dump(ssas_ds,fop)
    fop.close()
    crim.create_hist_sa_sea(G,list_ofNod,steady_sols_dict,dic_of_nodes_multi,ssas_ds,outfile_name='sub_hist_sa_out.png')
    crim.create_heat_maps_sea(G,list_ofNod,steady_sols_dict,dic_of_nodes_multi,ssas_ds,outfile_name='sub_heat_out.png')
    data_s=crim.create_tex_tabul(G,list_ofNod,steady_sols_dict,dic_of_nodes_multi,outfile_name='stead_sols.tex')
    crim.create_heat_maps_sea_s(G,list_ofNod,steady_sols_dict,dic_of_nodes_multi,ssas_ds,data_s,vm_s='stead_sols',outfile_name='3d.png')
    data_s=crim.create_tex_tabul(G,list_ofNod,no_iterations_dict,dic_of_nodes_multi,outfile_name='NoofIterations.tex')
    crim.create_heat_maps_sea_s(G,list_ofNod,steady_sols_dict,dic_of_nodes_multi,ssas_ds,data_s,vm_s='NoofIterations',outfile_name='3c.png')
    data_s=crim.create_tex_tabul(G,list_ofNod,no_zero_time_dict,dic_of_nodes_multi,outfile_name='NoofZeroTime.tex')
    crim.create_heat_maps_sea_s(G,list_ofNod,steady_sols_dict,dic_of_nodes_multi,ssas_ds,data_s,vm_s='NoofZeroTime',outfile_name='3a.png')
    data_s=crim.create_tex_tabul(G,list_ofNod,no_zero_val_dict,dic_of_nodes_multi,outfile_name='NoofZeroVal.tex')
    crim.create_heat_maps_sea_s(G,list_ofNod,steady_sols_dict,dic_of_nodes_multi,ssas_ds,data_s,vm_s='NoofZeroVal',outfile_name='3b.png')
    crim.create_tex_tabul(G,list_ofNod,comparison_dict,dic_of_nodes_multi,outfile_name='Compare_NS_S.tex')

    tem_dici,dici_tem= crim.create_tex_sum_steady(G,list_ofNod,steady_sols_dict_t,dic_of_nodes_multi,outfile_name='inOut.tex')
    crim.create_hist_in_out(dici_tem,tem_dici)#,outfile_name='hist_in_out_sea.png')
    
    # print sum(tem_dici.values())
    # print sum(dici_tem.values())
    crim.create_tex_sum_steady_sub(G,k,list_ofNod,steady_sols_dict_t,dic_of_nodes_multi,outfile_name='inOut_sub.tex')
    cent_dict=crim.create_tex_sum_central(G,tem_dici,dici_tem,dic_of_nodes_multi,outfile_name='scent_out.tex')
    idici_tem,item_dici,odici_tem,otem_dici=crim.create_inf_nei_clos(G,list_ofNod,steady_sols_dict_t,dic_of_nodes_multi)
    dinf_cinf_d=crim.create_dinf_tex(G,idici_tem,item_dici,odici_tem,otem_dici,list_ofNod,sas,ssas_ds)
    # print idici_tem,item_dici
    # print odici_tem,otem_dici
    # print aaaa
    def calc_centralization(dat_fr,col):
        mono=0
        dmax=max(dat_fr)
        for i in dat_fr:
            mono+=dmax-i
        return mono/len(dat_fr)


    import pandas as pd
    dinf_cinf_data=pd.DataFrame(dinf_cinf_d,columns=['Node','In-DINF', 'OB-Degree CI' , 'In-CINF'  , 'OB-Closeness CI'   ,'Degree'  , 'Closeness'])
    crim.create_pairplot_df(dinf_cinf_data)#,columns=['In-DINF', 'Out-DINF' , 'In-CINF'  , 'Out-CINF'   ,'Degree'  , 'Closeness'],outfile_name='pairplot_cdin_cdout_sea.png')
    # print aaa
    cent_data=[]#pd.DataFrame(cent_dict,columns=['Node' , 'In' , 'Out' , 'Degree'  , 'Closeness'  , 'Betweenness' , 'Eigenvector'  , 'Katz' , 'PageRank' , 'Communicability'])
    # print cent_data
    # print aaaa
    for kk,vv in cent_dict.items():
        # lldd=[kk]
        # print kk,vv
        # for vi in vv:
        #     lldd.append(vi)
            # print kk,lldd
        # print kk,vv
        cent_data.append(list(vv))
    # print cent_data
    # for kk in cent_data:
    #     print kk
    cent_data=pd.DataFrame(np.matrix(cent_data),columns=['Node' , 'In' , 'Out' , 'Degree'  , 'Closeness'  , 'Betweenness' , 'Eigenvector'  , 'Katz' , 'PageRank' , 'Communicability','Layer'])
    crim.create_pairplot(cent_data,columns=[ 'In' , 'Out' , 'Degree'  , 'Closeness'  , 'Betweenness' , 'Eigenvector'  , 'Katz' , 'PageRank' , 'Communicability'])
    # print cent_data
    # import seaborn as sns
    # import matplotlib.pyplot as plt
    # sns.set_context(rc={'lines.markeredgewidth': 0.1})
    # fig=plt.figure(figsize=(16,16))
    # axa=sns.pairplot(cent_data,vars=['In','Out'])
    # plt.show()
    # print aaa
    # ndata=np.array(lab)
    # ndata=np.matrix(ndata)
    # data=pd.DataFrame(ndata,columns=['In','Out'])
    # print 'Table of first no zero value time'
    # print table_of_no_zero_time.get_html_string(format=True)
    # print 
    # print 'Table of first no zero value value'
    # print table_of_no_zero_val.get_html_string(format=True)
    # print
    # print 'Table of iterations with precision %f ' %precision
    # print table_of_no_iterations
    # print 'Table of diffs shortest path' 
    # print table_of_comparison
    return (table_of_no_zero_time.get_html_string(format=True),table_of_no_zero_val.get_html_string(format=True),
            table_of_no_iterations.get_html_string(format=True),table_of_comparison.get_html_string(format=True),
            table_of_steady_sols.get_html_string(format=True))

def steady_sols_calc_multi_one_sim(k,G,dic_of_Graphs_final,n,p,sas,edgelist,iterations,fjfun,presion=.1,precision=.3,sa_u=0,source_u=[1.],su=1.,h=1.,form_float_val=6,form_float_val_stead=6):
    nodes=len(G.nodes())
    dic_of_nodes_multi={}
    for i in range(k):
        for j in range(i,k):
            # print i,j,uucount
            # ssas_ds[(i,j)]={}
            if i==j:
                dic_of_nodes_multi[i]=dic_of_Graphs_final[(i,j)].nodes()
    # dic_of_nodes_multi_r={}
    # for i,v in dic_of_nodes_multi:

    G.remove_nodes_from(nx.isolates(G))
    stt= '%i' %form_float_val
    # print stt
    ffv='%.' + stt+'f'
    stt= '%i' %form_float_val_stead
    ffvs='%.' + stt+'f'
    p=0.1
    lenghts=nx.all_pairs_shortest_path_length(G)
    list_ofNod=['Node/Node']
    # print len(G.nodes())
    # print G.nodes()
    for i in G.nodes():
        list_ofNod.append(i)
    # table_of_no_zero_time = PrettyTable(list_ofNod)
    # table_of_no_zero_val = PrettyTable(list_ofNod)
    # table_of_no_iterations = PrettyTable(list_ofNod)
    # table_of_comparison=PrettyTable(list_ofNod)
    # table_of_steady_sols=PrettyTable(list_ofNod)
    steady_sols_dict={}
    steady_sols_dict_t={}
    # no_zero_time_dict={}
    # no_zero_val_dict={}
    # no_iterations_dict={}
    # comparison_dict={}
  
    # while infa<1.:
    #     while infb<1.:

    for nd in G.nodes():
        infa=0.
        
        if nd not in steady_sols_dict_t:
            steady_sols_dict_t[nd]={}
            steady_sols_dict[nd]={}
        ssas_ds={}
        source=[nd]
        # if len(source)==0:
        #     source = [closse[-1]]
        #     source_u=[su]
        #     ssas_ds[closse[-1]]=0
        # else:
        for nod  in source:
            for i in range(k):
                for j in range(i,k):
                    # ssas_ds[(i,j)]={}
                    ssas_ds[nod]=sa_u
        while infa-1.<=presion-(presion/2):
            infb=0.
            if infa not in steady_sols_dict_t[nd]:
                steady_sols_dict_t[nd][infa]={}
                steady_sols_dict[nd][infa]={}
            while infb-1.<=presion-(presion/2):
                if infb not in  steady_sols_dict_t[nd][infa]:
                    steady_sols_dict_t[nd][infa][infb]={}
                    steady_sols_dict[nd][infa][infb]={}

                uucount=0
                for i in range(k):
                    for j in range(i,k):
                        # print i,j,uucount
                        # ssas_ds[(i,j)]={}
                        if i==j:
                            gg=dic_of_Graphs_final[(i,j)].nodes()
                            # print gg,i,j
                            for nod in gg:
                                if nod not in source:
                                    if nod in dic_of_nodes_multi[0]:
                                        ssas_ds[nod]=infa
                                    elif nod in dic_of_nodes_multi[1]:
                                        ssas_ds[nod]=infb
                                    # if sas!='rand':
                                    #     ssas_ds[nod]=sas[uucount]
                                    # elif sas=='rand':
                                    #     ssas_ds[nod]=random.random()
                            uucount+=1
                # F,y_all,source,y_orig,final_d,snodds=influence_sim_dh_F_J_mu(nodes,p,iterations,
                #     G=G,new_old=None,source=source,source_u=source_u,su=su,h=h,
                #     funcion=fjfun,insrplot=False,ssas_d=ssas_ds)   
                # print ssas_ds
                dav=steady_sol_calc(G,source,ssas_ds,iterations)
                # row_nd=[nd]
                # row_val=[nd]
                # row_end=[nd]
                # row_comp=[nd]
                row_steady=[nd]
                row_steady_sols=0
                # for ii,jj in snodds.items():
                #     # print ii,jj
                #     row_nd.append(jj[0])
                #     row_comp.append(jj[0]-lenghts[nd][ii])
                #     vals=ffv %jj[1]
                #     # print vals,'llllllllll',ffv
                #     row_val.append(vals)
                # print iterations,nd,sas
                # if sas!='rand':
                # print 'Iterations %i and source %i with sa= [%.4f, %.4f]' %(iterations,nd,infa,infb)
                # elif sas=='rand':
                #     print 'Iterations %i and source %i with sa= random' %(iterations,nd)#,sas[0],sas[1])
                # no_zero_time_dict[nd]=row_nd
                # no_zero_val_dict[nd]=row_val
            
                # comparison_dict[nd]=row_comp
                ch=True

                for ii,jj in enumerate(G.nodes()):
                    if ch:
                        iii=ii
                    else:
                        iii=ii-1
                    if jj in source:
                        ch=False
                        iii=ii+1
                        # row_end.append(0)
                        # row_steady.append(ffvs %1.)
                        row_steady.append(0)
                        row_steady_sols+=0.
                        continue
                    row_steady.append(dav.item(iii))
                    row_steady_sols+=dav.item(iii)
                    # print ffvs %dav.item(iii)

                    # kk = y_all[jj]
                    # for ll,hh in enumerate(kk):
                    #     # print ll,hh
                    #     # 
                    #     if abs(hh-dav.item(iii)) <= precision:
                    #         row_end.append(ll)
                    #         break
                # table_of_no_iterations.add_row(row_end)
                # table_of_steady_sols.add_row(row_steady)
                # steady_sols_dict[nd]=row_steady
                steady_sols_dict_t[nd][infa][infb]=row_steady_sols
                steady_sols_dict[nd][infa][infb]=row_steady
                infb+=presion
            infa+=presion
        # print steady_sols_dict_t.keys()
        # print infa,infb
        print 'Iterations %i and source %i ' %(iterations,nd)#,infa,infb)
    print sorted(steady_sols_dict_t[0].keys())
    # for nd,vv in steady_sols_dict:
    idici_tem,item_dici,odici_tem,otem_dici=crim.create_inf_nei_clos_s(G,list_ofNod,steady_sols_dict,dic_of_nodes_multi)
    cinf,    cout,    dinf,    dout=crim.create_dinf_tex_s(G,idici_tem,item_dici,odici_tem,otem_dici,list_ofNod)
    # print cinf,   cout,    dinf,    dout
    # print aaa
    # 
    # print idici_tem,item_dici
    # print odici_tem,otem_dici
    # print aaaa
    def calc_centralization(dat_fr):
        dici={}
        for l,v in dat_fr.items():
            mono=0
            dmax=max(v)
            for i in v:
                mono+=dmax-i
            dici[l]=mono/len(dat_fr)
        return dici

    cinf=calc_centralization(cinf)
    cout=calc_centralization(cout)
    dinf=calc_centralization(dinf)
    dout=calc_centralization(dout)
    # print cinf
    # print aaaa
    # import pickle
    
    fop=open('cinf.dmp','w')
    pickle.dump(cinf,fop)
    fop.close()
    fop=open('cout.dmp','w')
    pickle.dump(cout,fop)
    fop.close()
    fop=open('dinf.dmp','w')
    pickle.dump(dinf,fop)
    fop.close()
    fop=open('dout.dmp','w')
    pickle.dump(dout,fop)
    fop.close()


    st_dat={}
    cinf_dinf_dat={}
    for nd,v in steady_sols_dict_t.items():
        for infaf in v:
            vv=v[infaf]
            for infbf in vv:
                if (infaf,infbf) not in st_dat:
                    st_dat[(infaf,infbf)]=vv[infbf]

                else:
                    st_dat[(infaf,infbf)]+=vv[infbf]

    f= open('steady_sols_dict_t.dmp','w')
    pickle.dump(steady_sols_dict_t,f)
    f.close()
    f=open('Out_data_sum1.txt','w')
    for i in sorted(st_dat.keys()):
        f.write('%f,%f,%f\n' %(i[0],i[1],st_dat[i]))
    f.close()
    f=open('Out_data_sum1_nd.txt','w')
    # for i in 
    # print aaa
    # for nd,v in steady_sols_dict_t.items():
    #     st_dat=[]
    #     for infa,vv in v.items():
    #         for infb,vvv in vv.items():
    #             ml=(infa,infb,vvv)
    #             st_dat.append(ml)
    #     # print nd,st_dat
    #     crim.create_contures(st_dat,'%s_' %str(nd))
    # print aaa
    #         # no_iterations_dict[nd]=row_end
    # crim.create_hist_sa_sea(G,list_ofNod,steady_sols_dict,dic_of_nodes_multi,ssas_ds,outfile_name='sub_hist_sa_out.png')
    # crim.create_heat_maps_sea(G,list_ofNod,steady_sols_dict,dic_of_nodes_multi,ssas_ds,outfile_name='sub_heat_out.png')
    # crim.create_tex_tabul(G,list_ofNod,steady_sols_dict,dic_of_nodes_multi,outfile_name='stead_sols.tex')
    # crim.create_tex_tabul(G,list_ofNod,no_iterations_dict,dic_of_nodes_multi,outfile_name='NoofIterations.tex')
    # crim.create_tex_tabul(G,list_ofNod,no_zero_time_dict,dic_of_nodes_multi,outfile_name='NoofZeroTime.tex')
    # crim.create_tex_tabul(G,list_ofNod,no_zero_val_dict,dic_of_nodes_multi,outfile_name='NoofZeroVal.tex')
    # crim.create_tex_tabul(G,list_ofNod,comparison_dict,dic_of_nodes_multi,outfile_name='Compare_NS_S.tex')
    # tem_dici,dici_tem= crim.create_tex_sum_steady(G,list_ofNod,steady_sols_dict_t,dic_of_nodes_multi,outfile_name='inOut.tex')
    # crim.create_hist_in_out(dici_tem,tem_dici)#,outfile_name='hist_in_out_sea.png')
    
    # # print sum(tem_dici.values())
    # # print sum(dici_tem.values())
    # crim.create_tex_sum_steady_sub(G,list_ofNod,steady_sols_dict_t,dic_of_nodes_multi,outfile_name='inOut_sub.tex')
    # cent_dict=crim.create_tex_sum_central(G,tem_dici,dici_tem,dic_of_nodes_multi,outfile_name='scent_out.tex')
    # import pandas as pd
    # cent_data=[]#pd.DataFrame(cent_dict,columns=['Node' , 'In' , 'Out' , 'Degree'  , 'Closeness'  , 'Betweenness' , 'Eigenvector'  , 'Katz' , 'PageRank' , 'Communicability'])
    # # print cent_data
    # # print aaaa
    # for kk,vv in cent_dict.items():
    #     # lldd=[kk]
    #     cent_data.append(list(vv))
    # cent_data=pd.DataFrame(np.matrix(cent_data),columns=['Node' , 'In' , 'Out' , 'Degree'  , 'Closeness'  , 'Betweenness' , 'Eigenvector'  , 'Katz' , 'PageRank' , 'Communicability','Layer'])
    # crim.create_pairplot(cent_data,columns=[ 'In' , 'Out' , 'Degree'  , 'Closeness'  , 'Betweenness' , 'Eigenvector'  , 'Katz' , 'PageRank' , 'Communicability'])
    # return (table_of_no_zero_time.get_html_string(format=True),table_of_no_zero_val.get_html_string(format=True),
    #         table_of_no_iterations.get_html_string(format=True),table_of_comparison.get_html_string(format=True),
    #         table_of_steady_sols.get_html_string(format=True))




def steady_sols_calc_multi(k,G,dic_of_Graphs_final,n,p,sas,edgelist,iterations,fjfun,precision=.3,sa_u=0,source_u=[1.],su=1.,h=1.,form_float_val=6,form_float_val_stead=6):
    nodes=len(G.nodes())
    stt= '%i' %form_float_val
    # print stt
    ffv='%.' + stt+'f'
    stt= '%i' %form_float_val_stead
    ffvs='%.' + stt+'f'
    p=0.1
    lenghts=nx.all_pairs_shortest_path_length(G)
    list_ofNod=['Node/Node']
    for i in G.nodes():
        list_ofNod.append(i)
    table_of_no_zero_time = PrettyTable(list_ofNod)
    table_of_no_zero_val = PrettyTable(list_ofNod)
    table_of_no_iterations = PrettyTable(list_ofNod)
    table_of_comparison=PrettyTable(list_ofNod)
    table_of_steady_sols=PrettyTable(list_ofNod)
    for nd in G.nodes():
        ssas_ds={}
        source=[nd]
        if len(source)==0:
            source = [closse[-1]]
            source_u=[su]
            ssas_ds[closse[-1]]=0
        else:
            for nod  in source:
                for i in range(k):
                    for j in range(i,k):
                        ssas_ds[(i,j)]={}
                        ssas_ds[(i,j)][nod]=sa_u
        # print ssas_ds
        # print aaa
        uucount=0
        for i in range(k):
            for j in range(i,k):
                # print i,j,uucount
                # ssas_ds[(i,j)]={}

                gg=dic_of_Graphs_final[(i,j)].nodes()
                for nod in gg:
                    if nod not in source:
                        ssas_ds[(i,j)][nod]=sas[uucount]
                uucount+=1
        # print ssas_ds
        # print aaa
        # for nod in set(G.nodes())-set(source):
        #     ssas_ds[nod]=sa
        F,y_all,source,y_orig,final_d,snodds=influence_sim_dh_F_J_multi(k,nodes,p,ssas_ds,iterations,
            G,dic_of_Graphs_final,new_old=None,source=source,source_u=source_u,su=su,h=h,
            funcion=fjfun,insrplot=False)
        # print y_all
        print source
        print y_orig
        print final_d
        print snodds
        # print aaa
        dav=steady_sol_calc(G,F,source,ssas_ds,iterations,y_all)
        row_nd=[nd]
        row_val=[nd]
        row_end=[nd]
        row_comp=[nd]
        row_steady=[nd]
        # print snodds
        # print aaaa
        for ii,jj in snodds.items():
            row_nd.append(jj[0])
            row_comp.append(jj[0]-lenghts[nd][ii])
            vals=ffv %jj[1]
            # print vals,'llllllllll',ffv
            row_val.append(vals)
        print 'Iterations %i and source %i with sa= %.4f' %(iterations,nd,sas)
        # print len(row_nd),len(row_nd)
        table_of_no_zero_time.add_row(row_nd)
        table_of_comparison.add_row(row_comp)
        table_of_no_zero_val.add_row(row_val)
        ch=True

        for ii,jj in enumerate(G.nodes()):
            if ch:
                iii=ii
            else:
                iii=ii-1
            if jj in source:
                ch=False
                iii=ii+1
                row_end.append(0)
                row_steady.append(ffvs %1.)
                continue
            row_steady.append(ffvs %dav.item(iii))
            # print ffvs %dav.item(iii)

            kk = y_all[jj]
            for ll,hh in enumerate(kk):
                # print ll,hh
                if abs(hh-dav.item(iii)) <= precision:
                    row_end.append(ll)
                    break
        table_of_no_iterations.add_row(row_end)
        table_of_steady_sols.add_row(row_steady)
    # print 'Table of first no zero value time'
    # print table_of_no_zero_time.get_html_string(format=True)
    # print 
    # print 'Table of first no zero value value'
    # print table_of_no_zero_val.get_html_string(format=True)
    # print
    # print 'Table of iterations with precision %f ' %precision
    # print table_of_no_iterations
    # print 'Table of diffs shortest path' 
    # print table_of_comparison
    return (table_of_no_zero_time.get_html_string(format=True),table_of_no_zero_val.get_html_string(format=True),
            table_of_no_iterations.get_html_string(format=True),table_of_comparison.get_html_string(format=True),
            table_of_steady_sols.get_html_string(format=True))


# from chAs import synthetic_multi_level_bip_dic
# k=3
# iterations=100
# fjfun='ssa*xnei[(iij,jji)]+(1-ssa)*y_orig[nd]'
# fjfun='ssas_ds[(iij,jji)][nd]*xnei[(iij,jji)][nd]'#+(1-ssa)*y_orig[nd]'
#                     # xnei[(iij,jji)]=uu/len(nei)   ssas_ds
# fjfun2='ssas_ds[(iij,jji)]*xnei[(iij,jji)]'#+(1-ssa)*y_orig[nd]'

# sas=[.11,.12,.13,.22,.23,.33]
# n=[10,5,30]
# p=[.11,.12,.13,.22,.23,.33]
# G, dic_of_Graphs_final,  edgelist ,nmap ,mapping=synthetic_multi_level_bip_dic(k,n=[10,5,30],p=[.11,.12,.13,.22,.23,.33])
# steady_sols_calc_multi(k,G,dic_of_Graphs_final,n,p,sas,edgelist,iterations,fjfun,precision=.3,sa_u=0,source_u=[1.],su=1.,h=1.,form_float_val=6,form_float_val_stead=6)
