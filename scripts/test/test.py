import argparse, os
import pandas as pd
from google.cloud import storage
from sklearn.metrics import mean_squared_error
import pickle


def test(path_test, path_model, bucket_name):

    with open(path_model, "rb") as f:
        model = pickle.load(f)

    df_test = pd.read_csv(path_test)
    df_test['pred'] = model.predict(df_test.drop(['label'], axis=1))
    err = mean_squared_error(df_test['label'].values, df_test['pred'].values)
    with open('metrics.txt', 'a') as f:
        f.write(str(err))
    df_test.to_csv('df_pred.csv')

    # if we want to save in gcs
    gcs = storage.Client()
    gcs.get_bucket(bucket_name).blob('prediction.csv').upload_from_filename('df_pred.csv', content_type='text/csv')
    gcs.get_bucket(bucket_name).blob('metrics.txt').upload_from_filename('metrics.txt', content_type='text/csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path_test',
        type=str,
        help='data file to test',
        required=True)
    parser.add_argument(
        '--path_model',
        type=str,
        help='model file',
        required=True)
    parser.add_argument(
        '--bucket_name',
        type=str,
        help='bucket name',
        required=True)
    args = parser.parse_args()
    test(args.path_test, args.path_model, args.bucket_name)
