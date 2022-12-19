'''I THINK IM RUNNING INTO MEMORY ISSUES, PROBABLY HAVE TO TRAIN THE THING LOCALLY THEN SEND A MODEL OVER OR SOMETHING'''


#DEFAULT TENSORFLOW IMPORTS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from PIL import Image
import cv2
import os
import csv


import tensorflow as tf
#from tensorflow import keras
#from tensorflow.keras import layers
#from tensorflow.keras.models import Sequential

#CUSTOM IMPORTS
#import sys
#import os
# print("TENSORFLOW VERSION:", tf.__version__)
#
'''
1. GET 1 IMAGE AS BYTES, TURN BYTES INTO N BY N ARRAY
2. APPENED IMAGE TO ARRAY
3. DO FOR WHOLE PATH
4. LABEL PATH 1 OR 2
'''




def GETTING_IMAGES_TO_CSVS():
    for img in os.listdir(IMG_DIR='/root/mansura/Python/AI/porn_datasets/not_porn_test/'):
        count=27
        print(img)
        img_array = cv2.imread(os.path.join(IMG_DIR,img), cv2.IMREAD_GRAYSCALE)

        img_pil = Image.fromarray(img_array)
        img_28x28 = np.array(img_pil.resize((28, 28), Image.ANTIALIAS))

        img_array = (img_28x28.flatten())

        img_array  = img_array.reshape(-1,1).T

        # print(len(img_array))
        with open(f'/root/mansura/Python/AI/porn_datasets/testing/not_porn-test-{count}.csv', 'ab') as f:
            np.savetxt(f, img_array, delimiter=",")
        count += 1

        print("NUM FILES:", count )


def GENERATE_LABELS_FOR_PORN_CSVS():
    print("GENERATE_LABELS_FOR_PORN_CSVS")

    '''READING 
    
    /root/mansura/Python/AI/porn_datasets/testing
    '''
    '''ITERATING'''
    porn_labels = []
    directory = '/root/mansura/Python/AI/porn_datasets/testing'
    count = 0
    #PUT THE LABELS IN BY FILENAME 
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            full_file_string = str(f)
            file_string_just_file = full_file_string.split(directory)[1] # just grab the file
            if "not_porn" in file_string_just_file:
                porn_labels.append(0)  
            else:
                porn_labels.append(1)
            count += 1
    # check equal
    print("TOTAL COUNT:", count) 
    print("PORN LABELS:", len(porn_labels))
    # print(porn_labels)
    
    #for i in range(100):
    #    print(porn_labels[i])

    '''WRITE THIS TO A CSV FILE'''
    with open("/root/mansura/Python/AI/porn_datasets/test_labels.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerows([porn_labels]) #dunno why i have to pass it as a list
 
def CUSTOM_LOAD_DATA():
    print("CUSTOM_LOAD_DATA")
    train_images = []
    num_training_files = 0
    directory = '/root/mansura/Python/AI/porn_datasets/training'

    for filename in os.listdir(directory):
        if num_training_files > 10000:
            break
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            # print(f)
            with open(f) as file:
                content = file.readlines()
                # print(content)
                # exit(0)
                train_images.append(content)
                if num_training_files % 100 == 0:
                    print(f"TRAINING FILE: {num_training_files}")
                num_training_files +=1
    
    test_images = []
    num_testing_files = 0
    directory = '/root/mansura/Python/AI/porn_datasets/testing'
    for filename in os.listdir(directory):
        if num_testing_files > 10000:
            break
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            with open(f) as file:
                content = file.readlines()
                test_images.append(content)
                if num_testing_files % 10 == 0:
                    print(f"TESTING FILE FILE: {num_testing_files}")
                
                num_testing_files +=1
    

    train_labels = []
    directory = '/root/mansura/Python/AI/porn_datasets/labels.csv'
    with open(directory) as file:
        content = file.readlines()
        train_labels.append(content[0].split(","))
        train_labels= train_labels[0]
        

    test_labels = []
    directory = '/root/mansura/Python/AI/porn_datasets/test_labels.csv'
    with open(directory) as file:
        content = file.readlines()
        # print(type(content), content)
        test_labels.append(content[0].split(","))
        test_labels = test_labels[0]


        
    print("\nTRAINING IMAGES:", len(train_images))
    print("\nTESTING  IMAGES:", len(test_images))

    print("\nTRAINING LABELS:", len(train_labels))
    print("\nTESTING  LABELS:", len(test_labels))
    return train_images, train_labels, test_images, test_labels

'''
train_images, train_labels, test_images, test_labels = CUSTOM_LOAD_DATA()
#print(print(type(train_images[0])), train_images[0])
#print(train_images[0])

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=10)
#print(train_images)
#print(train_labels)
#print(test_images)
#print(test_labels)
'''

