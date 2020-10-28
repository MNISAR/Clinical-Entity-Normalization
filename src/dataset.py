import config
import torch


class EntityDataset:
    def __init__(self, texts, labels):
        # texts: [["hi", ",", "my", "name", "is", "abhishek"], ["hello".....]]
        # pos/tags: [[1 2 3 4 1 5], [....].....]]
        self.texts = texts
        self.labels = labels
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, item):
        text = self.texts[item]
        label = self.labels[item]

        ids = []
        target_label = []
        target_position = []

        mask_id = config.TOKENIZER.encode("[MASK]", add_special_tokens=False)

        for i, s in enumerate(text):
            inputs = config.TOKENIZER.encode(
                s,
                add_special_tokens=False
            )
            # abhishek: ab ##hi ##sh ##ek
            input_len = len(inputs)
            ids.extend(inputs)
            target_label.extend([label] * input_len)

        ids = ids[:config.MAX_LEN - 2]
        target_label = target_label[:config.MAX_LEN - 2]

        ids = [101] + ids + [102]
        target_label = [0] + target_label + [0]
        try:
            target_position = ids.index(mask_id) + 1 # index of [MASK] + 1 as we add [CLS]
        except:
            target_position = 0

        mask = [1] * len(ids)
        token_type_ids = [0] * len(ids)

        padding_len = config.MAX_LEN - len(ids)

        ids = ids + ([0] * padding_len)
        mask = mask + ([0] * padding_len)
        token_type_ids = token_type_ids + ([0] * padding_len)
        target_label = target_label + ([0] * padding_len)

        return {
            "ids": torch.tensor(ids, dtype=torch.long),
            "mask": torch.tensor(mask, dtype=torch.long),
            "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
            "target_label": torch.tensor(target_label, dtype=torch.long),
            "target_position": torch.tensor(target_position, dtype=torch.long)
        }