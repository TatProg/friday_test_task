def main():
    rows = int(input('Rows: '))
    cols = int(input('Columns: '))
    # создание двумерного массива размерности cols x rows
    arr = [[int(input()) for i in range(cols)] for j in range(rows)]

    for row in arr:
        print(row)

    print('Count rows with zeros: ')
    # подсчет числа ненулевых строк
    print(len([i for i in arr if 0 not in i]))

    n = int(input('Maximum search row: '))
    # Получение максимального числа в введенной строке
    print(f'Max in {n} row: {max(arr[n])}')


if __name__ == '__main__':
    main()
