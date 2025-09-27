from openscad import *
from math import sin, pi

def _mansard(x):
    if x < 0.75:
        y = x / 0.75 * 0.5
    else:
        y = (x - 0.75) / 0.5 + 0.5
    return y ** 2
 
funcs = {
    "basic": lambda x: x,
    "conical": lambda x: sin(x * pi/2),
    "mansard": _mansard,
}

def roof_generator(roof_height, pp0, pp1, roof_type, N = 5):
    assert len(pp0) == len(pp1)
    pp_size = len(pp0)
    N = int(N)
    func = funcs.get(roof_type, lambda x: x)
    
    points = []
    faces = [
        [i for i in range(pp_size)]
    ]
    
    for i in range(N):
        s = i / (N - 1)
        sp = func(s)
        sp_inv = 1 - sp
        h = s * roof_height

        for (x0, y0), (x1, y1) in zip(pp0, pp1):
            points.append([
                x0 * sp_inv + x1 * sp,
                y0 * sp_inv + y1 * sp,
                h,
            ])
                
    for i in range(1, N):
        n0 = pp_size * (i-1)
        n1 = pp_size * i

        for j in range(pp_size):
            faces.append([
              n1 + j,
              n1 + (j + 1) % pp_size,
              n0 + (j + 1) % pp_size,
              n0 + j,                
            ])
        
    return polyhedron(points, faces)
    
    
HW = 3
HDD = 1
X = [
        [-HW, -HDD],
        [-HW, +HDD],
        [+HW, +HDD],
        [+HW, -HDD], 
    ];
Y = [
        [-HW, -0],
        [-HW, +0],
        [+HW, +0],
        [+HW, -0],
    ];

yyy = roof_generator(3, X, Y, "mansard", N=20)
#show(yyy)