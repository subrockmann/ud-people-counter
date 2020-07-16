#!/usr/bin/env python3
"""
 Copyright (c) 2018 Intel Corporation.

 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
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
import logging as log
from openvino.inference_engine import IENetwork, IECore


class Network:
    """
    Load and configure inference plugins for the specified target devices 
    and performs synchronous and asynchronous modes for the specified infer requests.
    """

    def __init__(self):
        ### TODO: Initialize any class variables desired ###
        self.plugin = None
        self.network = None
        self.input_blob = None
        self.output_blob = None
        self.exec_network = None
        self.infer_request = None
        self.model = None

    def load_model(self, model, device="CPU", cpu_extension=None):
        ### TODO: Load the model ###
        self.model = model
        model_xml = model
        model_bin = os.path.splitext(model_xml)[0] + ".bin"
        
        # Initialize the plugin
        self.plugin = IECore()
        # Read the IR as a IENetwork
        self.network = IENetwork(model=model_xml, weights=model_bin)
        
        
        ### TODO: Add any necessary extensions ###
        if cpu_extension and "CPU" in device:
            self.plugin.add_extension(cpu_extension, device)
        ### TODO: Return the loaded inference plugin ###
        # Load the IENetwork into the plugin
        self.exec_network = self.plugin.load_network(self.network, device)
        
        
        ### TODO: Check for supported layers ###
        supported_layers = self.plugin.query_network(network=self.network,
                                                     device_name="CPU")
        unsupported_layers = []
        for l in self.network.layers.keys():
            if l not in supported_layers:
                unsupported_layers.append(l)
        
        if len(unsupported_layers) != 0:
            #print("Unsupported layers found: {}".format(unsupported_layers))
            #print("Check whether extensions are available to add to IECore.")
            exit(1)
            
        # print("IR successfully loaded into Inference Engine.")  # print statements cause problems with the ffmpeg display

        # Get the input layer
        self.input_blob = next(iter(self.network.inputs))
        self.output_blob = next(iter(self.network.outputs))
        ### Note: You may need to update the function parameters. ###
        return

    def get_input_shape(self):
        ### TODO: Return the shape of the input layer ###
        #return self.network.inputs[self.input_blob].shape
        input_shapes = {}
        for network_input in self.network.inputs:
            input_shapes[network_input] = (self.network.inputs[network_input].shape)
        #print(input_shapes)
        return input_shapes['image_tensor']

        
    
    def get_output_shape(self):
        ### TODO: Return the shape of the output layer ###
        return self.network.outputs[self.output_blob].shape

    def get_output_keys(self):
        ### TODO: Return the shape of the output layer ###
        return self.output_blob.keys()
    
    def exec_net(self, image):
        ### TODO: Start an asynchronous request ###
        '''
        Makes an asynchronous inference request, given an input image.
        '''
        if "faster" in str(self.model):
            #print ("Faster rcnn!")
            input_dict = {'image_tensor': image, 'image_info': image.shape[1:]}
        else:
            input_dict = {self.input_blob: image}
        self.exec_network.start_async(request_id=0, inputs=input_dict)
        return
        ### TODO: Return any necessary information ###
        ### Note: You may need to update the function parameters. ###
        return 

    def wait(self):
        ### TODO: Wait for the request to be complete. ###
        status = self.exec_network.requests[0].wait(-1)
        return status


    def get_output(self):
        ### TODO: Extract and return the output results
        '''
        Returns a list of the results for the output layer of the network.
        '''
        return self.exec_network.requests[0].outputs[self.output_blob]
        ### Note: You may need to update the function parameters. ###
        
