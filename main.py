from random import randint as rnd, choice


class Ship:
    def __init__(self, size, horizontal=True):
        self.size = size
        self.coords = []
        self.death = False
        self.horizontal = horizontal

    def place(self, row, col, pole):
        if self.horizontal:
            # Проверка на горизонтальное размещение
            if col + self.size > len(pole[0]):
                raise ValueError("Корабль не помещается на поле")
            # Проверка на соседние корабли по горизонтали
            for i in range(self.size):
                if col + i > 0 and pole[row][col + i - 1] == '■':
                    raise ValueError("Корабль не может стоять рядом с другим кораблем")
                if col + i < len(pole[0]) - 1 and pole[row][col + i + 1] == '■':
                    raise ValueError("Корабль не может стоять рядом с другим кораблем")
            # Проверка на соседние корабли по вертикали
            if row > 0 and any(pole[row - 1][col + i] == '■' for i in range(self.size)):
                raise ValueError("Корабль не может стоять рядом с другим кораблем")
            if row < len(pole) - 1 and any(pole[row + 1][col + i] == '■' for i in range(self.size)):
                raise ValueError("Корабль не может стоять рядом с другим кораблем")
            # Проверка на занятость клеток
            for i in range(self.size):
                if pole[row][col + i] == '■':
                    raise ValueError("Корабль не может стоять на другом корабле")
            # Размещение корабля по горизонтали
            for i in range(self.size):
                pole[row][col + i] = '■'
                self.coords.append((row, col + i))
        else:
            # Проверка на вертикальное размещение
            if row + self.size > len(pole):
                raise ValueError("Корабль не помещается на поле")
            # Проверка на соседние корабли по вертикали
            for i in range(self.size):
                if row + i > 0 and pole[row + i - 1][col] == '■':
                    raise ValueError("Корабль не может стоять рядом с другим кораблем")
                if row + i < len(pole) - 1 and pole[row + i + 1][col] == '■':
                    raise ValueError("Корабль не может стоять рядом с другим кораблем")
            # Проверка на соседние корабли по горизонтали
            if col > 0 and any(pole[row + i][col - 1] == '■' for i in range(self.size)):
                raise ValueError("Корабль не может стоять рядом с другим кораблем")
            if col < len(pole[0]) - 1 and any(pole[row + i][col + 1] == '■' for i in range(self.size)):
                raise ValueError("Корабль не может стоять рядом с другим кораблем")
            # Проверка на занятость клеток
            for i in range(self.size):
                if pole[row + i][col] == '■':
                    raise ValueError("Корабль не может стоять на другом корабле")
            # Размещение корабля по вертикали
            for i in range(self.size):
                pole[row + i][col] = '■'
                self.coords.append((row + i, col))

    def hit(self, row, col):
        if (row, col) in self.coords:
            self.coords.remove((row, col))
            if not self.coords:
                self.death = True
            return True
        return False


class Gamelogic:
    def __init__(self):
        self.ships = []
        self.enemy_ships = []
        self.pole = [['O' for _ in range(6)] for _ in range(6)]
        self.enemy_pole = [['O' for _ in range(6)] for _ in range(6)]
        self.hidden_pole = [['O' for _ in range(6)] for _ in range(6)]

    def show_pole(self, enemy=False):
        if enemy is False:
            print(f'Игровое поле Игрока!')
        else:
            print(f'Игровое Поле Компьютера!')
        print("  | ", end="")
        for i in range(1, 7):
            i = str(i)
            print(i + " | ", end="")
        print()
        if enemy is False:
            for i, row in enumerate(self.pole):
                print(i + 1, end=" | ")
                for cell in row:
                    print(cell, end=" | ")
                print()
        else:
            for i, row in enumerate(self.enemy_pole):
                print(i + 1, end=" | ")
                for cell in row:
                    print(cell, end=" | ")
                print()

    def create_ships(self):

        self.place_ship(self.pole, 3, 1)
        self.place_ship(self.pole, 2, 2)
        self.place_ship(self.pole, 1, 4)
        self.place_ship(self.hidden_pole, 3, 1, enemy=True)
        self.place_ship(self.hidden_pole, 2, 2, enemy=True)
        self.place_ship(self.hidden_pole, 1, 4, enemy=True)

    def place_ship(self, pole, size, count, enemy=False):
        for _ in range(count):
            while True:
                try:
                    horizontal = choice([True, False])
                    ship = Ship(size, horizontal)
                    row = int(rnd(0, 5))
                    col = int(rnd(0, 5))
                    ship.place(row, col, pole)
                    if enemy is False:
                        self.ships.append(ship)
                    else:
                        self.enemy_ships.append(ship)
                    break
                except ValueError:
                    pass

    def make_move(self):
        while True:
            try:
                row, col = map(int, input("Введите координаты выстрела (строка, столбец): ").split())
                row -= 1
                col -= 1
                if 0 <= row <= 5 and 0 <= col <= 5:
                    if self.enemy_pole[row][col] == 'O':
                        for ship in self.enemy_ships:
                            if ship.hit(row, col):
                                self.enemy_pole[row][col] = 'X'
                                if ship.death:
                                    print(f"Корабль противника потоплен")
                                    return True
                                else:
                                    print(f"Попадание!")
                                    return True
                        self.enemy_pole[row][col] = 'T'
                        print(f"Промах!")
                        return False
                    else:
                        print(f"Вы уже стреляли по этой клетке!")
                else:
                    print("Некорректные координаты. Введите числа от 1 до 6")
            except ValueError:
                print("Некорректные координаты. Введите два числа через пробел")

    def enemy_move(self):
        while True:
            row = rnd(0, 5)
            col = rnd(0, 5)
            if self.pole[row][col] in ('O', '■'):
                break
        for ship in self.ships:
            if ship.hit(row, col):
                self.pole[row][col] = 'X'
                if ship.death:
                    print(f"Ваш корабль потоплен")
                    return True
                else:
                    print(f"Противник попал!")
                    return True
        self.pole[row][col] = 'T'
        print(f"Противник промахнулся!")
        return False

    def check_lose(self):
        for ship in self.ships:
            if not ship.death:
                return False
        print(f"Вы проиграли!")
        return True

    def check_win(self):
        for ship in self.enemy_ships:
            if not ship.death:
                return False
        print(f"Вы победили!")
        return True

    @staticmethod
    def eggs():
        if rnd(1, 10) == 5:
            print('Это не баг, это фича.')


game = Gamelogic()
game.create_ships()
while True:
    game.show_pole()
    game.show_pole(enemy=True)
    if game.make_move():
        if game.check_win():
            break
    if game.enemy_move():
        if game.check_lose():
            game.eggs()
            break
