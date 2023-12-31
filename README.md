# ham_intermod
A webapp to compute intermodulation frequency distortion conflicts, given a list of radio frequencies to be used at an event.

Future Enhancements:
1. Automatically iterate through backup frequencies. Add "Backup" column to 
   CSV file. Group primary and backup frequencies with a common tag (such as
   "AAA"), so HamIM will automatically cycle through them one at a time rather
   than mixing them together in the same run.
2. After the initial run is complete, automatically tweak frequencies to search
   for a nearby solution with no IMD. Start by tweaking the frequencies with
   the highest hit scores. Tweak them left/right a small amount initially,
   working their way out to further frequencies. This will minimize the number
   of frequencies changed, and also minimize the amount any given frequency
   needs to change.
