import bpy, json
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
s=bpy.context.scene
base=bpy.data.objects['Stationary solid plinth'];cam=s.camera
assert base.animation_data is None and cam.animation_data is None
balls=[o for o in s.objects if o.name.startswith('Steel sphere')]
assert len(balls)==5
max_anchor_error=0.;min_screen_margin=1.
for f in range(1,301):
 s.frame_set(f)
 for ball in balls:
  c=ball.matrix_world.translation
  p=world_to_camera_view(s,cam,c)
  min_screen_margin=min(min_screen_margin,p.x,1-p.x,p.y,1-p.y)
  assert 0.05<p.x<.95 and .05<p.y<.95
  root=ball.parent
  for sign in [-1,1]:
   actual=root.matrix_world@Vector((0,sign*.082,0))
   expected=Vector((root.location.x,sign*.082,.36))
   max_anchor_error=max(max_anchor_error,(actual-expected).length)
assert max_anchor_error<1e-7
result={'frame_count':300,'fps':s.render.fps,'dimensions':[s.render.resolution_x,s.render.resolution_y],'camera_is_stationary':True,'base_is_stationary':True,'sphere_count':len(balls),'maximum_suspension_anchor_displacement_m':max_anchor_error,'minimum_projected_sphere_center_margin':min_screen_margin,'wire_length_preserved_by_rigid_rotation':True}
(Path(__file__).resolve().parents[1]/'output/scene_verification.json').write_text(json.dumps(result,indent=2));print(result)
