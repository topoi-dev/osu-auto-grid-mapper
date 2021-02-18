import subprocess

def mp3towav(filename):
    print('Converting mp3 to wav...')
    mp3_file = filename + '.mp3'
    output_file = filename + '.wav'

    subprocess.call(['ffmpeg', '-i', mp3_file, output_file])