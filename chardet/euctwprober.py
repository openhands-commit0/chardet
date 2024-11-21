from .chardistribution import EUCTWDistributionAnalysis
from .codingstatemachine import CodingStateMachine
from .enums import ProbingState
from .mbcharsetprober import MultiByteCharSetProber
from .mbcssm import EUCTW_SM_MODEL

class EUCTWProber(MultiByteCharSetProber):

    def __init__(self):
        super().__init__()
        self.coding_sm = CodingStateMachine(EUCTW_SM_MODEL)
        self.distribution_analyzer = EUCTWDistributionAnalysis()
        self.reset()

    def reset(self):
        super().reset()
        self._state = ProbingState.DETECTING

    @property
    def charset_name(self):
        return "EUC-TW"

    @property
    def language(self):
        return "Traditional Chinese"