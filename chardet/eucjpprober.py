from .chardistribution import EUCJPDistributionAnalysis
from .codingstatemachine import CodingStateMachine
from .enums import MachineState, ProbingState
from .jpcntx import EUCJPContextAnalysis
from .mbcharsetprober import MultiByteCharSetProber
from .mbcssm import EUCJP_SM_MODEL

class EUCJPProber(MultiByteCharSetProber):

    def __init__(self):
        super().__init__()
        self.coding_sm = CodingStateMachine(EUCJP_SM_MODEL)
        self.distribution_analyzer = EUCJPDistributionAnalysis()
        self.context_analyzer = EUCJPContextAnalysis()
        self.reset()