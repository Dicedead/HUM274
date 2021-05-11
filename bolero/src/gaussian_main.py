from brownian_noise import *

# not chosen as it doesn't induce the wanted effect on the listener, isn't calming and grounding as an exposition
# should be and nearly sounds distracting
white_noise = gaussian_noise(0, duration=10)
play_sound(white_noise)

# for similar reasons to white noise, we didn't choose pink_noise as it still isn't very pleasant to listen to
pink_noise = gaussian_noise(1, duration = 10)
play_sound(pink_noise)

# we chose to work with brown noise as it is much "smoother", nearly holding some reminiscence of the
# sound of waves, and works well as a calm eposition
brown_noise = gaussian_noise(2, duration = 100)
play_sound(brown_noise)

# on the brown noise's spectrogram, we can see the decay in the associated power as the frequency increases
show_spectrogram(brown_noise)

# wave plot of the brown noise
librosa.display.waveplot(brown_noise, sr=FRAMERATE)

# we divide by 2 to reduce the amplitude of the waves (the traduction to a wav file sometimes struggled if the waves
# had too big an amplitude), the file saving is commented out (the file is already in the media folder)

# write(f"media{platform_str}brown_noise.wav", FRAMERATE, brown_noise / 2.0)
