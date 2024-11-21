"""
All of the Enums that are used throughout the chardet package.

:author: Dan Blanchard (dan.blanchard@gmail.com)
"""

class InputState:
    """
    This enum represents the different states a universal detector can be in.
    """
    PURE_ASCII = 0
    ESC_ASCII = 1
    HIGH_BYTE = 2

class LanguageFilter:
    """
    This enum represents the different language filters we can apply to a
    ``UniversalDetector``.
    """
    CHINESE_SIMPLIFIED = 1
    CHINESE_TRADITIONAL = 2
    JAPANESE = 4
    KOREAN = 8
    NON_CJK = 16
    ALL = 31
    CHINESE = CHINESE_SIMPLIFIED | CHINESE_TRADITIONAL
    CJK = CHINESE | JAPANESE | KOREAN

class ProbingState:
    """
    This enum represents the different states a prober can be in.
    """
    DETECTING = 0
    FOUND_IT = 1
    NOT_ME = 2

class MachineState:
    """
    This enum represents the different states a state machine can be in.
    """
    START = 0
    ERROR = 1
    ITS_ME = 2

class SequenceLikelihood:
    """
    This enum represents the likelihood of a character following the previous one.
    """
    NEGATIVE = 0
    UNLIKELY = 1
    LIKELY = 2
    POSITIVE = 3

    @classmethod
    def get_num_categories(cls):
        """:returns: The number of likelihood categories in the enum."""
        return 4  # NEGATIVE through POSITIVE

class CharacterCategory:
    """
    This enum represents the different categories language models for
    ``SingleByteCharsetProber`` put characters into.

    Anything less than CONTROL is considered a letter.
    """
    UNDEFINED = 255
    LINE_BREAK = 254
    SYMBOL = 253
    DIGIT = 252
    CONTROL = 251