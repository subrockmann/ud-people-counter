# Project Write-Up

You can use this document as a template for providing your project write-up. However, if you
have a different format you prefer, feel free to use it as long as you answer all required
questions.

In investigating potential people counter models, I tried each of the following three models:

## Model description SSD Mobilenet

Model name: ssd_mobilenet_v2_coco_2018_03_29<br>
Model size before conversion: 67 MB<br>
Model size after conversion (.bin + .xml): 66 MB<br>
Inference time before conversion: 0.084s<br>
Inference time after conversion: 0.016s<br>

Code for downloading the model:
```
wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
tar -xvf ssd_mobilenet_v2_coco_2018_03_29.tar.gz
```

### Conversion of the model
```
python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model models/ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config models/ssd_mobilenet_v2_coco_2018_03_29/pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json
```

### How to run the app
```
python3 main.py -i resources/Pedestrian_Detect_2_1_1.mp4 -m models/ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.4 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://0.0.0.0:3004/fac.ffm
```

### Conclusion SSD Mobilenet
The model has significant problems to detect the second person for long periods of time. Changing the probabiltiy threshold did not help to solve this problem. Therefore the model is not suitable for the application.


## Model description SSD Inception

Model name: ssd_inception_v2_coco_2018_01_28<br>
Model size before conversion: 98 MB<br>
Model size after conversion (.bin + .xml): 97 MB<br>
Inference time before conversion: 0.132 s<br>
Inference time after conversion: 0.194 s<br>

Code for downloading the model:
```
wget http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz
tar -xvf ssd_inception_v2_coco_2018_01_28.tar.gz
```


### Convertion of the model
```
python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model models/ssd_inception_v2_coco_2018_01_28/frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config models/ssd_inception_v2_coco_2018_01_28/pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json
```

### How to run the complete app
python3 main.py -i resources/Pedestrian_Detect_2_1_1.mp4 -m models/ssd_inception_v2_coco_2018_01_28/frozen_inference_graph.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.4 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://0.0.0.0:3004/fac.ffm

### Conclusion SSD Inception
This model also has significant problems to detect the second person for long periods of time. Changing the probabiltiy threshold did not help to solve this problem. Therefore the model is not suitable for the application.

## Model description

Model name: faster_rcnn_inception_v2_coco_2018_01_28<br>
Model size before conversion: 55 MB<br>
Model size after conversion (.bin + .xml): 52 MB<br>
Inference time before conversion: 0.397s<br>
Inference time after conversion: 0.164s<br>

Code for downloading the model:
```
wget http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz
tar -xvf faster_rcnn_inception_v2_coco_2018_01_28.tar.gz
```

### Conversion fo the faster rcnn_inception model
```
python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model /home/workspace/models/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config /home/workspace/models/faster_rcnn_inception_v2_coco_2018_01_28/pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/faster_rcnn_support.json
```

### How to run the  app 
```
python3 main.py -i resources/Pedestrian_Detect_2_1_1.mp4 -m models/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.4 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://0.0.0.0:3004/fac.ffm
```
### Conclusion Faster RCNN
This model has a much better accuracy in detecting the persons. It's inference is also slightly faster than SSD Inception. Therefore Faster RCNN is the choosen model for this application.

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


## Assess Model Use Cases

Potential use cases of the people counter app:

* During COVID19 the app might be used to count people in public places, to avoid infections
* In retail the app might be used to detect areas of the shop that are highly frequented, this could help to optimize the shop layout and increase revenue
* The app could be used by drones to detect people after natural diseasters
*...


## Assess Effects on End User Needs

Lighting, model accuracy, and camera focal length/image size have different effects on a
deployed edge model. 

The model works best if it is getting inputs that are similar to the ones used during training. 
* different camera focal lengths, have an impact on the distortion of the images
* different lighting will make people more difficult to detect due to missing contrasts
* larger image sizes will make it more difficult, because the image will be downscaled and the details might disappear.