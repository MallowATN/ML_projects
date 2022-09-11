import os
import git
import wget
import shutil



custom_model_name = 'my_ssd_mobnet'
pretrained_model_name = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
pretrained_mode_url = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
tf_record_script_name = 'generate_tfrecord.py'
label_map_name = 'label_map.pbtxt'

paths = {
    'WORKSPACE_PATH': os.path.join('TFOD','Tensorflow', 'workspace'),
    'SCRIPTS_PATH': os.path.join('TFOD','Tensorflow','scripts'),
    'APIMODEL_PATH': os.path.join('TFOD','Tensorflow','models'),
    'ANNOTATION_PATH': os.path.join('TFOD','Tensorflow','workspace','annotations'),
    'IMAGE_PATH': os.path.join('TFOD','Tensorflow','workspace','images'),
    'MODEL_PATH': os.path.join('TFOD','Tensorflow','workspace','models'),
    'PRETRAINED_MODEL_PATH': os.path.join('TFOD','Tensorflow','workspace','pre-trained-models'),
    'CHECKPOINT_PATH': os.path.join('TFOD','Tensorflow','workspace','models',custom_model_name),
    'OUTPUT_PATH': os.path.join('TFOD','Tensorflow','workspace','models',custom_model_name,'export'),
    'TFJS_PATH': os.path.join('TFOD','Tensorflow','workspace','models',custom_model_name,'tfjsexport'),
    'TFLITE_PATH': os.path.join('TFOD','Tensorflow','workspace','models',custom_model_name,'tfliteexport'),
    'PROTOC_PATH': os.path.join('TFOD','Tensorflow','protoc')
}

files = {
    'PIPELINE_CONFIG': os.path.join('TFOD','Tensorflow','workspace','models', custom_model_name,'pipeline.config'),
    'TF_RECORD_SCRIPT': os.path.join(paths['SCRIPTS_PATH'], tf_record_script_name),
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], label_map_name)
}

for path in paths.values():
    if not os.path.exists(path):
        if os.name == 'nt':
            os.makedirs(path)
# print(files)

# if not os.path.exists(os.path.join(paths['APIMODEL_PATH'], 'research', 'object_detection')):
#     os.makedirs(r'C:\Users\antho\Desktop\VSC\TFOD\Tensorflow\models\research\object_detection')
#     git.Git('TFOD/Tensorflow/models').clone('https://github.com/tensorflow/models')

#Tensorflow Object Detection
'''Refer to Jupyter Notebook file'''
# you need to install cuda and cuDNN, put the files from cuDNN to cuda, add to environments to enable...etc follow Nicholas Renotte's guide on youtube with tensorflow

# import object_detection
