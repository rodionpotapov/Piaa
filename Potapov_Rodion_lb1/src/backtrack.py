import sys
import random
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

def solve_square_legacy(N):
    # --- 1) N % 2 == 0 ---
    if N % 2 == 0:
        half = N // 2
        squares = [
            (1, 1, half),
            (half + 1, 1, half),
            (1, half + 1, half),
            (half + 1, half + 1, half)
        ]
        # Допустим, считаем это единственным решением в контексте данного алгоритма
        return squares, len(squares), 1

    # --- 2) N % 3 == 0 ---
    elif N % 3 == 0:
        third = N // 3
        squares = [
            (1, 1, 2 * third),
            (2 * third + 1, 1, third),
            (1, 2 * third + 1, third),
            (2 * third + 1, third + 1, third),
            (third + 1, 2 * third + 1, third),
            (2 * third + 1, 2 * third + 1, third)
        ]
        return squares, len(squares), 1

    # --- 3) Общий (бэктрекинг) случай ---
    else:
        # Инициализация
        grid = [[0] * N for _ in range(N)]

        # best[0] = минимальное кол-во квадратов
        # best[1] = список квадратов (одно из лучших решений)
        # best[2] = кол-во таких решений
        best = [float('inf'), [], 0]

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
                    if grid[y+dy][x+dx] != 0:
                        return False
            return True

        def place(x, y, s, val):
            for dy in range(s):
                for dx in range(s):
                    grid[y+dy][x+dx] = val

        sol = []  # рекурсия будет хранить ТОЛЬКО дополнительные квадраты

        def backtrack(count):
            # Если уже превысили текущее лучшее
            if count > best[0]:
                return

            pos = find_empty()
            if pos is None:
                # Покрытие готово
                if count < best[0]:
                    best[0] = count
                    best[1] = sol.copy()  # копируем текущее решение
                    best[2] = 1           # сбрасываем счётчик решений
                elif count == best[0]:
                    best[2] += 1
                return

            x, y = pos
            max_s = N - 1  # теоретический максимум
            # но смысл есть не ставить квадрат больше, чем (N - x) или (N - y)
            max_s = min(max_s, N - x, N - y)

            for s in range(max_s, 0, -1):
                if can_place(x, y, s):
                    place(x, y, s, 1)
                    sol.append((x+1, y+1, s))
                    backtrack(count + 1)
                    sol.pop()
                    place(x, y, s, 0)

        #
        # Ставим "pre"-квадраты (a, b) из оригинального кода
        #
        a = (N + 1) // 2
        b = N - a
        pre = [
            (a, a, a),
            (N - b + 1, 1, b),
            (1, N - b + 1, b)
        ]
        # Помещаем их в grid
        for (xx, yy, ss) in pre:
            place(xx - 1, yy - 1, ss, 1)

        # Запускаем рекурсию с count = 0, 
        # поскольку новые квадраты (sol) пока пусты.
        backtrack(0)

        # На выходе best содержит данные о тех дополнительных квадратах,
        # которые нужны поверх pre.
        # Собираем полное решение:
        full_solution = pre + best[1]
        solution_count = len(full_solution)
        variants = best[2]

        return full_solution, solution_count, variants


def solve_tiling(N, M):
    if N == M:
        return solve_square_legacy(N)  # если квадрат
    swapped = False
    if M > N:
        N, M = M, N
        swapped = True

    if M != 0 and (N % M) == 0:
        # Случай полос
        squares = []
        k = N // M
        for i in range(k):
            y_top = i * M + 1
            squares.append((1, y_top, M))
        result = squares

    else:
        grid = [[0]*M for _ in range(N)]
        
        # best[0] = минимальное количество квадратов
        # best[1] = одно из лучших решений (список)
        # best[2] = счётчик ВСЕХ различных решений с этим количеством квадратов
        best = [float('inf'), [], 0]  # <-- Изм.

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

            # Изменяем условие с >= на >, чтобы искать другие решения с тем же числом квадратов
            if count > best[0]:  # <-- Изм.: только если count >, а не >=
                print(f"[Rect Tiling] Пропускаем, т.к. count={count} > {best[0]}")
                print(f"[Rect Tiling] <- Выход из backtrack (count={count})")
                return

            pos = find_empty()
            if pos is None:
                # Полное покрытие
                print(f"[Rect Tiling] Полное покрытие из {count} квадратов: {sol}")
                
                if count < best[0]:
                    # Нашли новое, более лучшее решение
                    best[0] = count
                    best[1] = sol.copy()
                    best[2] = 1   # сбрасываем счётчик и ставим 1, так как это первое решение такого качества
                    print(f"[Rect Tiling] Новое лучшее решение! count={count}, всего 1 решение")
                elif count == best[0]:
                    # Нашли ещё одно решение с таким же количеством квадратов
                    best[2] += 1
                    print(f"[Rect Tiling] Еще одно решение c {count} квадратами! Теперь их {best[2]}")
                    # Можно менять best[1], если хотите хранить последнее
                print(f"[Rect Tiling] <- Выход из backtrack (count={count})")
                return

            x, y = pos
            max_s = min(M - x, N - y)
            for s in range(max_s, 0, -1):
                print(f"[Rect Tiling] Попытка поставить квадрат со стороной {s} в ({x},{y})")
                if can_place(x, y, s):
                    print(f"[Rect Tiling] Успешно поставили квадрат {s} в ({x},{y})")
                    place(x, y, s, 1)
                    sol.append((x + 1, y + 1, s))
                    print(f"[Rect Tiling] Текущее решение: {sol}")
                    backtrack(count + 1)
                    print(f"[Rect Tiling] Убираем квадрат {sol[-1]}")
                    sol.pop()
                    place(x, y, s, 0)
                else:
                    print(f"[Rect Tiling] Невозможно поставить квадрат {s} в ({x},{y})")
            print(f"[Rect Tiling] <- Выход из backtrack (count={count})")

        backtrack(0)
        
        # Возвращаем best[1], но счётчик решений лежит в best[2]
        result = best[1]

    if swapped:
        rotated = []
        for (x, y, s) in result:
            rotated.append((y, x, s))
        result = rotated

    # Можно вернуть кортеж: (лучшая_укладка, количество_квадратов, число_вариантов)
    # или просто результат. Ниже — пример, как вернуть всё.
    return result, len(result), best[2]  


def visualize_tiling(N, M, squares):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, M)
    ax.set_ylim(0, N)
    for i, (x, y, s) in enumerate(squares):
        color = (random.random(), random.random(), random.random())
        rect = Rectangle((x - 1, y - 1), s, s, edgecolor='black', facecolor=color, alpha=0.6)
        ax.add_patch(rect)
        # Для наглядности нумеруем квадраты в центре
        ax.text((x - 1) + s/2, (y - 1) + s/2,
                f"{i+1}", color='black', ha='center', va='center', fontsize=8)
    ax.set_aspect('equal', 'box')
    ax.invert_yaxis()
    plt.title(f"Covering a {N} x {M} rectangle with squares")
    plt.show()


if __name__ == "__main__":
    N, M = map(int, input().split())

    # Теперь solve_tiling возвращает ТРИ значения:
    squares, count_squares, variants = solve_tiling(N, M)

    print("\nИтоговое решение:", squares)
    print("Количество квадратов в этом решении:", count_squares)
    print("Число всех таких решений с минимальным числом квадратов:", variants)

    # Визуализируем само покрытие
    visualize_tiling(N, M, squares)