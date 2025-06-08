Grid = list[list['Tile']]                # 迷宫瓷砖二维列表的类型
Entities = dict[tuple[int, int], 'Entity'] 
Position = tuple[int, int]                # 位置类型，表示 (行, 列)

# 瓷砖常量定义
WALL = 'W'          # 墙壁
FLOOR = ' '         # 地板
GOAL = 'G'          # 目标：用来放置箱子的目标点
FILLED_GOAL = 'X'   # 填充后的目标，当箱子到达目标时更改为此符号

# 实体常量定义
CRATE = 'C'             # 箱子
PLAYER = 'P'            # 玩家
STRENGTH_POTION = 'S'   # 增加力量的药水
MOVE_POTION = 'M'       # 增加步数的药水
FANCY_POTION = 'F'      # 同时增加力量和步数的药水

# 移动方向常量
UP = 'w'     # 向上移动
DOWN = 's'   # 向下移动
LEFT = 'a'   # 向左移动
RIGHT = 'd'  # 向右移动

# 每个方向对应的改变值（行, 列）
DIRECTION_DELTAS = {
    UP: (-1, 0),     # 向上移动行数减少
    DOWN: (1, 0),    # 向下移动行数增加
    LEFT: (0, -1),   # 向左移动列数减少
    RIGHT: (0, 1),   # 向右移动列数增加
}


def read_file(maze_file: str) -> tuple[list[list[str]], list[int, int]]:
    """ 
    读取迷宫文件并转换为基本数据格式
    返回用简单格式表示的迷宫和一个列表，包含玩家的初始力量值和剩余步数
    """
    with open(maze_file, 'r') as file:
        lines = file.readlines()  
        # 第1行包含玩家初始状态数值，其余行代表迷宫地图数据
        maze = [list(line.strip()) for line in lines[1:]]  
        # 将第一行的数据转换成整数列表，代表玩家初始力量和步数
        player_stats = [int(item) for item in lines[0].strip().split(' ')]

    return maze, player_stats