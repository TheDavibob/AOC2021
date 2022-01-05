import numpy as np
import common


class Position:
    def __init__(self, init_u, init_v):
        self.x = 0
        self.y = 0
        self.u = init_u
        self.v = init_v

    def step(self):
        self.x += self.u
        self.y += self.v

        print(self.x, self.y)

        self.v -= 1
        if self.u > 0:
            self.u -= 1
        elif self.u < 0:
            self.u += 1

    def reach_target(self, x_min, x_max, y_min, y_max):
        while (self.x <= x_max) and (self.y >= y_min):
            self.step()
            if (x_min <= self.x <= x_max) and (y_min <= self.y <= y_max):
                return True

        return False


def x_position(n, u_0):
    if n < u_0:
        return (u_0+1) * n - n*(n+1)//2
    else:
        return (u_0+1)**2 - (u_0+1)*(u_0+2)//2


def y_position(n, v_0):
    return (v_0+1) * n - n*(n+1)//2


def big_grid(u0_range, v0_range, n_range, x_range, y_range):
    u0 = np.arange(*u0_range)
    v0 = np.arange(*v0_range)
    n = np.arange(*n_range)

    U0 = u0[None, :]
    N = np.minimum(n[:, None], u0[None, :])
    x = N * (1 + U0) - N * (N + 1) // 2
    y = n[:, None] * (1 + v0[None, :]) - n[:, None] * (n[:, None] + 1) // 2

    y_valid = ((y >= y_range[0]) & (y <= y_range[1]))
    x_valid = ((x >= x_range[0]) & (x <= x_range[1]))

    combo_grid = np.einsum('ij,ik->ijk', x_valid, y_valid)
    successful_combos = np.where(combo_grid)
    ns = n[successful_combos[0]]
    us = u0[successful_combos[1]]
    vs = v0[successful_combos[2]]

    return ns, us, vs



if __name__ == "__main__":
    n, u, v= big_grid((0, 500), (-300, 300), (0, 500), (209, 238), (-86, -59))
    print(f"Part 1: {y_position(np.max(v), np.max(v))}")
    print(f"Part 2: {np.unique(np.vstack((u, v)), axis=1).shape[1]}")