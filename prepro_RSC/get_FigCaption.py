import argparse
import os
from xml.etree import ElementTree as ET
import pickle
import sys

def ParserAF(head,node):
    title=str()
    abstract=str()
    for node1 in node:
        if head+'titlegrp' == node1.tag:
            for node2 in node1:
                if head+'title' == node2.tag:
                    title+=''.join(node2.itertext())
        if head+'abstract' == node1.tag:
            for node2 in node1:
                if head+'p' == node2.tag:
                    abstract+=''.join(node2.itertext())
    assert title != ''
    #assert abstract != ''
    return title, abstract

def ParserSection(head,node):
    Section = dict()
    Section['no'] = str()
    Section['title'] = str()
    Section['figure'] = list()
    Section['sebSect'] = list()
    Section['scheme'] = list()
    Section['table'] = list()
    Fig_sec=list()
    Sch_sec=list()
    Tabl_sec=list()
    for node1 in node:
        if head+'no' == node1.tag:
            Section['no']=''.join(node1.itertext())
        if head+'title' == node1.tag:
            Section['title']=''.join(node1.itertext())
        if 'subsect' in node1.tag:
            subSection,Fig,Sch,Tabl=ParserSection(head,node1)
            Section['sebSect'].append(subSection)
            Fig_sec.extend(Fig)
            Sch_sec.extend(Sch)
            Tabl_sec.extend(Tabl)
        if head+'figure' == node1.tag:
            figure=dict()
            caption=str()
            figure['id'] = node1.attrib['id']
            figure['xsrc'] = node1.attrib['xsrc']
            for node2 in node1:
                if head+'title' == node2.tag:
                    caption=''.join(node2.itertext())
            figure['caption']=caption
            Section['figure'].append(figure)
            Fig_sec.append(figure)
        if head+'scheme' == node1.tag:
            scheme=dict()
            caption=str()
            scheme['id'] = node1.attrib['id']
            scheme['xsrc'] = node1.attrib['xsrc']
            for node2 in node1:
                if head+'title' == node2.tag:
                    caption=''.join(node2.itertext())
            scheme['caption']=caption
            Section['scheme'].append(scheme)
            Sch_sec.append(scheme)
        if head+'table-entry' == node1.tag:
            table=dict()
            caption=str()
            table['id']=node1.attrib['id']
            for node2 in node1:
                if head+'title' == node2.tag:
                    caption=''.join(node2.itertext())
            table['caption']=caption
            Section['table'].append(table)
            Tabl_sec.append(table)
    return Section,Fig_sec,Sch_sec,Tabl_sec

def unify_contents(contents):
    ids=set()
    unified_content=list()
    for content in contents:
        content_id = int(content['id'][3:])
        if content_id not in ids:
            ids.add(content_id)
            unified_content.append(content)
        else:
            print('Duplication!!')
    ids_sorted=sorted(list(ids))
    print(contents)
    if len(ids_sorted)!=0:
        assert len(ids_sorted)==ids_sorted[-1]
    return unified_content

def ParserAB(head,node):
    art_body=list()
    Fig_ALL=list()
    Sch_ALL=list()
    Tabl_ALL=list()
    for node1 in node:
        if head+'section' == node1.tag:
            Section,Fig_sec,Sch_sec,Tabl_sec=ParserSection(head,node1)
            art_body.append(Section)
            Fig_ALL.extend(Fig_sec)
            Sch_ALL.extend(Sch_sec)
            Tabl_ALL.extend(Tabl_sec)
    Fig_ALL=unify_contents(Fig_ALL)
    Sch_ALL=unify_contents(Sch_ALL)
    Tabl_ALL=unify_contents(Tabl_ALL)
    return art_body,Fig_ALL,Sch_ALL,Tabl_ALL

def get_FigCaption(data_dir):
    paper_data=dict()
    xml_path=os.path.join(data_dir,data_dir.split('/')[-1]+'.XML')
    tree=ET.parse(xml_path)
    root=tree.getroot()
    head='{'+root.attrib[list(root.attrib.keys())[1]].split()[0]+'}'
    for node in root:
        if head+'art-front' == node.tag:
            title, abstract = ParserAF(head,node)
            paper_data['title']=title
            paper_data['abstract']=abstract
        elif head+'art-body' == node.tag:
            art_body,Fig_ALL,Sch_ALL,Tabl_ALL = ParserAB(head,node)
            paper_data['art-body']=art_body
            paper_data['Fig_ALL']=Fig_ALL
            paper_data['Scheme_ALL']=Sch_ALL
            paper_data['Tabl_ALL']=Tabl_ALL
    return paper_data

def extract_xml(data_dir):
    paper_data=dict()
    xml_path=os.path.join(data_dir,data_dir.split('/')[-1]+'.XML')
    tree=ET.parse(xml_path)
    root=tree.getroot()
    head='{'+root.attrib[list(root.attrib.keys())[1]].split()[0]+'}'
    paper_data['ID'] = ''.join(tree.findall('.//{}art-admin/{}ms-id'.format(head, head))[0].itertext())
    #paper_data['year'] = ''.join(tree.findall('.//{}art-admin/{}date/{}year'.format(head, head, head))[0].itertext())
    for node in root:
        if head+'art-front' == node.tag:
            title, abstract = ParserAF(head,node)
            paper_data['title']=title
            paper_data['abstract']=abstract
    figure_nodes=tree.findall('.//{}figure'.format(head))
    table_entry_nodes=tree.findall('.//{}table-entry'.format(head))
    scheme_nodes=tree.findall('.//{}scheme'.format(head))
    table_nodes=tree.findall('.//{}table'.format(head))
    chart_nodes=tree.findall('.//{}chart'.format(head))
    para_nodes=tree.findall('.//{}p'.format(head))
    paper_data['Fig_ALL']=figure_parse(figure_nodes,head)
    paper_data['Scheme_ALL']=figure_parse(scheme_nodes,head)
    paper_data['Tabl_ALL_caption']=table_caption_parse(table_entry_nodes,head)
    paper_data['Tabl_ALL_not_caption']=table_not_caption_parse(table_entry_nodes,table_nodes,head)
    paper_data['Chart_ALL']=figure_parse(chart_nodes,head)
    return paper_data

def figure_parse(nodes,head):
    Fig_sec=list()
    for node1 in nodes:
        figure=dict()
        caption=str()
        figure['id'] = node1.attrib['id']
        figure['xsrc'] = node1.attrib['xsrc']
        for node2 in node1:
            if head+'title' == node2.tag:
                caption=''.join(node2.itertext())
        figure['caption']=caption
        Fig_sec.append(figure)
    return Fig_sec

def scheme_parse(nodes,head):
    Sch_sec=list()
    for node1 in nodes:
        scheme=dict()
        caption=str()
        scheme['id'] = node1.attrib['id']
        scheme['xsrc'] = node1.attrib['xsrc']
        for node2 in node1:
            if head+'title' == node2.tag:
                caption=''.join(node2.itertext())
        scheme['caption']=caption
        Sch_sec.append(scheme)
    return Sch_sec

def table_caption_parse(nodes,head):
    Tabl_sec=list()
    for node1 in nodes:
        table=dict()
        caption=str()
        table['id']=node1.attrib['id']
        for node2 in node1:
            if head+'title' == node2.tag:
                caption=''.join(node2.itertext())
        table['caption']=caption
        table['node']=node1
        Tabl_sec.append(table)
    return Tabl_sec
    
def table_not_caption_parse(caption_nodes,nodes,head):
    caption_nodes_children=getchildren_for_table(caption_nodes,head)
    not_caption_nodes=list()
    for node in nodes:
        if node not in caption_nodes_children:
            table=dict()
            table['node']=node
            not_caption_nodes.append(table)
    return not_caption_nodes
    
def getchildren_for_table(caption_nodes,head):
    children=list()
    for caption_node in caption_nodes:
        children.extend(caption_node.findall('.//{}table'.format(head)))
    return children

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--data_dir', default='./paper/2015/C5TA06020F',help='')
    args = parser.parse_args()
    paper_data=extract_xml(args.data_dir)
    print(paper_data)
    with open('tmp.pkl','wb') as f:
        pickle.dump(paper_data,f)