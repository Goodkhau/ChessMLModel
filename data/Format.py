import datasets as ds
from base.model_V1_0.DataFormatter import TrainingData as formatter


def populate_training_data() -> None:
    hugging_face_link: str = 'angeluriot/chess_games'

    dataset: ds.IterableDatasetDict = ds.load_dataset(hugging_face_link, streaming=True)
    for game in dataset['train']:
        format = formatter(san_chess_notation=game['moves_san'])
        #data: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices(format.san_to_tensorslices())
        for tensor in format.san_to_feature_tensorslices():
            print(tensor)
        break