import sys
import random
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

def solve_square_legacy(N):
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
            print(f"[Square Legacy] -> Вход в backtrack (count={count})")
            if count >= best[0]:
                print(f"[Square Legacy] Пропускаем дальнейшие шаги, так как count={count} >= {best[0]}")
                print(f"[Square Legacy] <- Выход из backtrack (count={count})")
                return
            pos = find_empty()
            if pos is None:
                best[0] = count
                best[1] = sol.copy()
                print(f"[Square Legacy] Новое лучшее решение из {count} квадратов: {best[1]}")
                print(f"[Square Legacy] <- Выход из backtrack (count={count})")
                return
            x, y = pos
            for s in range(min(N - x, N - y, N - 1), 0, -1):
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
            print(f"[Square Legacy] <- Выход из backtrack (count={count})")

        a = (N + 1) // 2
        b = N - a
        pre = [(a, a, a), (N - b + 1, 1, b), (1, N - b + 1, b)]
        for xx, yy, ss in pre:
            place(xx - 1, yy - 1, ss, 1)
        backtrack(0)
        return pre + best[1]

def solve_tiling(N, M):
    if N == M:
        return solve_square_legacy(N)
    swapped = False
    if M > N:
        N, M = M, N
        swapped = True

    if M != 0 and (N % M) == 0:
        squares = []
        k = N // M
        for i in range(k):
            y_top = i * M + 1
            squares.append((1, y_top, M))
        result = squares
    elif N == 2 * M:
        result = [(1, 1, M), (1, M + 1, M)]
    elif (N - M) > (N // 2):
        grid = [[0] * M for _ in range(N)]
        best = [float('inf'), []]

        def find_empty():
            for y in range(N):
                for x in range(M):
                    if grid[y][x] == 0:
                        return x, y
            return None

        def can_place(x, y, s):
            if x + s > M or y + s > N:
                return False
            for dy in range(s):
                for dx in range(s):
                    if grid[y + dy][x + dx] != 0:
                        return False
            return True

        def place(x, y, s, val):
            for dy in range(s):
                for dx in range(s):
                    grid[y + dy][x + dx] = val

        sol = []

        def backtrack(count):
            print(f"[Rect Tiling (branch3)] -> Вход в backtrack (count={count})")
            if count >= best[0]:
                print(f"[Rect Tiling (branch3)] Пропускаем, т.к. count={count} >= {best[0]}")
                print(f"[Rect Tiling (branch3)] <- Выход из backtrack (count={count})")
                return
            pos = find_empty()
            if pos is None:
                best[0] = count
                best[1] = sol.copy()
                print(f"[Rect Tiling (branch3)] Новое лучшее решение из {count} квадратов: {best[1]}")
                print(f"[Rect Tiling (branch3)] <- Выход из backtrack (count={count})")
                return
            x, y = pos
            max_s = min(M - x, N - y)
            for s in range(max_s, 0, -1):
                print(f"[Rect Tiling (branch3)] Попытка поставить квадрат со стороной {s} в ({x},{y})")
                if can_place(x, y, s):
                    print(f"[Rect Tiling (branch3)] Успешно поставили квадрат {s} в ({x},{y})")
                    place(x, y, s, 1)
                    sol.append((x + 1, y + 1, s))
                    print(f"[Rect Tiling (branch3)] Текущее частичное решение: {sol}")
                    backtrack(count + 1)
                    print(f"[Rect Tiling (branch3)] Убираем квадрат {sol[-1]}")
                    sol.pop()
                    place(x, y, s, 0)
                else:
                    print(f"[Rect Tiling (branch3)] Невозможно поставить квадрат {s} в ({x},{y})")
            print(f"[Rect Tiling (branch3)] <- Выход из backtrack (count={count})")

        if N >= 2 * M:
            place(0, 0, M, 1)
            sol.append((1, 1, M))
            place(0, N - M, M, 1)
            sol.append((1, N - M + 1, M))
        else:
            place(0, 0, M, 1)
            sol.append((1, 1, M))

        backtrack(len(sol))
        result = best[1]
    else:
        grid = [[0]*M for _ in range(N)]
        best = [float('inf'), []]

        def find_empty():
            for y in range(N):
                for x in range(M):
                    if grid[y][x] == 0:
                        return x, y
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
            print(f"[Rect Tiling] -> Вход в backtrack (count={count})")
            if count >= best[0]:
                print(f"[Rect Tiling] Пропускаем, т.к. count={count} >= {best[0]}")
                print(f"[Rect Tiling] <- Выход из backtrack (count={count})")
                return
            pos = find_empty()
            if pos is None:
                best[0] = count
                best[1] = sol[:]
                print(f"[Rect Tiling] Новое лучшее решение из {count} квадратов: {best[1]}")
                print(f"[Rect Tiling] <- Выход из backtrack (count={count})")
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
            print(f"[Rect Tiling] <- Выход из backtrack (count={count})")

        backtrack(0)
        result = best[1]

    if swapped:
        rotated = []
        for (x, y, s) in result:
            rotated.append((y, x, s))
        return rotated
    else:
        return result

def visualize_tiling(N, M, squares):
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
    print(f"\nИтоговое решение: {squares}")
    print("Количество квадратов:", len(squares))
    visualize_tiling(N, M, squares)