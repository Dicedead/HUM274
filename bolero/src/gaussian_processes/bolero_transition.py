from util import *


# opening our midi file and putting it on a stream
mf = midi.MidiFile()
mf.open(f"media{platform_str}Bolero-Ravel_Flute_Bat_Strings.mid")
mf.read()
s = stream.Stream()
s.append(midi.translate.midiFileToStream(mf))
mf.close()
