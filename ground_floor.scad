include <consts.scad>
use <board_joint.scad>
use <roof_generator.py>
use <window.scad>

HW = HOUSE_WIDTH / 2;
HD = HOUSE_DEPTH / 2;
HDD = HD + 1;
HH = HOUSE_HEIGHT / 2;
JOINT_HEIGHT = HOUSE_HEIGHT - HEIGHT;
JOINT_HEIGHT_BOTTOM = HOUSE_HEIGHT / 2;

FIGURES = import("figures.json");
echo(FIGURES);

PP_FULL = [
    [-HW, -HD],
    [-HW, +HD],
    [+HW, +HD],
    [+HW, -HD],
];

PP_ROOF_FULL = [
    [
        [-HW, -HDD],
        [-HW, +HDD],
        [+HW, +HDD],
        [+HW, -HDD], 
    ],
    [
        [-HW, -0],
        [-HW, +0],
        [+HW, +0],
        [+HW, -0],
    ],    
];

PP_SIDE = [
    [-HW, -HD],
    [-HW, +HD],
    [+HD, +HD],
    [+HD, -HD],
];

PP_ROOF_SIDE = [
    [
        [-HW, -HDD],
        [-HW, +HDD],
        [+HDD, +HDD],
        [+HDD, -HDD],
    ],
    [
        [-HW, -0],
        [-HW, +0],
        [0, +0],
        [0, -0],
    ],
];

PP_EDGE = [
    [-HW, -HD],
    [+HD, -HD],
    [+HD, +HW],
    [-HD, +HW],
    [-HD, +HD],
    [-HW, +HD],
];

PP_ROOF_EDGE = [
    [   
        [-HW,  -HDD],
        [+HDD, -HDD],
        [+HDD, +HW],
        [-HDD, +HW],
        [-HDD, +HDD],
        [-HW,  +HDD],
    ],
    [
        [-HW, -0],
        [+0, -0],
        [+0, +HW],
        [-0, +HW],
        [-0, +0],
        [-HW, +0],
    ],
];


module zero_floor(pp) {
    color("grey")
    _ground();
    
    color("red")
    translate([0, 0, GROUND_HEIGHT])
    _body(pp);
}

module next_floor(pp) {
    color("red")
    _body(pp);
    
    _joint(pp, JOINT_HEIGHT_BOTTOM);
}

module roof(pp, pp0, pp1) {
    color("cyan")
    roof_generator(HOUSE_HEIGHT, pp0, pp1, "mansard", N=20);
    
    _joint(pp, JOINT_HEIGHT_BOTTOM);   
}

module _ground() {
    difference() {
        linear_extrude(GROUND_HEIGHT)
        square(HOUSE_WIDTH, true);
        
        board_joint(HEIGHT * 1.5, CLEARANCE);
    }
}

module _joint(pp, height, clearance=0.0) {
    final_scale = 0.6;
    scale = height * (final_scale - 1) / JOINT_HEIGHT + 1;
    
    mirror([0, 0, 1])
    linear_extrude(height, scale=scale)
    offset(OFFSET)
    polygon([for(p = pp) [
        p[0] + sign(p[0]) * (clearance - WALL_HEIGHT),
        p[1] + sign(p[1]) * (clearance - WALL_HEIGHT),
    ]]);
}

module _body(pp) {
    difference() {
        linear_extrude(HOUSE_HEIGHT)
        polygon(pp);
        
        translate([0, 0, HOUSE_HEIGHT])
        _joint(pp, JOINT_HEIGHT, CLEARANCE);
    }   
}

module floor_stack(pp, pp_floor) {
    H = HOUSE_HEIGHT * 2;
    
    zero_floor(pp);

    translate([0, 0, H])
    next_floor(pp);

    //translate([0, 0, H * 2])
    //next_floor(pp);
    
    translate([0, 0, H * 2])
    roof(pp, pp_floor[0], pp_floor[1]);
}

module floor_decorate(objects, ttt) {
    union() {
        difference() {
            children();
            for(window_t = objects) {
                translate([window_t[0], window_t[1], window_t[2]])
                translate(ttt)
                rotate([0, 0, window_t[3]])
                window_hole();
            }
        }
        
        for(window_t = objects) {
            translate([window_t[0], window_t[1], window_t[2]])
            translate(ttt)
            rotate([0, 0, window_t[3]])
            window();
        }
    }
}


module floor_stack_full() {
    pp = PP_FULL;
    pp_roof = PP_ROOF_FULL;
    H = HOUSE_HEIGHT * 2;
    
    windows = [
        [-HW * 2/3, HD - HEIGHT / 2, HOUSE_HEIGHT / 2, 180],
        [+HW * 2/3, HD - HEIGHT / 2, HOUSE_HEIGHT / 2, 180],
        [0, HD - HEIGHT / 2, HOUSE_HEIGHT / 2, 180],
        [-HW * 2/3, -(HD - HEIGHT / 2), HOUSE_HEIGHT / 2, 0],
        [+HW * 2/3, -(HD - HEIGHT / 2), HOUSE_HEIGHT / 2, 0],
        [0, -(HD - HEIGHT / 2), HOUSE_HEIGHT / 2, 0],
    ];
    
    floor_decorate(windows, [0, 0, HEIGHT*2])
    zero_floor(pp);

    translate([0, 0, H])
    floor_decorate(windows, [0, 0, 0])
    next_floor(pp);
    
    translate([0, 0, H * 2])
    roof(pp, pp_roof[0], pp_roof[1]);
}

module floor_stack_side() {
    pp = PP_SIDE;
    pp_roof = PP_ROOF_SIDE;
    H = HOUSE_HEIGHT * 2;
    
    windows = [
        [-HW * 1/2 , HD - HEIGHT / 2, HOUSE_HEIGHT / 2, 180],
        [+HW * 1/4, HD - HEIGHT / 2, HOUSE_HEIGHT / 2, 180],
        [-HW * 1/2, -(HD - HEIGHT / 2), HOUSE_HEIGHT / 2, 0],
        [+HW * 1/4, -(HD - HEIGHT / 2), HOUSE_HEIGHT / 2, 0],
        [HD - HEIGHT / 2, 0, HOUSE_HEIGHT / 2, 90],
    ];
    
    floor_decorate(windows, [0, 0, HEIGHT*2])
    zero_floor(pp);

    translate([0, 0, H])
    floor_decorate(windows, [0, 0, 0])
    next_floor(pp);
    
    translate([0, 0, H * 2])
    roof(pp, pp_roof[0], pp_roof[1]);
}

module floor_stack_edge() {
    pp = PP_EDGE;
    pp_roof = PP_ROOF_EDGE;
    H = HOUSE_HEIGHT * 2;
    
    windows = [
        [-HW * 1/2, -(HD - HEIGHT / 2), HOUSE_HEIGHT / 2, 0],
        [+HW * 1/4, -(HD - HEIGHT / 2), HOUSE_HEIGHT / 2, 0],
        [(HD - HEIGHT / 2), +HW/3 -HW * 1/2, HOUSE_HEIGHT / 2, 90],
        [(HD - HEIGHT / 2), +HW/3 +HW * 1/4, HOUSE_HEIGHT / 2, 90],
    ];
    
    floor_decorate(windows, [0, 0, HEIGHT*2])
    zero_floor(pp);

    translate([0, 0, H])
    floor_decorate(windows, [0, 0, 0])
    next_floor(pp);
    
    translate([0, 0, H * 2])
    roof(pp, pp_roof[0], pp_roof[1]);
}


M = HOUSE_WIDTH * 1.5;

translate([0, 0])
floor_stack_full();

translate([M, 0])
floor_stack_side();

translate([-M, 0])
rotate([0, 0, 180])
floor_stack_edge();

/*
translate([-M, -M])
rotate([0, 0, 90])
floor_stack(PP_FULL);

translate([-M, -M * 2])
rotate([0, 0, 270])
floor_stack(PP_SIDE);
*/