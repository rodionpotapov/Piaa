import math
import sys
import random
import time
import heapq
import matplotlib.pyplot as plt
sys.setrecursionlimit(10**7)

####################################################
# Генерация матриц
####################################################
def generate_random_symmetric_matrix(synthetic, n, low=1, high=25):
    if synthetic == 1:
        matrix = [[-1 if i == j else 0 for j in range(n)] for i in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                value = random.uniform(low, high)
                matrix[i][j] = value
                matrix[j][i] = value
        return matrix
    return [[-1 if i == j else random.uniform(low, high) for j in range(n)] for i in range(n)]

####################################################
# 1) Branch & Bound (две нижние оценки)
####################################################
def prim_mst(n, dist, nodes):
    """Вспомогательная функция: вес MST для подмножества nodes."""
    if len(nodes) == 0:
        return 0
    
    INF = math.inf
    visited = [False] * n
    min_edge = [INF] * n
    min_edge[nodes[0]] = 0
    mst_weight = 0.0
    
    for _ in range(len(nodes)):
        u = -1
        for node in nodes:
            if not visited[node] and (u == -1 or min_edge[node] < min_edge[u]):
                u = node
        
        if u == -1:
            return INF
        
        visited[u] = True
        mst_weight += min_edge[u]
        
        for v in nodes:
            if not visited[v] and dist[u][v] != -1 and dist[u][v] < min_edge[v]:
                min_edge[v] = dist[u][v]
    
    return mst_weight

def two_min_edges_sum(n, dist, nodes):
    """Вспомогательная функция: полусумма двух мин. рёбер на каждую вершину."""
    total = 0.0
    for c in nodes:
        edges_from_c = [dist[c][j] for j in range(n) if j != c and dist[c][j] != -1]
        if len(edges_from_c) < 2:
            return math.inf
        edges_from_c.sort()
        total += edges_from_c[0] + edges_from_c[1]
    return total / 2

def solve_tsp_bb(n, dist):
    """Метод ветвей и границ (Branch & Bound) с двумя нижними оценками."""
    INF = math.inf
    
    # Для эвристики (очереди) найдём min_edges[i] = минимальное ребро из i
    min_edges = []
    for i in range(n):
        m = INF
        for j in range(n):
            if j != i and dist[i][j] != -1 and dist[i][j] < m:
                m = dist[i][j]
        min_edges.append(m)
    
    best_cost = [INF]
    best_route = [[]]
    iteration_count = [0]
    pruning_count = [0]
    
    def lower_bound(current_city, current_cost, visited):
        remaining_nodes = [c for c in range(n) if c not in visited]
        
        # Оценка 1
        first_estimate = two_min_edges_sum(n, dist, remaining_nodes)
        
        # Оценка 2 (MST + 2 рёбра)
        if len(remaining_nodes) == 0:
            mst_part = 0
        else:
            mst_part = prim_mst(n, dist, remaining_nodes)
            if mst_part == INF:
                return INF
            outgoing = [dist[current_city][c] for c in remaining_nodes if dist[current_city][c] != -1]
            incoming = [dist[c][0] for c in remaining_nodes if dist[c][0] != -1]
            if not outgoing or not incoming:
                return INF
            mst_part += min(outgoing) + min(incoming)
        
        return current_cost + max(first_estimate, mst_part)
    
    def branch_and_bound(current, visited, path, cost):
        iteration_count[0] += 1
        
        if len(visited) == n:
            if dist[current][0] != -1:
                final_cost = cost + dist[current][0]
                if final_cost < best_cost[0]:
                    best_cost[0] = final_cost
                    best_route[0] = path + [0]
            return
        
        bound = lower_bound(current, cost, visited)
        if bound >= best_cost[0]:
            pruning_count[0] += 1
            return
        
        candidates = []
        for next_city in range(n):
            if next_city not in visited and dist[current][next_city] != -1:
                heuristic = dist[current][next_city] + min_edges[next_city]
                heapq.heappush(candidates, (heuristic, next_city))
        
        # Проходим кандидатов
        while candidates:
            _, nxt = heapq.heappop(candidates)
            new_cost = cost + dist[current][nxt]
            if new_cost < best_cost[0]:
                branch_and_bound(nxt, visited | {nxt}, path + [nxt], new_cost)
    
    # Запуск
    branch_and_bound(0, {0}, [0], 0.0)
    
    if best_cost[0] == INF:
        return None, math.inf
    else:
        return best_route[0], best_cost[0]


####################################################
# 2) Приближённый алгоритм "ближайшего соседа"
####################################################
def nearest_neighbor_tsp(n, dist):
    """Простой жадный метод: всегда идти в ближайший непосещённый город."""
    visited = [False] * n
    path = [0]  
    visited[0] = True
    total_cost = 0.0

    for _ in range(n - 1):
        current_city = path[-1]
        min_dist = math.inf
        next_city = -1

        for j in range(n):
            if not visited[j] and dist[current_city][j] != -1 and dist[current_city][j] < min_dist:
                min_dist = dist[current_city][j]
                next_city = j

        if next_city == -1:  # тупик
            return None, math.inf

        total_cost += min_dist
        path.append(next_city)
        visited[next_city] = True

    # возвращаемся в 0
    if dist[path[-1]][0] == -1:
        return None, math.inf
    total_cost += dist[path[-1]][0]
    path.append(0)
    return path, total_cost

####################################################
# 3) Приближённый алгоритм "MST + обход"
####################################################
def build_mst_for_all(n, dist):
    INF = math.inf
    adj = [[INF]*n for _ in range(n)]
    
    # Преобразуем dist в "симметричную" adj
    for i in range(n):
        for j in range(n):
            if i == j or (dist[i][j] == -1 and dist[j][i] == -1):
                adj[i][j] = INF
            else:
                c1 = dist[i][j] if dist[i][j] != -1 else INF
                c2 = dist[j][i] if dist[j][i] != -1 else INF
                adj[i][j] = min(c1, c2)
    
    visited = [False]*n
    min_edge = [INF]*n
    parent = [-1]*n
    min_edge[0] = 0
    
    for _ in range(n):
        u = -1
        for i in range(n):
            if not visited[i] and (u == -1 or min_edge[i] < min_edge[u]):
                u = i
        if u == -1 or min_edge[u] == INF:
            break
        visited[u] = True
        for v in range(n):
            if not visited[v] and adj[u][v] < min_edge[v]:
                min_edge[v] = adj[u][v]
                parent[v] = u
    
    # Список смежности MST
    mst_graph = [[] for _ in range(n)]
    for v in range(1, n):
        p = parent[v]
        if p != -1:
            w = adj[p][v]
            mst_graph[p].append((v, w))
            mst_graph[v].append((p, w))
    return mst_graph

def dfs_mst(u, mst_graph, visited, order):
    visited[u] = True
    order.append(u)
    for (nx, w) in mst_graph[u]:
        if not visited[nx]:
            dfs_mst(nx, mst_graph, visited, order)

def mst_approx_tsp(n, dist):
    """2-приближённый алгоритм: строим MST, делаем DFS, превращаем в тур."""
    mst_g = build_mst_for_all(n, dist)
    visited_dfs = [False]*n
    order = []
    dfs_mst(0, mst_g, visited_dfs, order)
    
    # Убираем повторы в порядке первого появления
    seen = set()
    path = []
    for city in order:
        if city not in seen:
            path.append(city)
            seen.add(city)
    path.append(0)  # замыкаем
    
    # Считаем стоимость пути
    total_cost = 0.0
    for i in range(len(path)-1):
        c1 = path[i]
        c2 = path[i+1]
        if dist[c1][c2] == -1:
            return None, math.inf
        total_cost += dist[c1][c2]
    
    return path, total_cost

def main():
    n = int(input("Введите число городов n: "))
    dist = generate_random_symmetric_matrix(0,n)
    
    print("\nМатрица расстояний:")
    for row in dist:
        print([f"{x:.2f}" if x != -1 else "-1" for x in row])
    
    # 1) Branch & Bound
    start = time.time()
    path_bb, cost_bb = solve_tsp_bb(n, dist)
    time_bb = time.time() - start
    
    if path_bb is None:
        print("\nМетод ветвей и границ: Не удалось построить путь.")
    else:
        print("\nМетод ветвей и границ (Branch&Bound):")
        print("  Маршрут:", " → ".join(map(str, path_bb)))
        print(f"  Стоимость: {cost_bb:.2f}")
        print(f"  Время: {time_bb:.4f} c")
    
    # 2) Ближайший сосед
    start = time.time()
    path_nn, cost_nn = nearest_neighbor_tsp(n, dist)
    time_nn = time.time() - start
    
    if path_nn is None:
        print("\nБлижайший сосед: Не удалось построить путь.")
    else:
        print("\nБлижайший сосед (Nearest Neighbor):")
        print("  Маршрут:", " → ".join(map(str, path_nn)))
        print(f"  Стоимость: {cost_nn:.2f}")
        print(f"  Время: {time_nn:.4f} c")
    
    # 3) MST + DFS
    start = time.time()
    path_mst, cost_mst = mst_approx_tsp(n, dist)
    time_mst = time.time() - start
    
    if path_mst is None:
        print("\nАМР (MST + DFS): Не удалось построить путь.")
    else:
        print("\nАМР (MST + DFS):")
        print("  Маршрут:", " → ".join(map(str, path_mst)))
        print(f"  Стоимость: {cost_mst:.2f}")
        print(f"  Время: {time_mst:.4f} c")
    
    # Выводим сравнение
    print("\nСравнение (для n=%d):" % n)
    if path_bb is not None:
        print(f"  Branch&Bound:   cost={cost_bb:.2f}, time={time_bb:.4f}")
    if path_nn is not None:
        print(f"  NearestNeighbor: cost={cost_nn:.2f}, time={time_nn:.4f}")
    if path_mst is not None:
        print(f"  MST-Approx:      cost={cost_mst:.2f}, time={time_mst:.4f}")
    
    max_n = min(n, 12) 
    ns = list(range(3, max_n+1))
    
    times_bb = []
    times_nn = []
    times_mst= []
    
    for cur_n in ns:
        test_dist = generate_random_symmetric_matrix(0,cur_n)
        
        # Branch&Bound
        start = time.time()
        _, _ = solve_tsp_bb(cur_n, test_dist)
        times_bb.append(time.time() - start)
        
        # Nearest neighbor
        start = time.time()
        _, _ = nearest_neighbor_tsp(cur_n, test_dist)
        times_nn.append(time.time() - start)
        
        # MST-based
        start = time.time()
        _, _ = mst_approx_tsp(cur_n, test_dist)
        times_mst.append(time.time() - start)
        
        print(f"n={cur_n} => BB={times_bb[-1]:.4f}  NN={times_nn[-1]:.4f}  MST={times_mst[-1]:.4f}")
    
    plt.figure(figsize=(8,6))
    plt.plot(ns, times_bb, 'r-o', label='Branch & Bound')
    plt.plot(ns, times_nn, 'g-o', label='Nearest Neighbor')
    plt.plot(ns, times_mst,'b-o', label='MST Approx')
    plt.xlabel("Число городов (n)")
    plt.ylabel("Время (с)")
    plt.title("Сравнение времени работы: B&B vs NN vs MST-Approx")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()