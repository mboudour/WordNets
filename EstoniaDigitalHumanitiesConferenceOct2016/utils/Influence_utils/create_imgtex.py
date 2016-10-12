import itertools
import networkx as nx
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
sns.set(style="white")

def create_tex_tabul(G,list_ofNod,steady_dict,dic_of_nodes_multi,outfile_name='tab_out.tex'):
    print outfile_name

    fop=open(outfile_name,'w')
    lat=r'''\documentclass[10pt]{article}

\usepackage{lscape}
\usepackage{adjustbox}
\begin{document}
 \global\pdfpageattr\expandafter{\the\pdfpageattr/Rotate 90}
\begin{landscape}
\begin{table}[ht]
\centering
\begin{adjustbox}{width=2\textwidth,center=\textwidth}
\small
\begin{tabular}{'''.decode('utf-8')
    fop.write(lat)
    # fop.write('\n')
    lats=r'|'
    latl=r'   '
    for i in list_ofNod:
        latl+='%s' %i +' & '
        if i =='Node/Node':
            lats+='c||'

        elif i == dic_of_nodes_multi[0][-1]:
            lats+='r||'
        else:
            lats+='r|'
    lats+='}\n'+'\hline'
    latl=latl[:-2]
    latl+='\\\ '+'\n'+'\hline \hline'+'\n'
    fop.write(lats)
    fop.write('\n')
    fop.write(latl)
    latll=r''
    noad=[]
    uu=0
    for i in list_ofNod:
        if i =='Node/Node':
            continue
        else:
            # if uu==0:
            nlnl=[]
            for kk,ii in enumerate(steady_dict[i]):
                latll+='%s & ' %ii
                if kk>0:
                    nlnl.append(ii)
            latll=latll[:-2]
            if i ==dic_of_nodes_multi[0][-1]:
                latll+='\\\ \n \hline \hline'+'\n'
            else:
                latll+='\\\ \n \hline '+'\n'
            uu+=1
            # if uu==len(G.nodes()):
            #     uu=0
            noad.append(nlnl)
    fop.write(latll)
    fop.write(r'''\end{tabular}
\end{adjustbox}
\end{table}

\end{landscape}
\end{document}'''.decode('utf-8'))
    fop.close()
    return noad


def create_tex_sum_steady(G,list_ofNod,steady_dict,dic_of_nodes_multi,outfile_name='sttab_out.tex'):
    print outfile_name
    # print list_ofNod,dic_of_nodes_multi
    fop=open(outfile_name,'w')
    lat=r'''\documentclass[10pt]{article}

\usepackage{lscape}
\usepackage{adjustbox}
\begin{document}
 %\global\pdfpageattr\expandafter{\the\pdfpageattr/Rotate 90}

\begin{table}[ht]
\centering
\begin{adjustbox}{width=1\textwidth,center=\textwidth}
\small
\begin{tabular}{|c||r|r|r|r|} \hline 
    Node/In-Out-sums & In & Out & Av-In & Av-Out\\ 
    \hline \hline'''.decode('utf-8')
    fop.write(lat)
    fop.write('\n')
    # lats=r'|'
    latl=r'   '
    dici_tem={}
    tem_dici={}
    # print steady_dict
    # print len()
    for i in list_ofNod:
        if i =='Node/Node':# or kk==0:
            continue

        for kk,j in enumerate(list_ofNod[1:]):

            # print steady_dict[i],j,kk
        # for j in steady_dict[i]:
            if j not in dici_tem:

                dici_tem[j]=steady_dict[i][kk]
            else:
                dici_tem[j]+=steady_dict[i][kk]
    # print dici_tem
    # print steady_dict
    # latll=r''
    for kk,i in enumerate(list_ofNod):
        sumout=0
        if i =='Node/Node':
            continue
        else:
            # for 
            for ii in steady_dict[i]:
                sumout+=ii
        tem_dici[i]=sumout
        latl+='%s & %.6f & %.6f & %.6f & %.6f' %(i,dici_tem[i]-1 ,sumout-1,(dici_tem[i]-1)/len(list_ofNod[2:]),(sumout-1)/len(list_ofNod[2:]))
            # latll=latll[:-2]
        if i ==dic_of_nodes_multi[0][-1]:
            latl+='\\\ \n  \hline'+'\n'
        else:
            latl+='\\\ \n \hline '+'\n'
    fop.write(latl)
    fop.write(r'''\end{tabular}
\end{adjustbox}
\end{table}

\end{document}'''.decode('utf-8'))
    fop.close()
    return tem_dici,dici_tem

def create_tex_sum_central(G,tem_dici,dici_tem,dic_of_nodes_multi,outfile_name='scent_out.tex'):
    print outfile_name
    # print list_ofNod,dic_of_nodes_multi
    fop=open(outfile_name,'w')
    lat=r'''\documentclass[10pt]{article}

\usepackage{lscape}
\usepackage{adjustbox}
\begin{document}
 %\global\pdfpageattr\expandafter{\the\pdfpageattr/Rotate 90}

\begin{table}[ht]
\centering
\begin{adjustbox}{width=1\textwidth,center=\textwidth}
\small
\begin{tabular}{|c||r|r|r|r|r|r|r|r|r||} \hline 
    Node/Centralities & In & Out & Degree  & Closeness  & Betweenness & Eigenvector  & Katz & PageRank & Communicability  \\ 
    \hline \hline'''.decode('utf-8')
    fop.write(lat)
    fop.write('\n')
    degce=nx.degree_centrality(G)
    cloce=cent=nx.closeness_centrality(G)
    becen=nx.betweenness_centrality(G)
    eigce=nx.eigenvector_centrality(G,max_iter=2000)
    katce=nx.katz_centrality_numpy(G)#,1/phi-0.01)
    pagce=nx.pagerank(G)
    # comce=nx.communicability_centrality(G)
    comce=nx.communicability_centrality_exp(G)
    from scipy import stats
    dic_of_nodes_multi_r={ii:i for i,v in dic_of_nodes_multi.items() for ii in v}
    # print stats.pearsonr(degce.values(),dici_tem.values())
    # lats=r'|'
    cent_dics={}
    latl=r'   '
    for i in dici_tem:
        latl+='%i & %.6f & %.6f & %.6f & %.6f & %.6f & %.6f & %.6f & %.6f & %.6f ' %(i, dici_tem[i]/15.,
            tem_dici[i]/15.,degce[i],cloce[i],becen[i],eigce[i],katce[i],pagce[i],comce[i])+r'''\\  \hline
'''.decode('utf-8')
        cent_dics[i]=(i, dici_tem[i]/15.,
            tem_dici[i]/15.,degce[i],cloce[i],becen[i],eigce[i],katce[i],pagce[i],comce[i],dic_of_nodes_multi_r[i])
    fop.write(latl)
    fop.write('In & %.6f  &   & %.6f & %.6f & %.6f & %.6f & %.6f & %.6f & %.6f ' %(sum(dici_tem.values()), stats.pearsonr(degce.values(),dici_tem.values())[0]
        ,stats.pearsonr(cloce.values(),dici_tem.values())[0],stats.pearsonr(becen.values(),dici_tem.values())[0],
        stats.pearsonr(eigce.values(),dici_tem.values())[0],stats.pearsonr(katce.values(),dici_tem.values())[0],
        stats.pearsonr(pagce.values(),dici_tem.values())[0],stats.pearsonr(comce.values(),dici_tem.values())[0]) +r'''\\  \hline
'''.decode('utf-8'))
    fop.write('Out &   &  %.6f  & %.6f & %.6f & %.6f & %.6f & %.6f & %.6f & %.6f ' %(sum(tem_dici.values()), stats.pearsonr(degce.values(),tem_dici.values())[0]
        ,stats.pearsonr(cloce.values(),tem_dici.values())[0],stats.pearsonr(becen.values(),tem_dici.values())[0],
        stats.pearsonr(eigce.values(),tem_dici.values())[0],stats.pearsonr(katce.values(),tem_dici.values())[0],
        stats.pearsonr(pagce.values(),tem_dici.values())[0],stats.pearsonr(comce.values(),tem_dici.values())[0]) +r'''\\  \hline
'''.decode('utf-8'))


    # # print steady_dict
    # # print len()
    # for i in list_ofNod:
    #     if i =='Node/Node':# or kk==0:
    #         continue

    #     for kk,j in enumerate(list_ofNod[1:]):

    #         # print steady_dict[i],j,kk
    #     # for j in steady_dict[i]:
    #         if j not in dici_tem:

    #             dici_tem[j]=steady_dict[i][kk]
    #         else:
    #             dici_tem[j]+=steady_dict[i][kk]
    # # print dici_tem
    # # print steady_dict
    # # latll=r''
    # for kk,i in enumerate(list_ofNod):
    #     sumout=0
    #     if i =='Node/Node':
    #         continue
    #     else:
    #         # for 
    #         for ii in steady_dict[i]:
    #             sumout+=ii
    #     tem_dici[i]=sumout
    #     latl+='%s & %.6f & %.6f & %.6f & %.6f' %(i,dici_tem[i] ,sumout,dici_tem[i]/len(list_ofNod[1:]),sumout/len(list_ofNod[1:]))
    #         # latll=latll[:-2]
    #     if i ==dic_of_nodes_multi[0][-1]:
    #         latl+='\\\ \n \hline \hline'+'\n'
    #     else:
    #         latl+='\\\ \n \hline '+'\n'
    # fop.write(latl)
    fop.write(r'''\hline 
\end{tabular}
\end{adjustbox}
\end{table}

\end{document}'''.decode('utf-8'))
    fop.close()
    return cent_dics

def create_inf_nei_clos_s(G,list_ofNod,steady_dict,dic_of_nodes_multi,outfile_name='nei.tex'):
    idici_tem={}
    item_dici={}
    odici_tem={}
    otem_dici={}
    for nd in list_ofNod[1:]:
        v=steady_dict[nd]
   # for nd,v in steady_dict.items():
        idici_tem[nd]={}
        item_dici[nd]={}
        # odici_tem[nd]={}
        # otem_dici[nd]={}
        for infa in v:
            sumout=0
            vv=v[infa]
            for infb in vv:
                vvv=steady_dict[nd][infa][infb]
                if (infa,infb) not in idici_tem[nd]:
                    idici_tem[nd][(infa,infb)]=0
                if (infa,infb) not in item_dici[nd]:
                    item_dici[nd][(infa,infb)]=0
                    
                nei=G.neighbors(nd)
                # for infa
                for kk,j in enumerate(list_ofNod[1:]):

                    if j in nei:
                        sumout+=vvv[kk]
                    # print vvv,j,kk
                # for j in vvv:

                        if j not in idici_tem:
                            idici_tem[j]={(infa,infb):vvv[kk]}

                            # idici_tem[j][(infa,infb)]=vvv[kk]
                        else:
                            if (infa,infb) not in idici_tem[j]:
                                idici_tem[j][(infa,infb)]=vvv[kk]
                            else:
                                # print idici_tem[j][(infa,infb)],vvv[kk]
                                idici_tem[j][(infa,infb)]+=vvv[kk]
            item_dici[nd][(infa,infb)]=sumout
    for nd in list_ofNod[1:]:
        v=steady_dict[nd]
   # for nd,v in steady_dict.items():
        # idici_tem[nd]={}
        # item_dici[nd]={}
        odici_tem[nd]={}
        otem_dici[nd]={}
        for infa in v:
            vv=v[infa]
            for infb in vv:
                vvv=steady_dict[nd][infa][infb]
                if (infa,infb) not in odici_tem[nd]:
                    # idici_tem[nd][(infa,infb)]={}
                    # item_dici[nd][(infa,infb)]={}
                    odici_tem[nd][(infa,infb)]=0
                    otem_dici[nd][(infa,infb)]=0
    # for i in list_ofNod[1:]:
        # if i =='Node/Node':# or kk==0:
                sumout=0
                # nei=G.neighbors(i)
                for kk,j in enumerate(list_ofNod[1:]):
                    lpa=nx.shortest_path_length(G,nd,j)

                    # if j in nei:
                    sumout+=vvv[kk]*lpa

                    if j not in odici_tem:

                        odici_tem[j]={(infa,infb):vvv[kk]*lpa}
                        # idici_tem[j]={(infa,infb):vvv[kk]}

                    else:
                        if (infa,infb) not in odici_tem[j]:
                            odici_tem[j][(infa,infb)]=vvv[kk]*lpa
                        else:
                            odici_tem[j][(infa,infb)]+=vvv[kk]*lpa
            otem_dici[nd][(infa,infb)]=sumout
    return idici_tem,item_dici,odici_tem,otem_dici
        #     continue
def create_dinf_tex_s(G,idici_tem,item_dici,odici_tem,otem_dici,list_ofNod,outfile_name='In_out_dinf.tex'):
    # print outfile_name
    # print list_ofNod,dic_of_nodes_multi
    # fop=open(outfile_name,'w')
#     lat=r'''\documentclass[10pt]{article}

# \usepackage{lscape}
# \usepackage{adjustbox}
# \begin{document}
#  %\global\pdfpageattr\expandafter{\the\pdfpageattr/Rotate 90}

# \begin{table}[ht]
# \centering
# \begin{adjustbox}{width=1\textwidth,center=\textwidth}
# \small
# \begin{tabular}{|c||r|r|r|r|r|r||} \hline 
#     Node/*INF & In-DINF & Out-DINF & In-CINF  & Out-CINF &  Degree  & Closeness  \\ 
#     \hline \hline'''.decode('utf-8')
#     fop.write(lat)
    # fop.write('\n')
    degce=nx.degree_centrality(G)
    cloce=cent=nx.closeness_centrality(G)
    momo=len(list_ofNod[1:])-1
    # print list_ofNod,momo
    cinf={}
    cout={}
    dinf={}
    dout={}
    
    for i in list_ofNod[1:]:
        for infs in idici_tem[i]:
            if odici_tem[i][infs]==0:
                # print i,infs
                odici=100
            else:
                odici=odici_tem[i][infs]
            if otem_dici[i][infs] ==0:
                otem=100
            else:
                otem=otem_dici[i][infs]
            if infs not in cinf:
                cinf[infs]=[idici_tem[i][infs]/momo]
            else:
                cinf[infs].append(idici_tem[i][infs]/momo)
            if infs not in cout:
                cout[infs]=[item_dici[i][infs]/momo]
            else:
                # cinf[infs].append(idici_tem[i][infs]/momo)
                cout[infs].append(item_dici[i][infs]/momo)
                # if odici_tem[i][infs]==0:
                #     odici=100000
                # else:
                #     odici=odici_tem[i][infs]
            if infs not in dinf:
                dinf[infs]=[momo/odici]
            else:
                # cinf[infs].append(idici_tem[i][infs]/momo)
                # cout[infs].append(item_dici[i][infs]/momo)
                dinf[infs].append(momo/odici)
                # if otem_dici[i][infs] ==0:
                #     otem=1000000
                # else:
                #     otem=otem_dici[i][infs]
            if infs not in dout:
                dout[infs]=[momo/otem]
            else:
                # cinf[infs].append(idici_tem[i][infs]/momo)
                # cout[infs].append(item_dici[i][infs]/momo)
                # dinf[infs].append(momo/odici)
                dout[infs].append(momo/otem)
            # nlnl=[i, idici_tem[i]/momo,item_dici[i]/momo,momo/odici_tem[i],momo/otem_dici[i],degce[i],cloce[i]]
        # print i,idici_tem.keys(),item_dici.keys(),odici_tem.keys(),otem_dici.keys()
#         latl='%i & %.6f & %.6f & %.6f & %.6f & %.6f & %.6f ' %(i, idici_tem[i]/momo,item_dici[i]/momo,momo/odici_tem[i],momo/otem_dici[i],degce[i],cloce[i]) +r'''\\  \hline
# '''.decode('utf-8')
#         fop.write(latl)
#         fop.write('\n')
            # nono[infs].append(nlnl)
#     fop.write(r'''\hline 
# \end{tabular}
# \end{adjustbox}
# \end{table}

# \end{document}'''.decode('utf-8'))
#     fop.close()
    return cinf,    cout,    dinf,    dout

def create_inf_nei_clos(G,list_ofNod,steady_dict,dic_of_nodes_multi,outfile_name='nei.tex'):
    idici_tem={}
    item_dici={}
    odici_tem={}
    otem_dici={}
   
    for i in list_ofNod[1:]:
        # if i =='Node/Node':# or kk==0:
        #     continue
        sumout=0
        nei=G.neighbors(i)
        for kk,j in enumerate(list_ofNod[1:]):

            if j in nei:
                sumout+=steady_dict[i][kk]
            # print steady_dict[i],j,kk
        # for j in steady_dict[i]:

                if j not in idici_tem:

                    idici_tem[j]=steady_dict[i][kk]
                else:
                    idici_tem[j]+=steady_dict[i][kk]
        item_dici[i]=sumout
    for i in list_ofNod[1:]:
        # if i =='Node/Node':# or kk==0:
        #     continue
        sumout=0
        # nei=G.neighbors(i)
        for kk,j in enumerate(list_ofNod[1:]):
            lpa=nx.shortest_path_length(G,i,j)

            # if j in nei:
            sumout+=steady_dict[i][kk]*lpa

            if j not in odici_tem:

                odici_tem[j]=steady_dict[i][kk]*lpa
            else:
                odici_tem[j]+=steady_dict[i][kk]*lpa
        otem_dici[i]=sumout
    return idici_tem,item_dici,odici_tem,otem_dici

def create_dinf_tex(G,idici_tem,item_dici,odici_tem,otem_dici,list_ofNod,sas,ssas_ds,outfile_name='In_out_dinf.tex'):
    print outfile_name
    # print list_ofNod,dic_of_nodes_multi
    fop=open(outfile_name,'w')
    if sas=='rand':
        cap='S = '+ str(list(set(ssas_ds.values())))
    else:
        cap='S1 = %.2f, S2 = %.2f' %(sas[0],sas[1])
    lat=r'''\documentclass[10pt]{article}

\usepackage{lscape}
\usepackage{adjustbox}
\begin{document}
 %\global\pdfpageattr\expandafter{\the\pdfpageattr/Rotate 90}

\begin{table}[ht]
\centering
\caption{'''.decode('utf-8')+ cap +r'''} 
\begin{adjustbox}{width=1\textwidth,center=\textwidth}
\small
\begin{tabular}{|c||r|r|r|r|r|r||} \hline 
    Node/*INF & In-DINF & Out-DINF & In-CINF  & Out-CINF &  Degree  & Closeness  \\ 
    \hline \hline'''.decode('utf-8')
    fop.write(lat)
    fop.write('\n')
    degce=nx.degree_centrality(G)
    cloce=cent=nx.closeness_centrality(G)
    momo=len(list_ofNod[1:])-1
    # print list_ofNod,momo
    nono=[]
    
    for i in list_ofNod[1:]:
        nlnl=[i, idici_tem[i]/momo,item_dici[i]/momo,momo/odici_tem[i],momo/otem_dici[i],degce[i],cloce[i]]
        # print i,idici_tem.keys(),item_dici.keys(),odici_tem.keys(),otem_dici.keys()
        latl='%i & %.6f & %.6f & %.6f & %.6f & %.6f & %.6f ' %(i, idici_tem[i]/momo,item_dici[i]/momo,momo/odici_tem[i],momo/otem_dici[i],degce[i],cloce[i]) +r'''\\  \hline
'''.decode('utf-8')
        fop.write(latl)
        fop.write('\n')
        nono.append(nlnl)
    cin=[i[1] for i in nono]
    cou=[i[2] for i in nono]
    din=[i[3] for i in nono]
    dou=[i[4] for i in nono]
    deg=[i[5] for i in nono]
    clo=[i[6] for i in nono]
    def calc_centralization(dat_fr):
        mono=0
        # for l,v in dat_fr.items():
            # mono=0
        dmax=max(dat_fr)
        for i in dat_fr:
            mono+=dmax-i
        # dici=
        return mono/len(dat_fr)
    fop.write('Centralization & %.6f & %.6f & %.6f & %.6f &  %.6f & %.6f ' %(calc_centralization(cin),calc_centralization(cou),
        calc_centralization(din),calc_centralization(dou),calc_centralization(deg),calc_centralization(clo))  +r'''\\  \hline
'''.decode('utf-8'))
    fop.write(r'''\hline 
\end{tabular}
\end{adjustbox}
\end{table}

\end{document}'''.decode('utf-8'))
    fop.close()
    return nono


    # for kk,i in enumerate(list_ofNod[1:]):
    #     sumout=0
    #     # if i =='Node/Node':
    #     #     continue
    #     # else:
    #     nei=G.neighbors(i)

    #         # for 
    #     for ii in steady_dict[i]:
    #         if ii in nei:
    #             sumout+=ii
    #     tem_dici[i]=sumout

# 
# 
# 
def create_tex_sum_steady_sub(G,k,list_ofNod,steady_dict,dic_of_nodes_multi,outfile_name='sub_stab_out.tex'):
    print outfile_name
    # print list_ofNod,dic_of_nodes_multi
    # print steady_dict
    fop=open(outfile_name,'w')
    fop.write(r'''\documentclass[10pt]{article}

\usepackage{lscape}
\usepackage{adjustbox}
\begin{document}
 \global\pdfpageattr\expandafter{\the\pdfpageattr/Rotate 90}
'''.decode('utf-8'))
    # for itit in itertools.combinations_with_replacement(dic_of_nodes_multi.keys(),2):
    nlnl_nl=[]
    uu=0
    for itit in itertools.product(dic_of_nodes_multi.keys(),repeat=2):
        # print itit
    # print aaaaa
        if uu==0:
            mlml=[]
        fop.write(r'''\begin{landscape}
\begin{table}[ht]
\centering
\caption{'''.decode('utf-8')+ 'nodes of (%i, %i) graph ' %(itit[0],itit[1])+r'''} 
\begin{adjustbox}{width=1\textwidth,center=\textwidth}
\small
\begin{tabular}{|c||'''.decode('utf-8'))
        lat=''
        latl=''
        for mm  in dic_of_nodes_multi[itit[1]]:
            lat+='r|'
            latl+='%i & ' %mm
        lat+=r'''|r|} \hline 
    Node/Node & '''.decode('utf-8')
        fop.write(lat)
        fop.write(latl)
        fop.write(r''' Sum's\\ \hline \hline 
'''.decode('utf-8'))

        
        # lats=r'|'
        latl=r'   '
        dici_tem={}
        tem_dici={}
        for mm in dic_of_nodes_multi[itit[0]]:
            latl='%i & ' %mm
            rsum=0
            for nn in dic_of_nodes_multi[itit[1]]:
                latl+='%.6f & ' %steady_dict[mm][nn]
                rsum+=steady_dict[mm][nn]
                if nn not in dici_tem:
                    dici_tem[nn]=steady_dict[mm][nn]
                else:
                    dici_tem[nn]+=steady_dict[mm][nn]
            tem_dici[mm]=rsum
            if itit[0]==itit[1]:
                latl+='%.6f' %(rsum-1) +r'''\\ \hline \hline
            '''.decode('utf-8')
            else:
                latl+='%.6f' %(rsum) +r'''\\ \hline \hline
            '''.decode('utf-8')
            # print latl,mm
            fop.write(latl)
            # print latl
            # print dici_tem
            # print mm,nn
            # print aaaa
        latl="  Sum's & "

        for nn,nnv in dici_tem.items():
            if itit[0]==itit[1]:
                latl+='%.6f & ' %(nnv-1)
            else:
                latl+='%.6f & ' %(nnv)
#         latl=latl[:-2]+r'''\\ \hline \hline 
# '''.decode('utf-8')
        if itit[0]==itit[1]:
            latl+='%.6f , %.6f' %(sum(dici_tem.values())-len(dic_of_nodes_multi[itit[0]]),sum(tem_dici.values())-len(dic_of_nodes_multi[itit[0]]))
            mlml.append(sum(dici_tem.values())-len(dic_of_nodes_multi[itit[0]]) )
        else:
            latl+='%.6f , %.6f' %(sum(dici_tem.values()),sum(tem_dici.values()))
            mlml.append(sum(dici_tem.values()))
        latl +=r'''\\ \hline \hline 
'''.decode('utf-8')

        fop.write(latl)
        uu+=1
        if uu==k:
            uu=0
            nlnl_nl.append(mlml)
        # fop.write(latl)
        fop.write(r'''\end{tabular}
\end{adjustbox}
\end{table} 
\end{landscape}
    '''.decode('utf-8'))
     #    fop.write(r'''\newpage 
     # '''.decode('utf-8'))
    fop.write(r'''\end{document}'''.decode('utf-8'))
    fop.close()
    print nlnl_nl
    # return nlnl_nl
    # return tem_dici,dici_tem


def create_tex(outfile_name='out.tex',Ff=[]):#(5,6,15,24,44,8)):
    print outfile_name
    fop=open(outfile_name,'w')
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



\begin{document}'''.decode('utf-8')
    
    fop.write(lat)
    fop.write('\n')
    for ii in Ff:
        lat=r'''\begin{frame}

\begin{figure}[h!]
\centering
\begin{tikzpicture}[->, >=stealth, shorten >=1pt,auto,node distance=7 cm, semithick, scale = 0.7,transform shape]'''.decode('utf-8')


    # fop=open(outfile_name,'w')
        fop.write(lat)
        fop.write('\n')
        # g=ig.Graph.Full(len(Ff.vs))
        # print ii
        u=0
        v=int(float(45)/5.)-1
        for i in range(45):

            x=i%5
            y=int(float(i)/5.)

            if i+1 in ii:
                lattv=r'\node[draw,shape=rectangle,line width=1pt]'+ ' (%s) at (%s,%s) {$%s$};\n' %(i+1,x,v-y,i+1)
                col='blue'
            else:
                lattv=r'\node[draw,shape=circle,line width=1pt]'+ ' (%s) at (%s,%s) {$%s$};\n' %(i+1,x,v-y,i+1)
            fop.write(lattv)
        
        # lay=Ff.layout_circle()
        # # for vv in Ff.vs:
        # Ff.vs['layout']=lay

        # for vv in Ff.vs:
        #     nam=vv['name']
        #     la=vv['layout']

        #     lattv=r'\node[draw,shape=circle,line width=1pt]'+ ' (%s) at (%s,%s) {$%s$};\n' %(nam,(la[0]+1)*2.5,(la[1]+1)*1.5,nam)
        #     # print j
        #     fop.write(lattv)

        #     # print (j[0]+1)*5,(j[1]+1)*3.5
        # ed_dici=dict()
        # for ee in Ff.es:

        #     # print ee
        #     aa= Ff.vs[ee.source]['name']
        #     bb= Ff.vs[ee.target]['name']
        #     lab=ee['ed_label']
        #     if (aa,bb) not in ed_dici:
        #         ed_dici[(aa,bb)]=set()
        #         ed_dici[(aa,bb)].add(lab)
        #     else:
        #         ed_dici[(aa,bb)].add(lab)
        # for ab in ed_dici:
        #     lab=''
        #     for ll in ed_dici[ab]:
        #         if len(ll[1:])>1:
        #             lab+=ll[0]+'_{'+ll[1:]+'}, '
        #         else:
        #             lab+=ll[0]+'_'+ll[1:]+', '
        #     lab=lab[:-2]
        #     # print lab,ab[0],ab[1]
        #     late=r'\path'+' (%s) edge [bend right,line width=1pt] node [pos=0.5,sloped,below] {' %ab[0]
        #     late+=r'\tiny'+'{$%s$}} (%s);\n' %(lab,ab[1])
        #     fop.write(late)
        fop.write(r'''\end{tikzpicture}
    \end{figure}

    \end{frame}'''.decode('utf-8'))
        fop.write('\n')

    fop.write(r'''\end{document}'''.decode('utf-8'))
    fop.close()

# create_tex(outfile_name='out.tex',Ff=(5,6,15,24,44,8))
# v=int(float(45)/5.)-1
# for i in range(0,45):

#     x=i%5
#     y=int(float(i)/5.)
#     jj=v-y
#     print i+1,x,y,v,jj
#  
def create_heat_maps_sea(G,list_ofNod,steady_dict,dic_of_nodes_multi,ssas_ds,outfile_name='sub_heat_out_sea.png'):
    # import numpy as np
    # import seaborn as sns
    # import matplotlib.pyplot as plt
    fig=plt.figure(figsize=(18,18))
    # ax=fig.add_subplot(111)
    # ax1=plt.subplot2grid((7,5),(0,0),colspan=5,rowspan=5)
    ndat=[]
    for i in list_ofNod[1:]:
        # nndat=[]

        ndat.append(steady_dict[i][1:])
        # print steady_dict[i]
    ndata = np.array(ndat)
    data=ndata.astype(np.float)
    ax1=sns.heatmap(data,cmap=plt.cm.Greys,cbar=False)#,ax=ax)    
    # ax2=plt.subplot2grid((7,5),(0,5),rowspan=5)
    # lab=[ssas_ds[i] for i in list_ofNod[1:]]
    # # column_labels = [i for i in list_ofNod[1:]]
    # # ndat=[]
    # # for i in list_ofNod[1:]:
    # #     nndat=[]
    # ndata = np.array(lab)
    # ax2=sns.palplot(ndata,size=lab)#,ax=ax2) 
    plt.savefig(outfile_name)

def create_heat_maps_sea_s(G,list_ofNod,steady_dict,dic_of_nodes_multi,ssas_ds,data_s,vm_s='',outfile_name='sub_heat_out_sea.png'):
    fig=plt.figure(figsize=(18,18))
    # ndat=[]
    # for i in list_ofNod[1:]:
    #     # nndat=[]

    #     ndat.append(steady_dict[i][1:])
    #     # print steady_dict[i]
    ndata = np.array(data_s)
    data=ndata.astype(np.float)
    # print data_s
    # print aaa
    ax1=sns.heatmap(data,cmap=plt.cm.Greys,cbar=False)#,ax=ax)   
    # print outfile_name,vm_s 
    noutfile_name=vm_s+'_'+outfile_name
    # print noutfile_name
    plt.savefig(noutfile_name)

def create_hist_in_out(dici_tem,tem_dici,outfile_name='hist_in_out_sea.png'):
    fig=plt.figure(figsize=(6,18))
    ax=fig.add_subplot(311)
    # ax1=plt.subplot2grid((7,5),(0,0),colspan=5,rowspan=5)
    # ndat=[]
    # for i in list_ofNod[1:]:
    #     # nndat=[]

    #     ndat.append(steady_dict[i][1:])
        # print steady_dict[i]
    # ndata = np.array(ndat)
    # data=ndata.astype(np.float)
    # ax1=sns.heatmap(data,cmap=plt.cm.Greys)#,ax=ax)    
    # ax2=plt.subplot2grid((7,5),(0,5),rowspan=5)
    momo=1.*len(dici_tem.keys())
    lab=[v/momo for i,v in dici_tem.items()]
    # # column_labels = [i for i in list_ofNod[1:]]
    # # ndat=[]
    # # for i in list_ofNod[1:]:
    # #     nndat=[]
    ndata = np.array(lab)
    # ax2=sns.palplot(ndata,sitze=lab)#,ax=ax2) 
    axa=sns.distplot(ndata,kde=False,bins=10,rug=True,color='grey')#,color='grey')
    axa.set_title('In-Influenceability')
    ax=fig.add_subplot(312)
    lab=[v/momo for i,v in tem_dici.items()]
    ndata=np.array(lab)
    axa=sns.distplot(ndata,kde=False,bins=10,rug=True,color='grey')
    axa.set_title('Out-Influenceability')
    # lab=[]
    # for i,v in dici_tem.items():

    #     kv=tem_dici[i]
    #     lab.append([v/momo,kv/momo])
    # import pandas as pd
    # ndata=np.array(lab)
    # data=pd.DataFrame(ndata,columns=['In','Out'])
    # print data
    # ax=fig.add_subplot(313)

    # axa=sns.pairplot(data,vars=['In','Out'])



    # ndata=np.array(steady_dict[0][1:])
    # ax1=sns.distplot(ndata.astype(np.float),kde=False,rug=True,color='grey')
    # axa.set_xlim([-0.05,1.05])
    plt.savefig(outfile_name)

def create_contures(st_dat,figi,outfile_name='countour_sea.png'):
    st_data=pd.DataFrame(st_dat,columns=['Influence_Layer_A','Influence_Layer_B','Sum'])
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x=st_data['Influence_Layer_A'].aslist
    y=st_data['Influence_Layer_B'].aslist
    z=st_data['Sum'].aslist
    # x = np.linspace(0, 1, 100)
    # y = np.sin(x * 2 * np.pi) / 2 + 0.5
    ax.plot(x, y, z)#zs=0, zdir='z', label='zs=0, zdir=z')
    plt.show()
    g = sns.PairGrid(st_data, diag_sharey=False)
    g.map_lower(sns.kdeplot)#, cmap="Blues_d")
    g.map_upper(plt.scatter)
    g.map_diag(sns.kdeplot)#, lw=3)
    noutfile_name='%s_' %figi+outfile_name
    g.savefig(noutfile_name)
def create_pairplot_df(cent_data,mcolumns=['OB-Degree CI'  , 'OB-Closeness CI'],columns=['Degree'  , 'Closeness'],outfile_name='pairplot_KKKKKKKK.png'):
    # lab=[]
    # momo=1.*len(dici_tem.keys())
    # for i,v in dici_tem.items():
    from scipy import stats
    def corrfunc(x, y, **kws):
        r, _ = stats.pearsonr(x, y)
        ax = plt.gca()
        ax.annotate("r = {:.3f}".format(r),
                    xy=(.1, .9), xycoords=ax.transAxes)
    nel=len(columns)
    for ii,i in enumerate(mcolumns):
        # fig=plt.figure(figsize=(20,20))

        ncolumns=[columns[0],columns[1],i]
        # mncol=[columns[2],columns[3],i]
        # ax=fig.add_subplot(nel,1,ii+1)
    #     kv=tem_dici[i]
    #     lab.append([v,kv])
    # import pandas as pd
    # ndata=np.array(lab)
    # ndata=np.matrix(ndata)
    # data=pd.DataFrame(ndata,columns=columns)
    # print data
    # ax=fig.add_subplot(313)
    

        # axa=sns.pairplot(cent_data,vars=ncolumns,hue='Layer')#,vars=['In','Out'])
        # sns.set(context='notebook',rc={"figure.figsize": (6, 6)})#,color='grey'})
        g = sns.PairGrid(cent_data, vars=ncolumns,size=4)#,hue='Layer',size=4)#,palette="Set2",hue_kws={"marker": ["o", "s", "D"]})
        # g.fig=fig
        g.map_upper(plt.scatter,color='grey')
        # g.map_upper(corrfunc)
        g.map_diag(plt.hist)
        g.map_lower(plt.scatter,color='grey')
        g.map_lower(corrfunc)
        noutfile_name='%s_D_' %i+outfile_name
        g.savefig(noutfile_name)

        # ga = sns.PairGrid(cent_data, vars=mncol,size=4)#,hue='Layer',size=4)#,palette="Set2",hue_kws={"marker": ["o", "s", "D"]})
        # # g.fig=fig
        # ga.map_upper(plt.scatter,color='grey')
        # # g.map_upper(corrfunc)
        # ga.map_diag(plt.hist)
        # ga.map_lower(plt.scatter,color='grey')
        # ga.map_lower(corrfunc)
        # noutfile_name='%s_C_' %i+outfile_name
        # ga.savefig(noutfile_name)

def create_pairplot(cent_data,columns=['In','Out'],outfile_name='pairplot_in_out_sea.png'):
    # lab=[]
    # momo=1.*len(dici_tem.keys())
    # for i,v in dici_tem.items():
    from scipy import stats
    def corrfunc(x, y, **kws):
        r, _ = stats.pearsonr(x, y)
        ax = plt.gca()
        ax.annotate("r = {:.3f}".format(r),
                    xy=(.1, .9), xycoords=ax.transAxes)
    nel=len(columns[2:])
    for ii,i in enumerate(columns[2:]):
        # fig=plt.figure(figsize=(20,20))

        ncolumns=[columns[0],columns[1],i]
        # ax=fig.add_subplot(nel,1,ii+1)
    #     kv=tem_dici[i]
    #     lab.append([v,kv])
    # import pandas as pd
    # ndata=np.array(lab)
    # ndata=np.matrix(ndata)
    # data=pd.DataFrame(ndata,columns=columns)
    # print data
    # ax=fig.add_subplot(313)
    

        # axa=sns.pairplot(cent_data,vars=ncolumns,hue='Layer')#,vars=['In','Out'])
        # sns.set(context='notebook',rc={"figure.figsize": (6, 6)})#,color='grey'})
        g = sns.PairGrid(cent_data, vars=ncolumns,size=4)#,hue='Layer',size=4)#,palette="Set2",hue_kws={"marker": ["o", "s", "D"]})
        # g.fig=fig
        g.map_upper(plt.scatter,color='grey')
        # g.map_upper(corrfunc)
        g.map_diag(plt.hist)
        g.map_lower(plt.scatter,color='grey')
        g.map_lower(corrfunc)
        noutfile_name='%s_' %i+outfile_name
        g.savefig(noutfile_name)

    # print axa



    # ndata=np.array(steady_dict[0][1:])
    # ax1=sns.distplot(ndata.astype(np.float),kde=False,rug=True,color='grey')
    # axa.set_xlim([-0.05,1.05])
    # plt.savefig(outfile_name)

def create_hist_sa_sea(G,list_ofNod,steady_dict,dic_of_nodes_multi,ssas_ds,outfile_name='sub_heat_out_sea.png'):
    # import numpy as np
    # import seaborn as sns
    # import matplotlib.pyplot as plt

    fig=plt.figure(figsize=(6,6))
    # ax=fig.add_subplot(211)
    # ax1=plt.subplot2grid((7,5),(0,0),colspan=5,rowspan=5)
    ndat=[]
    # for i in list_ofNod[1:]:
    #     # nndat=[]

    #     ndat.append(steady_dict[i][1:])
        # print steady_dict[i]
    # ndata = np.array(ndat)
    # data=ndata.astype(np.float)
    # ax1=sns.heatmap(data,cmap=plt.cm.Greys)#,ax=ax)    
    # ax2=plt.subplot2grid((7,5),(0,5),rowspan=5)
    lab=[ssas_ds[i] for i in list_ofNod[1:]]
    # # column_labels = [i for i in list_ofNod[1:]]
    # # ndat=[]
    # # for i in list_ofNod[1:]:
    # #     nndat=[]
    ndata = np.array(lab)
    # ax2=sns.palplot(ndata,sitze=lab)#,ax=ax2) 
    axa=sns.distplot(ndata,kde=False,bins=10,rug=True,color='grey')
    # ax=fig.add_subplot(212)
    # ndata=np.array(steady_dict[0][1:])
    # ax1=sns.distplot(ndata.astype(np.float),kde=False,rug=True,color='grey')
    axa.set_xlim([-0.05,1.05])
    plt.savefig(outfile_name)

#           
def create_heat_maps(G,list_ofNod,steady_dict,dic_of_nodes_multi,ssas_ds,outfile_name='sub_heat_out.png'):
    import matplotlib.pyplot as plt
    import numpy as np
    # print list_ofNod[1:]
    # print dic_of_nodes_multi
    # print aaaa
    column_labels = list(list_ofNod[1:])
    row_labels = column_labels
    ndat=[]
    for i in list_ofNod[1:]:
        # nndat=[]

        ndat.append(steady_dict[i][1:])
        # print steady_dict[i]
    ndata = np.array(ndat)
    data=ndata.astype(np.float)
    # print np.size(data)
    # print data.shape
    # print np.amin(data)
    fig=plt.figure(figsize=(24,20))
    # ax=fig.add_subplot(111)
    ax1=plt.subplot2grid((7,5),(0,0),colspan=5,rowspan=5)
    # fig, ax = plt.subplots()
    heatmap = ax1.pcolor(data, cmap=plt.cm.Greys)
    # heatmap = ax.pcolor(data, cmap=plt.cm.Greys)

    # put the major ticks at the middle of each cell
    ax1.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
    ax1.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

    # want a more natural, table-like display
    ax1.invert_yaxis()
    ax1.xaxis.tick_top()

    ax1.set_xticklabels(row_labels, minor=False)
    ax1.set_yticklabels(column_labels, minor=False)

    ax2=plt.subplot2grid((7,5),(0,5),rowspan=5)
    row_labels= ['sa=random']
    lab=[ssas_ds[i] for i in list_ofNod[1:]]
    column_labels = [i for i in list_ofNod[1:]]
    # ndat=[]
    # for i in list_ofNod[1:]:
    #     nndat=[]
    ndata = np.array(lab)
    print np.size(ndata)
    print ndata.shape
    # print lab
    heatmap = ax2.pcolor(ndata, cmap=plt.cm.Greys)
    # heatmap = ax.pcolor(data, cmap=plt.cm.Greys)

    # put the major ticks at the middle of each cell
    ax2.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
    ax2.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

    # want a more natural, table-like display
    ax2.invert_yaxis()
    ax2.xaxis.tick_top()

    ax2.set_xticklabels(row_labels, minor=False)
    ax1.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

    #     ndat.append(steady_dict[i][1:])
        # print steady_dict[i]
    # data=ndata.astype(np.float)

    plt.savefig(outfile_name)

    # plt.show()