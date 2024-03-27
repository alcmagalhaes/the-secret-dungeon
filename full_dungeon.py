import random

class Dungeon:

    def __init__(self, width, height, max_rooms):
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.rooms = []
        self.corridors = []
        self.contents = {}  # Dicionário para armazenar o conteúdo de cada sala
        self.player_position = (0, 0)  # Posição inicial do jogador
        self.player_level = 1  # Nível inicial do jogador
        self.player_experience = 0  # Experiência inicial do jogador
        self.player_max_health = 100  # Saúde máxima inicial do jogador
        self.player_health = self.player_max_health  # Saúde inicial do jogador
        self.player_inventory = []  # Inventário do jogador
        self.player_spells = ['Fireball', 'Heal']  # Lista de magias disponíveis para o jogador
        self.trap_types = ['Spikes', 'Poison', 'Explosion']  # Tipos de armadilhas disponíveis
        self.puzzle_types = ['Math', 'Riddle', 'Pattern']  # Tipos de enigmas disponíveis

    def generate(self):
        for _ in range(self.max_rooms):
            # Gera uma sala aleatória
            room_width = random.randint(5, 10)
            room_height = random.randint(5, 10)
            room_x = random.randint(0, self.width - room_width)
            room_y = random.randint(0, self.height - room_height)
            new_room = (room_x, room_y, room_width, room_height)

            # Verifica se a sala não se sobrepõe a outras salas existentes
            if not any(self._intersect(new_room, other) for other in self.rooms):
                self.rooms.append(new_room)

                # Adiciona conteúdo à sala
                self.contents[new_room] = self._generate_room_contents()

        # Conecta as salas com corredores
        for i in range(len(self.rooms) - 1):
            x1, y1, _, _ = self.rooms[i]
            x2, y2, _, _ = self.rooms[i + 1]
            # Corredor horizontal
            if random.randint(0, 1) == 1:
                start_x = min(x1, x2) + random.randint(0, abs(x1 - x2))
                end_x = max(x1, x2) + random.randint(0, abs(x1 - x2))
                corridor = (start_x, y1 + random.randint(0, abs(y1 - y2)), end_x - start_x, 1)
            # Corredor vertical
            else:
                start_y = min(y1, y2) + random.randint(0, abs(y1 - y2))
                end_y = max(y1, y2) + random.randint(0, abs(y1 - y2))
                corridor = (x1 + random.randint(0, abs(x1 - x2)), start_y, 1, end_y - start_y)
            self.corridors.append(corridor)

        # Define a posição inicial do jogador
        self.player_position = (self.rooms[0][0] + self.rooms[0][2] // 2, self.rooms[0][1] + self.rooms[0][3] // 2)

    def move_player(self, dx, dy):
        # Move o jogador na masmorra
        x, y = self.player_position
        new_x = max(0, min(self.width - 1, x + dx))
        new_y = max(0, min(self.height - 1, y + dy))
        if self._is_valid_move(new_x, new_y):
            self.player_position = (new_x, new_y)
            self._player_interaction()

    def _is_valid_move(self, x, y):
        # Verifica se o movimento do jogador é válido (dentro da masmorra)
        return any(x >= room[0] and x < room[0] + room[2] and y >= room[1] and y < room[1] + room[3] for room in self.rooms)

    def _generate_room_contents(self):
        # Gera conteúdo aleatório para a sa    def move_player(self, dx, dy):
        # Move o jogador na masmorra
        x, y = self.player_position
        new_x = max(0, min(self.width - 1, x))
        new_y = max(0, min(self.height - 1, y))
        if self._is_valid_move(new_x, new_y):
            self.player_position = (new_x, new_y)
            self._player_interaction()
        contents = []
        num_items = random.randint(0, 3)
        for _ in range(num_items):
            item_type = random.choice(['chest', 'trap', 'enemy', 'treasure', 'puzzle'])
            contents.append(item_type)
        return contents

    def _intersect(self, room1, room2):
        # Verifica se duas salas se sobrepõem
        return (room1[0] < room2[0] + room2[2] and room1[0] + room1[2] > room2[0] and
                room1[1] < room2[1] + room2[3] and room1[1] + room1[3] > room2[1])

    def _player_interaction(self):
        # Realiza interação do jogador com elementos da masmorra
        player_x, player_y = self.player_position
        room_contents = self.contents.get(self._get_current_room())
        if room_contents:
            for item in room_contents:
                if item == 'chest':
                    self._open_chest()
                elif item == 'trap':
                    self._trigger_trap()
                elif item == 'enemy':
                    self._combat_with_enemy()
                elif item == 'treasure':
                    self._collect_treasure()
                elif item in self.player_spells:
                    self._cast_spell(item)
                elif item == 'puzzle':
                    self._solve_puzzle()

    def _combat_with_enemy(self):
        # Realiza um combate com um inimigo
        enemy_health = random.randint(10, 20)  # Saúde do inimigo (gerada aleatoriamente)
        player_attack = random.randint(5, 15)  # Ataque do jogador (gerado aleatoriamente)
        enemy_attack = random.randint(3, 10)  # Ataque do inimigo (gerado aleatoriamente)
        print("Você encontrou um inimigo! Inicia-se o combate!")
        while enemy_health > 0 and self.player_health > 0:
            print(f"Seu HP: {self.player_health} | HP do Inimigo: {enemy_health}")
            print("Escolha sua ação:")
            print("1. Atacar")
            print("2. Tentar fugir")
            choice = input("Escolha: ")
            if choice == '1':
                # Ataque do jogador
                enemy_health -= player_attack
                print(f"Você atacou o inimigo causando {player_attack} de dano!")
                if enemy_health <= 0:
                    print("Você derrotou o inimigo!")
                    self._gain_experience(20)  # Ganha experiência ao derrotar o inimigo
                    break
                # Ataque do inimigo
                self.player_health -= enemy_attack
                print(f"O inimigo contra-atacou causando {enemy_attack} de dano!")
                if self.player_health <= 0:
                    print("Você foi derrotado pelo inimigo!")
                    break
            elif choice == '2':
                # Tentativa de fuga
                escape_chance = random.randint(1, 10)
                if escape_chance > 5:
                    print("Você conseguiu fugir!")
                    break
                else:
                    print("Você não conseguiu fugir!")
            else:
                print("Escolha inválida. Por favor, escolha novamente.")

    def _open_chest(self):
        # Abre um baú e adiciona um item ao inventário do jogador
        print("Você encontrou um baú! Abrindo...")
        item = random.choice(['Potion', 'Sword', 'Armor'])  # Exemplo de tipos de itens
        self.player_inventory.append(item)
        print(f"Você encontrou um(a) {item}!")

    def _trigger_trap(self):
        # Aciona uma armadilha com efeito aleatório
        trap_type = random.choice(self.trap_types)
        print(f"Você ativou uma armadilha do tipo: {trap_type}!")
        if trap_type == 'Spikes':
            self._spikes_trap()
        elif trap_type == 'Poison':
            self._poison_trap()
        elif trap_type == 'Explosion':
            self._explosion_trap()

    def _collect_treasure(self):
        # Coleta um tesouro e ganha experiência
        print("Você encontrou um tesouro! Parabéns!")
        self._gain_experience(50)  # Ganha experiência ao coletar um tesouro

    def _cast_spell(self, spell):
        # Lança uma magia durante o combate
        if spell == 'Fireball':
            self._cast_fireball()
        elif spell == 'Heal':
            self._cast_heal()

    def _cast_fireball(self):
        # Lança uma bola de fogo no inimigo
        print("Você lançou uma bola de fogo no inimigo!")
        fireball_damage = random.randint(10, 20)
        enemy_health -= fireball_damage
        print(f"A bola de fogo causou {fireball_damage} de dano!")

    def _cast_heal(self):
        # Cura o jogador
        print("Você se curou!")
        heal_amount = random.randint(10, 20)
        self.player_health += heal_amount
        if self.player_health > self.player_max_health:
            self.player_health = self.player_max_health
        print(f"Você recuperou {heal_amount} de saúde!")

    def _spikes_trap(self):
        # Armadilha de espinhos: causa dano ao jogador
        trap_damage = random.randint(5, 15)
        self.player_health -= trap_damage
        print(f"Você foi atingido por espinhos! Sofreu {trap_damage} de dano!")

    def _poison_trap(self):
        # Armadilha de veneno: causa dano ao jogador ao longo do tempo
        poison_damage = random.randint(3, 10)
        duration = random.randint(2, 4)  # Duração do efeito de veneno
        print(f"Você foi envenenado! Sofrerá {poison_damage} de dano por {duration} turnos.")
        for _ in range(duration):
            self.player_health -= poison_damage
            print(f"Você sofreu {poison_damage} de dano devido ao veneno!")
            if self.player_health <= 0:
                print("Você morreu devido ao veneno!")
                break

    def _explosion_trap(self):
        # Armadilha de explosão: causa dano ao jogador e pode destruir a sala
        trap_damage = random.randint(10, 20)
        self.player_health -= trap_damage
        print(f"Você ativou uma explosão! Sofreu {trap_damage} de dano!")
        if random.random() < 0.5:
            # 50% de chance da sala ser destruída pela explosão
            print("A sala foi destruída pela explosão!")
            self.contents[self._get_current_room()] = []

    def _solve_puzzle(self):
        # Resolve um enigma com efeito aleatório
        puzzle_type = random.choice(self.puzzle_types)
        print(f"Você encontrou um enigma do tipo: {puzzle_type}!")
        if puzzle_type == 'Math':
            self._math_puzzle()
        elif puzzle_type == 'Riddle':
            self._riddle_puzzle()
        elif puzzle_type == 'Pattern':
            self._pattern_puzzle()

    def _math_puzzle(self):
        # Enigma de matemática: o jogador deve resolver uma equação simples
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operator = random.choice(['+', '-', '*'])
        equation = f"{num1} {operator} {num2}"
        result = eval(equation)
        print(f"Resolva a seguinte equação: {equation}")
        answer = input("Digite sua resposta: ")
        if answer.isdigit() and int(answer) == result:
            print("Você resolveu o enigma corretamente!")
        else:
            print("Resposta incorreta. Tente novamente!")

    def _riddle_puzzle(self):
        # Enigma de charada: o jogador deve responder a uma charada
        riddles = {
            "O que é, o que é? Tem dentes e não morde. Tem cama e não dorme.": "pente",
            "Qual é a palavra que fica mais curta quando você acrescenta duas letras a ela?": "curta"
        }
        riddle = random.choice(list(riddles.keys()))
        answer = input(f"{riddle}\nDigite sua resposta: ").lower()
        if answer == riddles[riddle]:
            print("Você resolveu o enigma corretamente!")
        else:
            print("Resposta incorreta. Tente novamente!")

    def _pattern_puzzle(self):
        # Enigma de padrão: o jogador deve identificar o próximo elemento em uma sequência
        patterns = {
            "2, 4, 6, 8, ...": "10",
            "1, 4, 9, 16, ...": "25"
        }
        pattern = random.choice(list(patterns.keys()))
        answer = input(f"Complete a sequência: {pattern}\nDigite o próximo número: ")
        if answer == patterns[pattern]:
            print("Você resolveu o enigma corretamente!")
        else:
            print("Resposta incorreta. Tente novamente!")

    def _gain_experience(self, experience):
        # Ganha experiência e verifica se o jogador sobe de nível
        self.player_experience += experience
        print(f"Você ganhou {experience} pontos de experiência!")
        if self.player_experience >= self.player_level * 100:
            self.player_level += 1
            self.player_max_health += 20  # Aumenta a saúde máxima do jogador ao subir de nível
            self.player_health = self.player_max_health  # Restaura a saúde do jogador ao subir de nível
            print(f"Você subiu para o nível {self.player_level}!")

    def _get_current_room(self):
        # Retorna a sala em que o jogador está atualmente
        for room in self.rooms:
            if (room[0] <= self.player_position[0] < room[0] + room[2] and
                room[1] <= self.player_position[1] < room[1] + room[3]):
                return room

    def print_dungeon(self):
        # Imprime a masmorra com salas e corredores marcados, e posição do jogador
        dungeon_map = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for room in self.rooms:
            for y in range(room[1], room[1] + room[3]):
                for x in range(room[0], room[0] + room[2]):
                    if 0 <= y < self.height and 0 <= x < self.width:  # Verifica limites da masmorra
                        dungeon_map[y][x] = 'R'
            for content in self.contents.get(room, []):
                x = room[0] + random.randint(1, room[2] - 2)
                y = room[1] + random.randint(1, room[3] - 2)
                if 0 <= y < self.height and 0 <= x < self.width:  # Verifica limites da masmorra
                    dungeon_map[y][x] = content[0].upper()  # Primeira letra do conteúdo em maiúsculo
        for corridor in self.corridors:
            for y in range(corridor[1], corridor[1] + corridor[3]):
                for x in range(corridor[0], corridor[0] + corridor[2]):
                    if 0 <= y < self.height and 0 <= x < self.width:  # Verifica limites da masmorra
                        dungeon_map[y][x] = 'C'
        player_x, player_y = self.player_position
        if 0 <= player_y < self.height and 0 <= player_x < self.width:  # Verifica limites da masmorra
            dungeon_map[player_y][player_x] = '@'  # Símbolo do jogador
        for row in dungeon_map:
            print(''.join(row))

# Exemplo de uso
dungeon = Dungeon(50, 20, 10)
dungeon.generate()
dungeon.print_dungeon()

# Movendo o jogador e interagindo com elementos da masmorra
#dungeon.move_player(1, 0)  # Movendo para a direita
#dungeon.print_dungeon()

# Agora, vamos interagir com os elementos da masmorra após o movimento
#dungeon.move_player(1, 0)  # Movendo para a direita novamente
#dungeon.print_dungeon()

# Testando combate com inimigo
#dungeon._combat_with_enemy()

# Testando interações com elementos da masmorra
dungeon._player_interaction()
