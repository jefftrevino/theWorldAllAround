from abjad import *
from ratioChains import *
import os
from itertools import permutations
from multiphonics import *
from random import *

seed(6)

def get_first_markup_from_left_to_right(leaves):
    for leaf in leaves:
        if markuptools.get_markup_attached_to_component(leaf):
            return markuptools.remove_markup_attached_to_component(leaf)[0]

def move_diagrams_to_single_notes(leaves):
    print 'group:'
    print leaves
    print 'chains:'
    for chain in tietools.iterate_tie_chains_in_expr(leaves):
        print chain
        if len(chain) > 1 and len(chain[0]) == 1:
            diagram = get_first_markup_from_left_to_right(chain)
            if diagram:
                diagram.attach(chain[0])
                print 'attached'

def add_rehearsal_marks_to_voice(voice):
    for x in range( len(voice)):
        if x % 10 == 0:
            marktools.LilyPondCommandMark("mark \\default")(voice[x][-1])

def tupletize_duration_recursively_by_ratio_at_depth(duration, ratio, depth):
    tuplet = tuplettools.make_tuplet_from_duration_and_ratio(duration, ratio)
    for x in range(depth):
        last_tuplet_created = tuplettools.get_first_tuplet_in_proper_parentage_of_component(tuplet.leaves[-1])
        last_tuplet_created[1:] = [ tuplettools.make_tuplet_from_duration_and_ratio( duration, ratio ) ]
    return tuplet

def replace_leaves_with_pitches(voice, pitches):
    if markuptools.get_markup_attached_to_component(voice[0]):
        diagram = markuptools.remove_markup_attached_to_component(voice[0])
    for leaf in voice.leaves:
        chord = Chord(leaf)
        chord[:] = []
        chord.extend(pitches)
        componenttools.move_parentage_and_spanners_from_components_to_components([leaf], [chord])
    if isinstance(voice[0], Chord):
        markup = diagram
        markup.attach(voice[0])

def change_note_heads_if_air_note(choice, voice):
    if hasattr(choice.override.note_head, 'style'):
        for note in voice:
            note.override.note_head.style = 'harmonic'

def make_diaphragm_bounce_voice(duration, depth, choice):
    print duration
    tuplet = tupletize_duration_recursively_by_ratio_at_depth(duration, [1,1,1], depth)
    voice = Voice([tuplet])
    if isinstance(choice, Chord) and len(choice) > 1: 
        diagram = markuptools.remove_markup_attached_to_component(choice)[0]
        pitches = choice.written_pitches
    else:    
        #change_note_heads_if_air_note(choice, voice)
        pitches = choice.written_pitches
    replace_leaves_with_pitches(voice, pitches)
    if isinstance(choice, Chord) and len(choice) > 1:
        diagram.attach(voice[0][0])
    voice.override.tuplet_bracket.stencil = False
    voice.override.tuplet_number.stencil = False
    voice.override.stem.stencil = False
    voice.override.stem.stencil = False
    return voice

def choose_multiphonic(multiphonics):
    group = sample(multiphonics.values(), 1)[0]
    multiphonic = sample(group.values(), 1)[0]
    return multiphonic
    

def apply_multiphonic(voice):
    multiphonic = choose_multiphonic(multiphonics)
    pitches = multiphonic[0]
    fingering = multiphonic[1]
    diagram = fingering()
    replace_leaves_with_pitches(voice,pitches)
    markup = markuptools.Markup(diagram,direction=Down)(voice.leaves[0])
    
def format_bounce(voice):
    for x in range( len(voice.leaves) ):
        if x % 2 is 0:
            marktools.Articulation('>')(voice.leaves[x])

def make_air_chord(bar):
    note = [x for x in bar if len(x) == 1][0]
    #make the air note
    air_note = Chord(note.written_pitches,(1,2))
    air_note.override.note_head.style = 'harmonic'
    #air_note.override.note_head.no_ledgers = True
    return air_note

def choose_fermata():
    prefixes = ['short', '', 'long', 'verylong']
    prefix = sample(prefixes,1)[0]
    mark_string = prefix + 'fermata'
    return mark_string

def make_rest():
    rest = Rest("r4")
    fermata_string = choose_fermata()
    marktools.LilyPondCommandMark(fermata_string, 'after')(rest)
    return rest

def replace_leaf_with_bounce(copies):
    candidates = [x for x in copies if not isinstance(x, Rest)]
    choice = sample(candidates,1)[0]
    bounce_depth = randint(6,11)
    if isinstance(choice, Note):
        voice = make_diaphragm_bounce_voice( choice.duration, bounce_depth, choice)
        change_note_heads_if_air_note(choice, voice)
    else:
        voice = make_diaphragm_bounce_voice(choice.duration, bounce_depth, choice)
    format_bounce(voice)
    componenttools.move_parentage_and_spanners_from_components_to_components([choice], [voice])
    
def bar_to_bars_with_rests_and_air_notes(bar):
    out_bars = []
    leaves = list(componenttools.copy_components_and_covered_spanners(bar.leaves))
    rest = make_rest()
    leaves.append( rest )
    air_note = make_air_chord(bar)
    leaves.append(air_note)
    for permutation in permutations(leaves):
        copies = componenttools.copy_components_and_covered_spanners(permutation)
        print copies
        new_bar = Measure((7,4), copies)
        choices = [0]*9
        choices.append(1)
        choice = sample(choices,1)[0]
        if choice:
            replace_leaf_with_bounce(new_bar.leaves)
        out_bars.append(new_bar)
    return out_bars
        
def add_air_and_rest_to_bars(bars):
    out_bars = []
    for bar in bars:
        permuted = bar_to_bars_with_rests_and_air_notes(bar)
        out_bars.extend(permuted)
    return out_bars

def tie_groups_in_bar(bar):
    for group in componenttools.yield_groups_of_mixed_klasses_in_sequence(bar, (Note, Chord)):
        tietools.TieSpanner(group[:])

def liberate_notes_from_voice(bar):
    for component in bar:
        if isinstance(component, Voice):
            componenttools.replace_components_with_children_of_components([component])

def delete_abutting_rests(voice):
    for x in reversed(range(len(voice) - 1)):
        if isinstance(voice[x], Rest) and isinstance(voice[x+1], Rest):
            del(voice[x])

def choose_and_skip(choices, to_skip):
    take_out = set([to_skip])
    choices = set(choices)
    choices = list(choices.difference(take_out) )
    return sample(choices, 1)[0]

def add_dynamic_to_first_in_bar_based_on_last(last, bar):
    dynamic = choose_and_skip( ['ppp', 'pp', 'p', 'mp'], last) 
    if isinstance(bar[0], Rest) and isinstance(bar[1], Tuplet):
        contexttools.DynamicMark(dynamic)(bar[1][0])
    elif isinstance(bar[0], Rest) and isinstance(bar[1], Chord):
        contexttools.DynamicMark(dynamic)(bar[1])
    elif isinstance(bar[0], Tuplet):
        contexttools.DynamicMark(dynamic)(bar[0][0])
    else:
        contexttools.DynamicMark(dynamic)(bar[0])
    return dynamic

def add_arrow_spanner_to_leaves(leaves):
    arrow = spannertools.TextSpanner(leaves)
    arrow.override.text_spanner.bound_details__right__arrow = True
    arrow.override.text_spanner.style = schemetools.Scheme('solid-line', quoting="'")

def add_arrow_spanner_to_leaves_in_expr(expr):
    for group in componenttools.yield_groups_of_mixed_klasses_in_sequence(expr.leaves, (Chord, Tuplet)):
        if len(group) > 1:
            add_arrow_spanner_to_leaves(group[:])

def make_voice_from_chart(print_measures, number_of_measures):
    voice = Voice([])
    for bar in print_measures:
        bar.automatically_adjust_time_signature = True
    out_bars = add_air_and_rest_to_bars(print_measures)
    out_bars = sample(out_bars, number_of_measures)
    for bar in out_bars:
        marktools.LilyPondCommandMark('break', 'after')(bar[-1])
    voice.extend(out_bars)
    tietools.remove_tie_spanners_from_components_in_expr(voice)
    voice.override.script.padding = 2
    voice.override.time_signature.stencil = False
    voice.override.stem.stencil = False
    voice.override.tuplet_bracket.stencil = False
    voice.override.tuplet_number.stencil = False
    return voice

def format_voice(voice):
    voice.override.script.padding = 2
    voice.override.time_signature.stencil = False
    voice.override.stem.stencil = False
    voice.override.tuplet_bracket.stencil = False
    voice.override.tuplet_number.stencil = False

def change_half_note_note_heads_in_group(group):
    for chord in group:
        if chord.duration == Duration(1,2):
            chord.override.note_head.duration_log = 2

def decorate_voice(voice):
    for bar in voice:
        liberate_notes_from_voice(bar)
    last = 'mp'
    for bar in voice:
        last = add_dynamic_to_first_in_bar_based_on_last(last, bar)
    componenttools.replace_components_with_children_of_components(voice[:])
    for group in componenttools.yield_groups_of_mixed_klasses_in_sequence(voice.leaves, (Chord, Chord)):
        if len(group) > 1:
            tietools.TieSpanner(group[:])
            add_arrow_spanner_to_leaves(group[:])
            #move_diagrams_to_single_notes(group[:])
        #change_half_note_note_heads_in_group(group)
    #delete_abutting_rests(voice)

def voice_to_staff(voice):
    staff = Staff([voice])
    #staff.override.bar_line.stencil = False
    return staff

def make_lilypond_file(score):
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    lilypond_file.default_paper_size = 'legal', 'landscape'
    lilypond_file.global_staff_size = 18
    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    lilypond_file.paper_block.top_margin = 15
    lilypond_file.paper_block.bottom_margin = 3
    lilypond_file.paper_block.left_margin = 15
    lilypond_file.paper_block.right_margin = 15
    lilypond_file.paper_block.markup_system_spacing__basic_distance = 15
    lilypond_file.paper_block.ragged_bottom = True
    lilypond_file.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 8, 0)
    return lilypond_file
    
def make_clarinet_solo_document(print_measures):
    voice = make_voice_from_chart(print_measures)
    decorate_voice(voice)
    score = make_score_from_voice(voice)
    lilypond_file = make_lilypond_file(score)
    show(lilypond_file)

def get_durations_between_rests(expr):
    durations = []
    last_end = Offset(0,1)
    for rest in iterationtools.iterate_rests_in_expr(expr):
        duration = rest.timespan.offsets[0] - last_end
        durations.append( duration )
        last_end = rest.timespan.offsets[0]
    last_duration = expr.timespan.offsets[1] - rest.timespan.offsets[0]
    durations.append( last_duration )
    return durations

def bars_to_pitch_sets(clarinet_voice):
    sets = []
    for bar in clarinet_voice:
        pitches = set( pitchtools.list_named_chromatic_pitches_in_expr(bar.leaves) )
        sets.append( pitches )
    return sets

def transpose_pitch_sets(sets):
    transposed_sets = []
    for pitch_set in sets:
        transposed_set = []
        for pitch in pitch_set:
            pitch -= 2
            transposed_set.append(pitch)
        transposed_sets.append( transposed_set)
    return transposed_sets

def get_transposed_pitch_sets_from_voice(clarinet_voice):
    sets = bars_to_pitch_sets(clarinet_voice)
    transposed_sets = transpose_pitch_sets(sets)
    return transposed_sets

def change_all_single_pitch_chords_note_heads(staff):
    for leaf in staff.leaves:
        if isinstance(leaf, Chord):
            if len(leaf) == 1:
                leaf.override.note_head.style = 'harmonic'

def chop_durations_in_half(durations):
    output = []
    for duration in durations:
        if duration == Duration(11,4) or duration == Duration(13,4):
            print duration / 2
            output.extend( [duration / 2, duration / 2] )
        else:
            output.append( duration)
    return output

clarinet_voice = make_voice_from_chart(print_measures, 42)
pitch_sets_by_bar = get_transposed_pitch_sets_from_voice(clarinet_voice)
print pitch_sets_by_bar
print '----'
decorate_voice(clarinet_voice)
rest_intervals_as_durations = get_durations_between_rests(clarinet_voice)
rest_intervals_as_durations = chop_durations_in_half(rest_intervals_as_durations)
harp_rest_intervals = rest_intervals_as_durations[:]
format_voice(clarinet_voice)
clarinet_staff = voice_to_staff(clarinet_voice)
change_all_single_pitch_chords_note_heads(clarinet_staff)
contexttools.TimeSignatureMark((7,4))(clarinet_staff[0])