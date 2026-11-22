import math
import os
import bpy
import bmesh
from mathutils import Vector

GLB = r'{{HOME}}\.claude\company\rnd\rnd-007\agy\T1.glb'
PNG = r'{{HOME}}\.claude\company\rnd\rnd-007\agy\T1.png'


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    return scene


def make_principled_material(
    name,
    base_color,
    roughness,
    ior=1.5,
    specular=0.5,
    coat_weight=0.0,
    coat_roughness=0.05,
):
    mat = bpy.data.materials.new(name=name)
    if hasattr(mat, "use_nodes") and not mat.use_nodes:
        mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = base_color
    bsdf.inputs["Roughness"].default_value = roughness

    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = ior
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = specular
    elif "Specular" in bsdf.inputs:
        bsdf.inputs["Specular"].default_value = specular
    if "Coat Weight" in bsdf.inputs:
        bsdf.inputs["Coat Weight"].default_value = coat_weight
    if "Coat Roughness" in bsdf.inputs:
        bsdf.inputs["Coat Roughness"].default_value = coat_roughness

    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def add_lathe_part(bm, profile, steps, mat_index, closed_shell=True):
    """Build a revolved mesh section from (radius, z) profile points."""
    rings = []
    for r, z in profile:
        if r <= 1e-7:
            rings.append([bm.verts.new((0.0, 0.0, z))])
        else:
            ring = []
            for i in range(steps):
                angle = 2.0 * math.pi * i / steps
                ring.append(
                    bm.verts.new((r * math.cos(angle), r * math.sin(angle), z))
                )
            rings.append(ring)

    new_faces = []
    for idx in range(len(rings) - 1):
        row0 = rings[idx]
        row1 = rings[idx + 1]
        if len(row0) == 1 and len(row1) == steps:
            v0 = row0[0]
            for i in range(steps):
                v1 = row1[i]
                v2 = row1[(i + 1) % steps]
                f = bm.faces.new((v0, v1, v2))
                f.material_index = mat_index
                f.smooth = True
                new_faces.append(f)
        elif len(row0) == steps and len(row1) == 1:
            v1 = row1[0]
            for i in range(steps):
                v0 = row0[i]
                v2 = row0[(i + 1) % steps]
                f = bm.faces.new((v0, v1, v2))
                f.material_index = mat_index
                f.smooth = True
                new_faces.append(f)
        elif len(row0) == steps and len(row1) == steps:
            for i in range(steps):
                i_next = (i + 1) % steps
                f = bm.faces.new((row0[i], row0[i_next], row1[i_next], row1[i]))
                f.material_index = mat_index
                f.smooth = True
                new_faces.append(f)

    if closed_shell and new_faces:
        bmesh.ops.recalc_face_normals(bm, faces=new_faces)
    return new_faces


def cubic_bezier(p0, p1, p2, p3, t):
    u = 1.0 - t
    return (
        (u ** 3) * p0
        + 3.0 * (u ** 2) * t * p1
        + 3.0 * u * (t ** 2) * p2
        + (t ** 3) * p3
    )


def cubic_bezier_tangent(p0, p1, p2, p3, t):
    u = 1.0 - t
    return (
        3.0 * (u ** 2) * (p1 - p0)
        + 6.0 * u * t * (p2 - p1)
        + 3.0 * (t ** 2) * (p3 - p2)
    ).normalized()


def add_handle(bm, mat_index, path_steps=14, ring_steps=10):
    """Sweep an oval handle along a cubic Bezier in the XZ plane."""
    p0 = Vector((0.0398, 0.0, 0.0770))
    p1 = Vector((0.0760, 0.0, 0.0830))
    p2 = Vector((0.0740, 0.0, 0.0300))
    p3 = Vector((0.0325, 0.0, 0.0280))

    binormal = Vector((0.0, 1.0, 0.0))
    rx = 0.0034  # half-thickness in profile plane
    ry = 0.0050  # half-width across Y

    rings = []
    for s in range(path_steps + 1):
        t = s / path_steps
        center = cubic_bezier(p0, p1, p2, p3, t)
        tangent = cubic_bezier_tangent(p0, p1, p2, p3, t)
        normal = binormal.cross(tangent).normalized()

        ring = []
        for k in range(ring_steps):
            theta = 2.0 * math.pi * k / ring_steps
            pos = (
                center
                + (math.cos(theta) * rx) * normal
                + (math.sin(theta) * ry) * binormal
            )
            ring.append(bm.verts.new(pos))
        rings.append(ring)

    new_faces = []
    for s in range(path_steps):
        r0 = rings[s]
        r1 = rings[s + 1]
        for k in range(ring_steps):
            k_next = (k + 1) % ring_steps
            f = bm.faces.new((r0[k], r1[k], r1[k_next], r0[k_next]))
            f.material_index = mat_index
            f.smooth = True
            new_faces.append(f)

    start_cap = bm.faces.new(list(reversed(rings[0])))
    start_cap.material_index = mat_index
    start_cap.smooth = False
    new_faces.append(start_cap)

    end_cap = bm.faces.new(rings[-1])
    end_cap.material_index = mat_index
    end_cap.smooth = False
    new_faces.append(end_cap)

    bmesh.ops.recalc_face_normals(bm, faces=new_faces)
    return new_faces


def build_coffee_cup_asset(scene):
    ceramic_mat = make_principled_material(
        name="DarkBrownCeramic",
        base_color=(0.055, 0.020, 0.008, 1.0),
        roughness=0.10,
        ior=1.52,
        specular=0.60,
        coat_weight=0.30,
        coat_roughness=0.05,
    )
    coffee_mat = make_principled_material(
        name="CreamCoffee",
        base_color=(0.680, 0.480, 0.280, 1.0),
        roughness=0.18,
        ior=1.34,
        specular=0.50,
    )

    radial_steps = 32
    bm = bmesh.new()

    # Saucer profile: foot rests at z=0.000, well floor at z=0.005, radius 7.25 cm
    saucer_profile = [
        (0.0000, 0.0025),
        (0.0260, 0.0020),
        (0.0320, 0.0000),
        (0.0370, 0.0000),
        (0.0520, 0.0045),
        (0.0660, 0.0110),
        (0.0720, 0.0160),
        (0.0725, 0.0180),
        (0.0705, 0.0190),
        (0.0560, 0.0135),
        (0.0360, 0.0075),
        (0.0300, 0.0052),
        (0.0000, 0.0050),
    ]
    add_lathe_part(bm, saucer_profile, radial_steps, mat_index=0, closed_shell=True)

    # Cup profile: base at z=0.0050, rim at z=0.0952 (cup height = 9.02 cm)
    cup_profile = [
        (0.0000, 0.0050),
        (0.0220, 0.0050),
        (0.0250, 0.0050),
        (0.0270, 0.0090),
        (0.0340, 0.0250),
        (0.0390, 0.0480),
        (0.0415, 0.0720),
        (0.0430, 0.0920),
        (0.0428, 0.0942),
        (0.0410, 0.0952),
        (0.0388, 0.0942),
        (0.0380, 0.0900),
        (0.0365, 0.0700),
        (0.0335, 0.0450),
        (0.0275, 0.0220),
        (0.0210, 0.0130),
        (0.0000, 0.0120),
    ]
    add_lathe_part(bm, cup_profile, radial_steps, mat_index=0, closed_shell=True)

    # Handle on +X side
    add_handle(bm, mat_index=0, path_steps=14, ring_steps=10)

    # Cream coffee surface inside the cup (outward winding gives +Z normals)
    coffee_profile = [
        (0.0000, 0.0810),
        (0.0150, 0.0810),
        (0.0280, 0.0810),
        (0.0355, 0.0812),
        (0.0382, 0.0820),
    ]
    # Reverse profile so add_lathe_part quad/tri winding faces +Z upward
    add_lathe_part(
        bm,
        list(reversed(coffee_profile)),
        radial_steps,
        mat_index=1,
        closed_shell=False,
    )

    mesh = bpy.data.meshes.new("CoffeeCupSetMesh")
    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(ceramic_mat)
    mesh.materials.append(coffee_mat)
    mesh.update()

    obj = bpy.data.objects.new("CoffeeCupSet", mesh)
    scene.collection.objects.link(obj)
    obj.location = (0.0, 0.0, 0.0)
    return obj


def setup_world(scene):
    world = bpy.data.worlds.new("StudioWorld")
    scene.world = world
    if hasattr(world, "use_nodes") and not world.use_nodes:
        world.use_nodes = True

    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()

    w_out = nodes.new("ShaderNodeOutputWorld")
    w_mix = nodes.new("ShaderNodeMixShader")

    bg_cam = nodes.new("ShaderNodeBackground")
    bg_cam.inputs["Color"].default_value = (0.52, 0.52, 0.52, 1.0)
    bg_cam.inputs["Strength"].default_value = 1.0

    bg_env = nodes.new("ShaderNodeBackground")
    bg_env.inputs["Color"].default_value = (0.35, 0.35, 0.35, 1.0)
    bg_env.inputs["Strength"].default_value = 0.45

    light_path = nodes.new("ShaderNodeLightPath")
    links.new(light_path.outputs["Is Camera Ray"], w_mix.inputs["Fac"])
    links.new(bg_env.outputs["Background"], w_mix.inputs[1])
    links.new(bg_cam.outputs["Background"], w_mix.inputs[2])
    links.new(w_mix.outputs["Shader"], w_out.inputs["Surface"])


def add_area_light(scene, name, location, target, energy, size, color=(1.0, 1.0, 1.0)):
    light_data = bpy.data.lights.new(name=name, type='AREA')
    light_data.energy = energy
    light_data.size = size
    light_data.color = color

    light_obj = bpy.data.objects.new(name=name, object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = Vector(location)
    direction = Vector(target) - Vector(location)
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    return light_obj


def setup_studio_lighting(scene):
    target = (0.0, 0.0, 0.045)
    add_area_light(
        scene,
        "KeyLight",
        location=(-0.30, -0.35, 0.35),
        target=target,
        energy=4.5,
        size=0.45,
        color=(1.0, 0.98, 0.95),
    )
    add_area_light(
        scene,
        "FillLight",
        location=(0.40, -0.25, 0.22),
        target=target,
        energy=2.2,
        size=0.60,
        color=(0.94, 0.97, 1.0),
    )
    add_area_light(
        scene,
        "RimLight",
        location=(-0.15, 0.45, 0.32),
        target=target,
        energy=4.0,
        size=0.40,
        color=(1.0, 1.0, 1.0),
    )
    add_area_light(
        scene,
        "TopSoftLight",
        location=(0.0, 0.0, 0.45),
        target=target,
        energy=1.5,
        size=0.55,
        color=(1.0, 0.99, 0.97),
    )


def setup_camera(scene):
    cam_data = bpy.data.cameras.new("PreviewCamera")
    cam_data.lens = 55.0
    cam_data.sensor_width = 36.0
    cam_data.clip_start = 0.01
    cam_data.clip_end = 10.0

    cam_obj = bpy.data.objects.new("PreviewCamera", cam_data)
    scene.collection.objects.link(cam_obj)

    target = Vector((0.0, 0.0, 0.042))
    azimuth = math.radians(-52.0)
    elevation = math.radians(28.0)
    distance = 0.30

    cam_pos = target + Vector((
        distance * math.cos(elevation) * math.cos(azimuth),
        distance * math.cos(elevation) * math.sin(azimuth),
        distance * math.sin(elevation),
    ))
    cam_obj.location = cam_pos
    cam_obj.rotation_euler = (target - cam_pos).to_track_quat('-Z', 'Y').to_euler()
    scene.camera = cam_obj
    return cam_obj


def configure_render(scene):
    engines = {
        item.identifier
        for item in scene.render.bl_rna.properties["engine"].enum_items
    }
    if "BLENDER_EEVEE" in engines:
        scene.render.engine = "BLENDER_EEVEE"
    elif "BLENDER_EEVEE_NEXT" in engines:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    else:
        scene.render.engine = "CYCLES"

    if hasattr(scene, "eevee") and hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 64

    view_transforms = {
        item.identifier
        for item in scene.view_settings.bl_rna.properties["view_transform"].enum_items
    }
    if "AgX" in view_transforms:
        scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = 0.0

    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.filepath = PNG


def main():
    scene = reset_scene()
    cup_obj = build_coffee_cup_asset(scene)
    setup_world(scene)
    setup_studio_lighting(scene)
    setup_camera(scene)
    configure_render(scene)

    os.makedirs(os.path.dirname(GLB), exist_ok=True)
    os.makedirs(os.path.dirname(PNG), exist_ok=True)

    bpy.ops.object.select_all(action='DESELECT')
    cup_obj.select_set(True)
    bpy.context.view_layer.objects.active = cup_obj
    bpy.ops.export_scene.gltf(
        filepath=GLB,
        export_format='GLB',
        use_selection=True,
        export_materials='EXPORT',
        export_yup=True,
    )

    bpy.ops.render.render(write_still=True)

    bpy.context.view_layer.update()
    cup_obj.data.calc_loop_triangles()
    tri_count = len(cup_obj.data.loop_triangles)
    dims = cup_obj.dimensions
    print(f"Triangle count: {tri_count}")
    print(f"Object dimensions (X, Y, Z) m: ({dims.x:.4f}, {dims.y:.4f}, {dims.z:.4f})")
    print(f"Object dimensions (X, Y, Z) cm: ({dims.x * 100:.2f}, {dims.y * 100:.2f}, {dims.z * 100:.2f})")


if __name__ == "__main__":
    main()
