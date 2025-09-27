include <consts.scad>
include <board_joint.scad>

module cell() {
    linear_extrude(HEIGHT)
    square(CELL_SIZE, true);
    
    translate([0, 0, HEIGHT])
    board_joint();
}

for(y=[0 : SIZE - 1]) {
    for(x=[0 : SIZE - 1]) {
        translate([x * CELL_SIZE, y * CELL_SIZE])
            cell();
    }
}