"""Training module"""

import os
import glob

import tensorflow as tf

ROOT_PATH = './data'
IMAGES_PATH = ROOT_PATH + os.sep + 'Brain_Data_Organised'
BEST_LEARNING_RATE = 0.001
BEST_SIZE = 1000
BEST_DROP_RATE = 0.2
TRAINING_EPOCHS = 50
TFLITE_MODEL_PATH = ROOT_PATH + os.sep + 'model.tflite'


def get_image_datasets(images_path, validation_split=0.2, target_size=(224, 224), batch_size=20):
    """Generates the training and validation image datasets"""
    img_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255, validation_split=validation_split)

    train_ds = img_generator.flow_from_directory(
        images_path, target_size=target_size, batch_size=batch_size, shuffle=True, class_mode='binary', subset='training'
    )

    validation_ds = img_generator.flow_from_directory(
        images_path, target_size=target_size, batch_size=batch_size, shuffle=True, class_mode='binary', subset='validation'
    )

    return train_ds, validation_ds


def create_model(input_shape=(224, 224, 3), inner_size=100, drop_rate=0.1, learning_rate=0.001):
    """Creates the CNN model based on Transfer Learning"""
    base_model = tf.keras.applications.InceptionV3(input_shape=input_shape, include_top=False, weights='imagenet')

    base_model.trainable = False

    model = tf.keras.Sequential(
        [
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(inner_size, activation='relu'),
            tf.keras.layers.Dropout(rate=drop_rate),
            tf.keras.layers.Dense(1, activation='sigmoid'),
        ]
    )

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss=tf.keras.losses.BinaryCrossentropy(), metrics=['accuracy'])

    return model


def train_model(model, train_ds, validation_ds, steps_per_epoch=20, epochs=20, callbacks=[]):
    """Trains the model"""
    history = model.fit(train_ds, validation_data=validation_ds, steps_per_epoch=steps_per_epoch, epochs=epochs, callbacks=callbacks)

    return history, model


def search_best_model(path):
    """Searches the best model among checkpoints"""
    saved_models = glob.glob(path + os.sep + 'model_*.h5')
    best_model = sorted(saved_models, reverse=True)[0]
    return best_model


def convert_model_to_tflite(model_path, tflite_model_path):
    """Converts the model to tflite"""
    model = tf.keras.models.load_model(model_path)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    with open(tflite_model_path, 'wb') as f_out:
        f_out.write(tflite_model)


if __name__ == '__main__':
    print('Reading image datasets')
    train_ds, validation_ds = get_image_datasets(images_path=IMAGES_PATH)

    print('Creating model')
    model = create_model(learning_rate=BEST_LEARNING_RATE, inner_size=BEST_SIZE, drop_rate=BEST_DROP_RATE)

    print('Training model')
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        ROOT_PATH + os.sep + 'model_{epoch:02d}_{val_accuracy:.3f}.h5', save_best_only=True, monitor='val_accuracy', mode='max'
    )
    callbacks = [checkpoint]
    train_model(model, train_ds=train_ds, validation_ds=validation_ds, epochs=TRAINING_EPOCHS, callbacks=callbacks)

    print('Serching best model')
    best_model_path = search_best_model(ROOT_PATH)
    print(f'Best model: {best_model_path}')

    print('Converting model to tflite')
    convert_model_to_tflite(best_model_path, TFLITE_MODEL_PATH)
