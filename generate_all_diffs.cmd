make run file=test_input/ray-behind.txt > behind_out
make run file=test_input/ray-color.txt > color_out
make run file=test_input/ray-expose1.txt > expose1_out
make run file=test_input/ray-expose2.txt > expose2_out
make run file=test_input/ray-overlap.txt > overlap_out
make run file=test_input/ray-shadow-basic.txt > shadow-basic_out
make run file=test_input/ray-shadow-suns.txt > shadow-suns_out
make run file=test_input/ray-sphere.txt > sphere_out
make run file=test_input/ray-sun.txt > sun_out
make run file=test_input/ray-suns.txt > suns_out
make run file=test_input/ray-view.txt > view_out
make run file=test_input/ray-bulb.txt > bulb_out
make run file=test_input/ray-shadow-bulb.txt > shadow-bulb_out

cd generate_diffs

start cmd.exe /C behind.cmd
start cmd.exe /C color.cmd
start cmd.exe /C expose1.cmd
start cmd.exe /C expose2.cmd
start cmd.exe /C overlap.cmd
start cmd.exe /C shadow-basic.cmd
start cmd.exe /C shadow-suns.cmd
start cmd.exe /C sphere.cmd
start cmd.exe /C sun.cmd
start cmd.exe /C suns.cmd
start cmd.exe /C view.cmd
start cmd.exe /C bulb.cmd
start cmd.exe /C shadow-bulb.cmd

cd ..
