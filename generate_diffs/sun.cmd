magick compare -fuzz 2% ../sun.png ../correct_outputs/ray-sun.png sun_compare.png
magick composite ../sun.png ../correct_outputs/ray-sun.png -alpha off -compose difference sun_rawdiff.png
magick convert sun_rawdiff.png -level 0%,8% sun_diff.png
magick convert +append ../correct_outputs/ray-sun.png ../sun.png sun_compare.png sun_rawdiff.png sun_diff.png ../sun_full_diff.png
del sun_compare.png
del sun_rawdiff.png
del sun_diff.png