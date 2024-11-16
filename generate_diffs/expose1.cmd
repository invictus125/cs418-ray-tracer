magick compare -fuzz 2% ../expose1.png ../correct_outputs/ray-expose1.png expose1_compare.png
magick composite ../expose1.png ../correct_outputs/ray-expose1.png -alpha off -compose difference expose1_rawdiff.png
magick convert expose1_rawdiff.png -level 0%,8% expose1_diff.png
magick convert +append ../correct_outputs/ray-expose1.png ../expose1.png expose1_compare.png expose1_rawdiff.png expose1_diff.png ../expose1_full_diff.png
del expose1_compare.png
del expose1_rawdiff.png
del expose1_diff.png