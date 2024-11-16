magick compare -fuzz 2% ../bulb.png ../correct_outputs/ray-bulb.png bulb_compare.png
magick composite ../bulb.png ../correct_outputs/ray-bulb.png -alpha off -compose difference bulb_rawdiff.png
magick convert bulb_rawdiff.png -level 0%,8% bulb_diff.png
magick convert +append ../correct_outputs/ray-bulb.png ../bulb.png bulb_compare.png bulb_rawdiff.png bulb_diff.png ../bulb_full_diff.png
del bulb_compare.png
del bulb_rawdiff.png
del bulb_diff.png