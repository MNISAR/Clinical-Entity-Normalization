import os


def reading_files(base_directory = "train", train_file_list="train_file_list", train_norm="train_norm"):
    """
    This method takes a base directory as input and 
    maps the norm fles and notes to a array and dictionary.
    return 
        1. data: array of dictionary(dict contains the file name, norm and note)
        2. CUI dictionary contains text and index for the dictionary in data
    """

    # reading train_file_list.txt to get list of training notes files
    files = []
    with open("{}/{}.txt".format(base_directory, train_file_list)) as f:
        for line in f.readlines():
            files.append(line.strip())
    print("Total number of files: ", len(files))

    # reading list of CUIs
    CUI = {}
    with open("{}/{}.txt".format(base_directory, train_norm)) as f:
        for line in f.readlines():
            CUI[line.strip()] = set()

    print("Total CUIs: ", len(CUI))

    # reading norm and note files from list of files
    data = []
    for _, filename in enumerate(files):
        norm_filename = "{}/train_norm/{}.norm".format(base_directory, filename)
        note_filename = "{}/train_note/{}.txt".format(base_directory, filename)

        with open(norm_filename) as f1:
            with open(note_filename) as f2:
                data.append({'name':filename, 
                             'norm':list(map(lambda x: x.strip().split("||"), f1.readlines())), 
                             'note':" ".join(list(map(lambda x: x.strip(), f2.readlines())))    })
        for x in data[-1]['norm']:
            if len(x)==4:
                (i, cui, st, en) = x
                mention = (data[-1]['note'][int(st):int(en)]).strip()
                CUI[cui].add((_, mention))
            elif len(x)>4:
                i,cui = x[0], x[1]
                mentions = []
                for i in range(2, len(x), 2):
                    mention = (data[-1]['note'][int(x[i]):int(x[i+1])]).strip()
                    mentions.append(mention)
                CUI[cui].add((_, "|".join(mentions)))
            else:
                raise ValueError("{} is wrong".format(x))

    print("Total Data: ", len(data))

    return data, CUI


if __name__ == "__main__":
    base_dir = "C:/Users/monil/Desktop/BMI 598 - NLP/Project/Clinical-Entity-Normalization/train"
    data, CUI = reading_files(base_dir)

    cui = "C0333307"
    print("For CUI: ", cui)
    print(CUI[cui])
    for _, mention in CUI[cui]:
        print(mention, " : ", data[_]['note'][:100], end="\n\n")