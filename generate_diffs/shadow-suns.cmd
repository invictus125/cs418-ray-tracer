magick compare -fuzz 2% ../shadow-suns.png ../correct_outputs/ray-shadow-suns.png shadow-suns_compare.png
magick composite ../shadow-suns.png ../correct_outputs/ray-shadow-suns.png -alpha off -compose difference shadow-suns_rawdiff.png
magick convert shadow-suns_rawdiff.png -level 0%,8% shadow-suns_diff.png
magick convert +append ../correct_outputs/ray-shadow-suns.png ../shadow-suns.png shadow-suns_compare.png shadow-suns_rawdiff.png shadow-suns_diff.png ../shadow-suns_full_diff.png
del shadow-suns_compare.png
del shadow-suns_rawdiff.png
del shadow-suns_diff.png