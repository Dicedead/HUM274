from music21 import instrument


class Underwater(instrument.Percussion):
    def __init__(self):
        super(Underwater, self).__init__()
        self.instrumentSound = "instruments/underwater.mid"
