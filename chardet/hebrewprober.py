from .charsetprober import CharSetProber
from .enums import ProbingState

class HebrewProber(CharSetProber):
    FINAL_KAF = 234
    NORMAL_KAF = 235
    FINAL_MEM = 237
    NORMAL_MEM = 238
    FINAL_NUN = 239
    NORMAL_NUN = 240
    FINAL_PE = 243
    NORMAL_PE = 244
    FINAL_TSADI = 245
    NORMAL_TSADI = 246
    MIN_FINAL_CHAR_DISTANCE = 5
    MIN_MODEL_DISTANCE = 0.01
    VISUAL_HEBREW_NAME = 'ISO-8859-8'
    LOGICAL_HEBREW_NAME = 'windows-1255'

    def __init__(self):
        super().__init__()
        self._final_char_logical_score = None
        self._final_char_visual_score = None
        self._prev = None
        self._before_prev = None
        self._logical_prober = None
        self._visual_prober = None
        self.reset()

    def reset(self):
        self._final_char_logical_score = 0
        self._final_char_visual_score = 0
        self._prev = ' '
        self._before_prev = ' '
        self._logical_prober = None
        self._visual_prober = None

    def set_model_probers(self, logical_prober, visual_prober):
        self._logical_prober = logical_prober
        self._visual_prober = visual_prober

    def is_final(self, c):
        return c in [self.FINAL_KAF, self.FINAL_MEM, self.FINAL_NUN,
                    self.FINAL_PE, self.FINAL_TSADI]

    def is_non_final(self, c):
        return c in [self.NORMAL_KAF, self.NORMAL_MEM, self.NORMAL_NUN,
                    self.NORMAL_PE, self.NORMAL_TSADI]

    def feed(self, byte_str):
        if self._state == ProbingState.NOT_ME:
            return self._state

        for c in byte_str:
            if c >= 128:
                # If we got a non-ascii character, check if it's a final or non-final letter
                if self.is_final(c):
                    # If the previous character was a non-final letter, this is logical
                    if self._prev == ' ':
                        self._final_char_logical_score += 0
                        self._final_char_visual_score += 0
                    elif self.is_non_final(self._prev):
                        self._final_char_logical_score += 1
                        self._final_char_visual_score -= 1
                    else:
                        self._final_char_logical_score += 0
                        self._final_char_visual_score += 0
                elif self.is_non_final(c):
                    # If the previous character was a final letter, this is visual
                    if self._prev == ' ':
                        self._final_char_logical_score += 0
                        self._final_char_visual_score += 0
                    elif self.is_final(self._prev):
                        self._final_char_logical_score -= 1
                        self._final_char_visual_score += 1
                    else:
                        self._final_char_logical_score += 0
                        self._final_char_visual_score += 0

            self._before_prev = self._prev
            self._prev = c

        return self._state

    def get_charset_name(self):
        # If we have both probers and one is significantly more confident,
        # use its charset name
        finalsub = abs(self._final_char_logical_score - self._final_char_visual_score)
        if finalsub >= self.MIN_FINAL_CHAR_DISTANCE:
            if self._final_char_logical_score > self._final_char_visual_score:
                return self.LOGICAL_HEBREW_NAME
            return self.VISUAL_HEBREW_NAME

        # If we don't have a clear winner, use the one with higher confidence
        if self._logical_prober and self._visual_prober:
            logical_conf = self._logical_prober.get_confidence()
            visual_conf = self._visual_prober.get_confidence()
            diff = abs(logical_conf - visual_conf)
            if diff >= self.MIN_MODEL_DISTANCE:
                if logical_conf > visual_conf:
                    return self.LOGICAL_HEBREW_NAME
                return self.VISUAL_HEBREW_NAME

        # Still no clear winner, return logical Hebrew by default
        return self.LOGICAL_HEBREW_NAME

    def get_state(self):
        # Assume we're good unless both model probers say otherwise
        if (self._logical_prober and self._visual_prober and
            self._logical_prober.get_state() == ProbingState.NOT_ME and
            self._visual_prober.get_state() == ProbingState.NOT_ME):
            return ProbingState.NOT_ME
        return ProbingState.DETECTING

    def get_confidence(self):
        # If we have a clear winner from final letters analysis, use that
        finalsub = abs(self._final_char_logical_score - self._final_char_visual_score)
        if finalsub >= self.MIN_FINAL_CHAR_DISTANCE:
            return 0.95

        # If we have both probers and one is significantly more confident,
        # use its confidence
        if self._logical_prober and self._visual_prober:
            logical_conf = self._logical_prober.get_confidence()
            visual_conf = self._visual_prober.get_confidence()
            diff = abs(logical_conf - visual_conf)
            if diff >= self.MIN_MODEL_DISTANCE:
                return max(logical_conf, visual_conf)

        # No clear winner, return a moderate confidence
        return 0.5