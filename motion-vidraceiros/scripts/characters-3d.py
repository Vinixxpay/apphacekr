import bpy,math,os
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'public/characters';OUT.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=False
scene.render.resolution_x=850;scene.render.resolution_y=670;scene.render.resolution_percentage=100
scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.render.threads_mode='FIXED';scene.render.threads=4
scene.world.color=(.035,.045,.07)
def mat(name,color,metal=0,rough=.35):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
blue=mat('iB electric blue',(.015,.22,.8),.35);navy=mat('Navy',(.009,.026,.09),.15);skin=mat('Warm porcelain',(.62,.36,.22));white=mat('Pearl',(.7,.85,.95),.2);hair=mat('Hair',(.018,.012,.013));gold=mat('Opportunity',(.1,.65,1),.7);black=mat('Screen',(.001,.005,.016),.3)
def uv(name,loc,scale,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(m);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for p in o.data.polygons:p.use_smooth=True
 return o
def cube(name,loc,scale,m,bevel=.1):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 mod=o.modifiers.new('Soft edges','BEVEL');mod.width=bevel;mod.segments=4;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o
def limb(name,a,b,r,m):
 d=Vector(b)-Vector(a);mid=(Vector(a)+Vector(b))/2;bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=mid);o=bpy.context.object;o.name=name;o.scale=(r,r,d.length/2+r*.45);o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(m)
 for p in o.data.polygons:p.use_smooth=True
 return o
people=[]
def person(x,y,s,shirt,hat=False):
 start=set(bpy.data.objects);z=.12
 def P(v):return(x+v[0]*s,y+v[1]*s,z+v[2]*s)
 uv('Torso',P((0,0,1.25)),(.42*s,.25*s,.54*s),shirt)
 for side in [-1,1]:
  limb('Trouser',P((side*.19,0,.93)),P((side*.2,-.01,.27)),.155*s,navy);uv('Shoe',P((side*.2,-.12,.14)),(.18*s,.31*s,.14*s),white)
  limb('Sleeve',P((side*.36,0,1.5)),P((side*.53,-.04,1.05)),.145*s,shirt)
  limb('Forearm',P((side*.53,-.04,1.05)),P((side*.35,-.34,1.05 if side==1 else .9)),.10*s,skin)
 uv('Head',P((0,-.015,2)),(.3*s,.27*s,.36*s),skin);uv('Hair',P((0,.02,2.23)),(.31*s,.27*s,.17*s),hair)
 for side in [-1,1]:uv('Eye',P((side*.103,-.26,2.04)),(.028*s,.025*s,.038*s),black)
 uv('Nose',P((0,-.28,1.96)),(.055*s,.065*s,.055*s),skin)
 if hat:uv('Worker cap',P((0,-.02,2.27)),(.34*s,.29*s,.17*s),blue);cube('Visor',P((0,-.28,2.23)),(.59*s,.29*s,.045*s),blue,.02)
 cube('Phone',P((.31,-.43,1.17)),(.23*s,.055*s,.4*s),navy,.035);cube('Phone screen',P((.31,-.466,1.17)),(.18*s,.012*s,.31*s),gold,.015)
 group=list(set(bpy.data.objects)-start);people.append(group)
person(0,-.45,1.25,blue,True);person(-1.65,.45,.91,white);person(1.65,.5,.96,navy)
for x,y,r in [(0,-.3,1),(-1.65,.45,.7),(1.65,.5,.72)]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=.16,location=(x,y,.05));o=bpy.context.object;o.data.materials.append(navy);be=o.modifiers.new('Rounded stage','BEVEL');be.width=.07;be.segments=3
 bpy.ops.mesh.primitive_torus_add(major_radius=r*.93,minor_radius=.018,major_segments=64,minor_segments=12,location=(x,y,.15));bpy.context.object.data.materials.append(gold)
# Floating glass panes behind the cast.
for i in [-1,1]:
 o=cube('Glass billboard',(i*1.45,1.1,1.65),(1.35,.08,2.6),blue,.14);o.rotation_euler[2]=i*.2
 for j in range(3):cube('Billboard graphic',(i*1.45,1.03,1.1+j*.4),(.8-j*.12,.025,.055),white,.02)
# Lighting: warm key, strong blue rim and soft fill.
def area(name,loc,power,color,size):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.color=color;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1.4))-o.location).to_track_quat('-Z','Y').to_euler()
area('Soft key',(-3,-5,7),1000,(.72,.86,1),5);area('Blue rim',(4,3,5),1500,(.04,.32,1),3);area('Warm fill',(3,-4,3),550,(1,.8,.62),4)
bpy.ops.object.camera_add(location=(4,-10,6));cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=6.35
cam.rotation_euler=(Vector((0,0,1.35))-cam.location).to_track_quat('-Z','Y').to_euler();scene.view_settings.view_transform='AgX'
# Six rendered angles form a smooth animated turn inside Remotion.
count=int(os.environ.get('IB_3D_FRAMES','12'))
for f in range(count):
 angle=2*math.pi*f/count
 cam.location=(2.5+math.sin(angle)*.65,-10,5.4+math.cos(angle)*.15);cam.rotation_euler=(Vector((0,0,1.35))-cam.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(OUT/f'{f:02}.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'out/characters.blend'))
