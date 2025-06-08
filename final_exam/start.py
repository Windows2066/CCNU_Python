from tkinter import messagebox, filedialog
from typing import Callable
from model import SokobanModel, Tile, Entity
from head import *
from paint import *
from gen import *

# -----------------------------------------------------------------------------
# FancyGameView 类：负责显示游戏界面的迷宫、实体和玩家图像
# -----------------------------------------------------------------------------
class FancyGameView(AbstractGrid):
    def __init__(
        self,
        master: tk.Frame | tk.Tk,
        dimensions: tuple[int, int],
        size: tuple[int, int],
        **kwargs
    ) -> None:
        """
        dimensions: 网格的行数和列数
        size: 网格的尺寸
        """
        super().__init__(
            master,
            dimensions,
            size
        )
        self._image_cache = {}

    def display(
        self,
        maze: Grid,
        entities: Entities,
        player_position: Position
    ):
        """
        maze: 迷宫，每个元素为瓷砖对象
        entities: 保存迷宫中各实体的位置信息
        player_position: 玩家当前所在的位置
        """
        self.clear()
        cell_width, cell_height = self.get_cell_size()

        for row, line in enumerate(maze):
            for col, tile in enumerate(line):
                type_ = maze[row][col]
                str_type_ = type_.get_type()
                if str_type_ == FLOOR:
                    image_name = 'images/Floor.png'
                elif str_type_ == WALL:
                    image_name = 'images/W.png'
                elif str_type_ == GOAL:
                    if type_.is_filled():
                        image_name = 'images/X.png'
                    else:
                        image_name = 'images/G.png'
                image = get_image(image_name, (cell_width, cell_height), self._image_cache)
                x, y = self.get_midpoint((row, col))
                self._image_cache[image_name] = image
                self.create_image(x, y, image=image)
        #
        # 绘制实体（例如箱子和药水）
        for position, entity in entities.items():
            str_type_ = entity.get_type()

            if str_type_ == CRATE:
                image_name = 'images/C.png'
            elif str_type_ == FANCY_POTION:
                image_name = 'images/F.png'
            elif str_type_ == MOVE_POTION:
                image_name = 'images/M.png'
            elif str_type_ == STRENGTH_POTION:
                image_name = 'images/S.png'
            elif str_type_ == "$":
                image_name = 'images/$.png'

            image = get_image(image_name, (cell_width, cell_height), self._image_cache)
            x, y = self.get_midpoint(position)
            self.create_image(x, y, image=image)
            self._image_cache[image_name] = image
            if str_type_ == CRATE:
                strength = entity.get_strength()
                self.annotate_position((position[0], position[1]), text=str(strength), font=CRATE_FONT)

        player_image_name = 'images/P.png'
        player_image = get_image(player_image_name, (cell_width, cell_height), self._image_cache)
        self._image_cache[player_image_name] = player_image
        x, y = self.get_midpoint(player_position)
        self.create_image(x, y, image=player_image)


# -----------------------------------------------------------------------------
# FancyStatsView 类：用于显示玩家状态统计信息
# -----------------------------------------------------------------------------
class FancyStatsView(AbstractGrid):
    def __init__(self, master: tk.Tk or tk.Frame) -> None:
        super().__init__(master, (3, 3), (660, STATS_HEIGHT))

    def draw_stats(self, moves_remaining: int, strength: int, money: int) -> None:
        """
        moves_remaining: 玩家剩余步数
        strength: 玩家力量
        money: 玩家金钱数
        """
        self.clear()

        self.annotate_position((0, 1), text="玩家状态", font=('Arial', 18, 'bold'))

        self.annotate_position((1, 0), text="剩余步数:")
        self.annotate_position((1, 1), text="力量:")
        self.annotate_position((1, 2), text="金钱:")

        self.annotate_position((2, 0), text=str(moves_remaining))
        self.annotate_position((2, 1), text=str(strength))
        self.annotate_position((2, 2), text="$" + str(money))


# -----------------------------------------------------------------------------
# Shop 类：商店界面，提供购买药水等物品的功能
# -----------------------------------------------------------------------------
class Shop(tk.Frame):
    def __init__(self, master: tk.Frame) -> None:
        super().__init__(master,)

        # 设置商店区域尺寸
        self.config(width=SHOP_WIDTH, height=MAZE_SIZE)

        self.title_label = tk.Label(self, text="商店", font=FONT)
        self.title_label.pack(side=tk.TOP)

    def create_buyable_item(self, item: str, amount: int, callback: Callable[[], None]
    ) -> None:
        """
        item: 物品标识符（如 S, M, F）
        amount: 物品的购买价格
        callback: 当物品被购买时调用的回调函数
        """
        if item.upper() == "S":
            good = '力量药水'
        elif item.upper() == "M":
            good = '增加步数'
        elif item.upper() == 'F':
            good = '魔法药水'

        label_text = f"{good}: ${amount}"

        # 创建一个用于显示物品信息的框架
        frame = tk.Frame(self, width=SHOP_WIDTH, height=30, bg='red')
        frame.pack()
        frame.pack_propagate(False)
        item_label = tk.Label(frame, text=label_text, width=20, height=30)
        item_label.pack(side=tk.LEFT)

        buy_button = tk.Button(frame, text="购买", command=lambda: callback(item), width=7, height=20, bg='white')
        buy_button.pack(side=tk.RIGHT)


# -----------------------------------------------------------------------------
# FancySokobanView 类：整体游戏界面的布局与各部分组件整合
# -----------------------------------------------------------------------------
class FancySokobanView:
    def __init__(self, master: tk.Tk, dimensions: tuple[int, int], size: tuple[int, int]) -> None:
        """
        初始化 FancySokobanView，同时构建整个游戏界面和布局。
        dimensions: 迷宫的行列数
        size: 迷宫区域的尺寸
        """
        global banner_image
        banner_image = get_image('images/banner.png', size=(660, BANNER_HEIGHT))
        title_banner = tk.Label(master, image=banner_image)
        title_banner.pack()

        # 创建游戏区域及统计区域的框架
        self.frame_2 = tk.Frame(master, width=660, height=MAZE_SIZE)
        self.frame_2.pack()
        self.frame_3 = tk.Frame(master, width=660, height=STATS_HEIGHT)
        self.frame_3.pack()

        # 初始化游戏画面视图
        self.F_G_view = FancyGameView(self.frame_2, dimensions=dimensions, size=(MAZE_SIZE, MAZE_SIZE))
        self.F_G_view.pack(side=tk.LEFT)

        # 初始化商店界面
        self.shop = Shop(self.frame_2)
        self.shop.pack_propagate(0)
        self.shop.pack(side=tk.RIGHT)

        # 初始化玩家统计视图
        self.F_S_view = FancyStatsView(self.frame_3)
        self.F_S_view.pack(side=tk.BOTTOM)

    def display_game(self, maze: Grid, entities: Entities, player_position: Position) -> None:
        """
        绘制当前游戏迷宫和实体状态。
        maze: 当前迷宫瓷砖二维列表
        entities: 当前迷宫中所有实体及其位置
        player_position: 玩家当前位置
        """
        self.F_G_view.clear()
        self.F_G_view.display(maze, entities, player_position)

    def display_stats(self, moves: int, strength: int, money: int) -> None:
        """
        绘制玩家统计数据。
        moves: 剩余步数
        strength: 玩家力量
        money: 玩家金钱
        """
        self.F_S_view.clear()
        self.F_S_view.draw_stats(moves, strength, money)

    def create_shop_items(self, shop_items: dict[str, int], button_callback: Callable[[str], None] | None = None) -> None:
        """
        根据传入的商品字典创建商店物品。
        shop_items: key为商品标识，val为价格
        button_callback: 商品购买时回调函数
        """
        # print(shop_items.items())
        for key, value in shop_items.items():
            self.shop.create_buyable_item(key, value, button_callback)


# -----------------------------------------------------------------------------
# ExtraFancySokoban 类：主要控制游戏逻辑与事件处理
# -----------------------------------------------------------------------------
class ExtraFancySokoban:
    def __init__(self, root: tk.Tk, maze_file: str) -> None:
        """
        加载模型并设置界面交互事件。
        maze_file: 迷宫数据文件路径
        """
        self.root = root
        # 初始化游戏模型
        self.model = SokobanModel(maze_file=maze_file)
        # 初始化游戏界面视图
        self.SokobanView = FancySokobanView(self.root, self.model.get_dimensions(), size=(MAZE_SIZE, MAZE_SIZE))

        self.redraw()

        # 在商店中显示可购买物品
        self.SokobanView.create_shop_items(self.model.get_shop_items(), self.create_shop_event)

        # 创建菜单栏
        self.create_menu()

        # 绑定键盘事件监听
        self.root.bind('<KeyPress>', self.handle_keypress)

    def create_menu(self):
        """
        创建程序菜单栏，包括保存和加载功能。
        """
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menuFile = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='文件', menu=self.menuFile)
        self.menuFile.add_command(label='保存', command=self.save_file)
        self.menuFile.add_command(label='加载', command=self.load_file)

    def save_file(self):
        """
        将当前游戏状态保存到文件中。
        """
        filename = filedialog.asksaveasfilename()
        entities = self.model.get_entities()
        strength = self.model.get_player_strength()
        moves_remaining = self.model.get_player_moves_remaining()
        player_position = self.model.get_player_position()
        maze = self.model.get_maze()

        new_maze = []

        # 将迷宫瓷砖对象转换为类型标识符组成的二维列表
        for m in maze:
            new_maze.append([i.get_type() for i in m])

        # 将实体信息写入迷宫数据中，若为箱子则保存其力量值
        for key, value in entities.items():
            if value.get_type() == CRATE:
                new_maze[key[0]][key[1]] = str(value.get_strength())
            else:
                new_maze[key[0]][key[1]] = value.get_type()

        # 标记玩家位置
        new_maze[player_position[0]][player_position[1]] = "P"

        with open(filename + '.txt', 'w', encoding='utf-8') as f:
            f.write(f"{strength} {moves_remaining}\n")
            for m in new_maze:
                f.write(''.join(m))
                f.write('\n')

    def load_file(self) -> None:
        """
        从文件加载游戏状态，并重新绘制界面。
        """
        file = filedialog.askopenfilename()
        self.model = SokobanModel(maze_file=file)
        self.redraw()

    def redraw(self):
        """
        重绘游戏界面，包括迷宫和统计信息。
        """
        self.SokobanView.display_game(maze=self.model.get_maze(), entities=self.model.get_entities(),
                                      player_position=self.model.get_player_position())
        self.SokobanView.display_stats(self.model.get_player_moves_remaining(), self.model.get_player_strength(),
                                       self.model.get_player_money())

    def continue_game(self, flag):
        result = messagebox.askyesno('', message=f'你{flag}了! 继续玩吗？')
        if result:
            save_map_to_file(generate_solvable_map(10, 10, 2, wall_prob=0.2), filename='random.txt')
            self.model.reset()
            self.redraw()
        else:
            self.root.destroy()

    def handle_keypress(self, event: tk.Event) -> None:
        """
        处理键盘输入事件，根据方向键或撤销键更新游戏状态。
        Tkinter 键盘事件
        """
        char = event.char.lower()
        if char in [UP, DOWN, LEFT, RIGHT]:
            self.model.attempt_move(char)
            self.redraw()
            if self.model.has_won():
                self.continue_game('赢')
            elif self.model.get_player_moves_remaining() == 0:
                self.continue_game('输')
        elif char == 'u':
            self.model.undo_move()
            self.redraw()
        else:
            pass

    def create_shop_event(self, item_id: str):
        """
        商店购买事件，根据物品标识购买相应道具。
        item_id: 物品标识符（例如 “S”, “M”, “F”）
        """
        self.model.attempt_purchase(item_id)
        self.redraw()

def play_game(root: tk.Tk, maze_file: str) -> None:
    root.title(string="推箱子")
    ExtraFancySokoban(root, maze_file)
    root.mainloop()


def main() -> None:
    root = tk.Tk()

    width = 660
    height = 600

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)
    save_map_to_file(generate_solvable_map(10, 10, 2, wall_prob=0.2), filename='random.txt')
    file = './maze_files/random.txt'

    play_game(root, file)


if __name__ == "__main__":
    main()