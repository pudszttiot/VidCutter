from moviepy.editor import VideoFileClip, clips_array

length = 30

clip1 = VideoFileClip("vid1.mp4").subclip(0, 0 + length)
clip2 = VideoFileClip("vid2.mp4").subclip(0, 0 + length)

combined = clips_array([[clip1, clip2]])

combined.write_videofile("test.mp4")
