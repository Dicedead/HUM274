from convergence_complexification import *


def generate_melody(key_melody, bass_melody, start_melody, length_melody, path_string):
    voices = notes_array(key_melody, bass_melody, start_melody, length_melody)
    string_res = run_slow_for(4)
    sequence = sequence_from_string_slow(string_res)
    instruments = [instrument.Piano(), instrument.Piano(), instrument.Piano(), instrument.Piano()]

    parts = combine_voices(len(voices[0]), sequence, voices, inst=instruments, time_sig="3/4")

    parts.write('midi', 'midi' + platform_str + path_string + '.mid')


if __name__ == '__main__':
    generate_melody(Key.DO_MAJOR, bass_do_major, start_chord_do_major, 10, "convergence_melody_do_Major_2")
