import ffmpeg
import subprocess
save_path = "composit_2024y_06m_05d_00h_51m_15s.mp4"
out_path= "composit_2024y_06m_05d_00h_51m_15s .mp4"
ffmpeg.input(save_path).output(out_path, vcodec='libx264', acodec='aac').run( overwrite_output=True)

# command = [
#     'ffmpeg',
#     '-i', input_path,
#     '-vcodec', 'libx264',
#     '-acodec', 'aac',
#     input_path
# ]
# subprocess.run(command, check=True)