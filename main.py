"""People Counter."""
"""
 Copyright (c) 2018 Intel Corporation.
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 withou
 t limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit person to whom the Software is furnished to do so, subject to
 the following conditions:
 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import sys
import time
import socket
import json
import cv2
import time

import logging as log
import paho.mqtt.client as mqtt

from argparse import ArgumentParser
from inference import Network



# MQTT server environment variables
HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname(HOSTNAME)
MQTT_HOST = IPADDRESS
MQTT_PORT = 3001
MQTT_KEEPALIVE_INTERVAL = 60


def build_argparser():
    """
    Parse command line arguments.

    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", required=True, type=str,
                        help="Path to an xml file with a trained model.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to image or video file")
    parser.add_argument("-l", "--cpu_extension", required=False, type=str,
                        default=None,
                        help="MKLDNN (CPU)-targeted custom layers."
                             "Absolute path to a shared library with the"
                             "kernels impl.")
    parser.add_argument("-d", "--device", type=str, default="CPU",
                        help="Specify the target device to infer on: "
                             "CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device "
                             "specified (CPU by default)")
    parser.add_argument("-pt", "--prob_threshold", type=float, default=0.5,
                        help="Probability threshold for detections filtering"
                        "(0.5 by default)")
    return parser


def connect_mqtt():
    ### TODO: Connect to the MQTT client ###
    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    return client

def draw_boxes(frame, result, args, width, height):
    '''
    Draw bounding boxes onto the frame.
    '''
    current_count = 0
    for box in result[0][0]: # Output shape is 1x1x100x7
        conf = box[2]
        if conf >= 0.5:
            xmin = int(box[3] * width)
            ymin = int(box[4] * height)
            xmax = int(box[5] * width)
            ymax = int(box[6] * height)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1) 
            current_count = current_count + 1
    return frame, current_count


def infer_on_stream(args, client):
    """
    Initialize the inference network, stream video to network,
    and output stats and video.

    :param args: Command line arguments parsed by `build_argparser()`
    :param client: MQTT client
    :return: None
    """
    
    log.basicConfig(filename='debug.log',level=log.DEBUG)
    
    # Initialise the class
    infer_network = Network()
    # Set Probability threshold for detections
    prob_threshold = args.prob_threshold

    ### TODO: Load the model through `infer_network` ###
    infer_network.load_model(args.model, args.device, args.cpu_extension)
    net_input_shape = infer_network.get_input_shape()
    log.info("Input shape: " + str(net_input_shape))
    net_output_shape = infer_network.get_output_shape()
    #print (net_output_shape)
    #net_output_keys = infer_network.get_output_keys()
    #print (net_output_keys)

     # Check if the input is from webcam, an image, or a video
    if args.input == 'CAM':
        args.input = 0

    ### TODO: Handle the input stream ###
    ### TODO: Read from the video capture ###
    # Get and open video capture
    cap = cv2.VideoCapture(args.input)
    cap.open(args.input)

    # Grab the shape of the input 
    width = int(cap.get(3))
    height = int(cap.get(4))

    
    # setup counter variables for statistics
    last_count = 0
    report_count = 0
    total_count = 0
 
    duration = 0
    duration_prev = 0

    frame_count = 0
    frame_count_prev = 0
    frame_threshold = 20
    
    
    
    ### TODO: Loop until stream is over ###
    # Process frames until the video ends, or process is exited

    
    while cap.isOpened():
        # Read the next frame
        flag, frame = cap.read()
        if not flag:
            break
        key_pressed = cv2.waitKey(60)

        ### TODO: Pre-process the image as needed ###
        ### TODO: Pre-process the frame
        p_frame = cv2.resize(frame, (net_input_shape[3], net_input_shape[2]))
        p_frame = p_frame.transpose((2, 0, 1))
        p_frame = p_frame.reshape(1, *p_frame.shape)  ###TODO: Check for B,H,W C

        ### TODO: Start asynchronous inference for specified request ###
        ### TODO: Perform inference on the frame
        start_time = time.time()
        infer_network.exec_net(p_frame)

        ### Wait for the result and get the output of the inference ###

        zero_detection = 0
        if infer_network.wait()== 0:
            result = infer_network.get_output()
            duration = time.time()- start_time
            log.info("Frame: "+ str(frame_count) + " - inference time: " + str(duration))

            ### Get the results of the inference request ###
            frame, current_count = draw_boxes(frame, result, args, width, height)
            #print(current_count)

            ### TODO: Extract any desired stats from the results ###
            ### TODO: Calculate and send relevant information on ###
            ### current_count, total_count and duration to the MQTT server ###
            ### Topic "person": keys of "count" and "total" ##

            # Only change the count if the same prediction has been made for frame_threshold frames
            # all other predictions might be false positives or false negatives

            if current_count != report_count:       # check if count has changed
                last_count = report_count           
                report_count = current_count

                if frame_count >=frame_threshold:
                    frame_count_prev = frame_count
                    frame_count = 0                 # reset frame counter 
                else:
                    frame_count = frame_count_prev+ frame_count
            
            else:                                               # count has not changed
                frame_count += 1                                
                if frame_count >=frame_threshold:               # nothing has changed for threshold number of frames
                    report_count = current_count                # current count has been consistent and can be published
                    if frame_count ==frame_threshold and current_count > last_count:  # person has entered the frame
                        start_time = time.time()
                        total_count = total_count + current_count - last_count          # due to weired GUI
                        client.publish("person", json.dumps({"total": total_count}))
                        client.publish("person", json.dumps({"count": current_count}))
                    elif frame_count ==frame_threshold and current_count < last_count:  # person has definetly left the frame
                        duration = int(time.time() - start_time)
                        client.publish("person/duration", json.dumps({"duration": duration}))
                        client.publish("person", json.dumps({"count": current_count}))
            
                        
        ### TODO: Send the frame to the FFMPEG server ###
        # Send frame to the ffmpeg server
        sys.stdout.buffer.write(frame)  
        sys.stdout.flush()

        ### TODO: Write an output image if `single_image_mode` ###
    cap.release()
    cv2.destroyAllWindows()


def main():
    """
    Load the network and parse the output.

    :return: None
    """
    # Grab command line args
    args = build_argparser().parse_args()
    # Connect to the MQTT server
    client = connect_mqtt()
    # Perform inference on the input stream
    infer_on_stream(args, client)


if __name__ == '__main__':
    main()
