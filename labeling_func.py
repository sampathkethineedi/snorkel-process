# import pandas as pd
#
# data = pd.read_csv('../id_labels.tsv',delimiter='\t')
# data.columns = ['id','label']
positive_words = {'good','great','best','amazing','excellent',
                  'awesome','incredible','increasing',
                  'rising','booming','healthy','buy','nice'
                  'strong','leading','leader','innovative'}
negative_words = {'bad','worst','boring','repeated','waste',
                  'refund','mediocre','falling','sell','loss',
                  'away','dropping','extending','expensive',
                  'drops','bumps','difficult'}


def LF_pos(s):
    span_words = s.get_parent().words
    if len(positive_words.intersection(span_words))>0:
        return 'Positive'
    else:
        return None


def LF_neg(s):
    span_words = s.get_parent().words
    if len(negative_words.intersection(span_words))>0:
        return 'Negative'
    else:
        return None


# def LF_gold(s):
#     id = s.get_parent().get_parent().name
#     res = data[data['id'].isin([id])]
#     return res['label'].item()

