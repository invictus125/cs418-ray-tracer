magick compare -fuzz 2% ../overlap.png ../correct_outputs/ray-overlap.png overlap_compare.png
magick composite ../overlap.png ../correct_outputs/ray-overlap.png -alpha off -compose difference overlap_rawdiff.png
magick convert overlap_rawdiff.png -level 0%,8% overlap_diff.png
magick convert +append ../correct_outputs/ray-overlap.png ../overlap.png overlap_compare.png overlap_rawdiff.png overlap_diff.png ../overlap_full_diff.png
del overlap_compare.png
del overlap_rawdiff.png
del overlap_diff.png