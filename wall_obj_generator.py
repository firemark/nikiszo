from math import atan2, degrees
from window import Window
from openscad import union

OBJS = {
    "window": Window([
        [0.5, 0.5], 
        [0.66, 0.33],
    ]),
    "window3": Window([
        [0.5, 0.5], 
        [0.33, 0.33, 0.33],
    ]),
}

def generate_wall_objs(main_obj, polygon, objs_matrix, z=0.0):
    objs = []
    holes = []
    for name, position, rotation in _generate_poses(polygon, objs_matrix, z):
        obj = generate_single_wall_obj(name)
        hole = generate_single_wall_hole(name)
        objs.append(obj.rotate(rotation).translate(position))
        holes.append(hole.rotate(rotation).translate(position))
    return main_obj.difference(holes).union(objs)
    #return union(objs)

    
def generate_single_wall_obj(name):
    return OBJS[name].show_obj()


def generate_single_wall_hole(name):
    return OBJS[name].show_hole()


def _generate_poses(polygon, objs_matrix, z=0.0):
    assert len(polygon) == len(objs_matrix)
    for i, objs in enumerate(objs_matrix):
        if not objs:
            continue
        p0 = polygon[i]
        p1 = polygon[(i+1) % len(polygon)]
        shift_vec = [
            p1[0] - p0[0],
            p1[1] - p0[1],
        ]
        yaw = atan2(-shift_vec[1], -shift_vec[0])
        rotation = [0, 0, degrees(yaw)]
        c = len(objs)
        
        position = [
            p0[0] + shift_vec[0] / (c * 2),
            p0[1] + shift_vec[1] / (c * 2),
            z,
        ]
        shift = [
            shift_vec[0] / c,
            shift_vec[1] / c,
        ]
        for obj in objs:
            print(position)
            yield obj, position, rotation
            position[0] += shift[0]
            position[1] += shift[1]
    
    
if __name__ == "__main__":
    _polygon = [
      [-30, +10],
      [-10, +10],
      [-10, +30],
      [+10, +30],
      [+10, -10],
      [-30, -10],
    ]
    objs_matrix = [
        ["window3"],
        ["window3"],
        ["window3"],
        ["window", "window", "window"],
        ["window", "window", "window"],
        ["window3"],
    ]
    from openscad import polygon
    
    main_obj = polygon(_polygon).linear_extrude(10)
    generate_wall_objs(main_obj, _polygon, objs_matrix, 5).show()
    