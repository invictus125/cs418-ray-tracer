magick compare -fuzz 2% ../shadow-plane.png ../correct_outputs/ray-shadow-plane.png shadow-plane_compare.png
magick composite ../shadow-plane.png ../correct_outputs/ray-shadow-plane.png -alpha off -compose difference shadow-plane_rawdiff.png
magick convert shadow-plane_rawdiff.png -level 0%,8% shadow-plane_diff.png
magick convert +append ../correct_outputs/ray-shadow-plane.png ../shadow-plane.png shadow-plane_compare.png shadow-plane_rawdiff.png shadow-plane_diff.png ../shadow-plane_full_diff.png
del shadow-plane_compare.png
del shadow-plane_rawdiff.png
del shadow-plane_diff.png