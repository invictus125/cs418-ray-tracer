magick compare -fuzz 2% ../behind.png ../correct_outputs/ray-behind.png behind_compare.png
magick composite ../behind.png ../correct_outputs/ray-behind.png -alpha off -compose difference behind_rawdiff.png
magick convert behind_rawdiff.png -level 0%,8% behind_diff.png
magick convert +append ../correct_outputs/ray-behind.png ../behind.png behind_compare.png behind_rawdiff.png behind_diff.png ../behind_full_diff.png
del behind_compare.png
del behind_rawdiff.png
del behind_diff.png