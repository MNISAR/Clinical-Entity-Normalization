# create dataset
import pandas as pd

def create_dataset(data):
    """
    This method will convert the text/notes to dataset by replacing one by one the mention by [MASK],
    thus creating gigantic amount of data.

    input:- data: list of dictionary (note, norm, filename)
    output:- pandas dataframe with original sentence, masked sentence, mention, CUI 
    """
    dataset = []
    for d in data:
        note = d['note']
        norm = d['norm']

        for x in norm:
            _, cui = x[0], x[1]
            for i in range(2, len(x), 2):
                st, end = int(x[i]), int(x[i+1])

                dataset.append({
                    'cui': cui,
                    'original_sentence': note,
                    'masked_sentence': note[:st] + "[MASK]" + note[end+1:],
                    'mention': note[st:end+1],
                    'position_start': st,
                    'position_end': end
                    }
                )
    return pd.DataFrame(dataset)
