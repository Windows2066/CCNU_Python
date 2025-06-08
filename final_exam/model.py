from head import *

COIN = '$'
COIN_AMOUNT = 5

class Tile:
    """ 迷宫中瓷砖的抽象基类 """
    # 定义瓷砖类型以及是否阻挡
    TYPE = 'Abstract Tile'
    BLOCKING = False

    def is_blocking(self) -> bool:
        """ 返回 True 表示该瓷砖是阻挡型 """
        return self.BLOCKING

    def get_type(self) -> str:
        """ 返回瓷砖的类型 """
        return self.TYPE

    def __str__(self) -> str:
        # 返回瓷砖的类型作为字符串表示
        return self.get_type()

    def __repr__(self) -> str:
        return str(self)


class Floor(Tile):
    """ 迷宫中非阻挡型的地板瓷砖 """
    TYPE = FLOOR


class Wall(Tile):
    """ 迷宫中阻挡型的墙壁瓷砖 """
    TYPE = WALL
    BLOCKING = True


class Goal(Tile):
    """ 目标瓷砖，用于放置箱子 """
    TYPE = GOAL

    def __init__(self) -> None:
        """ 构造函数，初始目标为未填充状态 """
        super().__init__()
        self._is_filled = False

    def fill(self) -> None:
        """ 将目标填充 """
        self._is_filled = True

    def unfill(self) -> None:
        """ 将目标状态恢复为未填充状态 """
        self._is_filled = False

    def is_filled(self) -> bool:
        """ 检查目标是否已被填充 """
        return self._is_filled

    def __str__(self):
        return FILLED_GOAL if self._is_filled else self.get_type()


class Entity:
    """ 迷宫中实体的抽象基类 """
    TYPE = 'Abstract Entity'
    MOVABLE = False

    def get_type(self) -> str:
        """ 获取实体的类型 """
        return self.TYPE

    def is_movable(self) -> bool:
        """ 判断实体是否可移动 """
        return self.MOVABLE

    def __str__(self):
        return self.get_type()

    def __repr__(self):
        return str(self)


class Crate(Entity):
    """ 迷宫中的箱子实体 """
    TYPE = CRATE
    MOVABLE = True

    def __init__(self, strength: int) -> None:
        """
        strength: 推动箱子所需的力量值
        """
        super().__init__()
        self._strength = strength

    def get_strength(self) -> int:
        """ 获取推动该箱子所需的力量 """
        return self._strength

    def __str__(self):
        return str(self._strength)  # 显示力量数值


class Coin(Entity):
    """ 玩家可以收集增加金钱 """
    TYPE = COIN


class Potion(Entity):
    """ 提供增益效果的药水实体的抽象基类 """
    TYPE = 'Potion'
    EFFECT = {}

    def effect(self) -> dict[str, int]:
        """ 
        返回药水的效果
        包括 'strength' 和 'moves'
        """
        return self.EFFECT


class StrengthPotion(Potion):
    """ 增加玩家力量的药水 """
    TYPE = STRENGTH_POTION
    EFFECT = {'strength': 2}


class MovePotion(Potion):
    """ 增加玩家剩余步数的药水 """
    TYPE = MOVE_POTION
    EFFECT = {'moves': 5}


class FancyPotion(Potion):
    """ 同时增加力量和步数的药水 """
    TYPE = FANCY_POTION
    EFFECT = {'strength': 2, 'moves': 2}


class Player(Entity):
    """ 玩家实体，记录力量、步数和金钱 """
    TYPE = PLAYER

    def __init__(self, start_strength: int, moves_remaining: int) -> None:
        """ 
        初始化玩家状态
        start_strength: 玩家初始力量
        moves_remaining: 玩家可用的移动步数
        """
        super().__init__()
        self._strength = start_strength
        self._moves_remaining = moves_remaining
        self._money = 0

    def get_money(self) -> int:
        """ 获取玩家金钱数量 """
        return self._money

    def add_money(self, money: int) -> None:
        """ 修改玩家金钱数量，可以为正或为负 """
        self._money += money

    def is_movable(self) -> bool:
        """ 当玩家剩余步数大于 0 时，可以移动 """
        return self._moves_remaining > 0

    def get_strength(self) -> int:
        """ 获取玩家当前力量 """
        return self._strength

    def add_strength(self, strength: int) -> None:
        """ 为玩家增加力量值 """
        self._strength += strength

    def get_moves_remaining(self) -> int:
        """ 获取玩家剩余步数 """
        return self._moves_remaining

    def add_moves_remaining(self, moves: int) -> None:
        """ 修改玩家剩余步数，可以为正或为负 """
        self._moves_remaining += moves

    def apply_effect(self, potion_effect: dict[str, int]) -> None:
        """ 应用药水效果，包括增加力量和步数 """
        self.add_strength(potion_effect.get('strength', 0))
        self.add_moves_remaining(potion_effect.get('moves', 0))


TILE_IDS_TO_CLASS = {
    FLOOR: Floor,
    WALL: Wall,
    GOAL: Goal,
    FILLED_GOAL: Goal,
}

ENTITY_IDS_TO_CLASS = {
    CRATE: Crate,
    COIN: Coin,
    PLAYER: Player,
    STRENGTH_POTION: StrengthPotion,
    MOVE_POTION: MovePotion,
    FANCY_POTION: FancyPotion,
}

def convert_maze(raw_maze: list[list[str]]) -> tuple[Grid, Entities, Position]:
    """ 
    将原始迷宫数据转换为瓷砖对象、实体字典和玩家初始位置
    raw_maze: 从文件中读取得到的原始迷宫数据列表
    返回迷宫瓷砖的二维列表，记录实体在迷宫中位置的字典，玩家初始所在位置的元组
    """
    proper_maze = []
    entities = {}
    player_position = None

    for i, row in enumerate(raw_maze):
        new_row = []
        for j, tile_type in enumerate(row):
            # 根据 tile_type 创建对应的瓷砖对象，默认用 Floor
            tile = TILE_IDS_TO_CLASS.get(tile_type, Floor)()
            if tile_type == FILLED_GOAL:
                tile.fill()  # 若为填充过的目标，则更新状态

            new_row.append(tile)
            # 若表示实体而非瓷砖，则创建对应实体对象
            if not TILE_IDS_TO_CLASS.get(tile_type):
                if tile_type == PLAYER:
                    player_position = (i, j)
                else:
                    if tile_type.isdigit():
                        tile_type = int(tile_type)
                        entity = Crate(tile_type)
                    else:
                        entity = ENTITY_IDS_TO_CLASS.get(tile_type)()

                    entities[(i, j)] = entity
        proper_maze.append(new_row)
    return proper_maze, entities, player_position

class SokobanModel:
    """ 推箱子游戏的模型类，负责管理迷宫状态和玩家操作 """
    ITEM_COSTS = {
        STRENGTH_POTION: 5,
        MOVE_POTION: 5,
        FANCY_POTION: 10,
    }

    def __init__(self, maze_file: str) -> None:
        """ 
        根据迷宫文件路径初始化模型
        maze_file: 迷宫文件的路径，例如 'maze_files/maze1.txt'
        """
        self._maze_file = maze_file
        self.reset()

    def reset(self) -> None:
        """ 重置游戏至初始状态 """
        raw_maze, player_stats = read_file(self._maze_file)
        # 将原始数据转换为瓷砖、实体和玩家初始位置
        self._maze, self._entities, self._player_position = convert_maze(raw_maze)
        self._player = Player(*player_stats)

        # 保存上一步状态，用于执行撤销操作
        self._last_state = {
            'maze': [[item for item in row] for row in self._maze],
            'entities': {key: value for key, value in self._entities.items()},
            'player_stats': player_stats,
            'player_position': self._player_position,
            'last_filled': None,
        }

    def get_shop_items(self) -> dict[str, int]:
        """ 返回商店中物品以及对应的购买价格 """
        return self.ITEM_COSTS

    def attempt_purchase(self, item: str) -> bool:
        """ 
        item: 物品的标识符
        """
        if self._player.get_money() < self.ITEM_COSTS.get(item):
            return False

        self._player.add_money(-self.ITEM_COSTS[item])
        self._entities[self._player_position] = ENTITY_IDS_TO_CLASS[item]()
        self._handle_potion(self._player_position)
        return True

    def get_maze(self) -> Grid:
        """ 返回当前迷宫瓷砖的二维列表 """
        return self._maze

    def get_dimensions(self) -> tuple[int, int]:
        """ 返回迷宫的行数和列数 """
        return len(self._maze), len(self._maze[0])

    def get_entities(self) -> Entities:
        """ 返回记录实体位置的字典 """
        return self._entities

    def get_player_position(self) -> Position:
        """ 获取玩家的当前位置 """
        return self._player_position

    def get_player_moves_remaining(self) -> int:
        """ 获取玩家剩余移动步数 """
        return self._player.get_moves_remaining()

    def get_player_strength(self) -> int:
        """ 获取玩家当前力量 """
        return self._player.get_strength()

    def get_player_money(self) -> int:
        """ 获取玩家拥有的金钱数量 """
        return self._player.get_money()

    def undo_move(self) -> None:
        """ 撤销上一次有效的移动操作 """
        self._maze = self._last_state['maze']
        self._entities = self._last_state['entities']
        self._player_position = self._last_state['player_position']
        self._player = Player(*self._last_state['player_stats'])
        if self._last_state['last_filled'] is not None:
            row, col = self._last_state['last_filled']
            self._get_tile(row, col).unfill()

    def attempt_move(self, direction: str) -> bool:
        """ 尝试按照给定方向移动玩家
        direction: 移动方向
        """
        if direction == 'u':
            self.undo_move()
            return True

        # 在进行有效移动前保存当前状态，用于后续撤销
        last_state = {
            'maze': [[item for item in row] for row in self._maze],
            'entities': {key: value for key, value in self._entities.items()},
            'player_stats': (self._player.get_strength(),
                             self._player.get_moves_remaining()),
            'player_position': self._player_position,
            'last_filled': None,
        }

        if not DIRECTION_DELTAS.get(direction):
            return False

        new_position = new_row, new_col = self._get_new_position(self._player_position, direction)

        if not self._in_bounds(new_row, new_col):
            return False

        if self._get_tile(new_row, new_col).is_blocking():
            return False

        # 若新位置上存在实体则进行相应处理
        entity_present = self._entities.get(new_position)
        if entity_present is not None:
            if entity_present.get_type() == CRATE:
                if not self._attempt_push(new_position, direction):
                    return False
            elif entity_present.get_type() == COIN:
                self._player.add_money(COIN_AMOUNT)
                self._entities.pop(new_position)
            elif isinstance(entity_present, Potion):
                self._handle_potion(new_position)

        self._player_position = new_position
        self._player.add_moves_remaining(-1)

        self._last_state = last_state
        return True

    def has_won(self) -> bool:
        """ 判断玩家是否已经赢得游戏（所有目标均被填充） """
        for row in self._maze:
            for tile in row:
                if tile.get_type() == GOAL and not tile.is_filled():
                    return False
        return True

    def _get_new_position(self, position: Position, direction: str) -> Position:
        """ 根据方向计算新的位置
        position: 当前 (行, 列) 位置
        direction: 移动的方向
        """
        delta = DIRECTION_DELTAS.get(direction)
        return position[0] + delta[0], position[1] + delta[1]

    def _get_tile(self, row: int, col: int) -> Tile:
        """ 获取指定位置的瓷砖对象 """
        return self._maze[row][col]

    def _in_bounds(self, row: int, col: int) -> bool:
        """ 判断指定位置是否在迷宫范围内 """
        return 0 <= row < len(self._maze) and 0 <= col < len(self._maze[0])

    def _attempt_push(self, position: Position, direction: str) -> bool:
        """ 
        position: 箱子当前的位置
        direction: 推动方向
        """
        new_row, new_col = self._get_new_position(position, direction)
        tile = self._get_tile(new_row, new_col)

        if not self._in_bounds(new_row, new_col):
            return False
        if tile.is_blocking():
            return False
        if (new_row, new_col) in self._entities:
            return False

        crate_strength = self._entities.get(position).get_strength()
        if crate_strength > self._player.get_strength():
            return False

        crate = self._entities.pop(position)

        # 如果箱子正好推动到未填充的目标上，则目标被填充，不再存放箱子
        if tile.get_type() == GOAL and not tile.is_filled():
            tile.fill()
            self._last_state['last_filled'] = (new_row, new_col)
            return True

        self._entities[(new_row, new_col)] = crate
        return True

    def _handle_potion(self, position: tuple[int, int]) -> None:
        """ 处理药水的效果，将药水效果应用到玩家身上
        position: 药水所在的位置
        """
        potion = self._entities.pop(position)
        self._player.apply_effect(potion.effect())