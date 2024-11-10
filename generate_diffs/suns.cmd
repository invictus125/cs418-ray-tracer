magick compare -fuzz 2% ../suns.png ../correct_outputs/ray-suns.png suns_compare.png
magick composite ../suns.png ../correct_outputs/ray-suns.png -alpha off -compose difference suns_rawdiff.png
magick convert suns_rawdiff.png -level 0%,8% suns_diff.png
magick convert +append ../correct_outputs/ray-suns.png ../suns.png suns_compare.png suns_rawdiff.png suns_diff.png ../suns_full_diff.png
del suns_compare.png
del suns_rawdiff.png
del suns_diff.png