from typing import override
import datasets as ds
import numpy as np
import tensorflow as tf
import os
from pathlib import Path
from matplotlib import pyplot as plt
from datetime import datetime

from base.model_V1_0.DataFormatter import TrainingData as formatter
from data.Pipeline_Interface import Pipeline_Interface
from data.TFRecords import TFRecords

from huggingface_hub import login


class Cycle_TFRecords(Pipeline_Interface):
    def __init__(self) -> None:
        return

    @override
    def train_model(self, model) -> None:
        datenow: str = datetime.now().strftime(format="%Y%m%d%H%M%S")
        pipeline: Pipeline_Interface = TFRecords(model.name)
        directory = f"{Path.cwd()}/data/training_data/{model.name}/"
        if not os.path.exists(directory):
            os.mkdir(directory)
        
        hugging_face_link: str = 'angeluriot/chess_games'
        hugging_face_token: str = ''
        login(token=hugging_face_token)

        complete_token: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices(tensors=np.empty((0,) + (8,8,8), dtype=np.int16))
        complete_label: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices(tensors=np.empty((0,) + (386,), dtype=np.int8))
        tfrecord_size: int = 1000
        limit_games: int = 25000

        counter: int = 0
        current_record: int = 0
        iteration: int = 0

        dataset: ds.IterableDatasetDict = ds.load_dataset(hugging_face_link, streaming=True)

        for index, game in enumerate[dict[str, list[str]]](dataset['train']):
            format = formatter(san_chess_notation=game['moves_san'])
            counter += 1

            if (counter <= tfrecord_size and (index%limit_games != 0 or index == 0)):
                token: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices((format.san_to_token_tensorslices()))
                label: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices((format.san_to_label_tensorslices()))
                complete_token = complete_token.concatenate(dataset=token)
                complete_label = complete_label.concatenate(dataset=label)
                continue
            
            tfrecord_path: str = f"{Path.cwd()}/data/training_data/{model.name}/{datenow}_{current_record:04}"
            print("Writing to file: " + tfrecord_path)
            with tf.io.TFRecordWriter(path=tfrecord_path) as writer:
                complete_data = tf.data.Dataset.zip(complete_token, complete_label)
                for token, label in complete_data:
                    writer.write(record=pipeline.serialize_features_with_labels(token, label))
            
            print(str(index) + ' of 14188454')
            
            complete_token = tf.data.Dataset.from_tensor_slices((format.san_to_token_tensorslices()))
            complete_label = tf.data.Dataset.from_tensor_slices((format.san_to_label_tensorslices()))
            counter = 1 # reset counter
            current_record += 1

            if index%limit_games == 0:
                print("Starting training.")
                pipeline.train_model(model)
                pipeline.remove_population()
                current_record = 0
                iteration+=1

                if iteration%5 == 0:
                    model.save(f"{Path.cwd()}/base/model_V1_0/outputs/{model.name}_{iteration//5-1:04}.keras")
        
        iteration+=1
        model.save(f"{Path.cwd()}/base/model_V1_0/outputs/{model.name}_{iteration//5:04}.keras")