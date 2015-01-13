#This models Lilypond's woodwind fingering interface.

#, First, a "key" class details the location and name of a key. location is always cc, lh, or rh (center column, left hand, or right hand). Key names depend on instruments.

class WoodwindFingering():
    """Model of a Lilypond woodwind fingering (three optional key_string lists grouped into three key groups: cc, lh, and rh) ."""
    def __init__(self, _instrument, cc = [ ], lh = [ ], rh = [ ], graphical = True, size = 1, thickness = 1 ):
        from abjad.tools import markuptools
        self.instrument = _instrument
        self.key_groups = [ ]
        if cc:
            self.cc = cc
            self.key_groups.append( cc.insert(0,'cc')  )
        if lh:
            self.lh = lh
            self.key_groups.append( cc.insert(0,'lh')  )
        if rh:
            self.rh = rh
            self.key_groups.append( cc.insert(0,'lh')  )
        
        self.lilypond_format = "
        
        #formattted_keys = ( formatted_keys[:-1] + ")" )
        #self.lilypond_format = '(' + self.group + ' . ' + formatted_keys
            
