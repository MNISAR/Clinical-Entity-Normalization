import os


def reading_files(base_directory = "train"):
    """
    This method takes a base directory as input and 
    maps the norm fles and notes to a array and dictionary.
    return 
        1. data: array of dictionary(dict contains the file name, norm and note)
        2. CUI dictionary contains text and index for the dictionary in data
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

    combined_texts_filename = "{}/{}.txt".format(base_directory, "combined_text")
    transformed_combined_texts_filename = "{}/{}.txt".format(base_directory, "transformed_combined_text")

    # reading norm and note files from list of files
    data = []
    all_notes = []
    all_transformed_notes = []
    for _, filename in enumerate(files):
        norm_filename = "{}/train_norm/{}.norm".format(base_directory, filename)
        note_filename = "{}/train_note/{}.txt".format(base_directory, filename)
        transformed_texts_filename = "{}/train_note/{}.txt".format(base_directory, "transformed_"+filename)

        with open(norm_filename) as f1:
            with open(note_filename) as f2:
                data.append({'name':filename, 
                             'norm':list(map(lambda x: x.strip().split("||"), f1.readlines())), 
                             'note':" ".join(list(map(lambda x: x.strip(), f2.readlines())))    })
        
        all_notes.append(data[-1]['note'])
        transformed_note = data[-1]['note']
        st, en = 0, 0
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
            transformed_note = transformed_note[:int(st)] + cui + transformed_note[int(en):]
        with open(transformed_texts_filename, 'w') as f3:
            f3.write(transformed_note)
        all_transformed_notes.append(transformed_note)


    with open(combined_texts_filename, 'w') as f4:
        f4.write('\n'.join(all_notes))
    with open(transformed_combined_texts_filename, 'w') as f5:
        f5.writelines('\n'.join(all_transformed_notes))



    # print("Total Data: ", len(data))

    return data, CUI


if __name__ == "__main__":
    base_dir = "C:/Users/Jaysn/Anaconda3/envs/NLP/Clinical-Entity-Normalization/train"
    data, CUI = reading_files(base_dir)

    # cui = "C0333307"
    # print("For CUI: ", cui)
    # print(CUI[cui])
    # for _, mention in CUI[cui]:
    #     print(mention, " : ", data[_]['note'][:100], end="\n\n")