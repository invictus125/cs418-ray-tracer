build:
	echo Done

run:
	python3 ./raytracer.py $(file)

cleanWin:
	del "*_out"
	del "*.png"
