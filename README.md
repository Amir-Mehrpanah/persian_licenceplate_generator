# Persian Licence Plate Generator
This repository helps you generate a veritable cornucopia of persian licence plates.
You're almost done with this part, [training your own CNN would be the next step](https://gluon-cv.mxnet.io/install.html)!

## Incentives 
Generated sample:\
![Sample](https://github.com/Amir-Mehrpanah/atumated_lp/blob/master/README_contents/simple_out.png)

For the sake of ease, generated licence plates come with their annotations: \
![Annotation sample](https://github.com/Amir-Mehrpanah/atumated_lp/blob/master/README_contents/ann_simple_out.png) 

Generated sample with perspective transformations:\
![Annotation sample](https://github.com/Amir-Mehrpanah/atumated_lp/blob/master/README_contents/transform.gif) 

On top of all that, it automatically generates associated xml files in pascal voc format: \
![Sample](https://github.com/Amir-Mehrpanah/atumated_lp/blob/master/README_contents/pascal_voc_bbox.png)

Sample neural network trained on this dataset:\
![Sample](https://github.com/Amir-Mehrpanah/atumated_lp/blob/master/README_contents/detections.png)

Model zoo [faster_rcnn_inception_v2_coco](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)
## How to Use
**Because of oop pattern you won't need to make significant changes 
unless you want something structurally different!**
```html
*Note: if you have trouble installing jsonnet on windows 
use win_conf.json instead and remove jsonnet dependencies
(For installing jsonnet on windows run: "pip install jsonnet-binary")
```
1. **Got all requirements installed:**\
    ```pip3 install --upgrade -r requirements.txt```
    
2. **Tweak configuration file: (optional)**
    * project_configurations.jsonnet
    
3. **Out-of-the-box data generation:**
    * With default parameters:\
    ```$ python3 main.py```
    * Override config parameters:\
    ```$ pyhton3 main.py --num_out_img 10000```\
    ```$ pyhton3 main.py --apply_misc_noise False```\
    ```$ pyhton3 main.py --apply_dirt False``` \
    ```$ pyhton3 main.py --output_directory 'output'``` (doesn't already exist) \
    ```$ pyhton3 main.py --img_per_package 8000``` 
