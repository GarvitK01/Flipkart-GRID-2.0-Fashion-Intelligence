import numpy as np
import keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create_model():

    """
    Create a Sequential Model for training on image data
    """
    new_input = keras.layers.Input(shape = (224, 224, 3))
    inception_v3 = keras.applications.InceptionV3(include_top = False, input_tensor=new_input)

    model = keras.Sequential()
    model.add(inception_v3)
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dropout(0.35))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dense(128))
    model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dense(2, activation = 'softmax'))

    return model


def create_image_generator():
    datagen = ImageDataGenerator(rescale = 1.0/255.0, horizontal_flip=True, zoom_range=[1.2, 1.5])

    generator_men = datagen.flow_from_directory(directory='Pics/Men/', target_size = (224, 224),
                                                batch_size=32, 
                                                class_mode='categorical'
                                            )

    generator_women = datagen.flow_from_directory(directory='Pics/Women/', target_size = (224, 224),
                                                batch_size=32, 
                                                class_mode='categorical'
                                            )

    return generator_men, generator_women



def train_save_model():

    model = create_model()

    model.compile(optimizer = "Adam", loss = 'categorical_crossentropy', metrics = ['accuracy'])

    # Creating Image Datagenerators for Training
    generator_men, generator_women = create_image_generator()

    # Training Model
    model.fit_generator(generator_men, epochs=15)
    model.fit_generator(generator_women, epochs = 15)

    #Saving Model
    model.save('inception_v3.h5')
