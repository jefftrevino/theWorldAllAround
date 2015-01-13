import os
from abjad import *
from WoodwindFingering import *

multiphonics = {'cresc': 
                    {2: (pitchtools.NamedChromaticPitchSet( ["ds'", "fs''"] ), 
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'five'), left_hand = ('R', 'thumb'), right_hand = ('e',) ), '' ),
                    3: (pitchtools.NamedChromaticPitchSet( ["f'", "gs''"] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'four', 'five'), left_hand = ('R', 'thumb') ), 'prominent gs' ),
                    4: (pitchtools.NamedChromaticPitchSet( ["c'", "ds''", "a''"] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'four', 'five', 'six'), left_hand = ('thumb',), right_hand=('f',)), 'dissonant/expressive'),
                    5: (pitchtools.NamedChromaticPitchSet( [ "c'", "e''", "as''" ]),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'four', 'five', 'six'), left_hand = ('R', 'cis'), right_hand=('fis',)), 'dissonant/expressive'),
                    7: (pitchtools.NamedChromaticPitchSet( [ "d'", "f''", "b''" ] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'three', 'four', 'five', 'six'), left_hand = ('R',)), 'intense/long cresc.'),
                    8: (pitchtools.NamedChromaticPitchSet( [ "d'", "fs''", "cqf'''" ] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'four', 'five', 'six'), left_hand = ('R',), right_hand = ('gis', 'four')), 'comes out easy, almost no cresc.'),
                    },
                'soft':
                    {1: (pitchtools.NamedChromaticPitchSet( [ "e'", "as'", "gqf''" ] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'four'), left_hand = ('R', 'thumb', 'cis'), right_hand = ('fis',)), ''),
                    2: (pitchtools.NamedChromaticPitchSet( [ "e'", "bf'", "g''" ] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'five', 'six'), left_hand = ('R', 'thumb', 'cis')), ''),
                    6: (pitchtools.NamedChromaticPitchSet( [ "f'", "c''", "aqf''" ] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'five', 'six'), left_hand = ('R', 'thumb',), right_hand = ('gis',)), ''),
                    8: (pitchtools.NamedChromaticPitchSet( [ "eqs'", "dqf''", "aqs''" ] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'four', 'five', 'six'), left_hand = ('R', 'thumb',), right_hand = ('f',)), ''),
                    },
                'diad':
                    {1: (pitchtools.NamedChromaticPitchSet( [ "ds'", "c''" ] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'four', 'five', 'six'), left_hand = ('R', 'thumb',), right_hand = ('f',)), ''),
                    6: (pitchtools.NamedChromaticPitchSet( [ "eqf'", "gqf''" ] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'four', 'five'), left_hand = ('R', 'thumb', 'cis'), right_hand = ('gis',)), ''),
                    7: (pitchtools.NamedChromaticPitchSet( [ "g'", "b''" ] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'five', 'six'), left_hand = ('R', 'thumb'), right_hand=('three', 'four')), 'prominent 4th'),
                    9: (pitchtools.NamedChromaticPitchSet( [ "fqs'", "cqs'''" ] ),
                        WoodwindFingering('clarinet', center_column = ('two', 'three', 'four', 'five', 'six'), left_hand = ('R', 'thumb'), right_hand = ('gis',) ), 'beats'),
                    12: (pitchtools.NamedChromaticPitchSet( [ "g'", "d'''" ] ),
                        WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'four'), left_hand = ('R',) ), 'dissonant/beats'),
                    #},
                #'shrill':
                 #   {1: (pitchtools.NamedChromaticPitchSet( [ "c'", "fs''", "c'''", "fs'''", "as'''" ] ),
                  #      WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'four', 'five', 'six'), left_hand = ('thumb', 'cis',) ), 'three pitches'),
                   # 13: (pitchtools.NamedChromaticPitchSet( [ "f", "d'''", "f'''", "as'''" ] ),
                    #    WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'four', 'five', 'six'), left_hand = ('thumb',), right_hand = ('f',)), 'resonant'),
                    #14: (pitchtools.NamedChromaticPitchSet( [ "g", "b''", "f'''", "a'''" ] ),
                    #    WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'four', 'five', 'six'), left_hand = ('thumb',)), 'resonant'),
                    #18: (pitchtools.NamedChromaticPitchSet( [ "e", "g''", "c'''", "e'''", "g'''", "a'''" ] ),
                     #   WoodwindFingering('clarinet', center_column = ('one', 'two', 'three', 'four', 'five', 'six'), left_hand = ('thumb',), right_hand = ('e',)), 'buzzy'),
                    }
                }

def make_multiphonic_markup(fingering, size=0.65, thickness=0.3, padding = 3, graphical=False):
    diagram = fingering()
    graphical = markuptools.MarkupCommand('override', schemetools.SchemePair('graphical', False))
    size = markuptools.MarkupCommand('override', schemetools.SchemePair('size', size))
    thickness = markuptools.MarkupCommand('override', schemetools.SchemePair('thickness', thickness))
    padded_markup = markuptools.MarkupCommand('pad-markup', schemetools.Scheme( padding ), [graphical, size, thickness, diagram])
    markup = markuptools.Markup(padded_markup, direction=Down)
    return markup

def make_impossible_entrances_and_exits(pitch_list, fingering):
    possibilities = []
    for pitch in pitch_list:
        in_measure = in_measure_from_pitch_list_and_fingering(pitch, pitch_list, fingering)
        out_measure = out_measure_from_pitch_list_and_fingering(pitch, pitch_list, fingering)
        possibilities.extend([in_measure, out_measure])
    return possibilities

def make_possible_entrances_and_exits(pitch_list,fingering):
    pitch = pitch_list.named_chromatic_pitches[0]
    in_measure = in_measure_from_pitch_list_and_fingering(pitch, pitch_list, fingering)
    out_measure = out_measure_from_pitch_list_and_fingering(pitch, pitch_list, fingering)
    return [ in_measure, out_measure ]
    

def in_measure_from_pitch_list_and_fingering(pitch, pitch_list, fingering):
    in_measure = Measure((4,4), [])
    chord = Chord([pitch], (1,2))
    in_measure.append( chord )
    chord.override.note_head.style = 'harmonic'
    chord = Chord(pitch_list, (1,2))
    markup = make_multiphonic_markup(fingering)
    markup.attach(chord)
    in_measure.append(chord)
    tietools.TieSpanner(in_measure[:])
    return in_measure
    
def out_measure_from_pitch_list_and_fingering(pitch, pitch_list, fingering):
    out_measure = Measure((4,4), [])
    chord = Chord(pitch_list, (1,2))
    markup = make_multiphonic_markup(fingering)
    markup.attach(chord)
    out_measure.append(chord)
    chord = Chord([pitch], (1,2))
    out_measure.append( chord )
    tietools.TieSpanner(out_measure[:])
    return out_measure

def multiphonic_dictionary_to_possibilities(dictionary):
    measures = []
    for value in dictionary.values():
        possibilities = make_possible_entrances_and_exits(value[0], value[1])
        measures.extend(possibilities)
    return measures

def multiphonics_to_possibilities(multiphonics):
    measures = []
    for value in multiphonics.values():
        print 'here.'
        measures = multiphonic_dictionary_to_possibilities(value)
        measures.extend(measures)
    return measures

def make_and_edit_measures(multiphonics):
    print_measures = []
    cresc_measures = multiphonic_dictionary_to_possibilities(multiphonics['cresc'])
    print_measures.extend( cresc_measures )
    soft_measures = multiphonic_dictionary_to_possibilities(multiphonics['soft'])
    print_measures.extend(soft_measures)
    diad_measures = multiphonic_dictionary_to_possibilities(multiphonics['diad'])
    print_measures.extend(diad_measures)
    return print_measures

print_measures = make_and_edit_measures(multiphonics)