from .chardistribution import Big5DistributionAnalysis
from .codingstatemachine import CodingStateMachine
from .enums import ProbingState
from .mbcharsetprober import MultiByteCharSetProber
from .mbcssm import BIG5_SM_MODEL

class Big5Prober(MultiByteCharSetProber):

    def __init__(self):
        super().__init__()
        self.coding_sm = CodingStateMachine(BIG5_SM_MODEL)
        self.distribution_analyzer = Big5DistributionAnalysis()
        self.reset()

    def reset(self):
        super().reset()
        self._state = ProbingState.DETECTING

    @property
    def charset_name(self):
        return "Big5"

    @property
    def language(self):
        return "Traditional Chinese"