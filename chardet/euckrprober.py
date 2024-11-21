from .chardistribution import EUCKRDistributionAnalysis
from .codingstatemachine import CodingStateMachine
from .enums import ProbingState
from .mbcharsetprober import MultiByteCharSetProber
from .mbcssm import EUCKR_SM_MODEL

class EUCKRProber(MultiByteCharSetProber):

    def __init__(self):
        super().__init__()
        self.coding_sm = CodingStateMachine(EUCKR_SM_MODEL)
        self.distribution_analyzer = EUCKRDistributionAnalysis()
        self.reset()

    def reset(self):
        super().reset()
        self._state = ProbingState.DETECTING

    @property
    def charset_name(self):
        return "EUC-KR"

    @property
    def language(self):
        return "Korean"