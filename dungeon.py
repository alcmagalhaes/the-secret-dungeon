import random

class Dungeon:
    def __init__(self, width, height, max_rooms):
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.rooms = []
        self.corridors = []
        self.contents = {}
        self.player = Player()
        self.generator = MapGenerator(width, height, max_rooms)
        self.puzzle_manager = PuzzleManager()
        self.trap_manager = TrapManager()

    def generate_map(self):
        self.generator.generate()
        self.rooms, self.corridors = self.generator.get_map()

    def move_player(self, dx, dy):
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        if self._is_valid_move(new_x, new_y):
            self.player.move(dx, dy)
            self._player_interaction()

    def _player_interaction(self):
        current_room = self._get_current_room()
        if current_room in self.contents:
            for item in self.contents[current_room]:
                if item == 'enemy':
                    CombatManager.start_combat(self.player)
                elif item == 'puzzle':
                    self.puzzle_manager.solve_puzzle()
                elif item == 'trap':
                    self.trap_manager.trigger_trap()

    def _is_valid_move(self, x, y):
        # Verifica se o movimento é válido
        # Implementação dos limites do mapa e colisões com paredes
        return 0 <= x < self.width and 0 <= y < self.height

    def _get_current_room(self):
        # Retorna o número da sala onde o jogador está atualmente
        for room_number, (x1, y1, x2, y2) in enumerate(self.rooms):
            if x1 <= self.player.x <= x2 and y1 <= self.player.y <= y2:
                return room_number
        return None
