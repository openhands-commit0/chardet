from .charsetprober import CharSetProber
from .enums import ProbingState
FREQ_CAT_NUM = 4
UDF = 0
OTH = 1
ASC = 2
ASS = 3
ACV = 4
ACO = 5
ASV = 6
ASO = 7
CLASS_NUM = 8
Latin1_CharToClass = (OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC, OTH, OTH, OTH, OTH, OTH, OTH, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS, OTH, OTH, OTH, OTH, OTH, OTH, UDF, OTH, ASO, OTH, OTH, OTH, OTH, OTH, OTH, ACO, OTH, ACO, UDF, ACO, UDF, UDF, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, ASO, OTH, ASO, UDF, ASO, ACO, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH, ACV, ACV, ACV, ACV, ACV, ACV, ACO, ACO, ACV, ACV, ACV, ACV, ACV, ACV, ACV, ACV, ACO, ACO, ACV, ACV, ACV, ACV, ACV, OTH, ACV, ACV, ACV, ACV, ACV, ACO, ACO, ACO, ASV, ASV, ASV, ASV, ASV, ASV, ASO, ASO, ASV, ASV, ASV, ASV, ASV, ASV, ASV, ASV, ASO, ASO, ASV, ASV, ASV, ASV, ASV, OTH, ASV, ASV, ASV, ASV, ASV, ASO, ASO, ASO)
Latin1ClassModel = (0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 1, 1, 3, 3, 0, 3, 3, 3, 1, 2, 1, 2, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 1, 3, 1, 1, 1, 3, 0, 3, 1, 3, 1, 1, 3, 3)

class Latin1Prober(CharSetProber):

    def __init__(self):
        super().__init__()
        self._last_char_class = None
        self._freq_counter = None
        self.reset()