magick compare -fuzz 2% ../color.png ../correct_outputs/ray-color.png color_compare.png
magick composite ../color.png ../correct_outputs/ray-color.png -alpha off -compose difference color_rawdiff.png
magick convert color_rawdiff.png -level 0%,8% color_diff.png
magick convert +append ../correct_outputs/ray-color.png ../color.png color_compare.png color_rawdiff.png color_diff.png ../color_full_diff.png
del color_compare.png
del color_rawdiff.png
del color_diff.png