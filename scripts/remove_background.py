"""
This script will be used to remove noisy background from cars images to
improve the quality of our data and get a better model.
The main idea is to use a vehicle detector to extract the car
from the picture, getting rid of all the background, which may cause
confusion to our CNN model.
We must create a new folder to store this new dataset, following exactly the
same directory structure with its subfolders but with new images.
"""

import argparse
from utils.car_nocar_classifier import get_vehicle_coordinates
import pandas as pd
import cv2
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Train your model.")
    parser.add_argument(
        "data_folder",
        type=str,
        help=(
            "Full path to the directory having all the cars images. Already "
            "splitted in train/test sets. E.g. "
            "`/home/app/src/data/car_ims_v1/`."
        ),
    )
    parser.add_argument(
        "output_data_folder",
        type=str,
        help=(
            "Full path to the directory in which we will store the resulting "
            "cropped pictures. E.g. `/home/app/src/data/car_ims_v2/`."
        ),
    )

    args = parser.parse_args()

    return args


def main(data_folder, output_data_folder):

    a=data_folder+'/car_dataset_labels.csv'
    df=pd.read_csv(a)


    for clas in df['class'].unique():
        a=output_data_folder + '/cars_ims_v2/'

        if os.path.isdir(a + 'train/'+clas) is False:
            os.makedirs(a + 'train/'+clas)
        if os.path.isdir(a+ 'test/'+clas) is False:  
            os.makedirs(a + 'test/'+clas)
        # if os.path.isdir('/home/app/src/data/cars_ims_v2/' + 'train/'+clas) is False:
        #     os.makedirs('/home/app/src/data/cars_ims_v2/' + 'train/'+clas)
        # if os.path.isdir('/home/app/src/data/cars_ims_v2/' + 'test/'+clas) is False:  
        #     os.makedirs('/home/app/src/data/cars_ims_v2/' + 'test/'+clas)

    #for root, dirs, files in os.walk("/home/app/src/data/car_ims_v1/", topdown=False):
    for root, dirs, files in os.walk(data_folder+"/car_ims_v1/", topdown=False):
        for name in files:
            im = cv2.imread(os.path.join(root, name))
            coordinates = get_vehicle_coordinates(im)
            cropped_im = im[coordinates[1]:coordinates[3],coordinates[0]:coordinates[2],:]
            a=root[:28]+'2/'+root[30:]+'/'+name
            cv2.imwrite(a, cropped_im)

    # for root, dirs, files in os.walk('../data/cars_ims_v1/', topdown=False):
    #     for name in files:
    #         coordinates = get_vehicle_coordinates(os.path.join(root, name))
    #         cropped_im = im[ycoordinates[1]:coordinates[3],coordinates[0]:coordinates[2],:]
    #         cv2.imwrite(root[:14]+'2'+root[15:], cropped_im)

#This function looks for the csv inside every forlder, runs detectron on every auto labeled row and saves bboxes coordinates
def detectron_only_cars(input_folder, output_folder,threshold=0):
    for root, dirs, files in tqdm(os.walk(input_folder, topdown=False)):
        df=pd.read_csv(os.path.join(root,"car_nocar_class.csv"),index_col=False)
        df=df[(df['label']=='auto') & (df['score']>threshold)]

            


#This function crops auto labeled images in every folder and makes os.link to the output folder
def crops_and_links():
    
if __name__ == "__main__":
    args = parse_args()
    main(args.data_folder, args.output_data_folder)
