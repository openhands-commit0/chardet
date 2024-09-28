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