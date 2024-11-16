magick compare -fuzz 2% ../plane.png ../correct_outputs/ray-plane.png plane_compare.png
magick composite ../plane.png ../correct_outputs/ray-plane.png -alpha off -compose difference plane_rawdiff.png
magick convert plane_rawdiff.png -level 0%,8% plane_diff.png
magick convert +append ../correct_outputs/ray-plane.png ../plane.png plane_compare.png plane_rawdiff.png plane_diff.png ../plane_full_diff.png
del plane_compare.png
del plane_rawdiff.png
del plane_diff.png