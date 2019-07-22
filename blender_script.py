#!/usr/bin/python3

import locale
import sys
import array
import bmesh
import bpy

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')


def bmesh_copy_from_object(obj, transform=True, triangulate=True, apply_modifiers=False):
    """
    Returns a transformed, triangulated copy of the mesh
    """

    assert(obj.type == 'MESH')

    if apply_modifiers and obj.modifiers:
        import bpy
        me = obj.to_mesh(bpy.context.scene, True,
                         'PREVIEW', calc_tessface=False)
        bm = bmesh.new()
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
        del bpy
    else:
        me = obj.data
        if obj.mode == 'EDIT':
            bm_orig = bmesh.from_edit_mesh(me)
            bm = bm_orig.copy()
        else:
            bm = bmesh.new()
            bm.from_mesh(me)

    # TODO. remove all customdata layers.
    # would save ram

    if transform:
        bm.transform(obj.matrix_world)

    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces)

    return bm


def bmesh_calc_area(bm):
    """
    Calculate the surface area.
    """
    return sum(f.calc_area() for f in bm.faces)


def volume_area(filepath):
    bpy.ops.import_mesh.stl(
        filepath=filepath)

    import numpy as np
    obj = bpy.context.active_object

    v = obj.dimensions
    obj.scale = v / max(v)  # normaliserar storleken till 1m
    bpy.ops.transform.resize(value=v)

    bm = bmesh_copy_from_object(obj, apply_modifiers=True)
    volume = bm.calc_volume()
    area = bmesh_calc_area(bm)
    bm.free()
    return volume, area


argv = sys.argv
argv = argv[argv.index("--") + 1:]

volume, area = volume_area(argv[0])

print("VOLUME: {} cm^3".format(round(volume, 2)))
print("SURFACE: {} cm^3".format(round(area, 2)))

# PLA kostar typ 14kr per kubikcentimeter

KOSTNAD_PER_CM3 = 14
THICKNESS = 0.2/1000  # 0.2mm^3

volume = area*THICKNESS
cost = volume*KOSTNAD_PER_CM3

cost = locale.currency(cost, grouping=True)

print("COST: {}".format(cost))
