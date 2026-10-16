import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
(ROOT/'output/frames').mkdir(parents=True, exist_ok=True)
S=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
S.cycles.device='GPU';S.cycles.samples=64;S.cycles.adaptive_threshold=.025;S.cycles.denoiser='OPTIX';S.cycles.use_denoising=True
S.render.resolution_x=1920;S.render.resolution_y=1080;S.render.resolution_percentage=100;S.render.fps=30;S.render.use_persistent_data=True
S.frame_set(1);S.render.filepath='//frames/';bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'output/newtons_cradle.blend'))
for f in range(1,301):
 path=ROOT/'output/frames'/f'{f:04d}.png'
 if path.exists():continue
 S.frame_set(f);S.render.filepath=str(path);bpy.ops.render.render(write_still=True)
print('RENDER_COMPLETE',flush=True)
