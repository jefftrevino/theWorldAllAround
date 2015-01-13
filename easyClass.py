import copy
from abjad.tools.abctools import AbjadObject

class WoodwindDiagram(AbjadObject):
    def __init__(self, instrument_name, center_column=None, left_hand=None, right_hand=None):
        self._instrument_name = instrument_name
        if center_column == None:
            self._center_column = []
        else:
            self._center_column = center_column
        if left_hand == None:
            self._left_hand = []
        else:
            self._left_hand = left_hand
        if right_hand == None:
            self._right_hand = []
        else:
            self._right_hand = right_hand
            
    def __repr__(self):
        return self._make_woodwind_diagram_markup_command().lilypond_format
    
    ### SPECIAL METHODS ###    
    
    def _make_woodwind_diagram_markup_command(self):
        key_groups_as_scheme = [ ]
        schemed_cc_list = schemetools.Scheme(self._center_column[:])
        schemed_lh_list = schemetools.Scheme(self._left_hand[:])
        schemed_rh_list = schemetools.Scheme(self._right_hand[:])
        if self._center_column:
            cc_scheme_pair = schemetools.SchemePair('cc', schemed_cc_list)
            key_groups_as_scheme.append( cc_scheme_pair)
        else:
            cc_scheme_pair = schemetools.SchemePair('cc', ())
            key_groups_as_scheme.append( cc_scheme_pair)
        if self._left_hand:
            lh_scheme_pair = schemetools.SchemePair('lh', schemed_lh_list)
            key_groups_as_scheme.append( lh_scheme_pair)
        else:
            lh_scheme_pair = schemetools.SchemePair('lh', ())
            key_groups_as_scheme.append( lh_scheme_pair)
        if self._right_hand:
            rh_scheme_pair = schemetools.SchemePair('rh', schemed_rh_list)
            key_groups_as_scheme.append( rh_scheme_pair)
        else:
            rh_scheme_pair = schemetools.SchemePair('rh', ())
            key_groups_as_scheme.append( rh_scheme_pair)
        key_groups_as_scheme = schemetools.Scheme(key_groups_as_scheme[:], quoting="'")
        instrument_as_scheme = schemetools.Scheme(self._instrument_name, quoting = "'")
        return markuptools.MarkupCommand('woodwind-diagram', instrument_as_scheme, key_groups_as_scheme)
    
    def _print_guide(self):
        if self._instrument_name == 'clarinet':
            print("list of valid key strings for clarinet:\npossibilities for one:\n(one oneT one1qT oneT1q one1q one1qT1h one1hT1q one1qT3q one3qT1q one1qTF oneFT1q one1hT oneT1h one1h one1hT3q one3qT1h one1hTF oneFT1h one3qT oneT3q one3q one3qTF oneFT3q oneFT oneF)\npossibilities for two:\n(two twoT two1qT twoT1q two1q two1qT1h two1hT1q two1qT3q two3qT1q two1qTF twoFT1q two1hT twoT1h two1h two1hT3q two3qT1h two1hTF twoFT1h two3qT twoT3q two3q two3qTF twoFT3q twoFT twoF)\npossibilities for three:\n(three threeT three1qT threeT1q three1q three1qT1h three1hT1q three1qT3q three3qT1q three1qTF threeFT1q three1hT threeT1h three1h three1hT3q three3qT1h three1hTF threeFT1h three3qT threeT3q three3q three3qTF threeFT3q threeFT threeF)\npossibilities for four:\n(four fourT four1qT fourT1q four1q four1qT1h four1hT1q four1qT3q four3qT1q four1qTF fourFT1q four1hT fourT1h four1h four1hT3q four3qT1h four1hTF fourFT1h four3qT fourT3q four3q four3qTF fourFT3q fourFT fourF)\npossibilities for five:\n(five fiveT five1qT fiveT1q five1q five1qT1h five1hT1q five1qT3q five3qT1q five1qTF fiveFT1q five1hT fiveT1h five1h five1hT3q five3qT1h five1hTF fiveFT1h five3qT fiveT3q five3q five3qTF fiveFT3q fiveFT fiveF)\npossibilities for six:\n(six sixT six1qT sixT1q six1q six1qT1h six1hT1q six1qT3q six3qT1q six1qTF sixFT1q six1hT sixT1h six1h six1hT3q six3qT1h six1hTF sixFT1h six3qT sixT3q six3q six3qTF sixFT3q sixFT sixF)\npossibilities for h:\n(h hT h1qT hT1q h1q h1qT1h h1hT1q h1qT3q h3qT1q h1qTF hFT1q h1hT hT1h h1h h1hT3q h3qT1h h1hTF hFT1h h3qT hT3q h3q h3qTF hFT3q hFT hF)\nlh\npossibilities for thumb:\n(thumb thumbT)\npossibilities for R:\n(R RT)\npossibilities for a:\n(a aT)\npossibilities for gis:\n(gis gisT)\npossibilities for ees:\n(ees eesT)\npossibilities for cis:\n(cis cisT)\npossibilities for f:\n(f fT)\npossibilities for e:\n(e eT)\npossibilities for fis:\n(fis fisT)\nrh\npossibilities for one:\n(one oneT)\npossibilities for two:\n(two twoT)\npossibilities for three:\n(three threeT)\npossibilities for four:\n(four fourT)\npossibilities for b:\n(b bT)\npossibilities for fis:\n(fis fisT)\npossibilities for gis:\n(gis gisT)\npossibilities for e:\n(e eT)\npossibilities for f:\n(f fT)")
            print("\n   diagram syntax\n\n   Lilypond woodwind diagram syntax divides an instrument into keyholes and keys.\n   Keyholes belong to the central column (cc) group.\n   Keys belong to either left-hand (lh) or right-hand (rh) groups.\n   In Abjad's diagrams, central column (cc) keyholes appear along a central dotted line.\n   Keys are grouped relative to the presence or absence of a dividing horizontal line:\n   If a horizontal line divides a side of the diagram, keys above the line are left-hand keys (lh)\n   and those below are right-hand keys (rh).\n   If no horizontal line appears, all keys on that side of the diagram are left-hand keys (lh).\n   A key located along the central dotted line will be grouped according to the playing hand of the nearest keyhole fingers.")
            print("\n   To draw half- or quarter-covered keys, and to draw trills,\n   refer to the comprehensive list of possible key strings that precedes this explanation.")
            print ("\n\n             a  gis\n    R        |\n            one\n    thumb    h\n            two\n             |  ees\n --------- three\n             |\n         one | cis\n         two |    f\n       three | e\n        four |    fis\n             |\n            four\n             |\n            five\n           b |\n            six\n      fis    |\n         gis |\n      e      |\n          f  |")
            print("\n   clarinet\n   as modeled in LilyPond by Mike Solomon\n   diagram explanation and key string index above\n")
    
    ### PUBLIC PROPERTIES ###
    
    @property
    def lilypond_format(self):
        return self._make_woodwind_diagram_markup_command().lilypond_format
    
    @property
    def print_guide(self):
        return self._print_guide()
    
    @property
    def instrument_name(self):
        return self._instrument_name
        
    @property
    def center_column(self):
        return self._center_column
    
    @property
    def left_hand(self):
        return self._left_hand
    
    @property
    def right_hand(self):
        return self._right_hand