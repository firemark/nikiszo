include <consts.scad>

module roof_generator(roof_height, pp0, pp1, func, N = 5) {
    assert(len(pp0) == len(pp1));
    pp_size = len(pp0);
    
    pp_points = [
        for(i = [0 : N - 1])
        let(
            s = i / (N - 1),
            sp = func(s),
            sp_inv = 1 - sp,
            h = s * roof_height
        )
        for (j = [0 : pp_size - 1])
        [
            pp0[j][0] * sp_inv + pp1[j][0] * sp,
            pp0[j][1] * sp_inv + pp1[j][1] * sp,
            h,
        ]
    ];
        
    pp_faces = [
        [for(i = [0 : pp_size - 1]) i],
        for(i = [1 : N - 1])
        let(
            n0 = pp_size * (i-1),
            n1 = pp_size * i
        )
        for (j = [0 : pp_size - 1])
        [ 
          n1 + j,
          n1 + (j + 1) % pp_size,
          n0 + (j + 1) % pp_size,
          n0 + j, 
        ],
    ];
              
    polyhedron(points=pp_points, faces=pp_faces);
}

HW = HOUSE_WIDTH / 2;
HDD = HOUSE_DEPTH / 2;
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

roof_generator(10, X, Y, func_roof_mansard, N=20);