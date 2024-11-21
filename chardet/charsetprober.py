import logging
import re
from .enums import ProbingState
INTERNATIONAL_WORDS_PATTERN = re.compile(b'[a-zA-Z]*[\x80-\xff]+[a-zA-Z]*[^a-zA-Z\x80-\xff]?')

class CharSetProber:
    SHORTCUT_THRESHOLD = 0.95

    def __init__(self, lang_filter=None):
        self._state = None
        self.lang_filter = lang_filter
        self.logger = logging.getLogger(__name__)
        self.active = True

    @staticmethod
    def filter_international_words(buf):
        """
        We define three types of bytes:
        alphabet: english alphabets [a-zA-Z]
        international: international characters [\x80-ÿ]
        marker: everything else [^a-zA-Z\x80-ÿ]
        The input buffer can be thought to contain a series of words delimited
        by markers. This function works to filter all words that contain at
        least one international character. All contiguous sequences of markers
        are replaced by a single space ascii character.
        This filter applies to all scripts which do not use English characters.
        """
        filtered = bytearray()
        in_word = False
        prev_marker = True
        for byte in buf:
            # Get the byte value as an integer
            byte_int = byte if isinstance(byte, int) else ord(byte)
            
            # Check if it's an alphabet character
            is_alpha = (byte_int >= 65 and byte_int <= 90) or (byte_int >= 97 and byte_int <= 122)
            # Check if it's an international character
            is_international = byte_int >= 0x80 and byte_int <= 0xFF
            
            if is_alpha or is_international:
                if prev_marker and not in_word:
                    in_word = True
                if in_word:
                    filtered.append(byte_int)
            else:  # it's a marker
                if in_word:
                    in_word = False
                    if not prev_marker:
                        filtered.append(32)  # ASCII space
                prev_marker = True
                continue
            prev_marker = False
            
        return bytes(filtered)

    @staticmethod
    def remove_xml_tags(buf):
        """
        Returns a copy of ``buf`` that retains only the sequences of English
        alphabet and high byte characters that are not between <> characters.
        This filter can be applied to all scripts which contain both English
        characters and extended ASCII characters, but is currently only used by
        ``Latin1Prober``.
        """
        filtered = bytearray()
        in_tag = False
        for byte in buf:
            byte_int = byte if isinstance(byte, int) else ord(byte)
            
            if byte_int == ord('<'):
                in_tag = True
                continue
            elif byte_int == ord('>'):
                in_tag = False
                continue
            
            if not in_tag:
                filtered.append(byte_int)
                
        return bytes(filtered)

    def reset(self):
        """
        Reset the prober state to its initial value.
        """
        self._state = ProbingState.DETECTING

    def feed(self, buf):
        """
        Feed a chunk of bytes to the prober and update its state.
        """
        raise NotImplementedError

    def get_confidence(self):
        """
        Return confidence level of the prober.
        """
        raise NotImplementedError

    @property
    def charset_name(self):
        """
        Return the charset name detected by the prober.
        """
        raise NotImplementedError

    @property
    def state(self):
        """
        Return the state of the prober.
        """
        return self._state

    @property
    def language(self):
        """
        Return the language detected by the prober.
        """
        raise NotImplementedError