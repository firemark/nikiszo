include <consts.scad>

module side(clearance=0.0) {
    linear_extrude(HEIGHT, scale=0.9)
    offset(OFFSET)
    square([
        MARGIN * 2 - OFFSET + clearance,
        MARGIN - OFFSET + clearance
    ], center=true);
}

module center_side(clearance=0.0) {
    difference() {
        linear_extrude(HEIGHT)
        offset(OFFSET)
        square(MARGIN * 2 - OFFSET + clearance, center=true);
        
        linear_extrude(HEIGHT * 2, scale=1.1)
        offset(OFFSET)
        square(MARGIN - OFFSET, center=true);
    }
}

module four_sides(clearance=0.0) {
    for(rot=[0 : 3]) {
        rotate([0, 0, rot*90])
        translate([0, CELL_SIZE / 2 - MARGIN * 2,])
        side(clearance);
    }
}

module board_side(clearance) {
    union() {
        center_side();
        four_sides();
    }
}