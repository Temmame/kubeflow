import argparse, os
import pandas as pd
from google.cloud import storage


def preprocess(file_gcs_path, bucket_name):

    # client
    gcs = storage.Client()
    file_ = file_gcs_path.split('/')[-1]
    gcs.get_bucket(bucket_name).blob(file_).download_to_filename('df.csv')
    df = pd.read_csv('df.csv')

    # preprocess
    df = df.fillna(0)

    # split
    TRAINING_SPLIT = 0.8
    df_train = df.loc[:int(TRAINING_SPLIT * len(df)), :]
    df_test = df.loc[int(TRAINING_SPLIT * len(df)):, :]

    # upload pd dataframe into gcs
    df_train.to_csv('df_train.csv', index=False)
    gcs.get_bucket(bucket_name).blob('df_train.csv').upload_from_filename('df_train.csv', content_type='text/csv')
    # upload pd dataframe into gcs
    df_test.to_csv('df_test.csv', index=False)
    gcs.get_bucket(bucket_name).blob('df_test.csv').upload_from_filename('df_test.csv', content_type='text/csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file_gcs_path',
        type=str,
        help='url of data file to preprocess',
        required=True)
    parser.add_argument(
        '--bucket_name',
        type=str,
        help='bucket name',
        required=True)
    args = parser.parse_args()
    preprocess(args.file_gcs_path, args.bucket_name)
