def main():
    # Ввод стоимостей операций
    cost_replace, cost_insert, cost_delete, cost_delete2 = map(float, input().split())

    # Ввод строк A и B
    A = input().strip()
    B = input().strip()

    n = len(A)
    m = len(B)

    # Базовые случаи
    if n == 0:
        print(int(m * cost_insert) if (m * cost_insert).is_integer() else m * cost_insert)
        return
    if m == 0:
        print(int(n * cost_delete) if (n * cost_delete).is_integer() else n * cost_delete)
        return

    # Инициализация DP-массивов
    dp_prev2 = [j * cost_insert for j in range(m + 1)]
    dp_prev1 = [0] * (m + 1)
    dp_prev1[0] = cost_delete  # Стоимость удаления первого символа A

    # Заполнение для i=1
    for j in range(1, m + 1):
        delete_cost = dp_prev2[j] + cost_delete
        insert_cost = dp_prev1[j - 1] + cost_insert
        if A[0] == B[j - 1]:
            replace_cost = dp_prev2[j - 1]
        else:
            replace_cost = dp_prev2[j - 1] + cost_replace
        dp_prev1[j] = min(delete_cost, insert_cost, replace_cost)

    if n == 1:
        result = dp_prev1[m]
        print(int(result) if result.is_integer() else result)
        return

    # Основной цикл для i >= 2
    for i in range(2, n + 1):
        current = [0] * (m + 1)
        # Обработка j=0
        delete2_val = float('inf')
        if i >= 2 and A[i - 2] != A[i - 1]:
            delete2_val = dp_prev2[0] + cost_delete2
        current[0] = min(i * cost_delete, delete2_val)

        # Обработка j >= 1
        for j in range(1, m + 1):
            delete1 = dp_prev1[j] + cost_delete
            insert = current[j - 1] + cost_insert
            if A[i - 1] == B[j - 1]:
                replace_val = dp_prev1[j - 1]
            else:
                replace_val = dp_prev1[j - 1] + cost_replace
            delete2_val = float('inf')
            if i >= 2 and A[i - 2] != A[i - 1]:
                delete2_val = dp_prev2[j] + cost_delete2
            current[j] = min(delete1, insert, replace_val, delete2_val)

        dp_prev2 = dp_prev1
        dp_prev1 = current

    result = dp_prev1[m]
    print(int(result) if result.is_integer() else result)


if __name__ == "__main__":
    main()