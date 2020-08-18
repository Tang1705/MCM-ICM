import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation


class Autocell(object):
    """
    实例化
    width : 元胞数组的宽度
    height ： 元胞数组的宽度
    从而实例化 cells 元胞数组
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = np.random.randint(0, 2, (width, height))

    """
    向周围八个格子方向滚动，并相加，得到格子周围的活着的元胞数
    周围3个重生变为1
    周围2个且为1，则为1
    """

    def next_gengeration(self):
        nbrs_count = sum(np.roll(np.roll(self.cells, n, 0), m, 1)
                         for n in (-1, 0, 1) for m in (-1, 0, 1)
                         if (n != 0 or m != 0))
        self.cells = (nbrs_count == 3) | ((self.cells == 1) & (nbrs_count == 2)).astype('int')

    """
    画元胞数组
    """
    def display_animation(self):
        plt.fig, ax = plt.subplots()
        ax.patch.set_facecolor('gray')
        ax.set_aspect('equal', 'box')


        def update_ax(i):
            ax.cla()
            label = 'timestep{0}'.format(i)
            print(label)
            ax.set_title(label)
            # plt.xticks(())
            # plt.yticks(())
            ax.xaxis.set_major_locator(plt.NullLocator())
            ax.yaxis.set_major_locator(plt.NullLocator())
            for a in range(self.width):
                for b in range(self.height):
                    color = 'gray' if not self.cells[a, b] else 'black'
                    rect = plt.Rectangle([a * 1.2 + 0.2, b * 1.2 + 2], 1, 1, facecolor=color, edgecolor=color)
                    ax.add_patch(rect)
                    ax.autoscale_view()
            self.next_gengeration()
            return ax

        anim = animation.FuncAnimation(plt.fig, update_ax, frames=np.arange(0,10), interval=100)
        plt.show()
        # 保存gif
        anim.save("./images/元胞自动机.gif", dpi=80, writer='pillow')


if __name__ == '__main__':
    autocell = Autocell(20, 20)
    autocell.display_animation()
