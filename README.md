# Atomated LP
```diff
 - i'm currrently working on it!  
```
This repository helps you generate a veritable cornucopia of persian licence plates.
Training your own CNN would be the next step though!

## Incentives 
Generated sample:\
 ![Sample](https://github.com/Amir-Mehrpanah/atumated_lp/blob/master/README_contents/simple_out.png)

For the sake of ease, generated licence plates come with their annotations: \
![Annotation sample](https://github.com/Amir-Mehrpanah/atumated_lp/blob/master/README_contents/ann_simple_out.png) 

Generated sample with perspective transformations:\
<img src="https://github.com/Amir-Mehrpanah/atumated_lp/blob/master/README_contents/transformed.gif" width="544" height="336" />

## How to Use
**Because of oop pattern you won't need to make significant changes 
unless you want something structurally different!**
1. **Got all requirements installed**:
    * opencv-python
    * jsonnet
    * json
    
2. **Tweak configuration file (optional)**:
    * project_configurations.jsonnet
    
3. **Out-of-the-box data generation**:
    * With default parameters (specified in the former step):\
    ```$ python3 main.py```
    * Override parameters:\
    ```$ pyhton3 main.py --num_out_img 1000```