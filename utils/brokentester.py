import os
import cv2
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Train your model.")
    parser.add_argument(
        "data_folder",
        type=str,
        help=(
            "Full path to the directory having all the cars images. "
        ),
    )
    args = parser.parse_args()

    return args

# Directory to search for images

def detect_0kb(img_path,img_name):
    statfile = os.stat(img_path)
    filesize = statfile.st_size
    if filesize < 1024:
        os.remove(img_path)
    else:
        detect_and_fix(img_path, img_name)

  # manage here the 'faulty image' case


def detect_and_fix(img_path, img_name):
    # detect for premature ending
    try:
        with open(img_path, 'rb') as im:
            im.seek(-2, 2)
            #print(img_name)
            if im.read() == b'\xff\xd9':  # EOI	  0xFF, 0xD9		End Of Image
                a=1
                #print('Image OK :', img_name)
            else:
                # fix image
                img = cv2.imread(img_path)
                cv2.imwrite(img_path, img)
                print('FIXED corrupted image :', img_name)
    except(IOError, SyntaxError) as e:
        print(e)
        print("Unable to load/write Image : {} . Image might be destroyed".format(img_path))


def main(dir_path):

    for root, dirs, files in os.walk(dir_path, topdown=False):
        print('processing ',root)
        for file in files:
            if file.endswith('.jpg'):
                img_path = os.path.join(root, file)
                detect_0kb(img_path, file)
                

    # for path in os.listdir(dir_path):
    #     print(path)
    #     # Make sure to change the extension if it is nor 'jpg' ( for example 'JPG','PNG' etc..)
    #     if path.endswith('.jpg'):
    #         img_path = os.path.join(dir_path, path)
    #         detect_0kb(img_path=img_path)
    #         detect_and_fix(img_path=img_path, img_name=path)

    print("Process Finished")


if __name__ == "__main__":
    args = parse_args()
    main(args.data_folder)