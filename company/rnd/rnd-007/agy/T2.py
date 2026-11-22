import math
import os
import random

import bmesh
import bpy
from mathutils import Matrix, Vector

GLB = r'{{HOME}}\.claude\company\rnd\rnd-007\agy\T2.glb'
PNG = r'{{HOME}}\.claude\company\rnd\rnd-007\agy\T2.png'


def create_material(name, base_color, metallic=0.0, roughness=0.5):
    """Create a simple Principled BSDF material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()

    out = nt.nodes.new(type='ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness

    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def add_quad_box(bm, corners_bot, corners_top, mat_idx, bevel=0.0, smooth=False):
    """
    Create a hexahedron from 4 bottom and 4 top (x, y, z) tuples.
    Winding order of each quad: front-left, front-right, back-right, back-left.
    """
    before_faces = set(bm.faces)
    vb = [bm.verts.new(c) for c in corners_bot]
    vt = [bm.verts.new(c) for c in corners_top]

    faces = [
        bm.faces.new((vb[3], vb[2], vb[1], vb[0])),  # bottom
        bm.faces.new((vt[0], vt[1], vt[2], vt[3])),  # top
        bm.faces.new((vb[0], vb[1], vt[1], vt[0])),  # front (-Y)
        bm.faces.new((vb[1], vb[2], vt[2], vt[1])),  # right (+X)
        bm.faces.new((vb[2], vb[3], vt[3], vt[2])),  # back (+Y)
        bm.faces.new((vb[3], vb[0], vt[0], vt[3])),  # left (-X)
    ]

    if bevel > 0.0:
        edges = list({e for f in faces for e in f.edges})
        bmesh.ops.bevel(
            bm,
            geom=edges,
            offset=bevel,
            offset_type='OFFSET',
            segments=1,
            profile=0.5,
            affect='EDGES',
            clamp_overlap=True,
        )

    new_faces = set(bm.faces) - before_faces
    for f in new_faces:
        f.material_index = mat_idx
        f.smooth = smooth

    new_verts = list({v for f in new_faces for v in f.verts})
    return new_verts


def add_axis_box(bm, x0, x1, y0, y1, z0, z1, mat_idx, bevel=0.0, smooth=False):
    """Create an axis-aligned box with optional 1-segment bevel."""
    bot = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)]
    top = [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    return add_quad_box(bm, bot, top, mat_idx, bevel=bevel, smooth=smooth)


def add_prism(bm, segments, radius, depth, matrix, mat_idx, smooth_sides=True):
    """Create a closed n-gon cylinder/disc centered at origin along local Z."""
    before_faces = set(bm.faces)
    hz = 0.5 * depth
    bot_verts = []
    top_verts = []

    for i in range(segments):
        ang = 2.0 * math.pi * i / segments
        ca, sa = math.cos(ang) * radius, math.sin(ang) * radius
        bot_verts.append(bm.verts.new(matrix @ Vector((ca, sa, -hz))))
        top_verts.append(bm.verts.new(matrix @ Vector((ca, sa, hz))))

    bm.faces.new(list(reversed(bot_verts))).smooth = False
    bm.faces.new(top_verts).smooth = False

    for i in range(segments):
        j = (i + 1) % segments
        f = bm.faces.new((bot_verts[i], bot_verts[j], top_verts[j], top_verts[i]))
        f.smooth = smooth_sides

    new_faces = set(bm.faces) - before_faces
    for f in new_faces:
        f.material_index = mat_idx

    return list({v for f in new_faces for v in f.verts})


def add_rivet(bm, center, normal, radius, height, mat_idx, segments=6):
    """Create a faceted low-poly dome rivet oriented along normal."""
    before_faces = set(bm.faces)
    n = normal.normalized()
    quat = n.to_track_quat('Z', 'Y')
    rot = quat.to_matrix().to_4x4()
    xform = Matrix.Translation(center) @ rot

    base_verts = []
    mid_verts = []
    for i in range(segments):
        ang = 2.0 * math.pi * i / segments
        ca, sa = math.cos(ang), math.sin(ang)
        base_verts.append(bm.verts.new(xform @ Vector((ca * radius, sa * radius, 0.0))))
        mid_verts.append(
            bm.verts.new(xform @ Vector((ca * radius * 0.62, sa * radius * 0.62, height * 0.68)))
        )

    apex = bm.verts.new(xform @ Vector((0.0, 0.0, height)))
    for i in range(segments):
        j = (i + 1) % segments
        bm.faces.new((base_verts[i], base_verts[j], mid_verts[j], mid_verts[i]))
        bm.faces.new((mid_verts[i], mid_verts[j], apex))

    new_faces = set(bm.faces) - before_faces
    for f in new_faces:
        f.material_index = mat_idx
        f.smooth = True

    return list({v for f in new_faces for v in f.verts})


def add_torus(bm, major_r, minor_r, major_seg, minor_seg, matrix, mat_idx):
    """Create a closed torus ring transformed by matrix."""
    before_faces = set(bm.faces)
    rings = []
    for i in range(major_seg):
        theta = 2.0 * math.pi * i / major_seg
        ct, st = math.cos(theta), math.sin(theta)
        ring = []
        for j in range(minor_seg):
            phi = 2.0 * math.pi * j / minor_seg
            cp, sp = math.cos(phi), math.sin(phi)
            r = major_r + minor_r * cp
            pos = Vector((r * ct, r * st, minor_r * sp))
            ring.append(bm.verts.new(matrix @ pos))
        rings.append(ring)

    for i in range(major_seg):
        ni = (i + 1) % major_seg
        for j in range(minor_seg):
            nj = (j + 1) % minor_seg
            bm.faces.new((rings[i][j], rings[ni][j], rings[ni][nj], rings[i][nj]))

    new_faces = set(bm.faces) - before_faces
    for f in new_faces:
        f.material_index = mat_idx
        f.smooth = True

    return list({v for f in new_faces for v in f.verts})


def body_half_extents(z):
    """Linearly interpolate outer wood half-width and half-depth along body height."""
    t = max(0.0, min(1.0, (z - 0.022) / (0.240 - 0.022)))
    hw = 0.255 + (0.280 - 0.255) * t
    hd = 0.165 + (0.185 - 0.165) * t
    return hw, hd


def build_chest_mesh():
    """Procedurally construct the stylised wooden treasure chest in bmesh."""
    bm = bmesh.new()

    # Material indices
    MAT_WOOD = 0
    MAT_INNER = 1
    MAT_METAL = 2
    MAT_BRASS = 3
    MAT_GOLD = 4

    # ------------------------------------------------------------------
    # 1. LOWER BODY: 4 corner feet + hollow inner box + outer planks
    # ------------------------------------------------------------------
    # 4 sturdy bottom corner feet (resting at z = 0.0)
    hw0, hd0 = body_half_extents(0.022)
    foot_w = 0.056
    foot_d = 0.052
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            cx = sx * (hw0 - 0.026)
            cy = sy * (hd0 - 0.024)
            add_axis_box(
                bm,
                cx - 0.5 * foot_w,
                cx + 0.5 * foot_w,
                cy - 0.5 * foot_d,
                cy + 0.5 * foot_d,
                0.0,
                0.024,
                MAT_METAL,
                bevel=0.003,
            )

    # Hollow inner wooden shell (floor at z = 0.044, walls up to z = 0.240)
    wall_in_inset = 0.024
    wall_out_inset = 0.012
    # Solid lower floor slab
    add_quad_box(
        bm,
        [
            (-(hw0 - wall_out_inset), -(hd0 - wall_out_inset), 0.020),
            ((hw0 - wall_out_inset), -(hd0 - wall_out_inset), 0.020),
            ((hw0 - wall_out_inset), (hd0 - wall_out_inset), 0.020),
            (-(hw0 - wall_out_inset), (hd0 - wall_out_inset), 0.020),
        ],
        [
            (-(hw0 - wall_out_inset + 0.004), -(hd0 - wall_out_inset + 0.004), 0.046),
            ((hw0 - wall_out_inset + 0.004), -(hd0 - wall_out_inset + 0.004), 0.046),
            ((hw0 - wall_out_inset + 0.004), (hd0 - wall_out_inset + 0.004), 0.046),
            (-(hw0 - wall_out_inset + 0.004), (hd0 - wall_out_inset + 0.004), 0.046),
        ],
        MAT_INNER,
    )

    # 4 inner lining walls + top rim cap
    hw_t, hd_t = body_half_extents(0.240)
    # Front & back inner walls
    for sy in (-1.0, 1.0):
        y_out_b = sy * (hd0 - wall_out_inset)
        y_in_b = sy * (hd0 - wall_in_inset)
        y_out_t = sy * (hd_t - wall_out_inset)
        y_in_t = sy * (hd_t - wall_in_inset)
        y0b, y1b = min(y_out_b, y_in_b), max(y_out_b, y_in_b)
        y0t, y1t = min(y_out_t, y_in_t), max(y_out_t, y_in_t)
        add_quad_box(
            bm,
            [(-(hw0 - wall_out_inset), y0b, 0.044), ((hw0 - wall_out_inset), y0b, 0.044),
             ((hw0 - wall_out_inset), y1b, 0.044), (-(hw0 - wall_out_inset), y1b, 0.044)],
            [(-(hw_t - wall_out_inset), y0t, 0.240), ((hw_t - wall_out_inset), y0t, 0.240),
             ((hw_t - wall_out_inset), y1t, 0.240), (-(hw_t - wall_out_inset), y1t, 0.240)],
            MAT_INNER,
        )
    # Left & right inner walls
    for sx in (-1.0, 1.0):
        x_out_b = sx * (hw0 - wall_out_inset)
        x_in_b = sx * (hw0 - wall_in_inset)
        x_out_t = sx * (hw_t - wall_out_inset)
        x_in_t = sx * (hw_t - wall_in_inset)
        x0b, x1b = min(x_out_b, x_in_b), max(x_out_b, x_in_b)
        x0t, x1t = min(x_out_t, x_in_t), max(x_out_t, x_in_t)
        add_quad_box(
            bm,
            [(x0b, -(hd0 - wall_in_inset), 0.044), (x1b, -(hd0 - wall_in_inset), 0.044),
             (x1b, (hd0 - wall_in_inset), 0.044), (x0b, (hd0 - wall_in_inset), 0.044)],
            [(x0t, -(hd_t - wall_in_inset), 0.240), (x1t, -(hd_t - wall_in_inset), 0.240),
             (x1t, (hd_t - wall_in_inset), 0.240), (x0t, (hd_t - wall_in_inset), 0.240)],
            MAT_INNER,
        )

    # Top wooden rim bars around the chest opening
    rim_z0, rim_z1 = 0.232, 0.244
    add_axis_box(bm, -hw_t, hw_t, -hd_t, -(hd_t - wall_in_inset), rim_z0, rim_z1, MAT_WOOD, bevel=0.002)
    add_axis_box(bm, -hw_t, hw_t, (hd_t - wall_in_inset), hd_t, rim_z0, rim_z1, MAT_WOOD, bevel=0.002)
    add_axis_box(bm, -hw_t, -(hw_t - wall_in_inset), -(hd_t - wall_in_inset), (hd_t - wall_in_inset), rim_z0, rim_z1, MAT_WOOD, bevel=0.002)
    add_axis_box(bm, (hw_t - wall_in_inset), hw_t, -(hd_t - wall_in_inset), (hd_t - wall_in_inset), rim_z0, rim_z1, MAT_WOOD, bevel=0.002)

    # 3 horizontal plank tiers on front, back, left, right walls
    plank_tiers = [(0.022, 0.092), (0.094, 0.166), (0.168, 0.236)]
    plank_thick = 0.016
    for pz0, pz1 in plank_tiers:
        hwb, hdb = body_half_extents(pz0)
        hwt, hdt = body_half_extents(pz1)

        # Front & Back planks
        for sy in (-1.0, 1.0):
            yb_out, yt_out = sy * hdb, sy * hdt
            yb_in, yt_in = sy * (hdb - plank_thick), sy * (hdt - plank_thick)
            yb0, yb1 = min(yb_out, yb_in), max(yb_out, yb_in)
            yt0, yt1 = min(yt_out, yt_in), max(yt_out, yt_in)
            add_quad_box(
                bm,
                [(-(hwb - 0.002), yb0, pz0), ((hwb - 0.002), yb0, pz0),
                 ((hwb - 0.002), yb1, pz0), (-(hwb - 0.002), yb1, pz0)],
                [(-(hwt - 0.002), yt0, pz1), ((hwt - 0.002), yt0, pz1),
                 ((hwt - 0.002), yt1, pz1), (-(hwt - 0.002), yt1, pz1)],
                MAT_WOOD,
                bevel=0.0025,
            )

        # Left & Right planks
        for sx in (-1.0, 1.0):
            xb_out, xt_out = sx * hwb, sx * hwt
            xb_in, xt_in = sx * (hwb - plank_thick), sx * (hwt - plank_thick)
            xb0, xb1 = min(xb_out, xb_in), max(xb_out, xb_in)
            xt0, xt1 = min(xt_out, xt_in), max(xt_out, xt_in)
            add_quad_box(
                bm,
                [(xb0, -(hdb - 0.015), pz0), (xb1, -(hdb - 0.015), pz0),
                 (xb1, (hdb - 0.015), pz0), (xb0, (hdb - 0.015), pz0)],
                [(xt0, -(hdt - 0.015), pz1), (xt1, -(hdt - 0.015), pz1),
                 (xt1, (hdt - 0.015), pz1), (xt0, (hdt - 0.015), pz1)],
                MAT_WOOD,
                bevel=0.0025,
            )

    # ------------------------------------------------------------------
    # 2. LOWER BODY DARK METAL BANDS, CORNER BRACKETS, HANDLES, RIVETS
    # ------------------------------------------------------------------
    strap_t = 0.007
    # 2 vertical U-straps wrapping front, bottom, and back
    for sx_pos in (-0.17, 0.17):
        hw_s = 0.021
        # Front & Back vertical strap bars
        for sy in (-1.0, 1.0):
            yb_out = sy * (hd0 + strap_t)
            yt_out = sy * (hd_t + strap_t)
            yb_in = sy * (hd0 - 0.002)
            yt_in = sy * (hd_t - 0.002)
            yb0, yb1 = min(yb_out, yb_in), max(yb_out, yb_in)
            yt0, yt1 = min(yt_out, yt_in), max(yt_out, yt_in)
            add_quad_box(
                bm,
                [(sx_pos - hw_s, yb0, 0.016), (sx_pos + hw_s, yb0, 0.016),
                 (sx_pos + hw_s, yb1, 0.016), (sx_pos - hw_s, yb1, 0.016)],
                [(sx_pos - hw_s, yt0, 0.244), (sx_pos + hw_s, yt0, 0.244),
                 (sx_pos + hw_s, yt1, 0.244), (sx_pos - hw_s, yt1, 0.244)],
                MAT_METAL,
                bevel=0.002,
            )
            # Rivets along front and back straps
            n_dir = Vector((0.0, sy * 1.0, -0.09)).normalized()
            for rz in (0.056, 0.130, 0.204):
                _, r_hd = body_half_extents(rz)
                add_rivet(
                    bm,
                    Vector((sx_pos, sy * (r_hd + strap_t - 0.0005), rz)),
                    n_dir,
                    radius=0.0065,
                    height=0.0045,
                    mat_idx=MAT_METAL,
                )

        # Bottom connecting strap bar
        add_axis_box(
            bm,
            sx_pos - hw_s,
            sx_pos + hw_s,
            -(hd0 + strap_t),
            (hd0 + strap_t),
            0.014,
            0.023,
            MAT_METAL,
            bevel=0.002,
        )

    # 4 corner vertical metal angle brackets
    flange_w = 0.032
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            # Front/Back corner flange
            x0b = sx * (hw0 + strap_t)
            x1b = sx * (hw0 - flange_w)
            x0t = sx * (hw_t + strap_t)
            x1t = sx * (hw_t - flange_w)
            yb0 = sy * (hd0 + strap_t)
            yb1 = sy * (hd0 - 0.002)
            yt0 = sy * (hd_t + strap_t)
            yt1 = sy * (hd_t - 0.002)
            add_quad_box(
                bm,
                [(min(x0b, x1b), min(yb0, yb1), 0.020), (max(x0b, x1b), min(yb0, yb1), 0.020),
                 (max(x0b, x1b), max(yb0, yb1), 0.020), (min(x0b, x1b), max(yb0, yb1), 0.020)],
                [(min(x0t, x1t), min(yt0, yt1), 0.244), (max(x0t, x1t), min(yt0, yt1), 0.244),
                 (max(x0t, x1t), max(yt0, yt1), 0.244), (min(x0t, x1t), max(yt0, yt1), 0.244)],
                MAT_METAL,
                bevel=0.0018,
            )
            # Left/Right corner flange
            xb_side0 = sx * (hw0 + strap_t)
            xb_side1 = sx * (hw0 - 0.002)
            xt_side0 = sx * (hw_t + strap_t)
            xt_side1 = sx * (hw_t - 0.002)
            y_side0b = sy * (hd0 + strap_t)
            y_side1b = sy * (hd0 - flange_w)
            y_side0t = sy * (hd_t + strap_t)
            y_side1t = sy * (hd_t - flange_w)
            add_quad_box(
                bm,
                [(min(xb_side0, xb_side1), min(y_side0b, y_side1b), 0.020),
                 (max(xb_side0, xb_side1), min(y_side0b, y_side1b), 0.020),
                 (max(xb_side0, xb_side1), max(y_side0b, y_side1b), 0.020),
                 (min(xb_side0, xb_side1), max(y_side0b, y_side1b), 0.020)],
                [(min(xt_side0, xt_side1), min(y_side0t, y_side1t), 0.244),
                 (max(xt_side0, xt_side1), min(y_side0t, y_side1t), 0.244),
                 (max(xt_side0, xt_side1), max(y_side0t, y_side1t), 0.244),
                 (min(xt_side0, xt_side1), max(y_side0t, y_side1t), 0.244)],
                MAT_METAL,
                bevel=0.0018,
            )

    # Side carrying handles (positioned so overall chest width is ~60 cm)
    hz_handle = 0.140
    hw_mid, _ = body_half_extents(hz_handle)
    for sx in (-1.0, 1.0):
        px_in = sx * (hw_mid - 0.002)
        px_out = sx * (hw_mid + 0.010)
        add_axis_box(
            bm,
            min(px_in, px_out),
            max(px_in, px_out),
            -0.042,
            0.042,
            hz_handle - 0.024,
            hz_handle + 0.024,
            MAT_METAL,
            bevel=0.0025,
        )
        # Small bracket loop
        lx_in = sx * (hw_mid + 0.008)
        lx_out = sx * (hw_mid + 0.020)
        add_axis_box(
            bm,
            min(lx_in, lx_out),
            max(lx_in, lx_out),
            -0.016,
            0.016,
            hz_handle - 0.010,
            hz_handle + 0.010,
            MAT_METAL,
            bevel=0.002,
        )
        # Hanging torus ring (major_r=0.032, minor_r=0.0065)
        ring_x = sx * (hw_mid + 0.017)
        ring_center = Vector((ring_x, 0.0, hz_handle - 0.026))
        tilt = Matrix.Rotation(math.radians(sx * -18.0), 4, 'Y')
        align = Matrix.Rotation(math.radians(90.0), 4, 'Y')
        torus_mat = Matrix.Translation(ring_center) @ tilt @ align
        add_torus(bm, major_r=0.031, minor_r=0.0065, major_seg=10, minor_seg=6, matrix=torus_mat, mat_idx=MAT_METAL)

    # ------------------------------------------------------------------
    # 3. FRONT LOCK PLATE (DARK METAL + BRASS ESCUTCHEON)
    # ------------------------------------------------------------------
    lock_z0, lock_z1 = 0.130, 0.236
    _, lock_hd_bot = body_half_extents(lock_z0)
    _, lock_hd_top = body_half_extents(lock_z1)
    plate_thick = 0.010
    add_quad_box(
        bm,
        [(-0.046, -(lock_hd_bot + plate_thick), lock_z0), (0.046, -(lock_hd_bot + plate_thick), lock_z0),
         (0.046, -(lock_hd_bot - 0.002), lock_z0), (-0.046, -(lock_hd_bot - 0.002), lock_z0)],
        [(-0.052, -(lock_hd_top + plate_thick), lock_z1), (0.052, -(lock_hd_top + plate_thick), lock_z1),
         (0.052, -(lock_hd_top - 0.002), lock_z1), (-0.052, -(lock_hd_top - 0.002), lock_z1)],
        MAT_METAL,
        bevel=0.003,
    )
    # Lock plate corner rivets
    for rx in (-0.037, 0.037):
        for rz in (0.144, 0.220):
            _, rhd = body_half_extents(rz)
            add_rivet(
                bm,
                Vector((rx, -(rhd + plate_thick), rz)),
                Vector((0.0, -1.0, -0.09)),
                radius=0.0055,
                height=0.004,
                mat_idx=MAT_BRASS,
            )
    # Brass keyhole escutcheon & dark slot
    esc_z = 0.178
    _, esc_hd = body_half_extents(esc_z)
    esc_mat = (
        Matrix.Translation(Vector((0.0, -(esc_hd + plate_thick + 0.002), esc_z)))
        @ Matrix.Rotation(math.radians(90.0), 4, 'X')
    )
    add_prism(bm, segments=8, radius=0.018, depth=0.006, matrix=esc_mat, mat_idx=MAT_BRASS, smooth_sides=True)
    # Keyhole vertical bar
    add_axis_box(
        bm,
        -0.0035,
        0.0035,
        -(esc_hd + plate_thick + 0.0065),
        -(esc_hd + plate_thick + 0.0025),
        esc_z - 0.011,
        esc_z + 0.004,
        MAT_METAL,
        bevel=0.0008,
    )

    # ------------------------------------------------------------------
    # 4. ARCHED BARREL LID (BUILT CLOSED, THEN OPENED 30 DEGREES)
    # ------------------------------------------------------------------
    lid_verts = []
    hinge_y = hd_t
    hinge_z = 0.244
    n_arch = 7
    ry_out, rz_out = hd_t, 0.124
    ry_in, rz_in = hd_t - 0.022, 0.102

    # 7 arched plank slats across lid
    for i in range(n_arch):
        a0 = math.pi * (1.0 - (i + 0.03) / n_arch)
        a1 = math.pi * (1.0 - (i + 0.97) / n_arch)
        y0_o, z0_o = ry_out * math.cos(a0), hinge_z + rz_out * math.sin(a0)
        y1_o, z1_o = ry_out * math.cos(a1), hinge_z + rz_out * math.sin(a1)
        y0_i, z0_i = (ry_out - 0.016) * math.cos(a0), hinge_z + (rz_out - 0.016) * math.sin(a0)
        y1_i, z1_i = (ry_out - 0.016) * math.cos(a1), hinge_z + (rz_out - 0.016) * math.sin(a1)

        lid_verts.extend(
            add_quad_box(
                bm,
                [(-hw_t, y0_i, z0_i), (hw_t, y0_i, z0_i), (hw_t, y1_i, z1_i), (-hw_t, y1_i, z1_i)],
                [(-hw_t, y0_o, z0_o), (hw_t, y0_o, z0_o), (hw_t, y1_o, z1_o), (-hw_t, y1_o, z1_o)],
                MAT_WOOD,
                bevel=0.0025,
            )
        )

    # Inner arched vault ceiling + 2 wooden end caps
    for i in range(n_arch):
        a0 = math.pi * (1.0 - i / n_arch)
        a1 = math.pi * (1.0 - (i + 1) / n_arch)
        y0_i, z0_i = ry_in * math.cos(a0), hinge_z + rz_in * math.sin(a0)
        y1_i, z1_i = ry_in * math.cos(a1), hinge_z + rz_in * math.sin(a1)
        y0_o, z0_o = (ry_out - 0.010) * math.cos(a0), hinge_z + (rz_out - 0.010) * math.sin(a0)
        y1_o, z1_o = (ry_out - 0.010) * math.cos(a1), hinge_z + (rz_out - 0.010) * math.sin(a1)

        lid_verts.extend(
            add_quad_box(
                bm,
                [(-(hw_t - 0.022), y0_i, z0_i), ((hw_t - 0.022), y0_i, z0_i),
                 ((hw_t - 0.022), y1_i, z1_i), (-(hw_t - 0.022), y1_i, z1_i)],
                [(-(hw_t - 0.022), y0_o, z0_o), ((hw_t - 0.022), y0_o, z0_o),
                 ((hw_t - 0.022), y1_o, z1_o), (-(hw_t - 0.022), y1_o, z1_o)],
                MAT_INNER,
            )
        )

    # Left & right solid arched end caps + front/back lower rim strips
    for sx in (-1.0, 1.0):
        x0 = sx * hw_t
        x1 = sx * (hw_t - 0.022)
        xa, xb = min(x0, x1), max(x0, x1)
        for i in range(n_arch):
            a0 = math.pi * (1.0 - i / n_arch)
            a1 = math.pi * (1.0 - (i + 1) / n_arch)
            y0, z0 = ry_out * math.cos(a0), hinge_z + rz_out * math.sin(a0)
            y1, z1 = ry_out * math.cos(a1), hinge_z + rz_out * math.sin(a1)
            lid_verts.extend(
                add_quad_box(
                    bm,
                    [(xa, 0.0, hinge_z), (xb, 0.0, hinge_z), (xb, y1, z1), (xa, y1, z1)],
                    [(xa, y0, z0), (xb, y0, z0), (xb, y1, z1), (xa, y1, z1)],
                    MAT_WOOD,
                )
            )

    # 4 arched dark metal bands on lid (2 middle straps + 2 end rim bands)
    lid_band_specs = [
        (-0.17, 0.021),
        (0.17, 0.021),
        (-(hw_t - 0.008), 0.016),
        ((hw_t - 0.008), 0.016),
    ]
    for bx_center, b_hw in lid_band_specs:
        for i in range(n_arch):
            a0 = math.pi * (1.0 - i / n_arch)
            a1 = math.pi * (1.0 - (i + 1) / n_arch)
            y0_i, z0_i = (ry_out - 0.002) * math.cos(a0), hinge_z + (rz_out - 0.002) * math.sin(a0)
            y1_i, z1_i = (ry_out - 0.002) * math.cos(a1), hinge_z + (rz_out - 0.002) * math.sin(a1)
            y0_o, z0_o = (ry_out + strap_t) * math.cos(a0), hinge_z + (rz_out + strap_t) * math.sin(a0)
            y1_o, z1_o = (ry_out + strap_t) * math.cos(a1), hinge_z + (rz_out + strap_t) * math.sin(a1)

            lid_verts.extend(
                add_quad_box(
                    bm,
                    [(bx_center - b_hw, y0_i, z0_i), (bx_center + b_hw, y0_i, z0_i),
                     (bx_center + b_hw, y1_i, z1_i), (bx_center - b_hw, y1_i, z1_i)],
                    [(bx_center - b_hw, y0_o, z0_o), (bx_center + b_hw, y0_o, z0_o),
                     (bx_center + b_hw, y1_o, z1_o), (bx_center - b_hw, y1_o, z1_o)],
                    MAT_METAL,
                    bevel=0.0015,
                )
            )
            # Rivets on middle arched straps
            if abs(bx_center) < 0.20 and i in (0, 2, 4, 6):
                amid = 0.5 * (a0 + a1)
                ry_r, rz_r = ry_out + strap_t - 0.0005, rz_out + strap_t - 0.0005
                pos = Vector((bx_center, ry_r * math.cos(amid), hinge_z + rz_r * math.sin(amid)))
                nrm = Vector((0.0, math.cos(amid) / ry_r, math.sin(amid) / rz_r)).normalized()
                lid_verts.extend(add_rivet(bm, pos, nrm, radius=0.006, height=0.004, mat_idx=MAT_METAL))

    # Front lid hasp (moves with the lid when opened)
    lid_verts.extend(
        add_axis_box(
            bm,
            -0.024,
            0.024,
            -(ry_out + strap_t + 0.006),
            -(ry_out - 0.002),
            hinge_z - 0.044,
            hinge_z + 0.032,
            MAT_METAL,
            bevel=0.0025,
        )
    )
    lid_verts.extend(
        add_axis_box(
            bm,
            -0.012,
            0.012,
            -(ry_out + strap_t + 0.010),
            -(ry_out + strap_t + 0.003),
            hinge_z - 0.038,
            hinge_z - 0.012,
            MAT_BRASS,
            bevel=0.0018,
        )
    )

    # Rotate all lid vertices -30 degrees around X at the rear hinge line
    lid_verts = list(set(lid_verts))
    bmesh.ops.rotate(
        bm,
        cent=Vector((0.0, hinge_y, hinge_z)),
        matrix=Matrix.Rotation(math.radians(-30.0), 3, 'X'),
        verts=lid_verts,
    )

    # Rear barrel hinges (straddling the hinge line)
    for hx in (-0.17, 0.17):
        hinge_mat = (
            Matrix.Translation(Vector((hx, hinge_y + 0.007, hinge_z)))
            @ Matrix.Rotation(math.radians(90.0), 4, 'Y')
        )
        add_prism(bm, segments=8, radius=0.0095, depth=0.052, matrix=hinge_mat, mat_idx=MAT_METAL, smooth_sides=True)

    # ------------------------------------------------------------------
    # 5. TREASURE MOUND & INDIVIDUAL GOLD COINS INSIDE
    # ------------------------------------------------------------------
    def mound_height(x, y):
        nx = x / 0.24
        ny = y / 0.145
        dome = max(0.0, 1.0 - 0.52 * (nx * nx + ny * ny))
        ripple = 0.007 * math.sin(18.0 * x + 9.0 * y) * math.cos(14.0 * y - 6.0 * x)
        return 0.168 + 0.068 * dome + ripple

    gx, gy = 10, 7
    top_grid = []
    bot_grid = []
    for ix in range(gx + 1):
        u = ix / gx
        x_top = -0.238 + u * 0.476
        x_bot = -0.215 + u * 0.430
        col_t = []
        col_b = []
        for iy in range(gy + 1):
            v = iy / gy
            y_top = -0.145 + v * 0.290
            y_bot = -0.125 + v * 0.250
            z_top = mound_height(x_top, y_top)
            col_t.append(bm.verts.new((x_top, y_top, z_top)))
            col_b.append(bm.verts.new((x_bot, y_bot, 0.052)))
        top_grid.append(col_t)
        bot_grid.append(col_b)

    mound_faces = []
    for ix in range(gx):
        for iy in range(gy):
            mound_faces.append(
                bm.faces.new((
                    top_grid[ix][iy],
                    top_grid[ix + 1][iy],
                    top_grid[ix + 1][iy + 1],
                    top_grid[ix][iy + 1],
                ))
            )
    # Skirt walls around mound perimeter
    for ix in range(gx):
        mound_faces.append(bm.faces.new((bot_grid[ix][0], bot_grid[ix + 1][0], top_grid[ix + 1][0], top_grid[ix][0])))
        mound_faces.append(bm.faces.new((top_grid[ix][gy], top_grid[ix + 1][gy], bot_grid[ix + 1][gy], bot_grid[ix][gy])))
    for iy in range(gy):
        mound_faces.append(bm.faces.new((top_grid[0][iy], top_grid[0][iy + 1], bot_grid[0][iy + 1], bot_grid[0][iy])))
        mound_faces.append(bm.faces.new((bot_grid[gx][iy], bot_grid[gx][iy + 1], top_grid[gx][iy + 1], top_grid[gx][iy])))

    for f in mound_faces:
        f.material_index = MAT_GOLD
        f.smooth = True

    # Scatter ~88 individual 3D gold coins across the mound + 3 small stacks
    rng = random.Random(42)
    for _ in range(74):
        cx = rng.uniform(-0.212, 0.212)
        cy = rng.uniform(-0.122, 0.122)
        cz = mound_height(cx, cy) + rng.uniform(0.001, 0.008)
        r = rng.uniform(0.017, 0.022)
        d = rng.uniform(0.0045, 0.006)
        rx = math.radians(rng.uniform(-32.0, 32.0))
        ry = math.radians(rng.uniform(-32.0, 32.0))
        rz = math.radians(rng.uniform(0.0, 360.0))
        c_mat = (
            Matrix.Translation(Vector((cx, cy, cz)))
            @ Matrix.Rotation(rz, 4, 'Z')
            @ Matrix.Rotation(ry, 4, 'Y')
            @ Matrix.Rotation(rx, 4, 'X')
        )
        add_prism(bm, segments=10, radius=r, depth=d, matrix=c_mat, mat_idx=MAT_GOLD, smooth_sides=True)

    # 3 small angled coin stacks (5 coins each) for crisp stylised reads
    stacks = [(-0.14, -0.055, 5), (0.04, -0.045, 5), (0.15, 0.025, 4)]
    for sx_pos, sy_pos, count in stacks:
        base_z = mound_height(sx_pos, sy_pos) + 0.003
        tilt_x = math.radians(rng.uniform(-10.0, 10.0))
        tilt_y = math.radians(rng.uniform(-10.0, 10.0))
        for k in range(count):
            jx = rng.uniform(-0.003, 0.003)
            jy = rng.uniform(-0.003, 0.003)
            c_mat = (
                Matrix.Translation(Vector((sx_pos + jx, sy_pos + jy, base_z + k * 0.0056)))
                @ Matrix.Rotation(tilt_y, 4, 'Y')
                @ Matrix.Rotation(tilt_x, 4, 'X')
            )
            add_prism(bm, segments=10, radius=0.020, depth=0.0054, matrix=c_mat, mat_idx=MAT_GOLD, smooth_sides=True)

    # ------------------------------------------------------------------
    # 6. FINALIZE NORMALS, ORIGIN AT BOTTOM CENTRE, AND BOX UVs
    # ------------------------------------------------------------------
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    # Shift Z so lowest point is exactly z = 0.0, keep X/Y centered at chest base origin
    min_z = min(v.co.z for v in bm.verts)
    min_x = min(v.co.x for v in bm.verts)
    max_x = max(v.co.x for v in bm.verts)
    cx_shift = 0.5 * (min_x + max_x)
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((-cx_shift, 0.0, -min_z)))

    # Box-projected UV layer for clean game-ready export
    uv_layer = bm.loops.layers.uv.new('UVMap')
    for f in bm.faces:
        n = f.normal
        ax, ay, az = abs(n.x), abs(n.y), abs(n.z)
        for loop in f.loops:
            co = loop.vert.co
            if az >= ax and az >= ay:
                loop[uv_layer].uv = (co.x * 2.0 + 0.5, co.y * 2.0 + 0.5)
            elif ax >= ay and ax >= az:
                loop[uv_layer].uv = (co.y * 2.0 + 0.5, co.z * 2.0)
            else:
                loop[uv_layer].uv = (co.x * 2.0 + 0.5, co.z * 2.0)

    mesh = bpy.data.meshes.new('TreasureChestMesh')
    bm.to_mesh(mesh)
    bm.free()

    # Attach materials to mesh
    materials = [
        create_material('Mat_Wood_Plank', (0.28, 0.13, 0.055), metallic=0.0, roughness=0.68),
        create_material('Mat_Wood_Inner', (0.14, 0.06, 0.028), metallic=0.0, roughness=0.80),
        create_material('Mat_Dark_Metal', (0.085, 0.092, 0.105), metallic=0.88, roughness=0.38),
        create_material('Mat_Brass_Lock', (0.68, 0.45, 0.14), metallic=0.92, roughness=0.30),
        create_material('Mat_Gold_Coin', (0.95, 0.72, 0.14), metallic=0.96, roughness=0.22),
    ]
    for mat in materials:
        mesh.materials.append(mat)

    obj = bpy.data.objects.new('TreasureChest', mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def add_area_light(name, location, target, energy, color, size_x, size_y):
    """Create a soft rectangular area light aimed at target."""
    light_data = bpy.data.lights.new(name=name, type='AREA')
    light_data.energy = energy
    light_data.color = color
    light_data.shape = 'RECTANGLE'
    light_data.size = size_x
    light_data.size_y = size_y

    light_obj = bpy.data.objects.new(name=name, object_data=light_data)
    bpy.context.scene.collection.objects.link(light_obj)
    light_obj.location = Vector(location)
    direction = (Vector(target) - Vector(location)).normalized()
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    return light_obj


def setup_world(scene):
    """Set up a neutral light grey studio background with soft ambient fill."""
    world = bpy.data.worlds.new('StudioWorld')
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()

    out = nt.nodes.new(type='ShaderNodeOutputWorld')
    lp = nt.nodes.new(type='ShaderNodeLightPath')
    bg_cam = nt.nodes.new(type='ShaderNodeBackground')
    bg_env = nt.nodes.new(type='ShaderNodeBackground')
    mix = nt.nodes.new(type='ShaderNodeMixShader')

    bg_cam.inputs['Color'].default_value = (0.55, 0.55, 0.56, 1.0)
    bg_cam.inputs['Strength'].default_value = 1.0
    bg_env.inputs['Color'].default_value = (0.34, 0.34, 0.36, 1.0)
    bg_env.inputs['Strength'].default_value = 0.75

    nt.links.new(lp.outputs['Is Camera Ray'], mix.inputs['Fac'])
    nt.links.new(bg_env.outputs['Background'], mix.inputs[1])
    nt.links.new(bg_cam.outputs['Background'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])


def frame_camera(cam_obj, target_obj, view_dir, fill_ratio=0.78):
    """Position and aim camera in a 3/4 view so target_obj fills most of the square frame."""
    bpy.context.view_layer.update()
    world_verts = [target_obj.matrix_world @ v.co for v in target_obj.data.vertices]
    min_v = Vector((min(v.x for v in world_verts), min(v.y for v in world_verts), min(v.z for v in world_verts)))
    max_v = Vector((max(v.x for v in world_verts), max(v.y for v in world_verts), max(v.z for v in world_verts)))
    center = 0.5 * (min_v + max_v)

    vdir = Vector(view_dir).normalized()
    rot_quat = (-vdir).to_track_quat('-Z', 'Y')
    cam_obj.rotation_euler = rot_quat.to_euler()
    rot_mat = rot_quat.to_matrix()

    cam_right = rot_mat @ Vector((1.0, 0.0, 0.0))
    cam_up = rot_mat @ Vector((0.0, 1.0, 0.0))
    cam_back = rot_mat @ Vector((0.0, 0.0, 1.0))

    # Project vertices onto camera basis to find tight bounding distance and visual center offset
    us = [(v - center).dot(cam_right) for v in world_verts]
    vs = [(v - center).dot(cam_up) for v in world_verts]
    ws = [(v - center).dot(cam_back) for v in world_verts]

    u_mid = 0.5 * (min(us) + max(us))
    v_mid = 0.5 * (min(vs) + max(vs))
    aim_point = center + cam_right * u_mid + cam_up * v_mid

    tan_half_fov = (0.5 * cam_obj.data.sensor_width) / cam_obj.data.lens
    max_half_extent = fill_ratio * tan_half_fov

    req_dist = 0.5
    for u, v, w in zip(us, vs, ws):
        du = abs(u - u_mid)
        dv = abs(v - v_mid)
        need = max(du, dv) / max_half_extent - w
        if need > req_dist:
            req_dist = need

    cam_obj.location = aim_point + cam_back * req_dist


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene

    # Build model
    chest_obj = build_chest_mesh()

    # Ensure output directories exist
    os.makedirs(os.path.dirname(GLB), exist_ok=True)
    os.makedirs(os.path.dirname(PNG), exist_ok=True)

    # Export .glb (chest object only)
    bpy.ops.object.select_all(action='DESELECT')
    chest_obj.select_set(True)
    bpy.context.view_layer.objects.active = chest_obj
    bpy.ops.export_scene.gltf(
        filepath=GLB,
        export_format='GLB',
        use_selection=True,
        export_apply=True,
    )

    # Configure render engine (Cycles CPU preferred for headless reliability + soft shadows)
    engines = {item.identifier for item in scene.render.bl_rna.properties['engine'].enum_items}
    if 'CYCLES' in engines:
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 48
        scene.cycles.use_denoising = True
        try:
            scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        except Exception:
            pass
    elif 'BLENDER_EEVEE' in engines:
        scene.render.engine = 'BLENDER_EEVEE'
    elif 'BLENDER_EEVEE_NEXT' in engines:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'

    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'

    setup_world(scene)

    # Shadow catcher ground plane for Cycles soft contact shadow
    if scene.render.engine == 'CYCLES':
        g_bm = bmesh.new()
        bmesh.ops.create_grid(g_bm, x_segments=1, y_segments=1, size=4.0)
        g_mesh = bpy.data.meshes.new('ShadowCatcherMesh')
        g_bm.to_mesh(g_mesh)
        g_bm.free()
        g_obj = bpy.data.objects.new('ShadowCatcher', g_mesh)
        scene.collection.objects.link(g_obj)
        g_obj.is_shadow_catcher = True

    # Soft studio 3-point lighting
    chest_center = (0.0, 0.0, 0.24)
    add_area_light('KeyLight', (-1.25, -1.45, 1.85), chest_center, energy=115.0, color=(1.0, 0.96, 0.91), size_x=1.8, size_y=1.4)
    add_area_light('FillLight', (1.55, -1.15, 1.05), chest_center, energy=42.0, color=(0.90, 0.94, 1.0), size_x=2.2, size_y=1.6)
    add_area_light('RimLight', (-0.35, 1.45, 1.55), chest_center, energy=75.0, color=(1.0, 0.98, 0.94), size_x=1.5, size_y=1.2)

    # Camera setup: 3/4 view showing front lock, side handle, open lid, and coins inside
    cam_data = bpy.data.cameras.new('PreviewCamera')
    cam_data.lens = 50.0
    cam_data.sensor_width = 36.0
    cam_obj = bpy.data.objects.new('PreviewCamera', cam_data)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    frame_camera(cam_obj, chest_obj, view_dir=(0.82, -1.0, 0.78), fill_ratio=0.78)

    # Render PNG preview
    scene.render.filepath = PNG
    bpy.ops.render.render(write_still=True)

    # Print triangle count and object dimensions
    chest_obj.data.calc_loop_triangles()
    tri_count = len(chest_obj.data.loop_triangles)
    dims = chest_obj.dimensions
    print(f'Triangle count: {tri_count}')
    print(f'Object dimensions (m): X={dims.x:.4f}, Y={dims.y:.4f}, Z={dims.z:.4f}')
    print(f'Object dimensions (cm): X={dims.x * 100.0:.2f}, Y={dims.y * 100.0:.2f}, Z={dims.z * 100.0:.2f}')


if __name__ == '__main__':
    main()
