magick compare -fuzz 2% ../shadow-basic.png ../correct_outputs/ray-shadow-basic.png shadow-basic_compare.png
magick composite ../shadow-basic.png ../correct_outputs/ray-shadow-basic.png -alpha off -compose difference shadow-basic_rawdiff.png
magick convert shadow-basic_rawdiff.png -level 0%,8% shadow-basic_diff.png
magick convert +append ../correct_outputs/ray-shadow-basic.png ../shadow-basic.png shadow-basic_compare.png shadow-basic_rawdiff.png shadow-basic_diff.png ../shadow-basic_full_diff.png
del shadow-basic_compare.png
del shadow-basic_rawdiff.png
del shadow-basic_diff.png