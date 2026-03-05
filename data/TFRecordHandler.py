# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

from typing import override
import datasets as ds
import numpy as np
import tensorflow as tf
import os
from pathlib import Path
from matplotlib import pyplot as plt
from datetime import datetime

from base.Little_Blue.DataFormatter import TrainingData as formatter
from prompter import get_input


class TFRecords():
    def __init__(self, directory:str) -> None:
        self.directory: str = directory
        if not os.path.exists(directory):
            os.mkdir(directory)

    def get_tfrecords_in_dir(self) -> list[str]:
        return [f"{self.directory}/{file}" for file in os.listdir(self.directory)]
    
    def parse_function(self, example) -> tuple[tf.Tensor, tf.Tensor]:
        feature_description = {
            'token': tf.io.FixedLenFeature([], tf.string),
            'label': tf.io.FixedLenFeature([], tf.string)
        }
        parsed_example = tf.io.parse_single_example(example, feature_description)
        parsed_token: tf.Tensor =  tf.io.parse_tensor(parsed_example['token'], out_type=tf.int16)
        parsed_label: tf.Tensor =  tf.io.parse_tensor(parsed_example['label'], out_type=tf.int8)
        return (tf.reshape(tensor=parsed_token, shape=[8,8,8]), tf.reshape(tensor=parsed_label, shape=[386]))

    def serialize_features_with_labels(self, token: tf.Tensor, label: tf.Tensor):
        serialized_token = tf.io.serialize_tensor(token)
        serialized_label = tf.io.serialize_tensor(label)
        data: dict[str, tf.train.Feature] = {
            'token': tf.train.Feature(bytes_list=tf.train.BytesList(value=[serialized_token.numpy()])),
            'label': tf.train.Feature(bytes_list=tf.train.BytesList(value=[serialized_label.numpy()]))
        }
        example = tf.train.Example(features=tf.train.Features(feature=data))
        return example.SerializeToString()

    def remove_population(self) -> None:
        for tfrecord in self.get_tfrecords_in_dir():
            print('Removing: ' + tfrecord)
            os.remove(path=tfrecord)