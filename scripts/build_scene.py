import bpy, math, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
(ROOT/'output').mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
S=bpy.context.scene;S.unit_settings.system='METRIC';S.render.engine='CYCLES'
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
S.cycles.device='GPU';S.cycles.samples=40;S.cycles.use_denoising=True;S.cycles.denoiser='OPTIX';S.cycles.max_bounces=8
S.render.resolution_x=1280;S.render.resolution_y=720;S.render.resolution_percentage=100;S.render.fps=30;S.frame_start=1;S.frame_end=300
S.render.image_settings.file_format='PNG';S.render.use_persistent_data=True
S.view_settings.view_transform='AgX';S.view_settings.look='AgX - Medium High Contrast';S.view_settings.exposure=.3
W=bpy.data.worlds.new('Soft daylight');S.world=W;W.use_nodes=True;W.node_tree.nodes['Background'].inputs[0].default_value=(.65,.76,.9,1);W.node_tree.nodes['Background'].inputs[1].default_value=.25

def mat(name,c,metal=0,rough=.4):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
chrome=mat('Polished chrome steel',(.72,.76,.8),1,.095)
satin=mat('Brushed stainless steel',(.5,.55,.59),1,.23)
black=mat('Anodized graphite',(.025,.032,.039),.65,.3)
rubber=mat('Rubber feet',(.012,.014,.015),0,.8)
thread=mat('Fine stainless suspension wire',(.24,.28,.31),.75,.25)
wall=mat('Warm white painted plaster',(.76,.77,.74),0,.87)
white=mat('Ivory ceramic',(.82,.81,.76),0,.22)
navy=mat('Notebook dark blue linen',(.035,.066,.086),0,.9)
paper=mat('Paper edges',(.75,.73,.66),0,.8)
wood=mat('Natural walnut / longitudinal grain',(.28,.12,.05),0,.34)
n=wood.node_tree.nodes;l=wood.node_tree.links;p=n.get('Principled BSDF');tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=3.5;tex.inputs['Detail'].default_value=3;coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(1.2,95,12);l.new(coord.outputs['Generated'],mapping.inputs[0]);l.new(mapping.outputs[0],tex.inputs['Vector']);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.19;ramp.color_ramp.elements[0].color=(.085,.033,.014,1);ramp.color_ramp.elements[1].position=.82;ramp.color_ramp.elements[1].color=(.34,.17,.075,1);l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.00025;l.new(tex.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])

def cube(name,loc,size,material,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material)
 if bevel:m=o.modifiers.new('Soft manufactured edges','BEVEL');m.width=bevel;m.segments=4;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o

def sphere(name,loc,r,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=r,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o

def rod(name,a,b,r,material):
 a,b=Vector(a),Vector(b);delta=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=delta.length,location=(a+b)/2);o=bpy.context.object;o.name=name;o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o

def curve(name,pts,r,material):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=4;s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for p,v in zip(s.points,pts):p.co=(*v,1)
 o=bpy.data.objects.new(name,c);S.collection.objects.link(o);c.materials.append(material);return o

def light(name,loc,target,power,size,color,size_y=None):
 d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);S.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.energy=power;d.shape='RECTANGLE';d.size=size;d.size_y=size_y or size;d.color=color

# Desktop origin is the top surface, with metric-sized real materials.
cube('Walnut desktop',(0,0,-.035),(2.6,1.35,.07),wood,.012)
for x in [-1,1]:cube('Desk leg',(x,.22,-.39),(.055,.7,.72),black,.005)
cube('Office back wall',(0,2.8,1.3),(7,.12,3.5),wall,.01)
cube('Office floor',(0,0,-.79),(9,9,.04),mat('Warm grey floor',(.3,.31,.29),0,.9))
# Large window on the left, visibly subdivided in reflections.
frame=mat('Window frame',(.76,.79,.8),.25,.3)
for y in [-.6,.5,1.6]:cube('Window vertical mullion',(-1.65,y,1.25),(.06,.035,2.5),frame,.006)
for z in [.3,1.2,2.45]:cube('Window horizontal mullion',(-1.65,.5,z),(.06,2.25,.035),frame,.006)
light('Large early afternoon window',(-1.7,.0,1.35),(0,0,.15),190,1.3,(1,.91,.79),2.0)
light('Cool room bounce',(1.2,-.5,1.9),(0,0,.2),65,2,(.78,.87,1))
light('Rear soft daylight',(.2,1.7,1.4),(0,0,.2),95,1.6,(1,.97,.9))
# Restrained office cues outside the primary cradle silhouette.
cube('Notebook pages',(.67,.27,.026),(.27,.35,.036),paper,.006)
cube('Notebook bottom',(.67,.27,.006),(.28,.36,.005),navy,.004)
cube('Notebook cover',(.67,.27,.048),(.28,.36,.007),navy,.004)
rod('Silver pen',(.62,.21,.057),(.69,.40,.057),.004,satin)
# Ceramic cylinder mug with a real hollow interior and dark coffee surface.
pts=[]
profile=[(.038,0),(.042,.008),(.042,.095),(.039,.101),(.035,.097),(.035,.012),(.0,.012)]
verts=[];faces=[]
for r,z in profile:
 for k in range(64):a=2*math.pi*k/64;verts.append((-.64+r*math.cos(a),.38+r*math.sin(a),z+.003))
for j in range(len(profile)-1):
 for k in range(64):faces.append((j*64+k,j*64+(k+1)%64,(j+1)*64+(k+1)%64,(j+1)*64+k))
me=bpy.data.meshes.new('Mug profile');me.from_pydata(verts,[],faces);o=bpy.data.objects.new('Ceramic coffee mug',me);S.collection.objects.link(o);me.materials.append(white)
for p in me.polygons:p.use_smooth=True
curve('Mug handle',[(-.676-.038*math.sin(a),.38,.055+.035*math.cos(a)) for a in [i*math.pi/32 for i in range(33)]],.007,white)
rod('Coffee',(-.64,.38,.077),(-.64,.38,.078),.034,mat('Coffee',(.035,.012,.005),0,.17))
# Distant monitor and a modest shelf establish a clean office.
cube('Monitor body',(.47,1.0,.49),(.7,.055,.41),black,.012)
cube('Monitor glass',(.47,.969,.49),(.666,.003,.377),mat('Sleeping monitor',(.035,.055,.068),.2,.18),.005)
rod('Monitor stand',(.47,1,.04),(.47,1,.31),.024,satin);cube('Monitor foot',(.47,.98,.025),(.25,.19,.018),satin,.009)
cube('Background shelf',(-.9,2.3,.66),(1.1,.35,.045),wood,.01)
for i,col in enumerate([(.27,.34,.34),(.45,.37,.25),(.57,.6,.57),(.18,.23,.27)]):cube('Reference book',(-1.2+i*.105,2.3,.82),(.075,.22,.27+i*.02),mat('Book '+str(i),col),.003)
# Fixed cradle, rubber feet and a machined plinth.
for x in [-.27,.27]:
 for y in [-.085,.085]:rod('Fixed rubber foot',(x,y,.001),(x,y,.012),.017,rubber)
cube('Stationary solid plinth',(0,0,.026),(.65,.25,.033),black,.009)
cube('Brushed plinth inset',(0,0,.044),(.615,.222,.004),satin,.006)
# Two rounded inverted-U steel rails; no part of the frame is animated.
for y in [-.082,.082]:
 pts=[(-.285,y,.047),(-.285,y,.335)]
 for i in range(13):a=math.pi-math.pi/2*i/12;pts.append((-.26+.025*math.cos(a),y,.335+.025*math.sin(a)))
 pts.append((.26,y,.36))
 for i in range(13):a=math.pi/2-math.pi/2*i/12;pts.append((.26+.025*math.cos(a),y,.335+.025*math.sin(a)))
 pts.append((.285,y,.047));curve('Rigid polished support rail',pts,.006,satin)
 for x in [-.285,.285]:rod('Rail foot collar',(x,y,.045),(x,y,.06),.010,chrome)
for x in [-.26,.26]:rod('Frame cross brace',(x,-.082,.36),(x,.082,.36),.004,satin)
# Each rigid assembly rotates around its fixed support axis. All wires retain exact length.
import csv
angles=[[float(x) for x in row] for row in csv.reader(open(ROOT/'output/angles.csv'))]
for i in range(5):
 x=(i-2)*.054;root=bpy.data.objects.new('Pendulum %d | constrained axis'%(i+1),None);S.collection.objects.link(root);root.location=(x,0,.36)
 ball=sphere('Steel sphere %d'%(i+1),(0,0,-.235),.027,chrome);ball.parent=root
 for sign in [-1,1]:
  wire=rod('Taut suspension %d'%i,(0,sign*.082,0),(0,sign*.010,-.211),.00042,thread);wire.parent=root
  collar=sphere('Wire attachment',(0,sign*.010,-.211),.0016,chrome);collar.parent=root
  rod('Fixed wire saddle',(x-.003,sign*.082,.36),(x+.003,sign*.082,.36),.007,black)
 for k,row in enumerate(angles):
  root.rotation_euler[1]=-row[i];root.keyframe_insert(data_path='rotation_euler',index=1,frame=1+k*.25)
 if root.animation_data:
  for fc in root.animation_data.action.fcurves:
   for kp in fc.keyframe_points:kp.interpolation='LINEAR'
# Restrained engraved manufacturer-style label on the front of the base.
labelmat=mat('Subtle etched text',(.45,.5,.52),.7,.4)
c=bpy.data.curves.new('Base inscription','FONT');c.body='N E W T O N';c.size=.009;c.extrude=.00003;c.align_x='CENTER';o=bpy.data.objects.new('Base inscription',c);S.collection.objects.link(o);o.location=(0,-.1254,.023);o.rotation_euler=(math.pi/2,0,0);c.materials.append(labelmat)
bpy.ops.object.camera_add(location=(.64,-1.50,.49));cam=bpy.context.object;cam.name='Locked tripod / tabletop';target=Vector((0,0,.205));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=54;cam.data.sensor_width=36;cam.data.clip_start=.01;cam.data.clip_end=100;cam.data.dof.use_dof=True;cam.data.dof.focus_distance=(target-cam.location).length;cam.data.dof.aperture_fstop=9;S.camera=cam
S.frame_set(25);S.render.filepath=str(ROOT/'output/preview.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'output/newtons_cradle.blend'))
S.cycles.samples=48;bpy.ops.render.render(write_still=True)
