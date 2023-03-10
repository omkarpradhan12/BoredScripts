from winsound import Beep

key = {
   'B':3951,
   'E':2637,
   'G':3135,
   'F#':2959,
   'A':3520,
   'D#':2489,
   'F':2793,
   'D':2349,
   'C':2093,
   'C#':2217,
   'A#':3729
}

for i in "B E G F# E B A F#".split():
    Beep(key[i],500)

for i in "E G F# D# F B G B".split():
    Beep(key[i],500)

for i in "B E G F# E".split():
    Beep(key[i],500)

for i in "B D C# C".split():
    Beep(key[i],500)

for i in "A C B A# A# G E".split():
    Beep(key[i],500)
    
for i in "G B G B G C B A#".split():
    Beep(key[i],500)
    
for i in "F# G B A# A# B B".split():
    Beep(key[i],500)

for i in "G B G B G D D# C".split():
    Beep(key[i],500)

for i in "A C B A# A# G E".split():
    Beep(key[i],500)
    


