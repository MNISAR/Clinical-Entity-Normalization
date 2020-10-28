import transformers

MAX_LEN = 128
TRAIN_BATCH_SIZE = 32
VALID_BATCH_SIZE = 8
EPOCHS = 10
BASE_MODEL_PATH = "bert-base-uncased"
MODEL_PATH = "model.bin"
# TRAINING_FILE = "../input/ner_dataset.csv"
TRAINING_FILE = "./train"
TOKENIZER = transformers.BertTokenizer.from_pretrained(
    BASE_MODEL_PATH,
    do_lower_case=True
)