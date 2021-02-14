
# Note:  you will need the UMLS metathesarus as offline data store to get definitions. I did it seperately and unfortunately cannot include it this repo.

# training/finetuning
    In the "fine tuning" directory rin the files in this order.
    1. Run get_data_for_bert_train.py  [This file will generate a "dataframe_with_candidate_cuis_train.csv" that will be used to train NSP model] [dependency: "/2020AA/MRDEF.rrf"]
    2. Run get_definitions.py   [This program will read the file generated above and add definition from UMLS to it. Will generate "all_data_train.pk"]
    3. Run the notebook - all_data to BERT_INput.ipynb [This program will generate input embeddings of particular size for BERT]  
    4. Run Colab notebook - BertModel_NSP.ipynb [This program will generate embeddings for NSP training. Will generate a "extendable.hdf5" file that contains all embeddings and truth values]
    5. Run Colab notebook - NSP_classifier_train.ipyn [This program will train a neural network for NSP classification. Will generate a pyTorch NN model]

# testing/prediction
    In the "fine tuning" directory rin the files in this order.
    1. Run get_data_for_bert_test.py  [This file will generate a "dataframe_with_candidate_cuis_test.csv" that will be used to test NSP model]
    2. Run get_definitions_test.py   [This program will read the file generated above and add definition from UMLS to it. Will generate "all_data_test.pk"]
    3. Run the notebook - all_data to BERT_INput.ipynb [This program will generate input embeddings of particular size for BERT]
    4. Run the notebook - BertModel_NSP.ipynb  [This program will generate embeddings for NSP testing. Will generate a "extendable_test.hdf5" file that contains all embeddings and truth values(gold standards)]
    5. Run Colab notebook - NSP_classifier_train.ipynb [This program will load the neural network for NSP classification, and test our embedding and produce accuracy results]