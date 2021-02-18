import numpy as np

# search for closest value in an array
def get_closest(array, value):
    array = np.asarray(array);     
    idx = (np.abs(array - value)).argmin();     
    return array[idx];

def calc_fourth_length(bpm):
    # from https://osu.ppy.sh/wiki/fi/osu%21_File_Formats/Osu_%28file_format%29
    beat_length = 1 / (bpm / 60 / 1000)
    beat_length_fourth = beat_length / 4
    return beat_length_fourth

def snap_timings(array, bpm):
    beat_length_fourth = calc_fourth_length(bpm)

    start_offset = array[0]
    end_offset = array[len(array)-1]

    matched_timings = [start_offset]
    current_timing = start_offset

    while (current_timing <= end_offset):
        current_timing+=beat_length_fourth
        matched_timings.append(round(current_timing))

    snapped_timings = []
    for timing in array:
        snapped_timings.append(get_closest(matched_timings, timing))

    return snapped_timings, beat_length_fourth

def adjust_onsets(timings, averages, slider_t = 0.4):
    # create dictionary of timings to averages
    adjusted = dict(zip(timings,averages))

    prev_avg = -1.0
    threshold = 0

    for i in adjusted:
        threshold+=adjusted[i]

    threshold = (threshold / len(adjusted)) * slider_t

    slider_ends = []
    prev_slider = False

    if(slider_t == 0):
        slider_ends = [1] * len(adjusted)
    elif(slider_t == 1):
        slider_ends = [0] * len(adjusted)
    else:
        for i in adjusted:
            if (adjusted[i] < prev_avg and (prev_avg-adjusted[i]) > threshold and not prev_slider):
                slider_ends.append(1)
                prev_slider = True
            else:
                slider_ends.append(0)
                prev_slider = False
            prev_avg = adjusted[i]
            # slider_ends.append(1)
            # slider_ends.append(0)

        # TODO: idk why i need to shift left one
        slider_ends.pop(0)
        slider_ends.append(0)

    # for i in range(len(slider_ends)):
    #     if (slider_ends[i] == 1):
    #         print("note " + str(i-1) + " is a slider")

    # return new timings and slider ends
    return [*adjusted], slider_ends
