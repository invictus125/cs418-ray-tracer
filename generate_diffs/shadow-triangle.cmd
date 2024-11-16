magick compare -fuzz 2% ../shadow-triangle.png ../correct_outputs/ray-shadow-triangle.png shadow-triangle_compare.png
magick composite ../shadow-triangle.png ../correct_outputs/ray-shadow-triangle.png -alpha off -compose difference shadow-triangle_rawdiff.png
magick convert shadow-triangle_rawdiff.png -level 0%,8% shadow-triangle_diff.png
magick convert +append ../correct_outputs/ray-shadow-triangle.png ../shadow-triangle.png shadow-triangle_compare.png shadow-triangle_rawdiff.png shadow-triangle_diff.png ../shadow-triangle_full_diff.png
del shadow-triangle_compare.png
del shadow-triangle_rawdiff.png
del shadow-triangle_diff.png