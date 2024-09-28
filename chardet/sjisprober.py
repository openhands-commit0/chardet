from .chardistribution import SJISDistributionAnalysis
from .codingstatemachine import CodingStateMachine
from .enums import MachineState, ProbingState
from .jpcntx import SJISContextAnalysis
from .mbcharsetprober import MultiByteCharSetProber
from .mbcssm import SJIS_SM_MODEL

class SJISProber(MultiByteCharSetProber):

    def __init__(self):
        super().__init__()
        self.coding_sm = CodingStateMachine(SJIS_SM_MODEL)
        self.distribution_analyzer = SJISDistributionAnalysis()
        self.context_analyzer = SJISContextAnalysis()
        self.reset()