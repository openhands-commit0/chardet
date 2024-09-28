from .charsetprober import CharSetProber
from .enums import ProbingState

class CharSetGroupProber(CharSetProber):

    def __init__(self, lang_filter=None):
        super().__init__(lang_filter=lang_filter)
        self._active_num = 0
        self.probers = []
        self._best_guess_prober = None