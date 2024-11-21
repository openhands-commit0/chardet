from .charsetprober import CharSetProber
from .codingstatemachine import CodingStateMachine
from .enums import MachineState, ProbingState
from .mbcssm import UTF8_SM_MODEL

class UTF8Prober(CharSetProber):
    ONE_CHAR_PROB = 0.5

    def __init__(self):
        super().__init__()
        self.coding_sm = CodingStateMachine(UTF8_SM_MODEL)
        self._num_mb_chars = None
        self.reset()

    def reset(self):
        super().reset()
        self.coding_sm.reset()
        self._num_mb_chars = 0

    @property
    def charset_name(self):
        return "utf-8"

    @property
    def language(self):
        return ""

    def feed(self, byte_str):
        for c in byte_str:
            coding_state = self.coding_sm.next_state(c)
            if coding_state == MachineState.ERROR:
                self._state = ProbingState.NOT_ME
                break
            elif coding_state == MachineState.ITS_ME:
                self._state = ProbingState.FOUND_IT
                break
            elif coding_state == MachineState.START:
                char_len = self.coding_sm.get_current_charlen()
                if char_len >= 2:
                    self._num_mb_chars += 1

        if self.state == ProbingState.DETECTING:
            if self.get_confidence() > self.SHORTCUT_THRESHOLD:
                self._state = ProbingState.FOUND_IT

        return self.state

    def get_confidence(self):
        unlike = 0.99
        if self._num_mb_chars < 6:
            for i in range(0, self._num_mb_chars):
                unlike = unlike * self.ONE_CHAR_PROB
            return 1.0 - unlike
        return unlike