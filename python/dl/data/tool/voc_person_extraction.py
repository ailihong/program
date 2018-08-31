# -*- coding: utf-8 -*-
"""
Created on Fri May 25 14:46:07 2018
从voc数据集中抽取person类的数据，重新生成xml和复制jpg
跳过part-‘head’
@author: bai
"""
import argparse
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class gen_xml():
    def __init__(self,root='annotation'):
        '''
        最多3层
        '''
        self.root_a = ET.Element(root)
        
        self.sub_root_a = None
        self.sub_sub_root_a = None
        
    def set_sub_node(self,last,sub_node,val):#last = root','sub_root' or 'sub_sub_root'
        if last == 'root':
            b = ET.SubElement(self.root_a, sub_node)
            b.text = val
        elif last == 'sub_root':
            b = ET.SubElement(self.sub_root_a, sub_node)
            b.text = val
        elif last == 'sub_sub_root':
            b = ET.SubElement(self.sub_sub_root_a, sub_node)
            b.text = val
            
    def set_sub_root(self,last,sub_root):#last = root','sub_root'
        if last == 'root':
            self.sub_root_a = ET.SubElement(self.root_a, sub_root)
        elif last == 'sub_root':
            self.sub_sub_root_a = ET.SubElement(self.sub_root_a, sub_root)
    def out(self,filename):
        fp = open(filename,'wb')
        tree = ET.ElementTree(self.root_a)
        tree.write(fp)
        fp.close()
        
def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    parser.add_argument('--JPEGImages','-J', dest='image_path',type=str, help='JPEGImages path to read',
                        default='None')
    parser.add_argument('--JPEGImages2','-J2', dest='image_path2',type=str, help='JPEGImages path to save',
                        default='None')
    parser.add_argument('--Annotations','-A', dest='xml_path', help='xml path to read',
                        default='None')
    parser.add_argument('--Annotations2','-A2', dest='xml_path2', help='xml path to save',
                        default='None')
    args = parser.parse_args()

    return args

def main(args):
    list_xml=os.listdir(args.xml_path)
    
    
    list_need=['filename','size','name','part']
    list_sub_need=['width','height','depth','xmin','ymin','xmax','ymax']
    if len(list_xml)==0:
        return
    
    #Max_xml_num = 9583
    xml_num = 0
    for xml_name in list_xml:
#        print(xml_name)
        my_xml = gen_xml('annotation')
        tree = ET.ElementTree(file=os.path.join(args.xml_path,xml_name))
        have_person = False
        save_person = False
        skip_part = False
        save_size = False
        save_person_n = 0
        save_size_n = 0
        for elem in tree.iter():
            if elem.tag in list_need:
                if elem.tag == 'filename':
                    my_xml.set_sub_node('root','filename','%s'%elem.text)
                if elem.tag == 'size':
                    save_size = True
                    my_xml.set_sub_root('root','size')
                if elem.tag == 'name' and elem.text in ['bird','cat','dog']:#['person','cat','dog'] for extract three class
                    my_xml.set_sub_root('root','object')
                    my_xml.set_sub_node('sub_root','name',elem.tag)
                    my_xml.set_sub_root('sub_root','bndbox')
#                    print('''set_sub_root('sub_root','bndbox')''')
                    save_person = True
                    have_person = True
                if elem.tag == 'part':
                    skip_part = True
#                    print('en_part,skip:',skip_part)
                    
            elif elem.tag in list_sub_need:
                if save_size and elem.tag in list_sub_need[:3]:
                    
                    my_xml.set_sub_node('sub_root','%s'%elem.tag,'%s'%elem.text)
                    save_size_n += 1
                    if save_size_n == 3:
                        save_size = False
                        save_size_n = 0
                        
                elif elem.tag in list_sub_need[3:]:
                    save_person_n += 1
#                    print('set_sub_node:%s,%s'%(elem.tag,elem.text))
                    
#                    print('save_person_n:',save_person_n)
                    if skip_part:
#                        print('skip:',skip_part)
                        if save_person_n == 4:
                            skip_part = False
                            save_person_n = 0
#                            print('de_part,skip:',skip_part)
                            
                    elif save_person:
                        my_xml.set_sub_node('sub_sub_root','%s'%elem.tag,'%s'%elem.text)
                        if save_person_n == 4:
                            save_person = False
                            save_person_n = 0
#                            print('saved person')
                            
        if have_person:
            
            image_filename = os.path.join(args.image_path,xml_name[:-3]+'jpg')
            image_filename2 = os.path.join(args.image_path2,xml_name[:-3]+'jpg')
            if os.path.exists(image_filename):
                xml_num += 1
                my_xml.out(os.path.join(args.xml_path2,xml_name))
                os.system('cp %s %s'%(image_filename,image_filename2))
                #if xml_num == Max_xml_num:
                #    break
    

if __name__ == '__main__':
    args = parse_args()
    if args.image_path == 'None' or args.xml_path == 'None':
        exit(0)
    main(args)
    print('end')
