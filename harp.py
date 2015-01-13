from categorizedPreparations import *
#for each bar,
#get the set of pitches in the clarinet part and transpose them down by a whole step to get concert pitches.
#compose four interval taleas, one per quarter of the form. Some intervals should stay the same, others should change.
interval_sets = [ 
    [6,1,0],
    [6,1, 2, 0, 8],
    [6,1, 2, 0, 8, 3],
    [1, 2, 0, 11],
    ]

#choose a new set of pitches based on the chosen intervals.
#choose an octave for those pitches.
#choose one pitch or an octave.
#if it's one pitch, make it a harmonic or not.
#use location of rests in clarinet parts to place harp events (shuffled)
#per bar, if an event exists, 
#get the pitches for that bar,
#choose two pitches and make them within a tenth. (wrapping)
def choose_pitch_based_on_bar_set(bar_set, interval_set):
    base_pitch = sample(bar_set, 1)[0]
    interval = sample(interval_set, 1)[0]
    up = randint(0,1)
    if up:
        out_pitch = pitchtools.NamedChromaticPitch( base_pitch + interval)
    else:
        out_pitch = pitchtools.NamedChromaticPitch( base_pitch - interval)
    if not isinstance(out_pitch.chromatic_pitch_number, int):
        out_pitch += 0.5
    return out_pitch

def reoctavize_pitch(pitch, last):
    class_name = pitch.chromatic_pitch_class_name
    octave_choices = [ ',,', ',', '', "'", "''"]
    choice = choose_and_skip(octave_choices, last)
    last = choice
    pitch = class_name + choice
    return last, pitchtools.NamedChromaticPitch(pitch)

def choose_and_reoctavize_pitch_based_on_bar_set(pitch_set, interval_set, last_octave):
    pitch = choose_pitch_based_on_bar_set(pitch_set, interval_set)
    last, shifted_pitch = reoctavize_pitch(pitch, last_octave)
    return last, shifted_pitch

def add_flageolet_to_note_based_on_pitch(note):
    if note.written_pitch.chromatic_pitch_number < 0:
        marktools.Articulation('flageolet', Down)(note)
    else:
        marktools.Articulation('flageolet', Up)(note)

def make_octave_chain(pitch, duration):
    if pitch.chromatic_pitch_number <= -24:
        pitches = [pitch, pitch + 12]
    else:
        pitches = [pitch, pitch - 12]
    chain = leaftools.make_tied_leaf(chordtools.Chord, duration, pitches = pitches )
    return chain

def make_chain(staff, total, previous_dynamic, interval_set, pitch_set, harp_rest_intervals, previous_octave):
    previous_octave, pitch = choose_and_reoctavize_pitch_based_on_bar_set(pitch_set, interval_set, previous_octave)
    duration = harp_rest_intervals.pop(0)
    total += duration
    print total
    octavization_chances = [0,0,0,1]
    octavization = sample(octavization_chances, 1)[0]
    if octavization:
        chain = make_octave_chain(pitch, duration)
    else:
        chain = leaftools.make_tied_leaf(notetools.Note, duration, pitches = pitch )
    previous_dynamic = attach_dynamic(chain[0], previous_dynamic)
    harmonic_chances = [0,0,0,1]
    harmonic = sample(harmonic_chances, 1)[0]
    if isinstance(chain[0], Note):
        if harmonic and chain[0].written_pitch.chromatic_pitch_number > -24 and chain[0].written_pitch.chromatic_pitch_number <= 17:
            add_flageolet_to_note_based_on_pitch(chain[0])
    staff.extend( chain )
    return total, previous_dynamic, previous_octave, chain

def add_harp_quarter_of_form_to_staff(staff, total, check_duration, previous_dynamic, interval_set, pitch_set, harp_rest_intervals, previous_octave):
    while total < check_duration:
        if harp_rest_intervals == []:
            break
        total, previous_dynamic, previous_octave, chain = make_chain( staff, total, previous_dynamic, interval_set, pitch_set, harp_rest_intervals, previous_octave)
        staff.extend( chain )
    return total, previous_dynamic, previous_octave

def make_harp_staff(harp_rest_intervals, interval_sets, pitch_sets_by_bar):
    previous_dynamic = 'f'
    previous_octave = ',,'
    shuffle(harp_rest_intervals)
    quarter = ( sum(harp_rest_intervals) / 4) 
    staff = Staff()
    total = Duration(0,1)
    for x in range(4):
        measure_index = int( total / Duration(7,4) )
        if total % Duration(7,4) == 0:
            measure_index -= 1
        pitch_set = pitch_sets_by_bar[ measure_index ]
        interval_set = interval_sets[ x ]
        total, previous_dynamic, previous_octave = add_harp_quarter_of_form_to_staff(staff, total, quarter * (x + 1), previous_dynamic, interval_set, pitch_set, harp_rest_intervals, previous_octave)
    componenttools.split_components_at_offsets(staff.leaves, [Duration(7,4)], cyclic = True)
    contexttools.TimeSignatureMark( (7,4) )(staff)
    return staff

def make_harp_double_staff(harp_rest_intervals, interval_sets, pitch_sets_by_bar):        
    staff = make_harp_staff(harp_rest_intervals, interval_sets, pitch_sets_by_bar)
    double_staff = split_components_to_piano_staff_at_pitch(staff[:], split_pitch = pitchtools.NamedChromaticPitch("c'"))
    format_piano_staff(double_staff)
    format_staff(double_staff[0])
    format_staff(double_staff[1])
    double_staff.override.script.padding = 1
    return double_staff

harp_staff = make_harp_double_staff(harp_rest_intervals, interval_sets, pitch_sets_by_bar)