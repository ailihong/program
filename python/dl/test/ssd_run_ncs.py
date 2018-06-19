#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright(c) 2017 Intel Corporation. 
# License: MIT See LICENSE file in root directory.


from mvnc import mvncapi as mvnc
import numpy
import cv2
import sys
import argparse,time

dim=(96,112) #width,height

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='batch rename')
    parser.add_argument('--image_file','-IF', dest='image', type=str,help='file one to copy',default='None')
    parser.add_argument('--graph','-G', dest='graph', type=str,help='file one to copy',default='None')
    args = parser.parse_args()

    return args
    
# ***************************************************************
# Labels for the classifications for the network.
# ***************************************************************
LABELS = ('background','person','dog','cat')

# Run an inference on the passed image
# image_to_classify is the image on which an inference will be performed
#    upon successful return this image will be overlayed with boxes
#    and labels identifying the found objects within the image.
# ssd_mobilenet_graph is the Graph object from the NCAPI which will
#    be used to peform the inference.
def run_inference(image_to_classify, ssd_mobilenet_graph):

    # get a resized version of the image that is the dimensions
    # SSD Mobile net expects
    resized_image = preprocess_image(image_to_classify)

    # ***************************************************************
    # Send the image to the NCS
    # ***************************************************************
    ssd_mobilenet_graph.LoadTensor(resized_image.astype(numpy.float16), None)

    # ***************************************************************
    # Get the result from the NCS
    # ***************************************************************
    output= ssd_mobilenet_graph.GetResult()
    print('output,num:%s',len(output[0]),output)

def preprocess_image(src):

    # scale the image
    img = cv2.resize(src, dim)

    # adjust values to range between -1.0 and + 1.0
    img = img - [127.5]
    img = img * 0.0078125
    
    return img


# This function is called from the entry point to do
# all the work of the program
def main(args):
    # name of the opencv window
    # Get a list of ALL the sticks that are plugged in
    # we need at least one
    devices = mvnc.EnumerateDevices()
    if len(devices) == 0:
        print('No devices found')
        quit()

    # Pick the first stick to run the network
    device = mvnc.Device(devices[0])

    # Open the NCS
    device.OpenDevice()

    # The graph file that was created with the ncsdk compiler
#    graph_file_name = 'graph'

    # read in the graph file to memory buffer
    with open(args.graph, mode='rb') as f:
        graph_in_memory = f.read()

    # create the NCAPI graph instance from the memory buffer containing the graph file.
    graph = device.AllocateGraph(graph_in_memory)

    # read the image to run an inference on from the disk
    infer_image = cv2.imread(args.image)

    # run a single inference on the image and overwrite the
    # boxes and labels
    now = time.time()
    run_inference(infer_image, graph)
    print('inference time:',time.time() - now)
    # display the results and wait for user to hit a key
    # Clean up the graph and the device
    graph.DeallocateGraph()
    device.CloseDevice()


# main entry point for program. we'll call main() to do what needs to be done.
if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(args))
