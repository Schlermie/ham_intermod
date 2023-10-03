""" Objects used in HamIM """

class Freq:
    """ A radio frequency and its associated attributes """
    def __init__(self, frequency, aggressor_score, victim_score, total_score):
        """ Initialize attributes for the radio frequency """
        self.frequency = frequency
        self.aggressor_score = aggressor_score
        self.victim_score = victim_score
        self.total_score = total_score