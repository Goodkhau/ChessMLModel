import gc
from tensorflow import Tensor
import datasets as ds
import numpy as np
import tensorflow as tf
import os

from typing import override
from pathlib import Path
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from huggingface_hub import login

from base.Little_Blue.DataFormatter import TrainingData as formatter
from data.Pipeline_Interface import Pipeline_Interface
from data.TFRecordHandler import TFRecords

TFRECORD_SIZE: int = 1000
LIMIT_GAMES: int = 100000
EPOCHS: int = 67

class Cycle_TFRecords(Pipeline_Interface):
    def __init__(self) -> None:
        self.pipeline_name: str = datetime.now().strftime(format="%Y%m%d%H%M%S")
    
    def _not_dir_mk(self, directory:str) -> None:
        if not os.path.exists(directory):
            os.mkdir(directory)

    def _make_direcory(self, model_name:str) -> None:
        self.directory: str = f"{Path.cwd()}/base/{model_name}/outputs/{self.pipeline_name}"
        
        graphplot_dir: str = f"{self.directory}/plots"
        keras_output: str = f"{self.directory}/keras"
        tensorboard_dir: str = f"{self.directory}/tensorboard"

        self._not_dir_mk(self.directory)
        self._not_dir_mk(graphplot_dir)
        self._not_dir_mk(keras_output)
        self._not_dir_mk(tensorboard_dir)

    @override
    def train_model(self, model) -> None:
        self._make_direcory(model.name)
        log_dir: str = f"{self.directory}/log.txt"

        tfrecord = TFRecords(f"{self.directory}/tfrecords")

        hugging_face_link: str = 'angeluriot/chess_games'
        hugging_face_token: str = ''
        login(token=hugging_face_token)

        huggingface_data: ds.IterableDatasetDict = ds.load_dataset(hugging_face_link, streaming=True)

        complete_token: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices(tensors=np.empty((0,) + (8,8,8), dtype=np.int16))
        complete_label: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices(tensors=np.empty((0,) + (386,), dtype=np.int8))

        iteration: int = 0
        tfrec_cnt: int = 0

        first: datetime = datetime.now()
        total_time: int = 0
        for index, game in enumerate[dict[str, list[str]]](huggingface_data['train']):
            format = formatter(san_chess_notation=game['moves_san'])

            if (index+1)%TFRECORD_SIZE != 0 or index == 14188453:
                token: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices((format.san_to_token_tensorslices()))
                label: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices((format.san_to_label_tensorslices()))
                complete_token = complete_token.concatenate(dataset=token)
                complete_label = complete_label.concatenate(dataset=label)
                continue

            with tf.io.TFRecordWriter(path=f'{tfrecord.directory}/{tfrec_cnt:04}') as writer:
                combined_data = tf.data.Dataset.zip(complete_token, complete_label)
                for token, label in combined_data:
                    writer.write(record=tfrecord.serialize_features_with_labels(token, label))  # pyright: ignore[reportUnknownArgumentType, reportArgumentType]
            tfrec_cnt += 1
            
            complete_token = tf.data.Dataset.from_tensor_slices((format.san_to_token_tensorslices()))
            complete_label = tf.data.Dataset.from_tensor_slices((format.san_to_label_tensorslices()))
            
            if (index+1)%LIMIT_GAMES != 0 and index != 14188453:
                continue
            
            with open(log_dir, 'a') as writer:
                _ = writer.write(str(index+1) + ' of 14188454\nStarting training.\n')
            
            for current, record_dir in enumerate[str](tfrecord.get_tfrecords_in_dir()):
                raw_dataset: tf.data.Dataset[tf.Tensor] = tf.data.TFRecordDataset(filenames=record_dir)
                dataset: tf.data.Dataset[tuple[Tensor, Tensor]] = raw_dataset.map(tfrecord.parse_function, num_parallel_calls=tf.data.AUTOTUNE)
            
                dataset = dataset.shuffle(buffer_size=1024, reshuffle_each_iteration=True)
                dataset = dataset.batch(batch_size=512)
                # dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)

                validation: tf.data.Dataset[tuple[tf.Tensor, tf.Tensor]] = dataset.skip(int(0.8*82*TFRECORD_SIZE))
                dataset = dataset.take(int(0.8*82*TFRECORD_SIZE))

                tensorboard_callback = tf.keras.callbacks.TensorBoard(f"{self.directory}/tensorboard")
                history = model.fit((dataset), epochs=EPOCHS, validation_data=(validation), callbacks=[tensorboard_callback])
            
                fig = plt.figure()
                plt.plot(history.history['loss'], color='teal', label='loss')
                plt.plot(history.history['accuracy'], color='lime', label='accuracy')
                fig.suptitle('Loss', fontsize=20)
                fig.suptitle('Accuracy', fontsize=20)
                plt.legend(loc='upper left')
                plt.savefig(f"{self.directory}/plots/{iteration-1:06}_{current}.pdf", format='pdf', bbox_inches='tight')

            with open(log_dir, 'a') as writer:
                second: datetime = datetime.now()
                time_taken: int = int((second-first).total_seconds())
                total_time += time_taken
                first = second
                time_mins: float = (total_time/(iteration+1) * (14188453-index)/LIMIT_GAMES)/60

                _ = writer.write(f"Cleaning ' + {str(gc.collect())} + ' objects\n")
                _ = writer.write(f"Finished in {time_taken/60} mins.\nEstimated time left: {time_mins//60}H  {time_mins%60}m\n")

            model.save(f"{self.directory}/keras/{iteration:04}.keras")
            tfrecord.remove_population()
            iteration+=1
            tfrec_cnt = 0
        
        model.save(f"{self.directory}/keras/{iteration:04}.keras")