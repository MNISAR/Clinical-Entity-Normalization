# Clinical-Entity-Normalization

# Description
This project is from [2019 n2c2 Shared-Task and Workshop(Track 3: Clinical Concept Normalization)](https://n2c2.dbmi.hms.harvard.edu/track3)

The project aims to create a natural language model that normalizes the mention (words) of medical terms using the available context from the sentence.
The goal is to assign CUI (concept unique ID) to clinical text which will normalize the mentions of different words used for same concept (seizure disorder & epilepsy). Or when same words are used for different context.

# Approach 1 (using Bert For Sentence Classification):
- BERT model with Classification head<br>
"""Input: Encoded sentences.
   Output: Class Lable."""<br>
   <img src="/resources/BERT_Classification_model.png?raw=true" alt="BertSC Model" height="300" width="400" align="center" />
- Our architecture:<br>
    <img src="/resources/BERT_Classification_architecture.png?raw=true" alt="BertSC architecture" height="300" width="400" align="center" />
- We developed a prediction model that uses pre-trained BertSC as base model and fine-tunes it on training data.
- Our architecture depends on information provided in training data to perform classification.
- We have usedd BertBaseUncased as the pre-trained base model. We recorded only 57.7% accuracy.

## steps to run
 - Refer the [readme](/SentenceClassification/readme.md) file inside the directory "SentenceClassification" for the step to run info.

# Approach 2 (using Bert For Next Sentence Prediction):
- BERT model with NextSentecePrediction head <br>
"""Input: Encoded representation of two sentences seperated with [SEP] tag.
   Output: isNext percentage
           isNotNext percentage"""<br>
    <img src="/resources/BERT_NSP_model.png?raw=true" alt="BertNSP Model" height="300" width="400" align="center" />
- Our architecture:<br>
    <img src="/resources/BERT_NSP_architecture.png?raw=true" alt="BertNSP architecture" height="300" width="400" align="center" />
- We developed a model that is fine-tuned using the data on hand and the UMLS metathesaurus, so that our system gets maximum information. So here we are not dependent only on training data.
- A thing to note here is that we have used BioBERT as our base model. This BERT is pre-trained on data from multiple medical sources including PubMed and UMLS, which are major sources.
- The accuracy recorded in this approach is 72.4% which is a major improvement from approach 1.


## steps to run
- Refer the [readme](/NextSentencePrediction/readme.md) file inside the directory "NextSentencePrediction" for the step to run info.

ref: Xu D, Gopale M, Zhang J, Brown K, Begoli E, Bethard S. Unified Medical Language System resources improve sieve-based generation and Bidirectional Encoder Representations from Transformers (BERT)-based ranking for concept normalization. J Am Med Inform Assoc. 2020 Oct 1;27(10):1510-1519. doi: 10.1093/jamia/ocaa080. PMID: 32719838; PMCID: PMC7566510.
