# Task 5: Clinical Entity normalization and linking

The CODE folder contains the necessary files that are required to run the program.
We used google colab to run the code.
The dependencies are iteslf resolved in the colab's environemnt and we have installed other required libraries within the code.

## how to run?
Training (fine-tune):
run all cells of the file training_pipeline.ipynb. This will load the dependencies and the data(our data) from a remote repository, fine-tune the BERT model on it. Then the model and meta-data files generated are stored in google drive.

Testing:
run all cells of the fiel testing_pipeline.ipynb. This will load files from google drive and test it on our test data and report accuracy.

The Model and meta_data are in the folder on drive with link: https://drive.google.com/drive/folders/1DRvN56VyGQkD8BaiXvcKHukecB54EVA8?usp=sharing

Other instructions on running the notebook files are provided inside the notebook itself.

These above steps will generate 3 files. "final_df.csv", "file_with_BERT_prediction.csv", "file_with_non_BERT_prediction.csv" which can be used to analyse the results.