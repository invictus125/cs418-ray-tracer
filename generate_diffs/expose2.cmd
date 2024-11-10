magick compare -fuzz 2% ../expose2.png ../correct_outputs/ray-expose2.png expose2_compare.png
magick composite ../expose2.png ../correct_outputs/ray-expose2.png -alpha off -compose difference expose2_rawdiff.png
magick convert expose2_rawdiff.png -level 0%,8% expose2_diff.png
magick convert +append ../correct_outputs/ray-expose2.png ../expose2.png expose2_compare.png expose2_rawdiff.png expose2_diff.png ../expose2_full_diff.png
del expose2_compare.png
del expose2_rawdiff.png
del expose2_diff.png