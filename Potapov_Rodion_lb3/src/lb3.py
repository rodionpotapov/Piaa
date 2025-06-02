def main():
    # Ввод стоимостей операций
    cost_replace, cost_insert, cost_delete, cost_delete2 = map(float, input().split())
    print(f"Costs: replace={cost_replace}, insert={cost_insert}, delete={cost_delete}, delete2={cost_delete2}")

    # Ввод строк A и B
    A = input().strip()
    B = input().strip()
    print(f"A = '{A}'")
    print(f"B = '{B}'")

    n = len(A)
    m = len(B)
    print(f"Lengths: n={n}, m={m}")

    # Базовые случаи
    if n == 0:
        result = m * cost_insert
        print(f"A empty → cost = {m} * {cost_insert} = {result}")
        print(int(result) if result.is_integer() else result)
        return
    if m == 0:
        result = n * cost_delete
        print(f"B empty → cost = {n} * {cost_delete} = {result}")
        print(int(result) if result.is_integer() else result)
        return

    # Инициализация DP-массивов
    dp_prev2 = [j * cost_insert for j in range(m + 1)]
    print(f"dp_prev2 (i=0): {dp_prev2}")
    dp_prev1 = [0] * (m + 1)
    dp_prev1[0] = cost_delete  # Стоимость удаления первого символа A
    print(f"dp_prev1 before filling (i=1, j=0): {dp_prev1}")

    # Заполнение для i=1
    for j in range(1, m + 1):
        delete_cost = dp_prev2[j] + cost_delete
        insert_cost = dp_prev1[j - 1] + cost_insert
        if A[0] == B[j - 1]:
            replace_cost = dp_prev2[j - 1]
        else:
            replace_cost = dp_prev2[j - 1] + cost_replace
        dp_prev1[j] = min(delete_cost, insert_cost, replace_cost)
        print(f"i=1, j={j}: delete={delete_cost}, insert={insert_cost}, replace={replace_cost} → dp_prev1[{j}]={dp_prev1[j]}")

    print(f"dp_prev1 after filling (i=1): {dp_prev1}")

    if n == 1:
        result = dp_prev1[m]
        print(f"n=1 → result = dp_prev1[{m}] = {result}")
        print(int(result) if result.is_integer() else result)
        return

    # Основной цикл для i >= 2
    for i in range(2, n + 1):
        print(f"\n--- i = {i} (A prefix: '{A[:i]}') ---")
        current = [0] * (m + 1)

        # Обработка j=0
        delete2_val = float('inf')
        if A[i - 2] != A[i - 1]:
            delete2_val = dp_prev2[0] + cost_delete2
        current[0] = min(i * cost_delete, delete2_val)
        print(f"j=0: delete_one_by_one={i}*{cost_delete}={i*cost_delete}, delete_two={delete2_val} → current[0]={current[0]}")

        # Обработка j >= 1
        for j in range(1, m + 1):
            delete1 = dp_prev1[j] + cost_delete
            insert = current[j - 1] + cost_insert
            if A[i - 1] == B[j - 1]:
                replace_val = dp_prev1[j - 1]
            else:
                replace_val = dp_prev1[j - 1] + cost_replace
            delete2_val = float('inf')
            if A[i - 2] != A[i - 1]:
                delete2_val = dp_prev2[j] + cost_delete2

            current[j] = min(delete1, insert, replace_val, delete2_val)
            print(
                f"i={i}, j={j}: delete1={dp_prev1[j]}+{cost_delete}={delete1}, "
                f"insert={current[j-1]}+{cost_insert}={insert}, "
                f"replace={'0' if A[i-1]==B[j-1] else f'{dp_prev1[j-1]}+{cost_replace}'}={replace_val}, "
                f"delete2={delete2_val} → current[{j}]={current[j]}"
            )

        print(f"current (i={i}): {current}")
        dp_prev2 = dp_prev1
        dp_prev1 = current
        print(f"dp_prev2 updated for next i: {dp_prev2}")
        print(f"dp_prev1 updated for next i: {dp_prev1}")

    result = dp_prev1[m]
    print(f"\nFinal result = dp_prev1[{m}] = {result}")
    print(int(result) if result.is_integer() else result)


if __name__ == "__main__":
    main()
