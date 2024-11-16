magick compare -fuzz 2% ../shadow-bulb.png ../correct_outputs/ray-shadow-bulb.png shadow-bulb_compare.png
magick composite ../shadow-bulb.png ../correct_outputs/ray-shadow-bulb.png -alpha off -compose difference shadow-bulb_rawdiff.png
magick convert shadow-bulb_rawdiff.png -level 0%,8% shadow-bulb_diff.png
magick convert +append ../correct_outputs/ray-shadow-bulb.png ../shadow-bulb.png shadow-bulb_compare.png shadow-bulb_rawdiff.png shadow-bulb_diff.png ../shadow-bulb_full_diff.png
del shadow-bulb_compare.png
del shadow-bulb_rawdiff.png
del shadow-bulb_diff.png