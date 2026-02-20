# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

import datasets as ds
import numpy as np
import tensorflow as tf
import os
from pathlib import Path
from matplotlib import pyplot as plt
from abc import ABC, abstractmethod
from datetime import datetime

from base.model_V1_0.DataFormatter import TrainingData as formatter
from prompter import get_input


class Pipeline_Interface(ABC):
    @abstractmethod
    def train_model(self, model) -> None:
        pass


class TFRecords(Pipeline_Interface):
    def __init__(self, name:str|None = None) -> None:
        self.name: str = name if name else datetime.now().strftime(format="%Y%m%d%H%M%S")

    def train_model(self, model) -> None:
        directory = f"{Path.cwd()}/data/training_data/{self.name}/"
        if not os.path.exists(directory):
            print(f"DataPipeline.py Error: data for TFRecord pipeline '/training_data/{self.name}/' does not exist.")
            return
        
        tfrecords: list[str] = []
        for file in os.listdir(directory):
            if file is 'data_spec.json':
                continue

            tfrecords.append(file)
        
        for tfrecord in tfrecords:
            dataset: tf.data.Dataset[tf.Tensor] = tf.data.TFRecordDataset(filenames=tfrecord)
            data_size = int(len(dataset))

            validation = dataset.skip(int(data_size*0.7)).take(int(data_size*0.2))
            evaulation = dataset.skip(int(data_size*0.9)).take(int(data_size*0.1))
            dataset = dataset.take(int(data_size*0.7))

            tensorboard_callback = tf.keras.callbacks.TensorBoard(f"{Path.cwd()}/base/{model.name}/{self.name}/logs/")

            history = model.fit(dataset, epochs=5, validation_data=validation, callbacks=[tensorboard_callback])

            fig = plt.figure()
            _ = plt.plot(history.history['loss'], color='teal', label='loss')
            _ = plt.plot(history.history['val_loss'], color='orange', label='val_loss')
            _ = fig.suptitle('Loss', fontsize=20)
            _ = plt.legend(loc='upper left')
            plt.show()


    def serialize_features_with_labels(self, token: tf.Tensor, label: tf.Tensor):
        serialized_token = tf.io.serialize_tensor(token)
        serialized_label = tf.io.serialize_tensor(label)
        data: dict[str, tf.train.Feature] = {
            'token': tf.train.Feature(bytes_list=tf.train.BytesList(value=[serialized_token.numpy()])),
            'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[serialized_label.numpy()]))
        }
        example = tf.train.Example(features=tf.train.Features(feature=data))
        return example.SerializeToString()


    def populate_training_data(self, default_size:int, default_games:int) -> None:
        hugging_face_link: str = 'angeluriot/chess_games'

        complete_token: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices(tensors=np.empty((0,) + (8,8,8), dtype=np.int16))
        complete_label: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices(tensors=np.empty((0,) + (386,), dtype=np.int8))
        tfrecord_size: int = default_size if default_size else get_input(lower=100000, upper=1000000, prompt="Enter the size of the TF records by the number of games.")
        limit_games: int = default_games if default_games else get_input(lower=1, upper=1000*tfrecord_size, prompt="Enter the number of games you want to process.")

        counter: int = 0
        current_record: int = 0

        dataset: ds.IterableDatasetDict = ds.load_dataset(hugging_face_link, streaming=True)
        directory = f"{Path.cwd()}/data/training_data/{self.name}/"
        if not os.path.exists(directory):
            os.mkdir(directory)

        for index, game in enumerate[dict[str, list[str]]](dataset['train']):
            format = formatter(san_chess_notation=game['moves_san'])
            counter += 1

            if (counter <= tfrecord_size and index < limit_games):
                token: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices((format.san_to_token_tensorslices()))
                label: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices((format.san_to_label_tensorslices()))
                complete_token = complete_token.concatenate(dataset=token)
                complete_label = complete_label.concatenate(dataset=label)
                continue

            tfrecord_path: str = f"{Path.cwd()}/data/training_data/{self.name}/{self.name}_{current_record:04}"
            with tf.io.TFRecordWriter(path=tfrecord_path) as writer:
                complete_data = tf.data.Dataset.zip(complete_token, complete_label)
                for token, label in complete_data:
                    writer.write(record=self.serialize_features_with_labels(token, label))  # pyright: ignore[reportUnknownArgumentType  # pyright: ignore[reportUnknownArgumentType, reportArgumentType]
            
            complete_token = tf.data.Dataset.from_tensor_slices((format.san_to_token_tensorslices()))
            complete_label = tf.data.Dataset.from_tensor_slices((format.san_to_label_tensorslices()))
            counter = 1 # reset counter
            current_record += 1

            print(str(index) + ' of ' + str(limit_games))
            if index >= limit_games:
                break