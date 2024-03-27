class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.level = 1
        self.experience = 0
        self.max_health = 100
        self.health = self.max_health
        self.inventory = []

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
