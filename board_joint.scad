include <consts.scad>

module board_side_joint(height, clearance=0.0) {
    linear_extrude(height)
    offset(OFFSET)
    square([
        MARGIN * 2 - OFFSET + clearance,
        MARGIN - OFFSET + clearance
    ], center=true);
}

module board_center_joint(height, clearance) {
    linear_extrude(HEIGHT)
    offset(OFFSET)
    square(MARGIN * 2 - OFFSET + clearance, center=true);
}

module board_joint(height=HEIGHT, clearance=0.0) {
    union() {
        board_center_joint(height, clearance);
        for(rot=[0 : 3]) {
            rotate([0, 0, rot*90])
            translate([0, CELL_SIZE / 2 - MARGIN * 2,])
            board_side_joint(height, clearance);
        }
    }
}