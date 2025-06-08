import random
from collections import deque
import os

def get_reachable(grid, start):
    height = len(grid)
    width = len(grid[0])
    reachable = set()
    queue = deque([start])
    reachable.add(start)
    while queue:
        i, j = queue.popleft()
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < height and 0 <= nj < width:
                if grid[ni][nj] != 'W' and (ni, nj) not in reachable:
                    reachable.add((ni, nj))
                    queue.append((ni, nj))
    return reachable

def generate_random_map(width=8, height=8, num_boxes=1, wall_prob=0.2):
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    # 设置边界为墙
    for i in range(width):
        grid[0][i] = 'W'
        grid[-1][i] = 'W'
    for j in range(height):
        grid[j][0] = 'W'
        grid[j][-1] = 'W'
    # 随机添加内部障碍
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if random.random() < wall_prob:
                grid[i][j] = 'W'
    # 筛选所有非障碍位置
    candidates = [(i, j) for i in range(1, height - 1)
                         for j in range(1, width - 1) if grid[i][j] == ' ']
    if not candidates:
        return None
    # 随机选取玩家位置
    player_pos = random.choice(candidates)
    grid[player_pos[0]][player_pos[1]] = 'P'
    # 检查玩家可达区域
    reachable = get_reachable(grid, player_pos)
    required_cells = 1 + 2 * num_boxes
    if len(reachable) < required_cells:
        return None
    # 从可达区域中排除玩家，选择箱子和目标位置
    candidates_reachable = [pos for pos in reachable if pos != player_pos]
    if len(candidates_reachable) < 2 * num_boxes:
        return None
    for _ in range(num_boxes):
        box_pos = random.choice(candidates_reachable)
        grid[box_pos[0]][box_pos[1]] = '1'
        candidates_reachable.remove(box_pos)
        target_pos = random.choice(candidates_reachable)
        grid[target_pos[0]][target_pos[1]] = 'G'
        candidates_reachable.remove(target_pos)
    return grid

def parse_grid(grid):
    """
    解析地图，返回墙、箱子、目标及玩家位置。
    """
    walls = set()
    boxes = set()
    targets = set()
    player = None
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            if ch == 'W':
                walls.add((i, j))
            elif ch == '1':
                boxes.add((i, j))
            elif ch == 'G':
                targets.add((i, j))
            elif ch == 'P':
                player = (i, j)
    return walls, boxes, targets, player

def get_player_reachable(player, walls, boxes, grid_size):
    """
    内层 BFS：计算玩家在当前状态下（箱子视为障碍）可行走的区域。
    """
    height, width = grid_size
    reachable = set()
    queue = deque([player])
    reachable.add(player)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        cur = queue.popleft()
        for di, dj in directions:
            nxt = (cur[0] + di, cur[1] + dj)
            if 0 <= nxt[0] < height and 0 <= nxt[1] < width:
                if nxt not in walls and nxt not in boxes and nxt not in reachable:
                    reachable.add(nxt)
                    queue.append(nxt)
    return reachable

def check_map_solvable(grid, max_steps=1000):
    """
    使用双层 BFS 检查地图是否有解。
    """
    walls, boxes, targets, player = parse_grid(grid)
    height = len(grid)
    width = len(grid[0])
    initial_state = (player, frozenset(boxes))
    queue = deque()
    queue.append((initial_state, 0))
    visited = set([initial_state])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        (cur_player, cur_boxes), steps = queue.popleft()
        if steps > max_steps:
            break
        if set(cur_boxes) == targets:
            return steps
        reachable = get_player_reachable(cur_player, walls, cur_boxes, (height, width))
        for box in cur_boxes:
            for di, dj in directions:
                req_pos = (box[0] - di, box[1] - dj)
                new_box = (box[0] + di, box[1] + dj)
                if req_pos in reachable and new_box not in walls and new_box not in cur_boxes:
                    new_boxes = set(cur_boxes)
                    new_boxes.remove(box)
                    new_boxes.add(new_box)
                    new_state = (box, frozenset(new_boxes))
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, steps + 1))
    return -1

def generate_solvable_map(width=8, height=8, num_boxes=1, wall_prob=0.2, max_attempts=1000):
    """
    不断生成随机地图，并利用双层 BFS 检查是否有解。
    若找到可解地图则返回。
    """
    for _ in range(max_attempts):
        grid = generate_random_map(width, height, num_boxes, wall_prob)
        if grid is None:
            continue
        if check_map_solvable(grid) >= 0:
            return grid
    raise Exception("无法生成满足要求的可解地图，请调整参数。")

def print_map(grid):
    for row in grid:
        print("".join(row))

def save_map_to_file(grid, filename="generated_map.txt", save_dir=r"E:\peixun\CCNU_Python\final_exam\maze_files"):
    os.makedirs(save_dir, exist_ok=True)
    full_path = os.path.join(save_dir, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write("100 100\n")
        for row in grid:
            f.write("".join(row) + "\n")
    # print(f"地图已保存到 {full_path}")

if __name__ == "__main__":
    grid = generate_solvable_map()
    print_map(grid)
    save_map_to_file(grid)