#include <consts.scad>

HEIGHT = 2
HOUSE_HEIGHT = CELL_SIZE  * 2/3;
CELL_SIZE = 20;
H = HOUSE_HEIGHT * 0.3;


class WallObj:
    
    def obj(self):
        pass
        
    def hole(self):
        pass
        
        
class Window:
    
    def obj(self):
        pass
        
    def hole(self):
        return (
            square([H, 1.61 * H])
            .linear_extrude(2 * HEIGHT, center=True)
            .rotate([90, 0, 0])
            translate([-H/2, 0, -H * 1.61/2])
        )


def _window_inner(size, blocks, margin):
    width, height = size
    block_size = [
        s - margin * (len(l) + 1)
        for s, l in zip(size, blocks)
    ]
    cell_size = [
        [s * b for b in l]
        for s, l in zip(block_size, blocks)
    ]
    shifts = [
        list(accumulate(
            [margin] + [s + margin for s in c[1:]]
        ))
        for c in cell_size
    ]
    holes = [
        ...
    ]

module _window_inner(size, blocks, margin) {
    width = size[0];
    height = size[1];
    c = len(blocks[0]);
    r = len(blocks[1]);
    block_size = [
        (width - margin * (c + 1)),
        (height - margin * (r + 1)),
    ];
    
    difference(){
        square(size);
        
        x_size = [
            for (x = [0 : c - 1])
            block_size[0] * blocks[0][x]
        ];
            
        y_size = [
            for (y = [0 : r - 1])
            block_size[1] * blocks[1][y]
        ];
        
        xxx = accumulator([
            margin,
            for (x = [1 : c - 1])
            x_size[x-1] + margin,
        ]);
            
        yyy = accumulator([
            margin,
            for (y = [1 : r - 1])
            y_size[y-1] + margin,
        ]);
            
        for (x = [0 : c - 1]) {
            xx = block_size[0] * blocks[0][x];
            for (y = [0 : r - 1]) {
                yy = block_size[1] * blocks[1][y];
                translate([xxx[x], yyy[y]])
                square([x_size[x], y_size[y]]);
            }
        }
    }
    
}


module _window(blocks) {
    Z = H / 3;
    A = H / 5;
    
    window_size = [H, H * 1.61];
    window_size_margin = [window_size[0] + 2*A, window_size[1] + 2*A];
    
    rotate([90, 0, 0])
    linear_extrude(HEIGHT, center=true)
    _window_inner(window_size, blocks, 0.6);
    
    rotate([90, 0, 0])
    translate([-A, -A])
    linear_extrude(HEIGHT)
    difference(){
        square(window_size_margin);
        
        translate([A, A])
        square(window_size);
    }
    
    rotate([90, 0, 0])
    translate([-A, -A])
    linear_extrude(HEIGHT * 4/3)
    square([window_size_margin[0], A]);    
}


module window() {
    translate([-H/2, 0, -H * 1.61/2])
    _window([[0.5, 0.5], [0.66, 0.33]]);
}

window();