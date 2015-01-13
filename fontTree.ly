date = #(strftime "%d-%m-%Y" (localtime (current-time)))
\header {
     title = \markup {
         \override #'(font-name . "Futura")
         "The World All Around"

     }
     
     subtitle = \markup {
     	\override #'(font-name . "Futura")
     	\date}
     
     opus = \markup {
         \override #'(font-name . "Futura")
         "Jeff Treviño"
     }
     tagline = \markup {
         \override #'(font-name . "Futura")
         \fontsize #-3.5
         {
             Engraved on \date using \with-url #"http://lilypond.org/"
             { LilyPond \simple #(lilypond-version) (http://lilypond.org/) }
         } 
     }
}

\paper  {
  myStaffSize = #16
  #(define fonts
    (make-pango-font-tree "Futura"
                          "Futura"
                          "Futura"
                           (/ myStaffSize 16)))
}
