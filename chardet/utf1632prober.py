from .charsetprober import CharSetProber
from .enums import ProbingState

class UTF1632Prober(CharSetProber):
    """
    This class simply looks for occurrences of zero bytes, and infers
    whether the file is UTF16 or UTF32 (low-endian or big-endian)
    For instance, files looking like ( \x00 \x00 \x00 [nonzero] )+
    have a good probability to be UTF32BE.  Files looking like ( \x00 [nonzero] )+
    may be guessed to be UTF16BE, and inversely for little-endian varieties.
    """
    MIN_CHARS_FOR_DETECTION = 20
    EXPECTED_RATIO = 0.94

    def __init__(self):
        super().__init__()
        self.position = 0
        self.zeros_at_mod = [0] * 4
        self.nonzeros_at_mod = [0] * 4
        self._state = ProbingState.DETECTING
        self.quad = [0, 0, 0, 0]
        self.invalid_utf16be = False
        self.invalid_utf16le = False
        self.invalid_utf32be = False
        self.invalid_utf32le = False
        self.first_half_surrogate_pair_detected_16be = False
        self.first_half_surrogate_pair_detected_16le = False
        self.reset()

    def validate_utf32_characters(self, quad):
        """
        Validate if the quad of bytes is valid UTF-32.

        UTF-32 is valid in the range 0x00000000 - 0x0010FFFF
        excluding 0x0000D800 - 0x0000DFFF

        https://en.wikipedia.org/wiki/UTF-32
        """
        value = (quad[0] << 24) | (quad[1] << 16) | (quad[2] << 8) | quad[3]
        if value > 0x0010FFFF:
            return False
        if 0xD800 <= value <= 0xDFFF:
            return False
        return True

    def validate_utf16_characters(self, pair):
        """
        Validate if the pair of bytes is  valid UTF-16.

        UTF-16 is valid in the range 0x0000 - 0xFFFF excluding 0xD800 - 0xFFFF
        with an exception for surrogate pairs, which must be in the range
        0xD800-0xDBFF followed by 0xDC00-0xDFFF

        https://en.wikipedia.org/wiki/UTF-16
        """
        value = (pair[0] << 8) | pair[1]
        if 0xD800 <= value <= 0xDBFF:
            return True  # First half of surrogate pair
        if 0xDC00 <= value <= 0xDFFF:
            return True  # Second half of surrogate pair
        if value >= 0xD800 and value <= 0xDFFF:
            return False  # Invalid surrogate value
        return True

    def reset(self):
        """
        Reset the prober to its initial state.
        """
        super().reset()
        self.position = 0
        self.zeros_at_mod = [0] * 4
        self.nonzeros_at_mod = [0] * 4
        self._state = ProbingState.DETECTING
        self.quad = [0, 0, 0, 0]
        self.invalid_utf16be = False
        self.invalid_utf16le = False
        self.invalid_utf32be = False
        self.invalid_utf32le = False
        self.first_half_surrogate_pair_detected_16be = False
        self.first_half_surrogate_pair_detected_16le = False
        self._charset_name = None

    def feed(self, byte_str):
        """
        Feed a chunk of bytes to the prober and update its state.
        """
        if self._state == ProbingState.NOT_ME:
            return self._state

        for byte in byte_str:
            self.quad[self.position % 4] = byte
            if byte == 0:
                self.zeros_at_mod[self.position % 4] += 1
            else:
                self.nonzeros_at_mod[self.position % 4] += 1

            if self.position % 4 == 3:  # We have a complete quad
                # Check UTF-32BE
                if not self.invalid_utf32be:
                    if not self.validate_utf32_characters(self.quad):
                        self.invalid_utf32be = True

                # Check UTF-32LE
                quad_le = self.quad[::-1]  # Reverse the quad for LE
                if not self.invalid_utf32le:
                    if not self.validate_utf32_characters(quad_le):
                        self.invalid_utf32le = True

            if self.position % 2 == 1:  # We have a complete pair
                # Check UTF-16BE
                if not self.invalid_utf16be:
                    pair_be = self.quad[(self.position - 1) % 4:(self.position + 1) % 4]
                    if not self.validate_utf16_characters(pair_be):
                        self.invalid_utf16be = True

                # Check UTF-16LE
                if not self.invalid_utf16le:
                    pair_le = self.quad[(self.position - 1) % 4:(self.position + 1) % 4][::-1]
                    if not self.validate_utf16_characters(pair_le):
                        self.invalid_utf16le = True

            self.position += 1

            # Early detection if we have enough data
            if self.position >= self.MIN_CHARS_FOR_DETECTION:
                # Check UTF-32BE pattern
                if (self.zeros_at_mod[0] > 0 and self.zeros_at_mod[1] > 0 and
                    self.zeros_at_mod[2] > 0 and not self.invalid_utf32be):
                    ratio = min(self.zeros_at_mod[0:3]) / (self.position / 4)
                    if ratio > self.EXPECTED_RATIO:
                        self._charset_name = "UTF-32BE"
                        self._state = ProbingState.FOUND_IT
                        return self._state

                # Check UTF-32LE pattern
                if (self.zeros_at_mod[1] > 0 and self.zeros_at_mod[2] > 0 and
                    self.zeros_at_mod[3] > 0 and not self.invalid_utf32le):
                    ratio = min(self.zeros_at_mod[1:4]) / (self.position / 4)
                    if ratio > self.EXPECTED_RATIO:
                        self._charset_name = "UTF-32LE"
                        self._state = ProbingState.FOUND_IT
                        return self._state

                # Check UTF-16BE pattern
                if self.zeros_at_mod[0] > 0 and not self.invalid_utf16be:
                    ratio = self.zeros_at_mod[0] / (self.position / 2)
                    if ratio > self.EXPECTED_RATIO:
                        self._charset_name = "UTF-16BE"
                        self._state = ProbingState.FOUND_IT
                        return self._state

                # Check UTF-16LE pattern
                if self.zeros_at_mod[1] > 0 and not self.invalid_utf16le:
                    ratio = self.zeros_at_mod[1] / (self.position / 2)
                    if ratio > self.EXPECTED_RATIO:
                        self._charset_name = "UTF-16LE"
                        self._state = ProbingState.FOUND_IT
                        return self._state

        return self._state

    @property
    def charset_name(self):
        return self._charset_name

    @property
    def language(self):
        return ""

    def get_confidence(self):
        if self._state == ProbingState.FOUND_IT:
            return 0.99
        return 0.0