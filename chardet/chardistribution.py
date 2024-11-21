from .big5freq import BIG5_CHAR_TO_FREQ_ORDER, BIG5_TABLE_SIZE, BIG5_TYPICAL_DISTRIBUTION_RATIO
from .euckrfreq import EUCKR_CHAR_TO_FREQ_ORDER, EUCKR_TABLE_SIZE, EUCKR_TYPICAL_DISTRIBUTION_RATIO
from .euctwfreq import EUCTW_CHAR_TO_FREQ_ORDER, EUCTW_TABLE_SIZE, EUCTW_TYPICAL_DISTRIBUTION_RATIO
from .gb2312freq import GB2312_CHAR_TO_FREQ_ORDER, GB2312_TABLE_SIZE, GB2312_TYPICAL_DISTRIBUTION_RATIO
from .jisfreq import JIS_CHAR_TO_FREQ_ORDER, JIS_TABLE_SIZE, JIS_TYPICAL_DISTRIBUTION_RATIO
from .johabfreq import JOHAB_TO_EUCKR_ORDER_TABLE

class CharDistributionAnalysis:
    ENOUGH_DATA_THRESHOLD = 1024
    SURE_YES = 0.99
    SURE_NO = 0.01
    MINIMUM_DATA_THRESHOLD = 3

    def __init__(self):
        self._char_to_freq_order = tuple()
        self._table_size = None
        self.typical_distribution_ratio = None
        self._done = None
        self._total_chars = None
        self._freq_chars = None
        self.reset()

    def reset(self):
        """reset analyser, clear any state"""
        self._done = False
        self._total_chars = 0
        self._freq_chars = 0

    def feed(self, char, char_len):
        """feed a character with known length"""
        if char_len == 2:
            # we only care about 2-bytes character in our distribution analysis
            order = -1
            if char[0] in self._char_to_freq_order:
                order = self._char_to_freq_order[char[0]]
            if order != -1 and order < self._table_size:
                self._total_chars += 1
                if order < 512:
                    self._freq_chars += 1

    def got_enough_data(self):
        # It is not necessary to receive all data to draw conclusion.
        # For charset probers, certain amount of data is enough
        return self._total_chars > self.ENOUGH_DATA_THRESHOLD

    def get_confidence(self):
        """return confidence based on existing data"""
        if self._total_chars <= 0 or self._freq_chars <= self.MINIMUM_DATA_THRESHOLD:
            return self.SURE_NO

        if self._total_chars != self._freq_chars:
            r = self._freq_chars / ((self._total_chars - self._freq_chars) * self.typical_distribution_ratio)
            if r < self.SURE_YES:
                return r

        # normalize confidence, (we don't want to be 100% sure)
        return self.SURE_YES

class EUCTWDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super().__init__()
        self._char_to_freq_order = EUCTW_CHAR_TO_FREQ_ORDER
        self._table_size = EUCTW_TABLE_SIZE
        self.typical_distribution_ratio = EUCTW_TYPICAL_DISTRIBUTION_RATIO

class EUCKRDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super().__init__()
        self._char_to_freq_order = EUCKR_CHAR_TO_FREQ_ORDER
        self._table_size = EUCKR_TABLE_SIZE
        self.typical_distribution_ratio = EUCKR_TYPICAL_DISTRIBUTION_RATIO

class JOHABDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super().__init__()
        self._char_to_freq_order = EUCKR_CHAR_TO_FREQ_ORDER
        self._table_size = EUCKR_TABLE_SIZE
        self.typical_distribution_ratio = EUCKR_TYPICAL_DISTRIBUTION_RATIO

class GB2312DistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super().__init__()
        self._char_to_freq_order = GB2312_CHAR_TO_FREQ_ORDER
        self._table_size = GB2312_TABLE_SIZE
        self.typical_distribution_ratio = GB2312_TYPICAL_DISTRIBUTION_RATIO

class Big5DistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super().__init__()
        self._char_to_freq_order = BIG5_CHAR_TO_FREQ_ORDER
        self._table_size = BIG5_TABLE_SIZE
        self.typical_distribution_ratio = BIG5_TYPICAL_DISTRIBUTION_RATIO

class SJISDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super().__init__()
        self._char_to_freq_order = JIS_CHAR_TO_FREQ_ORDER
        self._table_size = JIS_TABLE_SIZE
        self.typical_distribution_ratio = JIS_TYPICAL_DISTRIBUTION_RATIO

class EUCJPDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super().__init__()
        self._char_to_freq_order = JIS_CHAR_TO_FREQ_ORDER
        self._table_size = JIS_TABLE_SIZE
        self.typical_distribution_ratio = JIS_TYPICAL_DISTRIBUTION_RATIO