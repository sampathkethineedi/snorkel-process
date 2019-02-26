from snorkel import SnorkelSession
from snorkel.parser import TSVDocPreprocessor,CorpusParser
from snorkel.models import Document, Sentence, candidate_subclass
from snorkel.candidates import CandidateExtractor, Ngrams
from snorkel.matchers import Matcher
from snorkel.annotations import LabelAnnotator
from snorkel.learning import GenerativeModel

import numpy as np
from context import *
import labeling_func
from inspect import getmembers, isfunction

session = SnorkelSession()


def doc_parse(path):
    """
    Loads TSV file and parses to Snorkel Contexts
    """
    doc_preprocessor = TSVDocPreprocessor(path, encoding=u'utf-8', max_docs=2500)
    corpus_parser = CorpusParser()
    corpus_parser.apply(doc_preprocessor)
    print("Documents:", session.query(Document).count())
    print("Sentences:", session.query(Sentence).count())


def def_cand_extractor():
    """
    Defines a candidate extractor
    Make necessary changes to cand subclass, span, matcher and cand extractor
    :return: candExtractor, cSubClass
    """
    Text = candidate_subclass('Text', ['text'])
    sent_span = SentCandidate()
    defaultMatcher = Matcher()
    cand_extractor = CandidateExtractor(Text, [sent_span], [defaultMatcher])
    return cand_extractor, Text


def extract_candidates(candExtractor, cSubClass):
    """
    Extracts Snorkel candidates
    Splits data to train, dev and test sets
    """
    docs = session.query(Document).order_by(Document.name).all()
    train_sents = set()
    dev_sents = set()
    test_sents = set()

    for i, doc in enumerate(docs):
        for s in doc.sentences:
            if i % 10 == 8:
                dev_sents.add(s)
            elif i % 10 == 9:
                test_sents.add(s)
            else:
                train_sents.add(s)

    for i, sents in enumerate([train_sents, dev_sents, test_sents]):
        candExtractor.apply(sents, split=i)
        print("Number of candidates:", session.query(cSubClass).filter(cSubClass.split == i).count())


def apply_LF():
    """
    Load labeling functions and applies on the candidates extracted in train set
    :return: L_train
    """
    LF_list = [o[1] for o in getmembers(labeling_func) if isfunction(o[1])]
    labeler = LabelAnnotator(lfs=LF_list)
    np.random.seed(1701)
    L_train = labeler.apply(split=0)
    print(L_train.lf_stats(session))
    return L_train


def apply_GenMod(L_train):
    """
    Applies generative model on label matrix
    :return:
    """
    gen_model = GenerativeModel()
    gen_model.train(L_train, epochs=100, decay=0.95, step_size=0.1 / L_train.shape[0], reg_param=1e-6)
    print(gen_model.weights.lf_accuracy)
    gen_model.marginals(L_train)
    print(gen_model.learned_lf_stats())


def runSnorkelProcess(restart=True):
    """
    Main process flow
    :return:
    """
    if restart is True:
        doc_parse('../gold_labels.tsv')
        candExtractor, cSubClass = def_cand_extractor()
        extract_candidates(candExtractor, cSubClass)
    else:
        def_cand_extractor()
    l_train = apply_LF()
    apply_GenMod(l_train)


runSnorkelProcess(False)
