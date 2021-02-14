import pandas as pd
from UMLS_methods import find_defination_for_cui
import numpy as np
from tqdm import tqdm
import pickle

import pandas as pd
path = "/2020AA/MRDEF.rrf"  # path to a file in UMLS metathesaurus
df_definations = pd.read_csv(path, delimiter="|", encoding="utf-8", header=0, converters={5: lambda x: x.lower()})
df_definations.loc[len(df_definations)] = df_definations.columns
df_definations.columns = ["CUI", "AUI", "ATUI", "SATUI", "SAB", "DEF", "SUPPRESS", "CVF", "B" ]


def search_cui(cui):
    x = list(df_definations[df_definations["CUI"]==cui]["DEF"].to_numpy())
    return x
    
import concurrent.futures
def get_def(cuis):
    num_threads = len(cuis)
    definitions = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for cui in cuis:
            # future = executor.submit(find_defination_for_cui, cui)
            future = executor.submit(search_cui, cui)
            definitions.append(future)

    return [_.result() for _ in definitions]


all_data = []
df = pd.read_csv("dataframe_with_candidate_cuis_train.csv")
for index in tqdm(df.index):

    if index%100 == 0:
        with open("all_data.pk", "wb") as f:
            pickle.dump(all_data, f)

    row = df.loc[index]
    d = {
        'id': index,
        'actual_cui': row['cui'],
        'sentence': row['original_sentence'],
        'start': row['position_start'],
        'end': row['position_end']
    }
    try:
        candidate_cuis = eval(row['prediction'])
    except NameError:
        continue

    candidate_cui_names = eval(row['prediction_name'])
    cuis_definition = get_def(candidate_cuis)
    # print(len(cuis_definition), len(cuis_definition[0]))
    # there can be multiple definition for each CUI, we will use all
    for cui_name, cui_definitions, cui in zip(candidate_cui_names, cuis_definition, candidate_cuis):
        for definition in cui_definitions:
            d_ = {}
            for k,v in d.items():
                d_[k] = v
            d_["definition"] = f"{cui_name} means {definition}"
            d_['cui'] = cui
            all_data.append(d_)

with open("all_data_train.pk", "wb") as f:
    pickle.dump(all_data, f)
