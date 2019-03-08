import datetime
report = ['\n*** Report for process run on '+str(datetime.datetime.now())+' ***\n']


def doc_parse(path):
    """
    Loads TSV file and parses to Snorkel Contexts
    :param path: Path to TSV file
    :return: None
    """
    try:
        doc_preprocessor = TSVDocPreprocessor(path, encoding=u'utf-8', max_docs=2500)

        corpus_parser = CorpusParser()
        corpus_parser.apply(doc_preprocessor)
        print("Documents:", session.query(Document).count())
        print("Sentences:", session.query(Sentence).count())

    except Exception:
        print('Error loading TSV file')


def def_cand_extractor():
    """
    Defines a candidate extractor
    Make necessary changes to cand subclass, span, matcher and cand extractor
    :return: candExtractor, cSubClass
    """
    Text = candidate_subclass('Text', ['text'], values=['Positive', 'Negative', False])
    sent_span = SentCandidate()
    defaultMatcher = Matcher()
    cand_extractor = CandidateExtractor(Text, [sent_span], [defaultMatcher])
    return cand_extractor, Text


def extract_candidates(candExtractor, cSubClass):
    """
    Extracts Snorkel candidates
    Splits data to train, dev and test sets
    :param candExtractor: Candidate Extractor Schema
    :param cSubClass: Candidate sub class schema
    :return: None
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
        report.append("Candidates in split "+str(i)+' : '+
                      str(session.query(cSubClass).filter(cSubClass.split == i).count())+'\n')


def apply_LF(lf_file):
    """
    Load labeling functions and applies on the candidates extracted in train set
    :param lf_file: labeling functions python file
    :return: L_train
    """
    labeling_func = __import__(lf_file)
    LF_list = [o[1] for o in getmembers(labeling_func) if isfunction(o[1])]
    labeler = LabelAnnotator(lfs=LF_list)
    np.random.seed(1701)
    L_train = labeler.apply(split=0)
    L_train.todense()
    report.append('\n#LF Stats\n')
    report.append(L_train.lf_stats(session).to_csv(sep=' ', index=False, header=True))
    return L_train


def apply_GenMod(L_train):
    """
    Applies generative model on label matrix
    :param L_train: Label matrix
    :return: None
    """
    gen_model = GenerativeModel()
    # gen_model.train(L_train, epochs=100, decay=0.95, step_size=0.1 / L_train.shape[0], reg_param=1e-6)
    gen_model.train(L_train, cardinality=3)
    # print(gen_model.weights.lf_accuracy)
    train_marginals = gen_model.marginals(L_train)
    report.append('\n#Gen Model Stats\n')
    report.append(gen_model.learned_lf_stats().to_csv(sep=' ', index=False, header=True))
    save_marginals(session, L_train, train_marginals)


def generate_report(name):
    with open(name+'/report.txt', 'a') as file:
        for item in report:
            file.write(item)
        file.close()


def runSnorkelProcess(name, path, restart, lf):
    """
    Main process flow
    :param path: Path to TSV file
    :param restart: Flag to start from beginning
    :param lf: LF python file
    :return: None
    """
    if restart is True:
        doc_parse(path)
        candExtractor, cSubClass = def_cand_extractor()
        extract_candidates(candExtractor, cSubClass)
    else:
        def_cand_extractor()
    l_train = apply_LF(lf)
    apply_GenMod(l_train)
    generate_report(name)


if __name__ == "__main__":
    import argparse
    import os
    parser = argparse.ArgumentParser(description='Run Snorkel process')
    parser.add_argument('-n', '--name', dest='name', required=True, help='Name of the process')
    parser.add_argument('-p', '--path', dest='path', required=True, help='Path to TSV file')
    parser.add_argument('-lf', '--label_func', dest='lf', required=True, help='LF python file')
    parser.add_argument('-r', '--restart', dest='restart', action='store_true',
                        help='flag to restart process from beginning')
    parser.set_defaults(restart=False)
    args = parser.parse_args()

    if not os.path.exists(args.name):
        os.makedirs(args.name)

    os.environ["SNORKELDB"] = "sqlite:///" + os.getcwd() + os.sep + os.path.join(args.name+"/snorkel.db")

    import numpy as np
    from db_process import db_process
    from context import *
    from inspect import getmembers, isfunction

    from snorkel import SnorkelSession
    from snorkel.parser import TSVDocPreprocessor, CorpusParser
    from snorkel.models import Document, Sentence, candidate_subclass
    from snorkel.candidates import CandidateExtractor
    from snorkel.matchers import Matcher
    from snorkel.annotations import LabelAnnotator
    from snorkel.learning import GenerativeModel
    from snorkel.annotations import save_marginals

    session = SnorkelSession()
    runSnorkelProcess(args.name, args.path, args.restart, args.lf)
    db_process(args.name)
