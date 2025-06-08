import tkinter as tk
from PIL import ImageTk, Image
from typing import Union

MAZE_SIZE = 450            # 迷宫区域的尺寸
SHOP_WIDTH = 200           # 商店区域的宽度
BANNER_HEIGHT = 75         # 标题横幅的高度
STATS_HEIGHT = 75          # 玩家统计区域的高度
FONT = ('Arial', 16, 'bold')          # 通用字体
TITLE_FONT = ('Arial', 18, 'bold')     # 标题字体
CRATE_FONT = ('Arial', 20, 'bold')      # 箱子显示数字时的字体


def get_image(
    image_name: str,
    size: tuple[int, int],
    cache: dict[str, ImageTk.PhotoImage] = None
) -> ImageTk.PhotoImage:
    """
    加载并返回指定图片，并根据给定尺寸调整大小。
    如果提供了缓存字典，则在缓存中查找图片，避免重复加载。

    image_name: 图片文件路径
    size: 图片调整后的尺寸，格式为 (宽, 高)
    cache: 存储已加载图片的缓存字典；若为 None，则不进行缓存

    返回调整大小后的图片对象（ImageTk.PhotoImage）
    """
    # 如果没有提供缓存或图片不在缓存中，则加载图片并调整大小
    if cache is None or image_name not in cache:
        image = ImageTk.PhotoImage(image=Image.open(image_name).resize(size))
        if cache is not None:
            cache[image_name] = image
    # 如果图片已经存在于缓存中，则直接返回缓存的图片
    elif image_name in cache:
        return cache[image_name]
    return image


class AbstractGrid(tk.Canvas):
    """
    AbstractGrid 类继承自 Tkinter 的 Canvas，提供将 Canvas 用作网格的支持，包含计算单元格大小、转换坐标等实用方法。
    """

    def __init__(
        self,
        master: Union[tk.Tk, tk.Frame],
        dimensions: tuple[int, int],
        size: tuple[int, int],
        **kwargs
    ) -> None:
        """
        构造函数：初始化一个网格型 Canvas

        dimensions: 网格的行数和列数
        size: Canvas 尺寸
        kwargs: 其他可选参数，用于传递给 Canvas 的构造函数
        """
        super().__init__(
            master,
            width=size[0] + 1,
            height=size[1] + 1,
            highlightthickness=0,
            **kwargs
        )
        self._size = size
        # 初始化网格的行列数
        self.set_dimensions(dimensions)

    def set_dimensions(self, dimensions: tuple[int, int]) -> None:
        """
        设置网格的行数和列数。

        dimensions: 网格尺寸
        """
        self._dimensions = dimensions

    def get_cell_size(self) -> tuple[int, int]:
        """
        计算并返回每个单元格的尺寸。
        返回单元格尺寸
        """
        rows, cols = self._dimensions
        width, height = self._size
        return width // cols, height // rows

    def pixel_to_cell(self, x: int, y: int) -> tuple[int, int]:
        """
        将像素坐标转换为对应的网格单元格坐标。
        x: 像素横坐标
        y: 像素纵坐标
        返回网格单元格坐标
        """
        cell_width, cell_height = self.get_cell_size()
        return y // cell_height, x // cell_width

    def get_bbox(self, position: tuple[int, int]) -> tuple[int, int, int, int]:
        """
        根据网格单元格位置计算该单元格的边界框。
        position: 单元格坐标
        返回单元格边界框(x_min, y_min, x_max, y_max)
        """
        row, col = position
        cell_width, cell_height = self.get_cell_size()
        x_min, y_min = col * cell_width, row * cell_height
        x_max, y_max = x_min + cell_width, y_min + cell_height
        return x_min, y_min, x_max, y_max

    def get_midpoint(self, position: tuple[int, int]) -> tuple[int, int]:
        """
        获取指定网格单元格中心的像素坐标。
        position: 单元格坐标
        返回网格单元格中心坐标
        """
        row, col = position
        cell_width, cell_height = self.get_cell_size()
        x_pos = col * cell_width + cell_width // 2
        y_pos = row * cell_height + cell_height // 2
        return x_pos, y_pos

    def annotate_position(
        self,
        position: tuple[int, int],
        text: str,
        font=None
    ) -> None:
        """
        在指定的网格单元格中心位置添加文本注释。
        position: 单元格坐标
        text: 要显示的文本内容
        font: 可选字体参数，默认为 None
        """
        self.create_text(self.get_midpoint(position), text=text, font=font)

    def clear(self):
        """
        清除 Canvas 上所有的绘制内容。
        """
        self.delete("all")