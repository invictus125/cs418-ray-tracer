magick compare -fuzz 2% ../sphere.png ../correct_outputs/ray-sphere.png sphere_compare.png
magick composite ../sphere.png ../correct_outputs/ray-sphere.png -alpha off -compose difference sphere_rawdiff.png
magick convert sphere_rawdiff.png -level 0%,8% sphere_diff.png
magick convert +append ../correct_outputs/ray-sphere.png ../sphere.png sphere_compare.png sphere_rawdiff.png sphere_diff.png ../sphere_full_diff.png
del sphere_compare.png
del sphere_rawdiff.png
del sphere_diff.png