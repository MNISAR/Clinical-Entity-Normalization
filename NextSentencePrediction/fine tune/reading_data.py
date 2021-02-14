import os
from collections import defaultdict

# specific for training data
def reading_files(base_directory = "train"):
    """
    This method takes a base directory as input and 
    maps the norm fles and notes to a array and dictionary.
    return 
        1. data: array of dictionary(dict contains the file name, norm and note)
        2. CUI dictionary contains text and index for the dictionary in data
        3. iCUI dictionary with inverse mapping from mention to CUIs
    """

    # reading train_file_list.txt to get list of training notes files
    files = []
    with open("{}/train_file_list.txt".format(base_directory)) as f:
        for line in f.readlines():
            files.append(line.strip())
    print("Total number of files: ", len(files))

    # reading list of CUIs
    CUI = {}
    with open("{}/train_norm.txt".format(base_directory)) as f:
        for line in f.readlines():
            CUI[line.strip()] = set()

    print("Total CUIs: ", len(CUI))

    # reading norm and note files from list of files
    data, iCUI = [], defaultdict(set)
    for _, filename in enumerate(files):
        norm_filename = "{}/train_norm/{}.norm".format(base_directory, filename)
        note_filename = "{}/train_note/{}.txt".format(base_directory, filename)

        with open(norm_filename) as f1:
            with open(note_filename) as f2:
                data.append({'name':filename, 
                             'norm':list(map(lambda x: x.strip().split("||"), f1.readlines())), 
                             'note':" ".join(list(map(lambda x: x.strip(), f2.readlines())))    })
        for x in data[-1]['norm']:
            if len(x)>=4:
                i,cui = x[0], x[1]
                mentions = []
                for i in range(2, len(x), 2):
                    mention = (data[-1]['note'][int(x[i]):int(x[i+1])]).strip()
                    mentions.append(mention)
                    iCUI[mention].add(cui)
                CUI[cui].add("|".join(mentions))
            else:
                raise ValueError("{} is wrong".format(x))

    print("Total Data: ", len(data))

    return data, CUI, iCUI

def reading_files_test(base_directory = "testing"):
    """
    The test data has has notes and cui mapping gold standards. It DOES NOT perform CUI-> mention 

    returns a list of dictionary with {name, note, norm}
    """
    test_note_list = "{}/test/test_file_list.txt".format(base_directory)
    note_file_base = "{}/test/test_note".format(base_directory)
    norm_file_base = "{}/gold/test_norm".format(base_directory)
    # reading train_file_list.txt to get list of training notes files
    files = []
    with open(test_note_list) as f:
        for line in f.readlines():
            files.append(line.strip())
    print("Total number of files: ", len(files))

    data = []
    for _, file in enumerate(files):
        note_file_name = "{}/{}.txt".format(note_file_base, file)
        norm_file_name = "{}/{}.norm".format(norm_file_base, file)
        with open(norm_file_name) as f1:
            with open(note_file_name) as f2:
                data.append({'name':file, 
                             'norm':list(map(lambda x: x.strip().split("||"), f1.readlines())), 
                             'note':" ".join(list(map(lambda x: x.strip(), f2.readlines())))    })
    return data, {}
    
    

if __name__ == "__main__":
    base_dir = "C:/Users/monil/Desktop/BMI 598 - NLP/Project/Clinical-Entity-Normalization/train"
    # data, CUI, iCUI = reading_files(base_dir)

    # cui = "C0333307"
    # print("For CUI: ", cui)
    # print(CUI[cui])
    # for _, mention in CUI[cui]:
    #     print(mention, " : ", data[_]['note'][:100], end="\n\n")

    test_base_dir = "C:/Users/monil/Desktop/BMI 598 - NLP/Project/Clinical-Entity-Normalization/testing"
    test_data, _ = reading_files_test(test_base_dir)
    print(test_data[0])