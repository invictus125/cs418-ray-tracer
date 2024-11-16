magick compare -fuzz 2% ../tri.png ../correct_outputs/ray-tri.png tri_compare.png
magick composite ../tri.png ../correct_outputs/ray-tri.png -alpha off -compose difference tri_rawdiff.png
magick convert tri_rawdiff.png -level 0%,8% tri_diff.png
magick convert +append ../correct_outputs/ray-tri.png ../tri.png tri_compare.png tri_rawdiff.png tri_diff.png ../tri_full_diff.png
del tri_compare.png
del tri_rawdiff.png
del tri_diff.png