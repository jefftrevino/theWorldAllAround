from abjad import *
from random import *
from clarinetSolo import *

def choose_and_skip(choices, to_skip):
    take_out = set([to_skip])
    choices = set(choices)
    choices = list(choices.difference(take_out) )
    choice =  sample(choices, 1)[0]
    return choice

def replace_note_below_split_with_rest(note, split_pitch):
    if split_pitch.chromatic_pitch_number > note.written_pitch.chromatic_pitch_number:
            duration = note.written_duration
            rest = leaftools.make_tied_leaf( Rest, duration )
            index = note.parent.index( note )
            note.parent[ index: index+1 ] = rest

def remove_chord_pitches_below_split(chord, split_pitch):
    index = chord.parent.index( chord )
    for note in reversed(chord):
        if split_pitch.chromatic_pitch_number > note.written_pitch.chromatic_pitch_number:
            note_index = chord.written_pitches.index( note )
            chord.pop(note_index)
    if 0 == len(chord.written_pitches):
        rest = leaftools.make_tied_leaf( Rest, chord.written_duration )
        chord.parent[ index:index+1 ] = rest
        
def replace_note_above_split_with_rest(note, split_pitch):
    if split_pitch.chromatic_pitch_number <= note.written_pitch.chromatic_pitch_number:
            duration = note.written_duration
            rest = leaftools.make_tied_leaf( Rest, duration )
            index = note.parent.index( note )
            note.parent[ index: index+1 ] = rest

def remove_chord_pitches_above_split(chord, split_pitch):
    index = chord.parent.index( chord )
    popped = 0
    for note in reversed(chord):
        if split_pitch.chromatic_pitch_number <= note.written_pitch.chromatic_pitch_number:
            note_index = chord.written_pitches.index( note )
            chord.pop(note_index)
            popped = 1
    if 0 == len(chord.written_pitches):
        rest = leaftools.make_tied_leaf( Rest, chord.written_duration )
        chord.parent[ index:index+1 ] = rest
    #elif popped:
        #remove_number_label_from_chord(chord)

def remove_pitches_below_split_in_components(voice, split_pitch):
    for note in iterationtools.iterate_notes_in_expr(voice.leaves):
        replace_note_below_split_with_rest(note, split_pitch)
    for chord in iterationtools.iterate_chords_in_expr(voice.leaves):
        remove_chord_pitches_below_split(chord, split_pitch)

def remove_pitches_above_split_in_components(voice, split_pitch):
    for note in iterationtools.iterate_notes_in_expr(voice.leaves):
        replace_note_above_split_with_rest(note, split_pitch)
    for chord in iterationtools.iterate_chords_in_expr(voice.leaves):
        remove_chord_pitches_above_split(chord, split_pitch)

def split_components_to_piano_staff_at_pitch(components, split_pitch = pitchtools.NamedChromaticPitch("c'")):
    piano_staff = scoretools.PianoStaff()
    #piano_staff.engraver_consists.append("#Span_stem_engraver")
    treble_staff = Staff()
    treble_staff.name = "treble"
    bass_staff = Staff()
    bass_staff.name = "bass"
    copies = componenttools.copy_components_and_covered_spanners( components )
    treble_voice = Voice(copies)
    #treble_voice.override.script.padding = 
    copies = componenttools.copy_components_and_covered_spanners( components )
    bass_voice = Voice(copies)
    #bass_voice.override.script.padding = 
    remove_pitches_below_split_in_components(treble_voice, split_pitch)
    remove_pitches_above_split_in_components(bass_voice, split_pitch)
    bass_staff.extend(bass_voice)
    treble_staff.extend(treble_voice)
    contexttools.ClefMark('bass')(bass_staff)
    #marktools.LilyPondCommandMark("autoBeamOff")(bass_staff[0])
    #marktools.LilyPondCommandMark("voiceOne",)(bass_staff[0])
    piano_staff.extend([treble_staff,bass_staff])
    return piano_staff
    
def format_piano_staff(piano_staff):
    #piano_staff.override.bar_line.stencil = False
    p#iano_staff.override.span_bar.stencil = False
    piano_staff.override.beam.transparent = True
    piano_staff.override.tuplet_bracket.stencil = False
    piano_staff.override.tuplet_number.stencil = False
    piano_staff.override.dots.transparent = True
    piano_staff.override.rest.transparent = True
    piano_staff.override.tie.transparent = True
    piano_staff.override.stem.transparent = True
    piano_staff.override.flag.stencil = False
    #piano_staff[0].override.bar_line.stencil = False
    #piano_staff[1].override.bar_line.stencil = False

def get_pitch_class_string(abbreviation):
    base = abbreviation[0]
    base = base.upper()
    return markuptools.MarkupCommand("left-align", "\\teeny", base)

def add_markup_to_illegible_note(note):
    padding = 3
    if note.written_pitch.chromatic_pitch_number >= 31:
        class_abbreviation = str(note.written_pitch.named_chromatic_pitch_class)
        letter = get_pitch_class_string(class_abbreviation)
        padded_markup = markuptools.MarkupCommand('pad-markup', schemetools.Scheme( padding ), letter)
        markup = markuptools.Markup(padded_markup, direction=Up)(note)
    elif note.written_pitch.chromatic_pitch_number <= -27:
        class_abbreviation = str(note.written_pitch.named_chromatic_pitch_class)
        letter = get_pitch_class_string(class_abbreviation)
        padded_markup = markuptools.MarkupCommand('pad-markup', schemetools.Scheme( padding ), letter)
        markup = markuptools.Markup(padded_markup, direction=Down)(note)

def add_markup_to_illegible_notes_in_leaves(leaves):
    notes = [x for x in leaves if isinstance(x, Note)]
    for note in notes:
        add_markup_to_illegible_note(note)

def derive_unprepared_pitches(preparation_groups):
    all_prepared_pitches = [pitchtools.NamedChromaticPitch(x).chromatic_pitch_number for x in sequencetools.flatten_sequence(preparation_groups)]
    all_piano_pitches = set( [x - 39 for x in range(88)] )
    unprepared_pitches = list( all_piano_pitches.difference(all_prepared_pitches) )
    unprepared_pitches.sort()
    unprepared_pitches = [pitchtools.NamedChromaticPitch(x).chromatic_pitch_name for x in unprepared_pitches]
    return unprepared_pitches

def list_prepared_notes(preparation_groups):
    staff = Staff()
    for group in preparation_groups:
        pitches = [pitchtools.NamedChromaticPitch(x) for x in group]
        pitches.sort()
        pitches.reverse()
        notes = [Note(x,(1,4)) for x in pitches]
        voice = Voice(notes)
        staff.append(voice)
    return staff

def attach_dynamic(note, previous_dynamic):
    choices = ['ppp', 'pp', 'p', 'mp', 'mf', 'f']
    choice = choose_and_skip(choices, previous_dynamic)
    previous_dynamic = choice
    contexttools.DynamicMark(choice)(note)
    return previous_dynamic

def format_staff(staff):
    for group in componenttools.yield_groups_of_mixed_klasses_in_sequence(staff, (Note, Chord)):
        for chain in tietools.iterate_tie_chains_in_expr(group):
            marktools.LilyPondCommandMark('laissezVibrer', 'after')(chain[0])
            if isinstance(chain[0], Note):
                add_markup_to_illegible_note(chain[0])
            chain[0].override.note_head.duration_log = 2
            for note in chain[1:]:
                note.override.note_head.transparent = True
                note.override.note_head.no_ledgers = True
                note.override.accidental.stencil = False

def make_chain(staff, pitch_strings, total, previous_dynamic, to_skip):
    pitch_string = choose_and_skip(pitch_strings, to_skip)
    pitch = pitchtools.NamedChromaticPitch(pitch_string)
    duration = rest_intervals_as_durations.pop(0)
    total += duration
    chain = leaftools.make_tied_leaf(notetools.Note, duration, pitches = pitch )
    previous_dynamic = attach_dynamic(chain[0], previous_dynamic)
    to_skip = chain[0].written_pitch.chromatic_pitch_name
    staff.extend( chain )
    return total, to_skip, previous_dynamic, chain

def add_quarter_of_form_to_staff(
    staff, 
    total, 
    check_duration, 
    previous_dynamic, 
    pitch_strings, 
    unprepared_treble, 
    unprepared_wait_times,
    ):
    colors = ['red', 'green', 'blue', 'yellow']
    to_skip = pitch_strings[0]
    choice = sample(unprepared_wait_times, 1)[0]
    unpreparation_count = 0
    wait_time = sample(unprepared_wait_times, 1)[0]
    while total < check_duration:
        unpreparation_count += 1
        if rest_intervals_as_durations == []:
            break
        if unpreparation_count == wait_time:
            result = make_chain(
                staff, 
                unprepared_treble, 
                total, 
                previous_dynamic, 
                to_skip,
                )
            total, to_skip, previous_dynamic, chain = result
            #markuptools.Markup('unprepared!',direction=Up)(chain[0])
            unpreparation_count = 0
            wait_time = sample(unprepared_wait_times, 1)[0]
        else:
            total, to_skip, previous_dynamic, chain = make_chain( staff, pitch_strings, total, previous_dynamic, to_skip)
        staff.extend( chain )
    return total, previous_dynamic

def make_staff(rest_intervals_as_durations, preparation_groups, unprepared_treble):
    previous_dynamic = 'f'
    shuffle(rest_intervals_as_durations)
    quarter = ( sum(rest_intervals_as_durations) / 4) 
    staff = Staff()
    total = Duration(0,1)
    unprepared_wait_times = [0]
    for x in range(4):
        if x == 1:
            unprepared_wait_times = [5,6,7]
        elif x== 2:
            unprepared_wait_times = [2,3,4]
        elif x == 3:
            unprepared_wait_times = [1,2]
        pitch_strings = preparation_groups[3-x]
        total, previous_dynamic = add_quarter_of_form_to_staff(staff, total, quarter * (x + 1), previous_dynamic, pitch_strings, unprepared_treble, unprepared_wait_times)
    componenttools.split_components_at_offsets(staff.leaves, [Duration(7,4)], cyclic = True)
    contexttools.TimeSignatureMark( (7,4) )(staff)
    return staff

def choose_sustain_string_based_on_last(last):
    if last == 'sustainOn' or last == 'sustainOff\\sustainOn':
        choices = ['sustainOff', 'sustainOff\\sustainOn' ]
    elif last == 'sustainOff':
        choices =  ['sustainOn']
    choice = sample(choices, 1)[0]
    return choice

def choose_corda_string_based_on_last(last):
    choices = [ 'unaCorda', 'treCorde' ]
    choice = choose_and_skip(choices, last)
    return choice
    
def add_corda_mark_to_note_based_on_last(note, last, bass):
    choice = choose_corda_string_based_on_last(last)
    index = note.parent.index(note)
    mark = marktools.LilyPondCommandMark(choice, 'after')(bass[ index ])
    last = choice
    return last

def add_sustain_mark_to_note_based_on_last(note,last, bass):
    choice = choose_sustain_string_based_on_last(last)
    index = note.parent.index(note)
    mark = marktools.LilyPondCommandMark(choice, 'after')(bass[ index ])
    last = choice
    return last
    
def add_pedal_marks_to_piano_staff(staff, piano_staff):
    treble = piano_staff[0]
    bass = piano_staff[1]
    bass.set.pedal_sustain_style = 'mixed'
    marktools.LilyPondCommandMark('sustainOn', 'after')(bass[0])
    marktools.LilyPondCommandMark('unaCorda', 'after')(bass[0])
    last_sustain = 'sustainOn'
    last_corda = 'unaCorda'
    chains = list(tietools.iterate_tie_chains_in_expr(staff))
    chains = chains[1:]
    for chain in chains:
        add_sustain = randint(0,1)
        add_corda = randint(0,1)
        if add_sustain:
            last_sustain = add_sustain_mark_to_note_based_on_last(chain[0],last_sustain, bass)
        if add_corda:
            last_corda = add_corda_mark_to_note_based_on_last(chain[0], last_corda, bass)

def wrap_top_octave_down(staff):
    for chain in tietools.iterate_tie_chains_in_expr(staff):
        if chain[0].written_pitch.chromatic_pitch_number >= 36:
            chain[0].written_pitch -= 12

def make_piano_staff(rest_intervals_as_durations, preparation_groups, unprepared_treble):        
    staff = make_staff(rest_intervals_as_durations, preparation_groups, unprepared_treble)
    wrap_top_octave_down(staff)
    piano_staff = split_components_to_piano_staff_at_pitch(staff[:], split_pitch = pitchtools.NamedChromaticPitch("c'"))
    format_piano_staff(piano_staff)
    format_staff(piano_staff[0])
    format_staff(piano_staff[1])
    add_pedal_marks_to_piano_staff(staff, piano_staff)
    return piano_staff

#! d''', e'', c'''' are a unison.

preparation_groups = [ \
#celesta
[ "a''''", "g''''", "f''''", "e''''", "ef''''", "d''''", "b'''", "bf'''", "a'''","af'''", "g'''", "ef'''", "e'''", "cs'''", "c'''", "b''"], \
#between
["d''", "fs''", "f''", "a''" ], \
#pitched but not piano
[ "d,", "d", "g", "g'", "af'", "bf'", "c''", "b'", "e''", "fs'''"], \
#percussion
[ "d,,", "af", "a", "bf", "b", "c'", "cs'", "d'", "ef'", "cs''", "ef''", "af''", "f'''"] \
]

unprepared_pitches = derive_unprepared_pitches(preparation_groups)
unprepared_treble = [x for x in unprepared_pitches if Note(x).written_pitch.chromatic_pitch_number > -8]
piano_staff = make_piano_staff(rest_intervals_as_durations, preparation_groups, unprepared_treble)
#score = Score([piano_staff])
#show(score)
