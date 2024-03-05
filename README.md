# ham_intermod
A webapp to compute intermodulation frequency distortion conflicts, given a list of radio frequencies to be used at an event.

Future Enhancements:
1. For channel plans with backup channels, build an Aggregate Score from the
   accumulated scores of each derivative plan. 
2. After the initial run is complete, automatically tweak frequencies to search
   for a nearby solution with no IMD. Start by tweaking the frequencies with
   the highest hit scores. Tweak them left/right a small amount initially,
   working their way out to further frequencies. This will minimize the number
   of frequencies changed, and also minimize the amount any given frequency
   needs to change.
