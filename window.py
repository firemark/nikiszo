from openscad import square, union
from wall_obj import WallObj, _inner_generator

HEIGHT = 2
CELL_SIZE = 20;
HOUSE_HEIGHT = CELL_SIZE  * 2/3;
CELL_SIZE = 20;
H = HOUSE_HEIGHT * 0.3;
        
        
class Window(WallObj):
    
    def __init__(self):
        self.Z = H / 3
        self.A = H / 5
        
        self.window_size = [H, H * 1.61]
        self.window_size_margin = [
            self.window_size[0] + 2 * self.A,
            self.window_size[1] + 2 * self.A,
        ]
        self.blocks = [
            [0.5, 0.5], 
            [0.66, 0.33],
        ]
        self.inner_margin = 0.6
        
    def show_obj(self):
        return (
            self._window()
            .translate([
                -self.window_size[0] / 2, 
                0, 
                -self.window_size[1] / 2,
            ])
        )
            
    def show_hole(self):
        return (
            square([H, 1.61 * H])
            .linear_extrude(2 * HEIGHT, center=True)
            .rotate([90, 0, 0])
            .translate([-H/2, 0, -H * 1.61/2])
        )
        
    def _window(self):
        A = self.A
        
        inner = (
            self._window_inner()
            .linear_extrude(HEIGHT, center=True)
            .rotate([90, 0, 0])
        )
        
        frame = (
            square(self.window_size_margin)
            .difference([
                square(self.window_size)
                .translate([A, A]),
            ])
            .linear_extrude(HEIGHT)
            .translate([-A, -A])
            .rotate([90, 0, 0])
        )
        
        ledge = (
            square([self.window_size_margin[0], A])
            .linear_extrude(HEIGHT * 4/3)
            .translate([-A, -A])
            .rotate([90, 0, 0])
        )
        
        return union([
            inner,
            frame,
            ledge,
        ])

    def _window_inner(self):
        gen = _inner_generator(
            self.window_size,
            self.blocks, 
            self.inner_margin,
        )
        holes = [
            square(hole_size).translate(pos)
            for pos, hole_size in gen
        ]
        
        return square(self.window_size).difference(holes)


if __name__ == "__main__":
    obj = Window()
    obj.obj().show()