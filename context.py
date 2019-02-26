from snorkel.models.context import TemporaryContext
from snorkel.candidates import CandidateSpace
from builtins import object


class TemporarySentence(TemporaryContext):
    def __init__(self, sentence, meta=None):
        super(TemporarySentence, self).__init__()
        self.sentence = sentence
        self.char_end = len(sentence.text)
        self.char_start = 0
        self.meta = meta

    def __eq__(self, other):
        return self.sentence.id == other.id

    def __ne__(self, other):
        return not (self.__eq__(other))

    def __hash__(self):
        return hash(self.sentence.id)

    def get_stable_id(self):
        return self.sentence.id

    def _get_table_name(self):
        return 'span'

    def _get_polymorphic_identity(self):
        return 'span'

    def _get_insert_query(self):
        return """INSERT INTO span VALUES(:id, :sentence_id, :char_start, :char_end, :meta)"""

    def _get_insert_args(self):
        return {'sentence_id' : self.sentence.id,
                'char_start': self.char_start,
                'char_end'  : self.char_end,
                'meta'      : self.meta}

    def get_word_start(self):
        return self.char_to_word_index(self.char_start)

    def get_word_end(self):
        return self.char_to_word_index(self.char_end)

    def get_n(self):
        return self.get_word_end() - self.get_word_start() + 1

    def char_to_word_index(self, ci):
        """Given a character-level index (offset), return the index of the **word this char is in**"""
        i = None
        for i, co in enumerate(self.sentence.char_offsets):
            if ci == co:
                return i
            elif ci < co:
                return i - 1
        return i

    def word_to_char_index(self, wi):
        """Given a word-level index, return the character-level index (offset) of the word's start"""
        return self.sentence.char_offsets[wi]

    def get_attrib_tokens(self, a='words'):
        """Get the tokens of sentence attribute _a_ over the range defined by word_offset, n"""
        return self.sentence.__getattribute__(a)[self.get_word_start():self.get_word_end() + 1]

    def get_attrib_span(self, a, sep=" "):
        """Get the span of sentence attribute _a_ over the range defined by word_offset, n"""
        # NOTE: Special behavior for words currently (due to correspondence with char_offsets)
        if a == 'words':
            return self.sentence.text[self.char_start:self.char_end + 1]
        else:
            return sep.join(self.get_attrib_tokens(a))

    def get_span(self, sep=" "):
        return self.get_attrib_span('words', sep)

    def __contains__(self, other_span):
        return other_span.char_start >= self.char_start and other_span.char_end <= self.char_end

    def __getitem__(self, key):
        """
        Slice operation returns a new candidate sliced according to **char index**
        Note that the slicing is w.r.t. the candidate range (not the abs. sentence char indexing)
        """
        if isinstance(key, slice):
            char_start = self.char_start if key.start is None else self.char_start + key.start
            if key.stop is None:
                char_end = self.char_end
            elif key.stop >= 0:
                char_end = self.char_start + key.stop - 1
            else:
                char_end = self.char_end + key.stop
            return self._get_instance(char_start=char_start, char_end=char_end, sentence=self.sentence)
        else:
            raise NotImplementedError()

    def __repr__(self):
        return self.sentence.__repr__()


class SentCandidate(CandidateSpace):
    def apply(self, sentContext):
        yield TemporarySentence(sentContext)







