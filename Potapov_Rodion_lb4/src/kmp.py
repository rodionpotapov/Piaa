def pi_func(pattern):
    n = len(pattern)
    pi = [0] * n
    j = 0
    print(f"Строим pi-функцию для паттерна: '{pattern}'")
    for i in range(1, n):
        # откатываем j по π, пока не совпадёт
        while j > 0 and pattern[i] != pattern[j]:
            print(f"  i={i}, символ '{pattern[i]}' != '{pattern[j]}', откатываем j: {j}={pi[j-1]}")
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            print(f"  i={i}, символ '{pattern[i]}' == '{pattern[j-1]}', увеличиваем j = {j}")
        pi[i] = j
        print(f"  pi[{i}] = {pi[i]}")
    print(f"Готовый pi-массив: {pi}\n")
    return pi

def kmp_search(text, pattern):
    m, n = len(pattern), len(text)
    print(f"Ищем паттерн '{pattern}' в тексте '{text}'")
    if m == 0:
        print("Пустой паттерн: возвращаем []\n")
        return []
    pi = pi_func(pattern)
    j = 0
    indices = []
    for i in range(n):
        print(f"Шаг i={i}, text[i]='{text[i]}', текущее j={j}")
        # откаты по pi, если не совпадает
        while j > 0 and text[i] != pattern[j]:
            print(f"несовпадение '{text[i]}' != '{pattern[j]}', откатываем j: {j}→{pi[j-1]}")
            j = pi[j - 1]
        if text[i] == pattern[j]:
            j += 1
            print(f" совпадение '{text[i]}' == '{pattern[j-1]}', j→{j}")
        # полное совпадение?
        if j == m:
            start = i - m + 1
            print(f" найдено вхождение, start={start}")
            indices.append(start)
            j = pi[j - 1]
            print(f"  после фиксации сбрасываем j→{j}")
        print()
    print(f"Найденные вхождения: {indices}\n")
    return indices

def main():
    pattern = input().rstrip("\n")
    text = input().rstrip("\n")

    if len(pattern) == 0 or len(pattern) > len(text):
        print("Паттерн пустой или длиннее текста = -1")
        print(-1)
        return

    indices = kmp_search(text, pattern)

    if not indices:
        print("Совпадений не найдено = -1")
        print(-1)
    else:
        print("Выводим все стартовые индексы через запятую:")
        print(",".join(map(str, indices)))

if __name__ == "__main__":
    main()