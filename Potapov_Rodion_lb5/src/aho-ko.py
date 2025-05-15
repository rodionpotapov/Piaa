from collections import deque

class Node:
    _id_counter = 0

    def __init__(self, prefix=''):
        # Переходы по символам: буква → Node
        self.children = {}
        # Ссылка неудачи (failure link)
        self.fail = None
        # Явная терминальная ссылка (dict_link) на ближайшую вершину с непустым output
        self.dict_link = None
        # Список индексов шаблонов, которые завершаются в этой вершине
        self.output = []
        # Префикс (строка от корня до этой вершины), для отладки
        self.prefix = prefix
        # Уникальный идентификатор вершины, для отладки
        self.id = Node._id_counter
        Node._id_counter += 1


def build_trie(patterns):
    print("=== Построение бора (Trie) ===")
    root = Node(prefix='')
    for idx, pat in enumerate(patterns):
        print(f"\nВставляем шаблон #{idx+1} = '{pat}'")
        node = root
        for ch in pat:
            if ch not in node.children:
                # Создаём новую вершину, если перехода нет
                child = Node(prefix=node.prefix + ch)
                node.children[ch] = child
                print(f"  Создали вершину id={child.id}, prefix='{child.prefix}'")
            node = node.children[ch]
        # В этой вершине заканчивается шаблон idx
        node.output.append(idx)
        print(f"  Отмечаем окончание шаблона #{idx} в вершине id={node.id}, prefix='{node.prefix}'")

    # Печатаем итоговую структуру бора
    print("\n=== Итоговая структура бора ===")
    q = deque([root])
    seen = {root}
    while q:
        v = q.popleft()
        kids = {c: v.children[c].id for c in v.children}
        print(f"Вершина id={v.id}, prefix='{v.prefix}': дети={kids}, output={v.output}")
        for child in v.children.values():
            if child not in seen:
                seen.add(child)
                q.append(child)

    return root


def build_failure_links(root):
    print("\n=== Построение failure- и dict_link-ссылок ===")
    q = deque()
    root.fail = None
    root.dict_link = None  # у корня нет терминальной ссылки

    # Инициализируем первый уровень: все дети корня получают fail→root, dict_link=None
    for child in root.children.values():
        child.fail = root
        child.dict_link = None
        q.append(child)
        print(f"Устанавливаем: fail[{child.id}]='{child.prefix}' → root, dict_link[{child.id}] → None")

    # Обходим уровни в ширину
    while q:
        v = q.popleft()
        for ch, u in v.children.items():
            # находим fail для u: по символу ch из цепочки fail(v)
            f = v.fail
            while f and ch not in f.children:
                f = f.fail
            u.fail = f.children[ch] if f and ch in f.children else root

            # терминальная ссылка: если на fail-вершине есть output, оно ближайшее
            if u.fail.output:
                u.dict_link = u.fail
            else:
                u.dict_link = u.fail.dict_link

            print(f"Устанавливаем: fail[{u.id}]='{u.prefix}' → id={u.fail.id} ('{u.fail.prefix}'), "
                  f"dict_link[{u.id}] → "
                  f"{u.dict_link.id if u.dict_link else None} "
                  f"{'(->'+u.dict_link.prefix+')' if u.dict_link else ''}")

            q.append(u)

    print("=== Все ссылки установлены ===")


def aho_corasick_non_overlapping(text, patterns):
    # Шаг 1: строим бор
    root = build_trie(patterns)
    # Шаг 2: строим ссылки неудачи и терминальные ссылки
    build_failure_links(root)

    print("\n=== Поиск непересекающихся вхождений ===")
    blocked = set()   # занятые позиции в тексте
    result = []       # список найденных вхождений
    current = root

    print(f"Текст: '{text}'")
    for i, ch in enumerate(text):
        print(f"\nШаг {i+1}, символ='{ch}':")
        # 1) Пытаемся перейти по ch из current, иначе по fail
        while current and ch not in current.children:
            print(f"  Нет перехода из id={current.id}('{current.prefix}') по '{ch}', идём по fail→ "
                  f"id={current.fail.id if current.fail else None}")
            current = current.fail
        if not current:
            current = root
            print("  Достигли None, возвращаемся в корень")
        else:
            current = current.children[ch]
            print(f"  Переходим в вершину id={current.id}('{current.prefix}')")

        # 2) Собираем все найденные шаблоны: свои + через dict_link
        found = []
        # свои окончания
        if current.output:
            print(f"  Собственные окончания в этой вершине: {current.output} "
                  f"{[patterns[idx] for idx in current.output]}")
            found.extend(current.output)
        # через терминальные ссылки
        t = current.dict_link
        while t:
            print(f"  По dict_link идём в id={t.id}('{t.prefix}'), output={t.output} "
                  f"{[patterns[idx] for idx in t.output]}")
            found.extend(t.output)
            t = t.dict_link

        if not found:
            print("  Нет совпадений на этом шаге")

        # 3) Жадно берём самый приоритетный (длинный) шаблон, проверяем непересечение
        for idx in sorted(found, key=lambda idx: (-len(patterns[idx]), idx)):
            pat = patterns[idx]
            start = i - len(pat) + 1
            end = i + 1
            print(f"    Проверяем шаблон #{idx}='{pat}', диапазон [{start}..{end-1}]")
            # пропуск, если выходит за границы
            if start < 0:
                print("      Вне текста → пропускаем")
                continue
            # пропуск при пересечении
            if any(pos in blocked for pos in range(start, end)):
                print("      Пересекается с заблокированными позициями → пропускаем")
                continue
            # принимаем вхождение
            for pos in range(start, end):
                blocked.add(pos)
            result.append((start+1, idx+1))  # 1-based вывод
            print(f"      → Принято! Записываем ({start+1}, {idx+1}), блокируем {list(range(start,end))}")
            break  # после принятия одного шаблона переходим к следующему символу

        print(f"  Заблокированные позиции: {sorted(blocked)}")

    # Финальный вывод
    print("\n=== Поиск завершён. Результаты: ===")
    for pos, pid in sorted(result, key=lambda x: (x[0], x[1])):
        print(f"{pos} {pid}")

    return sorted(result, key=lambda x: (x[0], x[1]))


def main():
    text = input().strip()
    n = int(input())
    patterns = [input().strip() for _ in range(n)]
    aho_corasick_non_overlapping(text, patterns)

if __name__ == "__main__":
    main()
