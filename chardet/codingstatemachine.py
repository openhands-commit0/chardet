import logging
from .enums import MachineState

class CodingStateMachine:
    """
    A state machine to verify a byte sequence for a particular encoding. For
    each byte the detector receives, it will feed that byte to every active
    state machine available, one byte at a time. The state machine changes its
    state based on its previous state and the byte it receives. There are 3
    states in a state machine that are of interest to an auto-detector:

    START state: This is the state to start with, or a legal byte sequence
                 (i.e. a valid code point) for character has been identified.

    ME state:  This indicates that the state machine identified a byte sequence
               that is specific to the charset it is designed for and that
               there is no other possible encoding which can contain this byte
               sequence. This will to lead to an immediate positive answer for
               the detector.

    ERROR state: This indicates the state machine identified an illegal byte
                 sequence for that encoding. This will lead to an immediate
                 negative answer for this encoding. Detector will exclude this
                 encoding from consideration from here on.
    """

    def __init__(self, sm):
        self._model = sm
        self._curr_byte_pos = 0
        self._curr_char_len = 0
        self._curr_state = None
        self.logger = logging.getLogger(__name__)
        self.reset()

    def reset(self):
        """
        Reset the state machine to its initial state.
        """
        self._curr_state = MachineState.START
        self._curr_byte_pos = 0
        self._curr_char_len = 0

    def next_state(self, c):
        """
        Process one byte at a time and return the new state.
        """
        # for each byte we get its class
        byte_class = self._model['class_table'][c]
        if byte_class == 'eError':  # we represent error class as None
            self._curr_state = MachineState.ERROR
            return self._curr_state

        # for each byte class we get a state transition table
        if self._curr_state == MachineState.START:
            self._curr_byte_pos = 0
            self._curr_char_len = self._model['char_len_table'][byte_class]

        # from byte's class and state_table, we get its next state
        curr_state = self._curr_state * self._model['class_factor'] + byte_class
        self._curr_state = self._model['state_table'][curr_state]

        # we increment the byte position counter
        self._curr_byte_pos += 1

        return self._curr_state

    def get_current_charlen(self):
        """
        Return the length of the current character being detected.
        """
        return self._curr_char_len