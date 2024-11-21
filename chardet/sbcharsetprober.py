from collections import namedtuple
from .charsetprober import CharSetProber
from .enums import CharacterCategory, ProbingState, SequenceLikelihood
SingleByteCharSetModel = namedtuple('SingleByteCharSetModel', ['charset_name', 'language', 'char_to_order_map', 'language_model', 'typical_positive_ratio', 'keep_ascii_letters', 'alphabet'])

class SingleByteCharSetProber(CharSetProber):
    SAMPLE_SIZE = 64
    SB_ENOUGH_REL_THRESHOLD = 1024
    POSITIVE_SHORTCUT_THRESHOLD = 0.95
    NEGATIVE_SHORTCUT_THRESHOLD = 0.05

    def __init__(self, model, is_reversed=False, name_prober=None):
        super().__init__()
        self._model = model
        self._reversed = is_reversed
        self._name_prober = name_prober
        self._last_order = None
        self._seq_counters = None
        self._total_seqs = None
        self._total_char = None
        self._control_char = None
        self._freq_char = None
        self.reset()

    def reset(self):
        super().reset()
        self._last_order = 255
        self._seq_counters = [0] * SequenceLikelihood.get_num_categories()
        self._total_seqs = 0
        self._total_char = 0
        self._control_char = 0
        self._freq_char = 0

    def get_charset_name(self):
        if self._name_prober:
            return self._name_prober.get_charset_name()
        return self._model.charset_name

    @property
    def charset_name(self):
        return self._model.charset_name

    @property
    def language(self):
        return self._model.language

    def feed(self, byte_str):
        if not self._model.keep_ascii_letters:
            byte_str = self.filter_international_words(byte_str)
            if not byte_str:
                return self.state
        byte_str = self.filter_with_english_letters(byte_str)
        if not byte_str:
            return self.state

        char_len = len(byte_str)
        if char_len > 0:
            if not self._model.char_to_order_map or not self._model.language_model:
                self._state = ProbingState.NOT_ME
                return self.state

            for i, c in enumerate(byte_str):
                order = self._model.char_to_order_map.get(c, CharacterCategory.UNDEFINED)
                if order < CharacterCategory.CONTROL:
                    self._control_char += 1
                elif order == CharacterCategory.SAME_CLASS_WORD:
                    self._freq_char += 1

                if order < len(self._model.language_model):
                    if i > 0:
                        last_order = self._last_order
                        if last_order < len(self._model.language_model):
                            self._total_seqs += 1
                            if not self._reversed:
                                lm_cat = self._model.language_model[last_order][order]
                                self._seq_counters[lm_cat] += 1
                            else:
                                lm_cat = self._model.language_model[order][last_order]
                                self._seq_counters[lm_cat] += 1
                    self._last_order = order

            charset_name = self.charset_name
            if self._total_seqs > self.SB_ENOUGH_REL_THRESHOLD:
                cf = self.get_confidence()
                if cf > self.POSITIVE_SHORTCUT_THRESHOLD:
                    self._state = ProbingState.FOUND_IT
                elif cf < self.NEGATIVE_SHORTCUT_THRESHOLD:
                    self._state = ProbingState.NOT_ME

        return self.state

    def get_confidence(self):
        r = 0.01
        if self._total_seqs > 0:
            r = ((1.0 * self._seq_counters[SequenceLikelihood.POSITIVE]) / self._total_seqs
                 / self._model.typical_positive_ratio)
            r = r * (self._total_seqs / self.SAMPLE_SIZE)
            if r >= 1.0:
                r = 0.99
        return r