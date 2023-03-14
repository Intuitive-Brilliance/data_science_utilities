import splitfolders
import os
import argparse
import os
# import glob
# from typing import Mapping
# import cv2
import shutil
# from datetime import datetime
# from xml.dom import minidom
from transformer import Transformer
import sys
# import platform
# import xml.etree.ElementTree as ET

def split_folders(data_path,output_path):
    images_path = data_path+'/'+'images'
    all_classes = os.listdir(images_path)
    labels_path = data_path+'/'+'labels'
    # images_output = output_path+'/'+'images'
    # labels_output = output_path+'/'+'labels'

    splitfolders.ratio(images_path, # The location of dataset
                    output=output_path, # The output location
                    seed=42, # The number of seed
                    ratio=(.7, .2, .1), # The ratio of splited dataset
                    group_prefix=None, # If your dataset contains more than one file like ".jpg", ".pdf", etc
                    move=False # If you choose to move, turn this into True
                    )

    splitfolders.ratio(labels_path, # The location of dataset
                    output=output_path, # The output location
                    seed=42, # The number of seed
                    ratio=(.7, .2, .1), # The ratio of splited dataset
                    group_prefix=None, # If your dataset contains more than one file like ".jpg", ".pdf", etc
                    move=False # If you choose to move, turn this into True
                    )
    train_location = './'+output_path+'/train/'
    val_location = './'+output_path+'/val/'
    test_location = './'+output_path+'/test/'
 
    return train_location,val_location,test_location,all_classes


def xml2txt(xml_dir,out_dir):
    parser = argparse.ArgumentParser(description="Formatter from ImageNet xml to Darknet text format")
    parser.add_argument("-xml", help="Relative location of xml files directory" ,default='xml')
    parser.add_argument("-out", help="Relative location of output txt files directory", default="out")
    parser.add_argument("-c", help="Relative path to classes file", default="classes.txt")
    args = parser.parse_args()

    xml_dir = os.path.join(os.path.dirname(os.path.realpath('__file__')), xml_dir)
    if not os.path.exists(xml_dir):
        print("Provide the correct folder for xml files.")
        sys.exit()

    out_dir = os.path.join(os.path.dirname(os.path.realpath('__file__')), out_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if not os.access(out_dir, os.W_OK):
        print("%s folder is not writeable." % out_dir)
        sys.exit()
    
    
    transformer = Transformer(xml_dir=xml_dir, out_dir=out_dir)
    transformer.transform()

def remove_xmls(main_directory):
    # print(main_directory)
    xmls = os.listdir(main_directory)
    # print(xmls)
    for xml in xmls:
        print(xml)
        if xml.endswith('.xml'):
            xml_location = i+'/'+xml
            print(xml_location)
            os.remove(xml_location)

# split_folders("images\directories_of_images_per_class","labels\directories_of_labels_per_class")
if __name__=='__main__':
    data_path = 'data'
    output_path = 'new_data'
    print('Starting data split operation...')

    train_location,val_location,test_location,all_classes=split_folders(data_path,output_path)
    print('Data split operation completed!\nStarting label conversion...')

    for each_class in all_classes:
        for i in [train_location+each_class,test_location+each_class,val_location+each_class]:
            xml2txt(i,i.replace('images','labels'))
            # print(i)
            remove_xmls(i)

    print('Label conversion from xml to txt completed!')
