import os
import argparse
import math

import bpmdetection
import mp3towav
import filters
import snapobjects
import cclockwise_grid
from console_colors import colors

def calc_distance(x1, x2, y1, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def main() :
# Any initialization
    os.system("")
    print(colors.reset)

# 1. Detect filename extension (needs .wav output)
    parser = argparse.ArgumentParser(description="Determine extension for wav file processing.")
    parser.add_argument("--filename", required=True, help="audio file input")
    args = parser.parse_args()
    
    wav_filename = ''
    filename = os.path.splitext(args.filename)[0]
    extension = os.path.splitext(args.filename)[1]

    # Different file extensions (currently .mp3 and .wav)
    if extension == '.mp3':
        # convert mp3 to wav
        mp3towav.mp3towav(filename)
        wav_filename = filename + '.wav'
    elif extension == '.wav':
        wav_filename = args.filename
    else:
        print('man why cant u input a common audio file')
        return

# 2. Lowpass/highpass filters for better detection
    print(colors.c.lightcyan + '\nSelect a filter:' + colors.reset)
    print('0 - Use base mp3 (no filtering)')
    print('1 - Perform lowpass (focusing on bass | keeps low frequencies)')
    print('2 - Perform highpass (focusing on removing bass | keeps high frequencies)')
    f = input()

    if (f==str(1)) :
        print(colors.c.lightcyan + '\nSet filter intensity ' +  colors.reset + '(lower=more intense | default=100 | suggested range=10-400):')
        i = input()
        if (i == ''): filtered_filename = filters.low_pass_f(filename)
        else: filtered_filename = filters.low_pass_f(filename, int(i))
    elif (f==str(2)):
        print(colors.c.lightcyan + '\nSet filter intensity ' +  colors.reset + '(higher=more intense | default=10000 | suggested range=5000-30000):')
        i = input()
        if (i == ''): filtered_filename = filters.high_pass_f(filename)
        else: filtered_filename = filters.high_pass_f(filename, int(i))
    else:
        print(colors.reset + 'Not using filter...')
        filtered_filename = wav_filename

# 3. Find the song's BPM
    bpm = bpmdetection.bpm_detect(filtered_filename)
    print('BPM has been set to ' + str(bpm))

# 4. Start onset detection (creates onsets and averages)
    execution_string = "pyonset.py " + filtered_filename
    os.system(execution_string)

# 5. Write onsets to timing point list
    onsets_filename = os.path.splitext(filtered_filename)[0] + ".onsets.txt"
    onsets_f = open(onsets_filename)

    timing_points = [] 

    for timing_point in onsets_f:
        # convert from strings to timing points
        timing_point = float(timing_point)
        timing_point *= 1000
        timing_point = int(round(timing_point,0)) - 35 # ~45 offset most cases

        timing_points.append(timing_point) 
    onsets_f.close()
    
    # clean onsets file (i know theres better ways to do this too lazy rn)
    os.remove(onsets_filename)

# 6. Write averages to averages list
    avgs_filename = os.path.splitext(filtered_filename)[0] + ".averages.txt"
    avgs_f = open(avgs_filename)
    mov_averages = []
    for avg in avgs_f:
        # convert from strings to averages
        avg = float(avg)
        mov_averages.append(avg) 
    avgs_f.close()
    
    # clean averages file (i know theres better ways to do this too lazy rn)
    os.remove(avgs_filename)

# 7. Snap objects to new timing
    print(colors.c.lightcyan + '\nSnap objects to new timing automatically?' + colors.reset + ' (recommended) [y/n]')
    snap_input = input()
    if (snap_input == 'n' or snap_input == 'N'): 
        print('Not snapping objects...')
        snapped_timings = timing_points
        fourth_length = snapobjects.calc_fourth_length(bpm) 
    else: 
        print('Snapping objects...')
        snapped_timings, fourth_length = snapobjects.snap_timings(timing_points, bpm)
    
#8. Adjust timings for sliders
    print(colors.c.lightcyan + '\nSet slider threshold' + colors.reset + ' (default: 0.4 | range 0-1 | 0 = all sliders, 1 = none):')
    slider_t = input()
    if (slider_t == "" or float(slider_t) > 1 or float(slider_t) < 0):
        slider_t = 0.4
    else:
        slider_t = float(slider_t)
    
    print('Setting sliders...')
    snapped_timings, slider_ends = snapobjects.adjust_onsets(snapped_timings,mov_averages,slider_t)

# 9. Create note positions
    # parameters: note timings, estimate interval for 1/4th snapping, 
                  # grid size (default 32, recommended: mulitples of 4)
    note_locations = cclockwise_grid.map_cclockwise_grid(snapped_timings, round(fourth_length), 32)

# 10. Insert into hitobject file
    # overwrite any last outputs
    if os.path.exists('hitobjects.txt'):
        os.remove('hitobjects.txt')
    hitobjects_f = open("hitobjects.txt", "x")

    # nc = new combo, interval means how many notes until nc
    nc_counter = 1000
    nc_interval = 5
    nc = 5
    cur_note = 0

    while cur_note < len(snapped_timings):
        if (nc_counter >= (nc_interval-1)):
            nc_counter=0
            nc = 5
        else:
            nc_counter+=1
            nc = 1

        # if the next note is slider end, map slider and increment by 2
        if (cur_note+1 < len(slider_ends) and slider_ends[cur_note+1] == 1):
            # hitobjects_f.write(str(note_locations[cur_note][1]) + "," + str(note_locations[cur_note][0]) 
            #         + "," + str(snapped_timings[cur_note]) + "," + str(nc) + ",0,0:0:0:0:\n")
            d_val = calc_distance(note_locations[cur_note][1], note_locations[cur_note+1][1], 
                                    note_locations[cur_note][0],note_locations[cur_note+1][0]) + 1
            
            hitobjects_f.write(str(note_locations[cur_note][1]) + "," + 
                                str(note_locations[cur_note][0]) + "," + 
                                str(snapped_timings[cur_note]) + "," + 
                                str(nc+1) + ",0,L|" +
                                str(note_locations[cur_note+1][1]) + ":" + 
                                str(note_locations[cur_note+1][0]) + ",1," + 
                                str(d_val) + "\n")
            cur_note+=1
        else:
            # .osu format - x cord, y cord, timing, new combo (5 for nc, 1 for not),0,0:0:0:0: (rest is slider info)
            hitobjects_f.write(str(note_locations[cur_note][1]) + "," + 
                                str(note_locations[cur_note][0]) + "," + 
                                str(snapped_timings[cur_note]) + "," + 
                                str(nc) + ",0,0:0:0:0:\n")
        
        cur_note+=1

    hitobjects_f.close()

    print('Complete!')

    
if __name__ == '__main__':
    main()