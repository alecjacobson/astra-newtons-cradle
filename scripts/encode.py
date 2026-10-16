from pathlib import Path
import subprocess, imageio_ffmpeg
root=Path(__file__).resolve().parents[1]
f=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([f,'-y','-framerate','30','-start_number','1','-i',str(root/'output/frames/%04d.png'),'-frames:v','300','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(root/'output/newtons_cradle.mp4')],check=True)
