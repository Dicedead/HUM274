from music21 import instrument


class Underwater(instrument.Instrument):
    def __init__(self):
        super().__init__()
        self.instrumentName = 'Clavichord'
        self.instrumentAbbreviation = 'Clv'
        self.midiProgram = 7
        self.instrumentSound = 'keyboard.clavichord'
