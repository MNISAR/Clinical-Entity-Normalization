from reading_data import reading_files, reading_files_test
from create_dataset import create_dataset
from UMLS_methods import *
from tqdm import tqdm
import pandas as pd

# load training data
train_data, CUI, iCUI = reading_files("./train")
train_df = create_dataset(train_data)
### removing CUIs from dataset that have only one mentions
train_single_cui = []
for cui, mention in CUI.items():
    if len(mention) == 1:
        train_single_cui.append(cui)


# load test data
test_data, _ = reading_files_test("./testing")
test_df = create_dataset(test_data)

def fill_test_data(test_df, iCUI, num):
    test_df.at[:, 'prediction'] = None
    test_df.at[:, 'prediction_source'] = None
    for i in tqdm(test_df.index, desc=str(num)):
        tgt = get_tgt()
        st = get_st(tgt)
        mention = test_df.loc[i]['mention']
        if mention in iCUI:   # iterating train data
            if 'CUI-less' in iCUI[mention]:
                test_df.at[i, 'prediction'] = 'CUI-less'
                test_df.at[i, 'prediction_source'] = 'train_data'
            elif len(iCUI[mention])==1:
                test_df.at[i, 'prediction'] = list(iCUI[mention])[0]
                test_df.at[i, 'prediction_source'] = 'train_data'            
            else:
                test_df.at[i, 'prediction'] = iCUI[mention]
                test_df.at[i, 'prediction_source'] = 'BERT'
        else:
            CUIs = find_mention_in_UMLS_partial_name(mention, st)
            if len(CUIs)>=1 and CUIs[0]['cui']!='NONE':
                if len(CUIs)==1:
                    test_df.at[i, 'prediction'] = CUIs[0]['cui']
                    test_df.at[i, 'prediction_source'] = 'UMLS_partial'
                else:
                    test_df.at[i, 'prediction'] = [CUIs[_]['cui'] for _ in range(len(CUIs))]
                    test_df.at[i, 'prediction_source'] = 'BERT'
            else:
                test_df.at[i, 'prediction_source'] = 'Data available nowhere'
                test_df.at[i, 'prediction'] = "CUI-less"
    return test_df  

import concurrent.futures
num_threads = 15
len_df = int(len(test_df) / num_threads)

test_df_results = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    for _ in range(min(num_threads, len_df)):
        st = int((_)*len_df)
        end = st + len_df
        test_df_ = test_df[st:end]
        future = executor.submit(fill_test_data, test_df_, iCUI, _)
        test_df_results.append(future)

final_df = pd.concat([_.result() for _ in test_df_results])
final_df.to_csv("final_df.csv")
