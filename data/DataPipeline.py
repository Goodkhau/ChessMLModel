# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

import datasets as ds
import tensorflow as tf
from base.model_V1_0.DataFormatter import TrainingData as formatter
from prompter import get_input


def serialize_features_with_labels(token: tf.Tensor, label: tf.Tensor):
    data: dict[str, tf.train.Feature] = {
        'token': tf.train.Feature(int16_list=tf.train.Int16List(value=[token])),
        'label': tf.train.Feature(int8_list=tf.train.Int8List(value=[label])),
    }
    example = tf.train.Example(features=tf.train.Feature(feature=data))
    return example.SerializeToString()

def populate_training_data(name: str) -> None:
    hugging_face_link: str = 'angeluriot/chess_games'

    data: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensors(tensors=0)
    tfrecord_size: int = get_input(lower=100000, upper=1000000, prompt="Enter the size of the TF records by the number of games.")
    limit_games: int = get_input(lower=1, upper=1000*tfrecord_size, prompt="Enter the number of games you want to process.")

    counter: int = 0
    current_record: int = 0

    dataset: ds.IterableDatasetDict = ds.load_dataset(hugging_face_link, streaming=True)
    for index, game in enumerate[dict[str, list[str]]](dataset['train']):
        counter += 1

        if (counter <= tfrecord_size and index < limit_games):
            format = formatter(san_chess_notation=game['moves_san'])
            current: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices((format.san_to_token_tensorslices(), format.san_to_label_tensorslices()))
            data = data.concatenate(dataset=current)

        counter = 0 # reset counter
        tfrecord_path: str = f"training_data/{name}_{current_record:04}"
        with tf.io.TFRecordWriter(path=tfrecord_path) as writer:
            for tensor in data:
                serialized_example = serialize_features_with_labels(tensor[0], tensor[1])
                writer.write(record=serialized_example.numpy())
        
        if index >= limit_games:
            break