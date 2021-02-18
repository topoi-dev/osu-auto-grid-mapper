from pydub import AudioSegment

# Takes in filename *WITHOUT* extension and returns new filtered filename

def low_pass_f(filename, intensity=100):
    print('Performing low pass...')
    song = AudioSegment.from_wav(filename + '.wav')
    new = song.low_pass_filter(intensity)

    new_filename = filename + '_filtered.wav'
    new.export(new_filename, format="wav")
    return new_filename

def high_pass_f(filename, intensity=10000):
    print('Performing high pass...')
    song = AudioSegment.from_wav(filename + '.wav')
    new = song.high_pass_filter(intensity)

    new_filename = filename + '_filtered.wav'
    new.export(new_filename, format="wav")
    return new_filename