Medical Concept Normalization (MCN) Corpus


=== Annotations ===
Normalization maps clinical named entities in medical notes to the entries in the standardized medical vocabularies.
The MCN corpus consists of 100 discharge summaries from the fourth i2b2/VA shared task and provides normalization for the total of 10,919 concept mentions.

The annotation file name in MCN is the same as note file name in i2b2 but with "norm" file extension.

The annotations are released in the following format. Each column is separated by "||".
id||cui||char start||char end
"id" is used for the evaluation purpose.
The "cui" in the test data is replaced with "unk".

For disjoint mention spans, multiple "char start" and "char end" are attached to the end as illustrated in the example below.
id || cui || char start || char end || char start || char end ...
"pain in the left ... leg" derived from "pain in the left arm and leg" is an example of discontiguous mentions.

*** RELEASE to PARTICIPANTS BEGIN ***
train folder BEGIN
=> train_norm folder
==> contain training norm files (for model development).

=> train_note folder
==> contain training note files

=> train_file_list.txt
==> list of files in training data. Participants need to follow the file order to concatenate all of the predicted CUIs into a single file, "submission.txt" for running evaluation locally.

=> train_norm.txt
==> concatenate CUIs from norm files in train_norm folder following the file order in train_note_list.txt
==> THIS IS THE GOLD TRAINING DATA FOR EVALUATION DURING MODEL DEVELOPMENT
train folder END

test folder BEGIN
=> test_norm_cui_replaced_with_unk folder
==> contain testing norm files but all of the CUIs are replaced with "unk" (for model prediction of CUIs)

=> test_note folder
==> contain testing note files

=> test_file_list.txt
==> list of files in testing data. Participants need to follow the file order to concatenate all of the predicted CUIs into a single file, "submission.txt" and submit it to organizers for evaluation.
test folder END
*** RELEASE to PARTICIPANTS END ***


=== Evaluation ===
=> Accuracy is used to evaluate and compare the system performance.
=> Please follow the specifications below for the successful evaluation.
=> The predicted CUIs from each note are expected to be concatenated following the file order provided in train_file_list.txt / test_file_list.txt into a single submission file with file name, "submission.txt". Each row in the submission file is the CUI predicted by your system.
=> For model development evaluation, train_norm.txt released to participants is the ground truth of the training data containing CUIs concatenated from norm files in train_norm folder following the file order listed in train_note_list.txt.
=> Commnd:
==> python evaluation.py path_to_submission_file path_to_truth_file
=> Example:
==> python evaluation.py ./submission.txt ./train_norm.txt


=== Publication ===
https://www.sciencedirect.com/science/article/pii/S1532046419300504?via%3Dihub#!

=== Inter Annotator Agreement (IAA) ===
Pre-adjudication IAA: 67.69 %
Post-adjudication IAA: 74.20 %
