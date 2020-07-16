# Project Write-Up

You can use this document as a template for providing your project write-up. However, if you
have a different format you prefer, feel free to use it as long as you answer all required
questions.

## Model description SSD Mobilenet

Model name: ssd_mobilenet_v2_coco_2018_03_29
Model size before conversion: 67 MB
Model size after conversion (.bin + .xml): 66 MB
Inference time before conversion: 
Inference time after conversion:

Code for downloading the model:
```
wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
```

### Conversion of the model
```
python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model models/ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config models/ssd_mobilenet_v2_coco_2018_03_29/pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json
```

### How to run the app
```
python main.py -i resources/Pedestrian_Detect_2_1_1.mp4 -m models/ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.4 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://0.0.0.0:3004/fac.ffm
```

### Conclusion SSD Mobilenet
The model has significant problems to detect the second person for long periods of time. Changing the probabiltiy threshold did not help to solve this problem. Therefore the model is not suitable for the application.


## Model description SSD Inception

Model name: ssd_inception_v2_coco_2018_01_28
Model size before conversion: 98 MB
Model size after conversion (.bin + .xml): 97 MB
Inference time before conversion: 
Inference time after conversion:

Code for downloading the model:
```
wget http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz
```


### Convertion of the model
```
python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model models/ssd_inception_v2_coco_2018_01_28/frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config models/ssd_inception_v2_coco_2018_01_28/pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json
```

### How to run the complete app
python main.py -i resources/Pedestrian_Detect_2_1_1.mp4 -m models/ssd_inception_v2_coco_2018_01_28/frozen_inference_graph.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.4 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://0.0.0.0:3004/fac.ffm


## Model description

Model name: faster_rcnn_inception_v2_coco_2018_01_28
Model size before conversion: 55 MB
Model size after conversion (.bin + .xml): 52 MB
Inference time before conversion: 
Inference time after conversion:

Code for downloading the model:
```
wget http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz
```

### Conversion fo the faster rcnn_inception model
```
python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model /home/workspace/models/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config /home/workspace/models/faster_rcnn_inception_v2_coco_2018_01_28/pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/faster_rcnn_support.json
```

### How to run the  app 
```
python main.py -i resources/Pedestrian_Detect_2_1_1.mp4 -m models/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.4 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://0.0.0.0:3004/fac.ffm
```

## Explaining Custom Layers
The openVINO toolkit supports different neural network layers for a variety of neural network frameworks. The supported layers for each framework can be found [here](https://docs.openvinotoolkit.org/latest/openvino_docs_MO_DG_prepare_model_Supported_Frameworks_Layers.html)
If a network architecture uses layers that are not included in the supported layers there are several ways to run the model:
* When a device does not support a specific layer, you can use the HETERO plugin to run these layers on another device
* running the layer in the original framework
* Create a custom layer extension using the custom layer extractor and custom layer operation.

Potential reasons for handling custom layers:
* when a custom layer is not supported by the network and there is no device available that can run this custom layer
* running the layer in the original framework might not be possible due to hardware restrictions
* creating an intermediate representation that can run on one device saves time because it does not have to transfer data between the different devices

## Comparing Model Performance

My method(s) to compare models before and after conversion to Intermediate Representations
were...

The difference between model accuracy pre- and post-conversion was...

The size of the model pre- and post-conversion was...

The inference time of the model pre- and post-conversion was...

## Assess Model Use Cases

Some of the potential use cases of the people counter app are...

Each of these use cases would be useful because...

## Assess Effects on End User Needs

Lighting, model accuracy, and camera focal length/image size have different effects on a
deployed edge model. The potential effects of each of these are as follows...

## Model Research

[This heading is only required if a suitable model was not found after trying out at least three
different models. However, you may also use this heading to detail how you converted 
a successful model.]

In investigating potential people counter models, I tried each of the following three models:

- Model 1: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...
  
- Model 2: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...

- Model 3: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...
