import os
from abjad import *
from ratioChains import *
from harp import *

def format_score(clarinet_staff, piano_staff, harp_staff):
    contexttools.InstrumentMark('Clarinet', 'clar.',)(clarinet_staff)
    contexttools.InstrumentMark('Piano', 'Pno.', target_context=scoretools.PianoStaff)(piano_staff)
    contexttools.InstrumentMark(
        'Harp', 'Hp.',
        target_context=scoretools.PianoStaff
        )(harp_staff)
    score = Score([])
    score.append(clarinet_staff)
    score.append(piano_staff)
    score.append(harp_staff)
    marktools.BarLine('|.')(clarinet_staff[0][-1])
    marktools.BarLine('|.')(piano_staff[0][-1])
    score.override.rehearsal_mark.padding = 3
    score.override.bar_number.stencil = False
    score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 64)
    score.override.spacing_spanner.uniform_stretching = True
    score.override.spacing_spanner.strict_note_spacing = True
    score.override.time_signature.stencil = False
    contexttools.set_accidental_style_on_sequential_contexts_in_expr(score,'forget')
    return score
    
def make_lilypond_file(score):
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    lilypond_file.default_paper_size = 'tabloid', 'portrait'
    lilypond_file.global_staff_size = 14
    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    lilypond_file.paper_block.top_margin = 15
    lilypond_file.paper_block.left_margin = 20
    lilypond_file.paper_block.right_margin = 15
    lilypond_file.paper_block.markup_system_spacing__basic_distance = 5
    lilypond_file.paper_block.ragged_bottom = False
    lilypond_file.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 8, 0)
    directory = os.path.abspath(os.getcwd())
    fontTree = directory+'/fontTree.ly'
    lilypond_file.file_initial_user_includes.append(fontTree)
    return lilypond_file

def make_piece(clarinet_staff, piano_staff, harp_staff):
    score = format_score(clarinet_staff, piano_staff, harp_staff)
    lilypond_file = make_lilypond_file(score)
    show(lilypond_file)
    
make_piece(clarinet_staff, piano_staff, harp_staff)