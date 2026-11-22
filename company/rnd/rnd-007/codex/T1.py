# Run with Blender 5.1:
# blender --background --python coffee_cup.py

import bpy
import math
from mathutils import Vector

GLB_PATH = r'{{HOME}}\.claude\company\rnd\rnd-007\codex\T1.glb'
PNG_PATH = r'{{HOME}}\.claude\company\rnd\rnd-007\codex\T1.png'

# Blender units are metres. The cup body is 9 cm tall; the full scene
# (including saucer) is slightly taller.
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.render.engine = 'CYCLES'
scene.cycles.samples = 48
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False

def make_material(name, color, roughness, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    return mat

ceramic = make_material('Glossy dark brown ceramic', (0.095, 0.028, 0.012), 0.19)
coffee = make_material('Crema coffee', (0.72, 0.48, 0.25), 0.28)
saucer_mat = make_material('Dark brown saucer ceramic', (0.075, 0.022, 0.01), 0.2)
ground_mat = make_material('Neutral light grey ground', (0.42, 0.42, 0.42), 0.82)

def lathe(name, profile, material, segments=32):
    """Create a rotational mesh from (radius, z) profile points."""
    verts, faces = [], []
    for radius, z in profile:
        for i in range(segments):
            a = 2.0 * math.pi * i / segments
            verts.append((radius * math.cos(a), radius * math.sin(a), z))
    for row in range(len(profile) - 1):
        for i in range(segments):
            a = row * segments + i
            b = row * segments + (i + 1) % segments
            c = (row + 1) * segments + (i + 1) % segments
            d = (row + 1) * segments + i
            faces.append((a, b, c, d))
    faces.append(tuple(range(segments - 1, -1, -1)))
    last = (len(profile) - 1) * segments
    faces.append(tuple(last + i for i in range(segments)))
    mesh = bpy.data.meshes.new(name + ' Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(material)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# Cup is a continuous thick-walled profile: outer base, outside wall,
# rolled rim, inside wall and interior floor.
cup_profile = [
    (0.000, 0.007), (0.029, 0.007), (0.034, 0.010),
    (0.036, 0.016), (0.040, 0.085), (0.041, 0.090),
    (0.040, 0.093), (0.037, 0.093), (0.036, 0.090),
    (0.034, 0.023), (0.031, 0.019), (0.000, 0.019),
]
cup = lathe('Cup body', cup_profile, ceramic, 32)
cup['description'] = 'Low-poly hollow ceramic cup; body height 9 cm'

# Cream surface lies inside the cup, close to its interior wall.
coffee_profile = [
    (0.000, 0.070), (0.0305, 0.070), (0.0325, 0.071),
    (0.0325, 0.072), (0.000, 0.072),
]
lathe('Coffee surface', coffee_profile, coffee, 32)

# Saucer: shallow radial dish with a raised outer lip.
saucer_profile = [
    (0.000, 0.000), (0.050, 0.000), (0.061, 0.002),
    (0.069, 0.006), (0.073, 0.010), (0.072, 0.013),
    (0.068, 0.014), (0.063, 0.010), (0.052, 0.006),
    (0.000, 0.005),
]
lathe('Saucer', saucer_profile, saucer_mat, 40)

# A faceted torus handle on the cup's right side. Its centre is positioned
# so the handle joins the cup wall around the upper and lower thirds.
bpy.ops.mesh.primitive_torus_add(
    major_radius=0.027, minor_radius=0.0055,
    major_segments=20, minor_segments=8,
    location=(0.061, 0.0, 0.052),
    rotation=(math.pi / 2.0, 0.0, 0.0),
)
handle = bpy.context.object
handle.name = 'Cup handle'
handle.data.materials.append(ceramic)

# Bevel the torus shading lightly through flat polygon faces for a low-poly look.
for poly in handle.data.polygons:
    poly.use_smooth = False

# Origin at the bottom centre of the cup body.
cup.location = (0.0, 0.0, 0.0)
bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
bpy.context.view_layer.objects.active = cup
cup.select_set(True)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
cup.select_set(False)

# Ground plane for a soft studio shadow.
bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0.0, 0.0, -0.001))
ground = bpy.context.object
ground.name = 'Ground'
ground.data.materials.append(ground_mat)

# Neutral grey world background.
world = bpy.data.worlds.new('Studio grey world') if not bpy.data.worlds else bpy.data.worlds[0]
scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.42, 0.42, 0.42, 1.0)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.65

def area_light(name, location, energy, size, color=(1.0, 1.0, 1.0)):
    data = bpy.data.lights.new(name, type='AREA')
    data.energy = energy
    data.shape = 'DISK'
    data.size = size
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector((0.0, 0.0, 0.045)) - obj.location).to_track_quat('-Z', 'Y').to_euler()
    return obj

area_light('Large soft key', (0.18, -0.22, 0.28), 22.0, 0.20)
area_light('Soft fill', (-0.18, -0.06, 0.16), 10.0, 0.16)
area_light('Rim light', (0.02, 0.20, 0.22), 18.0, 0.14)

# Three-quarter view, aimed at the cup and saucer.
cam_data = bpy.data.cameras.new('Preview Camera')
camera = bpy.data.objects.new('Preview Camera', cam_data)
bpy.context.collection.objects.link(camera)
camera.location = (0.205, -0.285, 0.205)
target = Vector((0.0, 0.0, 0.047))
camera.rotation_euler = (target - camera.location).to_track_quat('-Z', 'Y').to_euler()
cam_data.type = 'ORTHO'
cam_data.ortho_scale = 0.205
scene.camera = camera

scene.view_settings.view_transform = 'AgX'
scene.render.filepath = PNG_PATH

# Export the scene objects as a binary glTF. Camera and lights are omitted.
bpy.ops.export_scene.gltf(
    filepath=GLB_PATH,
    export_format='GLB',
    export_cameras=False,
    export_lights=False,
    export_animations=False,
)

# Render and save the requested PNG preview.
bpy.ops.render.render(write_still=True)

# Count mesh triangles after triangulating each polygon conceptually.
triangle_count = sum(
    max(0, len(poly.vertices) - 2)
    for obj in scene.objects if obj.type == 'MESH'
    for poly in obj.data.polygons
)
# Report the cup mesh dimensions, whose origin is at its bottom centre.
bpy.context.view_layer.update()
dims = tuple(cup.dimensions)
print(f'Triangle count: {triangle_count}')
print(f'Cup body dimensions (m): X={dims[0]:.4f}, Y={dims[1]:.4f}, Z={dims[2]:.4f}')
