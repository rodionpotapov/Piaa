import sys
import random
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

def solve_square_legacy(N):
    """
    Раскладка для квадрата NxN.
    """
    if N % 2 == 0:
        half = N // 2
        return [
            (1, 1, half),
            (half + 1, 1, half),
            (1, half + 1, half),
            (half + 1, half + 1, half)
        ]
    elif N % 3 == 0:
        third = N // 3
        return [
            (1, 1, 2 * third),
            (2 * third + 1, 1, third),
            (1, 2 * third + 1, third),
            (2 * third + 1, third + 1, third),
            (third + 1, 2 * third + 1, third),
            (2 * third + 1, 2 * third + 1, third)
        ]
    else:
        grid = [[0] * N for _ in range(N)]
        best = [float('inf'), []]

        def find_empty():
            for y in range(N):
                for x in range(N):
                    if grid[y][x] == 0:
                        return x, y
            return None

        def can_place(x, y, s):
            if x + s > N or y + s > N:
                return False
            for dy in range(s):
                for dx in range(s):
                    if grid[y + dy][x + dx] != 0:
                        return False
            return True

        def place(x, y, s, value):
            for dy in range(s):
                for dx in range(s):
                    grid[y + dy][x + dx] = value

        sol = []

        def backtrack(count):
            # Отсечение
            if count >= best[0]:
                return
            
            pos = find_empty()
            if pos is None:
                best[0] = count
                best[1] = sol.copy()
                print(f"[Square Legacy] Новое лучшее решение из {count} квадратов: {best[1]}")
                return
            
            x, y = pos
            # Перебираем возможные размеры
            max_s = min(N - x, N - y, N - 1)
            for s in range(max_s, 0, -1):
                print(f"[Square Legacy] Попытка поставить квадрат со стороной {s} в ({x},{y})")
                if can_place(x, y, s):
                    print(f"[Square Legacy] Успешно поставили квадрат {s} в ({x},{y})")
                    place(x, y, s, 1)
                    sol.append((x + 1, y + 1, s))
                    print(f"[Square Legacy] Текущее частичное решение: {sol}")
                    backtrack(count + 1)
                    print(f"[Square Legacy] Убираем квадрат {sol[-1]}")
                    sol.pop()
                    place(x, y, s, 0)
                else:
                    print(f"[Square Legacy] Невозможно поставить квадрат {s} в ({x},{y})")

        a = (N + 1) // 2
        b = N - a
        pre = [(a, a, a), (N - b + 1, 1, b), (1, N - b + 1, b)]
        
        for xx, yy, ss in pre:
            place(xx - 1, yy - 1, ss, 1)

        backtrack(0)
        return pre + best[1]


def solve_tiling(N, M):
    """
    Универсальный бэктрекинг для покрытия прямоугольника N x M квадратиками.
    Добавлены логи на этапах постановки и удаления квадратов.
    """
    if N == M:
        return solve_square_legacy(N)

    swapped = False
    if M > N:
        N, M = M, N
        swapped = True

    grid = [[0]*M for _ in range(N)]
    best = [float('inf'), []]

    def find_empty():
        for y in range(N):
            for x in range(M):
                if grid[y][x] == 0:
                    return (x, y)
        return None

    def can_place(x, y, s):
        if x + s > M or y + s > N:
            return False
        for dy in range(s):
            for dx in range(s):
                if grid[y+dy][x+dx] != 0:
                    return False
        return True

    def place(x, y, s, val):
        for dy in range(s):
            for dx in range(s):
                grid[y+dy][x+dx] = val

    sol = []

    def backtrack(count):
        if count >= best[0]:
            return
        
        pos = find_empty()
        if pos is None:
            best[0] = count
            best[1] = sol[:]
            print(f"[Rect Tiling] Новое лучшее решение из {count} квадратов: {best[1]}")
            return
        
        x, y = pos
        max_s = min(M - x, N - y)
        for s in range(max_s, 0, -1):
            print(f"[Rect Tiling] Попытка поставить квадрат со стороной {s} в ({x},{y})")
            if can_place(x, y, s):
                print(f"[Rect Tiling] Успешно поставили квадрат {s} в ({x},{y})")
                place(x, y, s, 1)
                sol.append((x+1, y+1, s))
                print(f"[Rect Tiling] Текущее частичное решение: {sol}")
                backtrack(count+1)
                print(f"[Rect Tiling] Убираем квадрат {sol[-1]}")
                sol.pop()
                place(x, y, s, 0)
            else:
                print(f"[Rect Tiling] Невозможно поставить квадрат {s} в ({x},{y})")

    backtrack(0)

    if swapped:
        rotated = []
        for (x, y, s) in best[1]:
            newX = y
            newY = x
            rotated.append((newX, newY, s))
        return rotated
    else:
        return best[1]


def visualize_tiling(N, M, squares):
    """
    Рисуем итоговое покрытие (N x M) квадратами из списка squares.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, M)
    ax.set_ylim(0, N)
    for i, (x, y, s) in enumerate(squares):
        color = (random.random(), random.random(), random.random())
        rect = Rectangle((x - 1, y - 1), s, s, edgecolor='black', facecolor=color, alpha=0.6)
        ax.add_patch(rect)
        ax.text((x - 1) + s/2, (y - 1) + s/2,
                f"{i+1}", color='black', ha='center', va='center', fontsize=8)
    ax.set_aspect('equal', 'box')
    ax.invert_yaxis()
    plt.title(f"Covering a {N} x {M} rectangle with squares")
    plt.show()


if __name__ == "__main__":
    N, M = map(int, input().split())
    squares = solve_tiling(N, M)
    print('\nИтоговое решение:', squares)
    print('Количество квадратов:', len(squares))
    visualize_tiling(N, M, squares)