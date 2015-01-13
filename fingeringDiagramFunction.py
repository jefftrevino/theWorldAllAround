from abjad import *
def make_woodwind_diagram_markup_command(instrument, cc = [], lh = [], rh = []):
    key_groups_as_scheme = [ ]
    schemed_cc_list = schemetools.Scheme(cc[:])
    schemed_lh_list = schemetools.Scheme(lh[:])
    schemed_rh_list = schemetools.Scheme(rh[:])
    if cc:
        cc_scheme_pair = schemetools.SchemePair('cc', schemed_cc_list)
        key_groups_as_scheme.append( cc_scheme_pair)
    else:
        cc_scheme_pair = schemetools.SchemePair('cc', ())
        key_groups_as_scheme.append( cc_scheme_pair)
    if lh:
        lh_scheme_pair = schemetools.SchemePair('lh', schemed_lh_list)
        key_groups_as_scheme.append( lh_scheme_pair)
    else:
        lh_scheme_pair = schemetools.SchemePair('lh', ())
        key_groups_as_scheme.append( lh_scheme_pair)
    if rh:
        rh_scheme_pair = schemetools.SchemePair('rh', schemed_rh_list)
        key_groups_as_scheme.append( rh_scheme_pair)
    else:
        rh_scheme_pair = schemetools.SchemePair('rh', ())
        key_groups_as_scheme.append( rh_scheme_pair)
    print key_groups_as_scheme
    key_groups_as_scheme = schemetools.Scheme(key_groups_as_scheme[:], quoting="'")
    instrument_as_scheme = schemetools.Scheme(instrument, quoting = "'")
    return markuptools.MarkupCommand('woodwind-diagram', instrument_as_scheme, key_groups_as_scheme).lilypond_format
    
staff = Staff("c'")
diagram = make_woodwind_diagram_markup_command('clarinet', cc=['one', 'two', 'five'], lh=['ees', 'fis', 'e'], rh=['two', 'three', 'b', 'gis'] )
markup = markuptools.Markup(diagram, direction=Up)
markup.attach(staff[0])
show(staff)
    

