import pandas as pd
import numpy as np

import joblib
import torch

from sklearn import preprocessing
from sklearn import model_selection

from transformers import AdamW
from transformers import get_linear_schedule_with_warmup

import config
import dataset
import engine
from model import EntityModel


from reading_data import reading_files
from create_dataset import create_dataset
def process_data(data_path):
    data, CUI = reading_files(config.TRAINING_FILE)
    dataset = create_dataset(data)

    data = dataset.masked_sentence.to_numpy()
    label = dataset.mention.to_numpy()

    enc_label = preprocessing.LabelEncoder()

    label = enc_label.fit_transform(label)

    return data, label, enc_label

if __name__ == "__main__":
    sentences, label, enc_label = process_data(config.TRAINING_FILE)
    
    meta_data = {
        "enc_label": enc_label
    }

    joblib.dump(meta_data, "meta.bin")

    num_label = len(list(enc_label.classes_))

    (
        train_sentences,
        test_sentences,
        train_label,
        test_label,
    ) = model_selection.train_test_split(sentences, label, random_state=42, test_size=0.1)

    train_dataset = dataset.EntityDataset(
        texts=train_sentences, labels=train_label
    )

    train_data_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=config.TRAIN_BATCH_SIZE, num_workers=4
    )

    valid_dataset = dataset.EntityDataset(
        texts=test_sentences, labels=test_label
    )

    valid_data_loader = torch.utils.data.DataLoader(
        valid_dataset, batch_size=config.VALID_BATCH_SIZE, num_workers=1
    )

    device = torch.device("cuda")
    model = EntityModel(num_labels=num_label)
    model.to(device)

    param_optimizer = list(model.named_parameters())
    no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
    optimizer_parameters = [
        {
            "params": [
                p for n, p in param_optimizer if not any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.001,
        },
        {
            "params": [
                p for n, p in param_optimizer if any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.0,
        },
    ]

    num_train_steps = int(len(train_sentences) / config.TRAIN_BATCH_SIZE * config.EPOCHS)
    optimizer = AdamW(optimizer_parameters, lr=3e-5)
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=0, num_training_steps=num_train_steps
    )

    best_loss = np.inf
    for epoch in range(config.EPOCHS):
        train_loss = engine.train_fn(train_data_loader, model, optimizer, device, scheduler)
        test_loss = engine.eval_fn(valid_data_loader, model, device)
        print(f"Train Loss = {train_loss} Valid Loss = {test_loss}")
        if test_loss < best_loss:
            torch.save(model.state_dict(), config.MODEL_PATH)
            best_loss = test_loss
