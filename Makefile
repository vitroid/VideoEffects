%.mp4: %.avi
	ffmpeg -i $< -pix_fmt yuv420p $@
