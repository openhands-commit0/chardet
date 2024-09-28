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