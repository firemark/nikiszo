class WallObj:
    
    def show_obj(self):
        pass
        
    def show_hole(self):
        pass
        
        
def _inner_generator(size, blocks, margin):
    width, height = size
    x_ratios, y_ratios = blocks
    x_max_size = (width - margin * (len(x_ratios) + 1))
    y_max_size = (height - margin * (len(y_ratios) + 1))
    x = margin
    for x_ratio in x_ratios:
        x_size = x_ratio * x_max_size
        y = margin
        for y_ratio in y_ratios:
            y_size = y_ratio * y_max_size
            yield [x, y], [x_size, y_size]
            y += y_size + margin
        x += x_size + margin   