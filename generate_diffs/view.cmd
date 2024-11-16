magick compare -fuzz 2% ../view.png ../correct_outputs/ray-view.png view_compare.png
magick composite ../view.png ../correct_outputs/ray-view.png -alpha off -compose difference view_rawdiff.png
magick convert view_rawdiff.png -level 0%,8% view_diff.png
magick convert +append ../correct_outputs/ray-view.png ../view.png view_compare.png view_rawdiff.png view_diff.png ../view_full_diff.png
del view_compare.png
del view_rawdiff.png
del view_diff.png