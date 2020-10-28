import config
import torch
import transformers
import torch.nn as nn

def loss_fn(output, target, mask, num_labels):
    lfn = nn.CrossEntropyLoss()
    active_loss = mask.view(-1) == 1
    active_logits = output.view(-1, num_labels)
    active_labels = torch.where(
        active_loss,
        target.view(-1),
        torch.tensor(lfn.ignore_index).type_as(target)
    )
    loss = lfn(active_logits, active_labels)
    return loss


class EntityModel(nn.Module):
    def __init__(self, num_labels):
        super(EntityModel, self).__init__()
        self.num_labels = num_labels
        self.bert = transformers.BertModel.from_pretrained(config.BASE_MODEL_PATH)
        self.bert_drop_1 = nn.Dropout(0.3)
        self.out_tag = nn.Linear(768, self.num_labels)
    
    def forward(self, ids, mask, token_type_ids, target_label, target_position):
        o1, _ = self.bert(ids, attention_mask=mask, token_type_ids=token_type_ids)

        # we only consider the embedding of the masked o/p
        o1_masked_token = o1[target_position]

        # bo_tag = self.bert_drop_1(o1_masked_token)

        # tag = self.out_tag(bo_tag)
        tag = self.out_tag(o1_masked_token)

        loss = loss_fn(tag, target_label, mask, self.num_labels)


        return tag, loss