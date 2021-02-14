from reading_data import reading_files, reading_files_test
from create_dataset import create_dataset
from UMLS_methods import *
from tqdm import tqdm
import pandas as pd
import math

# load training data
train_data, CUI, iCUI = reading_files("./train")
train_df = create_dataset(train_data)


def fill_train_data(df, num):
    df.at[:, 'prediction'] = None
    df.at[:, 'prediction_source'] = None
    df.at[:, 'prediction_name'] = None
    for i in tqdm(df.index, desc=str(num)):
        tgt = get_tgt()
        st = get_st(tgt)
        mention = df.loc[i]['mention']
        CUIs = find_mention_in_UMLS_partial_name(mention, st)
        if len(CUIs)>=1 and CUIs[0]['cui']!='NONE':
            if len(CUIs)==1:
                df.at[i, 'prediction'] = CUIs[0]['cui']
                df.at[i, 'prediction_name'] = CUIs[0]['name']
                df.at[i, 'prediction_source'] = 'UMLS_partial'
            else:
                df.at[i, 'prediction'] = [CUIs[_]['cui'] for _ in range(len(CUIs))]
                df.at[i, 'prediction_name'] = [CUIs[_]['name'] for _ in range(len(CUIs))]
                df.at[i, 'prediction_source'] = 'BERT'
        else:
            df.at[i, 'prediction_source'] = 'Data available nowhere'
            df.at[i, 'prediction_name'] = "CUI-less"
            df.at[i, 'prediction'] = "CUI-less"
    return df  

import concurrent.futures
num_threads = 15
len_df = math.ceil(len(train_df) / num_threads)

train_df_results = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    for _ in range(min(num_threads, len_df)):
        st = int((_)*len_df)
        end = st + len_df
        train_df_ = train_df[st:end]
        future = executor.submit(fill_train_data, train_df_, _)
        train_df_results.append(future)

final_df = pd.concat([_.result() for _ in train_df_results])
final_df.to_csv("dataframe_with_candidate_cuis_train.csv")
