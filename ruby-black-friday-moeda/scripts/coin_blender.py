import bpy,math,os
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.resolution_x=480;scene.render.resolution_y=480;scene.render.resolution_percentage=100;scene.render.film_transparent=True
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.fps=30
scene.world.color=(.13,.13,.13)
def mat(name,color,metal=1,rough=.25):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1);n.inputs['Metallic'].default_value=metal;n.inputs['Roughness'].default_value=rough;return m
gold=mat('Liga dourada',(.7,.41,.1));silver=mat('Centro prateado',(.7,.74,.78));ink=mat('Relevo escuro',(.14,.16,.18),.8,.3)
bpy.ops.object.empty_add();root=bpy.context.object

def cyl(radius,depth,z,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=radius,depth=depth,location=(0,0,z));o=bpy.context.object;o.data.materials.append(material);o.parent=root
 bevel=o.modifiers.new('Borda arredondada','BEVEL');bevel.width=.012;bevel.segments=3;o.modifiers.new('Normais','WEIGHTED_NORMAL');return o
cyl(1,.14,0,gold);cyl(.74,.148,0,silver)
for z in [.078,-.078]:
 bpy.ops.mesh.primitive_torus_add(major_radius=.94,minor_radius=.018,major_segments=128,minor_segments=8,location=(0,0,z));o=bpy.context.object;o.data.materials.append(gold);o.parent=root
 for k in range(48):
  a=k*math.tau/48;bpy.ops.mesh.primitive_cube_add(size=1,location=(.845*math.cos(a),.845*math.sin(a),z));o=bpy.context.object;o.scale=(.06,.009,.006);o.rotation_euler.z=a+.45;o.data.materials.append(gold);o.parent=root
font=bpy.data.fonts.load('/workspace/apphacekr/lavai-gravacao-editada/public/fonts/Inter-ExtraBold.ttf')
def txt(body,loc,size,material,back=False):
 cu=bpy.data.curves.new('Gravacao','FONT');cu.body=body;cu.font=font;cu.size=size;cu.align_x='CENTER';cu.extrude=.006;cu.bevel_depth=.002;cu.bevel_resolution=2;o=bpy.data.objects.new(body,cu);bpy.context.collection.objects.link(o);o.location=loc;o.data.materials.append(material);o.parent=root
 if back:o.rotation_euler.y=math.pi
for back,z in [(False,.081),(True,-.081)]:
 txt('1',(0,-.16,z),.94,ink,back);txt('REAL',(0,-.45,z),.26,ink,back);txt('BRASIL',(0,.44,z),.12,ink,back)
# A fixed softbox set gives metallic glints while the coin rotates.
for loc,power,size in [((-3,3,5),650,4),((3,0,3),450,3),((0,-3,2),300,2)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(0,0,7));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=2.65;scene.camera=cam
scene.view_settings.view_transform='AgX'
scene.render.image_settings.color_depth='8'
scene.render.filepath='/workspace/scratch/ruby-moeda/frames/'
for frame in range(60):
 t=frame/59;ease=1-(1-t)**2;root.rotation_euler=(.18*math.sin(math.pi*t),6*math.pi*ease,.12*math.sin(math.pi*t));scene.render.filepath=f'/workspace/scratch/ruby-moeda/frames/{frame:03d}.png';bpy.ops.render.render(write_still=True)
