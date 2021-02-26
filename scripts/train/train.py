import argparse, os
import pandas as pd
from google.cloud import storage
from sklearn.linear_model import LinearRegression as LR
import pickle


def train(path_train, bucket_name):

    # read train data
    df_train = pd.read_csv(path_train)

    # train model
    lr = LR()
    X = df_train.drop(['label'], axis=1)
    Y = df_train['label']
    lr.fit(X, Y)

    # save model
    with open('model.pkl', 'wb') as model_file:
        pickle.dump(lr, model_file)

    # if we want to save model in gcs
    gcs = storage.Client()
    gcs.get_bucket(bucket_name).blob('trained_model/model.pkl').upload_from_filename('model.pkl')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path_train',
        type=str,
        help='path of data file to train',
        required=True)
    parser.add_argument(
        '--bucket_name',
        type=str,
        help='bucket name',
        required=True)
    args = parser.parse_args()
    train(args.path_train, args.bucket_name)
