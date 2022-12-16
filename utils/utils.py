import os
import yaml

import tensorflow as tf
import numpy as np
import pandas as pd
from models import MobilenetV2
from tqdm import tqdm



def validate_config(config):
    if "seed" not in config:
        raise ValueError("Missing experiment seed")

    if "data" not in config:
        raise ValueError("Missing experiment data")

    if "directory" not in config["data"]:
        raise ValueError("Missing experiment training data")


def load_config(config_file_path):
    # TODO
    # Load config here and assign to `config` variable
    with open(config_file_path, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    # Don't remove this as will help you doing some basic checks on config
    # content
    validate_config(config)

    return config


def get_class_names(config):
    return sorted(os.listdir(os.path.join(config["data"]["directory"])))


def walkdir(folder):
    for dirpath, _, files in os.walk(folder):
        for filename in files:
            yield (dirpath, filename)


#predicts car no_car label and creates a csv per folder with predictions for all images inside
def predict_from_folder(folder, input_size, class_names):
    model = MobilenetV2.create_model(
        '/home/app/src/model.18-0.0782-0.9802.h5')

    for root, dirs, files in tqdm(os.walk(folder, topdown=False)): 
        predictions = ()
        labels = []
        paths = []
        #checks if csv exists and predictions are done for the folder. Like a resume function
        if 'car_nocar_class.csv' not in files:
            df = pd.DataFrame(columns=['path', 'label', 'score', 'detectron'])
            for name in files:
                if name.endswith('jpg'):
                    path = os.path.join(root, name)
                    paths = np.append(paths, path)
                    img = tf.keras.utils.load_img(os.path.join(root, name), target_size=input_size)
                    img_array = tf.keras.utils.img_to_array(img)
                    img_array = tf.expand_dims(img_array, 0)
                    pred = model.predict(img_array)
                    max_idx = np.argmax(pred)
                    max_score = pred[0][max_idx]  # score / class_name / id
                    predicted_class = class_names[max_idx]
                    predictions = np.append(predictions, max_score)
                    #print(len(predictions))
                    labels = np.append(labels, predicted_class)
                    #print(len(labels))
            # print(df)
            # print(paths)
            # print(predictions)
            df['path'] = paths
            df['label'] = labels
            df['score'] = predictions
            df.to_csv(os.path.join(root,"car_nocar_class.csv"))

    # return predictions, labels

#predicts car no_car label and creates a csv per folder with predictions for all images inside with batches
def predict_from_folder_in_batches(folder, input_size, class_names):
    ##codigo de pablo con las modificaciones necesarias
    


def predict_from_folder_bu(folder, model, input_size, class_names):
    df=pd.DataFrame(columns=['path','label','score','detectron'])
    predictions = ()
    labels = []
    paths = []
    model=MobilenetV2.create_model('../experiments/exp_12/model.51-2.9506.h5')
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            path=os.path.join(root, name)
            print(path)
            paths=np.append(paths,path)
            img = tf.keras.utils.load_img(os.path.join(root, name), target_size=input_size)
            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)
            pred = model.predict(img_array)
            max_idx = np.argmax(pred)
            max_score = pred[0][max_idx]
            predicted_class = class_names[max_idx]
            predictions= np.append(predictions,max_score.astype(str))
            print(len(predictions))
            labels=np.append(labels,predicted_class)
            print(len(labels))
    df['path']=paths
    df['label']=labels
    df['score']=predictions


    


    return predictions, labels
