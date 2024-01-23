class Enemy:
    def __init__(self, position):
        self.last_two = 0
        self.cur_frame = -1
        self.x, self.y = position