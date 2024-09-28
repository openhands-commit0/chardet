from .chardistribution import JOHABDistributionAnalysis
from .codingstatemachine import CodingStateMachine
from .mbcharsetprober import MultiByteCharSetProber
from .mbcssm import JOHAB_SM_MODEL

class JOHABProber(MultiByteCharSetProber):

    def __init__(self):
        super().__init__()
        self.coding_sm = CodingStateMachine(JOHAB_SM_MODEL)
        self.distribution_analyzer = JOHABDistributionAnalysis()
        self.reset()