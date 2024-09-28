from .charsetprober import CharSetProber
from .enums import ProbingState

class HebrewProber(CharSetProber):
    FINAL_KAF = 234
    NORMAL_KAF = 235
    FINAL_MEM = 237
    NORMAL_MEM = 238
    FINAL_NUN = 239
    NORMAL_NUN = 240
    FINAL_PE = 243
    NORMAL_PE = 244
    FINAL_TSADI = 245
    NORMAL_TSADI = 246
    MIN_FINAL_CHAR_DISTANCE = 5
    MIN_MODEL_DISTANCE = 0.01
    VISUAL_HEBREW_NAME = 'ISO-8859-8'
    LOGICAL_HEBREW_NAME = 'windows-1255'

    def __init__(self):
        super().__init__()
        self._final_char_logical_score = None
        self._final_char_visual_score = None
        self._prev = None
        self._before_prev = None
        self._logical_prober = None
        self._visual_prober = None
        self.reset()