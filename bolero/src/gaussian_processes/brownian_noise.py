from util import *

# Using the Nyquist-Shannon theorem
FRAMERATE = 44100


def play_sound(wave, framerate=FRAMERATE):
    # Plays a sound wave expressed as an array of values
    return Audio(wave, rate=framerate, autoplay=True)


def show_spectrogram(wave):
    # Shows spectrogram of input wave
    X = librosa.stft(wave)
    Xdb = librosa.amplitude_to_db(abs(X))
    librosa.display.specshow(Xdb, sr=FRAMERATE, x_axis='time', y_axis='log')


def gaussian_noise(power, duration=1, framerate=FRAMERATE, min_frequency=20, max_frequency=20000):
    """
    Method to create gaussian noise inspired by https://github.com/felixpatzelt/colorednoise, the algorithm comes from :
    On generating power law noise. by Timmer and Koenig
    Astron. Astrophys (1995)

    :param power: power to which to elevate the frequencies of the form 1/(f^power) (0 -> white noise, 1 -> pink noise, 2 -> brown noise)
    :param duration: duration in seconds of the sample to create
    :param framerate: number of sample per second
    :param min_frequency: minimum frequency possible in the output, here set as the minimum frequency of the human hearing spectrum
    :param max_frequency: maximum frequency possible in the output, here set as the maximum frequency of the human hearing spectrum
    :return: a numpy array of length duration * framerate representing the sound value at each frame
    """
    # total number of frames in the output
    length = duration * framerate

    # generating sample frequencies in the Fourier domain
    sample_frequencies = rfftfreq(length)

    # frequency is in hertz = 1/s => the order is reversed for time periods
    min_period = 1 / float(max_frequency)
    max_period = 1 / float(min_frequency)

    # cutting of the array of frequencies at the minimum frequency
    nb_low_period = np.sum(sample_frequencies < min_period)
    if 0 < nb_low_period < len(sample_frequencies):
        sample_frequencies[:nb_low_period] = sample_frequencies[nb_low_period]

    # cutting of the array of frequencies at the minimum frequency
    nb_high_period = np.sum(sample_frequencies > max_period)
    if 0 < nb_high_period < len(sample_frequencies):
        index = len(sample_frequencies) - nb_high_period
        sample_frequencies[index:] = sample_frequencies[index - 1]

    # scaling factors
    scaling_factors = sample_frequencies ** (-power / 2.0)

    # Generating scaled random power + phase
    scaled_power = normal(scale=scaling_factors, size=np.array([len(sample_frequencies)]))
    scaled_phase = normal(scale=scaling_factors, size=np.array([len(sample_frequencies)]))

    # Combining power and phase
    signal = scaled_power + 1J * scaled_phase

    # Using the inverse Fourier transform to go back to the time domain
    output = irfft(signal, n=length, axis=-1)

    return output


if __name__ == "__main__":

    # not chosen as it doesn't induce the wanted effect on the listener, isn't calming and grounding as an exposition
    # should be and nearly sounds distracting
    white_noise = gaussian_noise(0, duration=10)
    play_sound(white_noise)

    # for similar reasons to white noise, we didn't choose pink_noise as it still isn't very pleasant to listen to
    pink_noise = gaussian_noise(1, duration=10)
    play_sound(pink_noise)

    # we chose to work with brown noise as it is much "smoother", nearly holding some reminiscence of the
    # sound of waves, and works well as a calm eposition
    brown_noise = gaussian_noise(2, duration=100)
    play_sound(brown_noise)

    # on the brown noise's spectrogram, we can see the decay in the associated power as the frequency increases
    show_spectrogram(brown_noise)

    # wave plot of the brown noise
    librosa.display.waveplot(brown_noise, sr=FRAMERATE)

    # we divide by 2 to reduce the amplitude of the waves (the traduction to a wav file sometimes struggled if the waves
    # had too big an amplitude), the file saving is commented out (the file is already in the media folder)

    # write(f"media{platform_str}brown_noise.wav", FRAMERATE, brown_noise / 2.0)
