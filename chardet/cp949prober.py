from .chardistribution import EUCKRDistributionAnalysis
from .codingstatemachine import CodingStateMachine
from .enums import ProbingState
from .mbcharsetprober import MultiByteCharSetProber
from .mbcssm import CP949_SM_MODEL

class CP949Prober(MultiByteCharSetProber):

    def __init__(self):
        super().__init__()
        self.coding_sm = CodingStateMachine(CP949_SM_MODEL)
        self.distribution_analyzer = EUCKRDistributionAnalysis()
        self.reset()

    def reset(self):
        super().reset()
        self._state = ProbingState.DETECTING

    @property
    def charset_name(self):
        return "CP949"

    @property
    def language(self):
        return "Korean"