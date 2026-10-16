from pathlib import Path
import time, subprocess, sys, json, shutil, zipfile
import imageio_ffmpeg
root=Path(__file__).resolve().parents[1]
while len(list((root/'output/frames').glob('*.png')))<300:
 time.sleep(10)
time.sleep(2)
subprocess.run([sys.executable,str(root/'scripts/encode.py')],check=True)
video=root/'output/newtons_cradle.mp4'
nframes,seconds=imageio_ffmpeg.count_frames_and_secs(str(video))
reader=imageio_ffmpeg.read_frames(str(video));meta=next(reader);decoded=sum(1 for _ in reader)
assert nframes==decoded==300 and abs(seconds-10)<.01
assert meta['size']==(1920,1080) and meta['fps']==30
report={'frames':decoded,'seconds':seconds,'size':meta['size'],'fps':meta['fps'],'bytes':video.stat().st_size,'all_frames_decoded':True}
(root/'output/video_verification.json').write_text(json.dumps(report,indent=2))
shutil.copy(root/'output/frames/0025.png',root/'output/preview.png')
with zipfile.ZipFile(root/'newtons_cradle_source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in [root/'README.txt',*sorted((root/'scripts').glob('*.py')),root/'output/newtons_cradle.blend',*sorted((root/'output').glob('*.json')),root/'output/angles.csv',root/'output/motion.npz']:
  z.write(p,str(p.relative_to(root)))
print('FINAL_VERIFIED',json.dumps(report),flush=True)
