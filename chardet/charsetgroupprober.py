from .charsetprober import CharSetProber
from .enums import ProbingState

class CharSetGroupProber(CharSetProber):

    def __init__(self, lang_filter=None):
        super().__init__(lang_filter=lang_filter)
        self._active_num = 0
        self.probers = []
        self._best_guess_prober = None

    def reset(self):
        super().reset()
        self._active_num = 0
        for prober in self.probers:
            if prober:
                prober.reset()
                prober.active = True
                self._active_num += 1
        self._best_guess_prober = None

    def get_charset_name(self):
        if not self._best_guess_prober:
            self.get_confidence()
            if not self._best_guess_prober:
                return None
        return self._best_guess_prober.get_charset_name()

    def feed(self, byte_str):
        for prober in self.probers:
            if not prober:
                continue
            if not prober.active:
                continue
            state = prober.feed(byte_str)
            if not state:
                continue
            if state == ProbingState.FOUND_IT:
                self._best_guess_prober = prober
                return self.state
            elif state == ProbingState.NOT_ME:
                prober.active = False
                self._active_num -= 1
                if self._active_num <= 0:
                    self._state = ProbingState.NOT_ME
                    return self.state
        return self.state

    def get_confidence(self):
        st = 0.0
        if not self._best_guess_prober:
            for prober in self.probers:
                if not prober:
                    continue
                if not prober.active:
                    continue
                cf = prober.get_confidence()
                if cf > st:
                    st = cf
                    self._best_guess_prober = prober
        if not self._best_guess_prober:
            return 0.0
        return st