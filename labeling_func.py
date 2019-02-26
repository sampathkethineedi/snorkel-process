import pandas as pd

data = pd.read_csv('id_labels.tsv',delimiter='\t')
data.columns = ['id','label']
positive_words = {'good','great','best','amazing','excellent','awesome','incredible','beautiful'}
negative_words = {'bad','worst','boring','repeated','waste','refund','mediocre'}


def LF_pos(s):
    span_words = s.get_parent().words
    if len(positive_words.intersection(span_words))>0:
        return 1
    else:
        return 0


def LF_neg(s):
    span_words = s.get_parent().words
    if len(negative_words.intersection(span_words))>0:
        return -1
    else:
        return 0


def LF_gold(s):
    id = s.get_parent().get_parent().name
    res = data[data['id'].isin([id])]
    return res['label'].item()

