import pprint
from itertools import *
from collections import defaultdict

#Тому, кто собрался читать этот код, максимально НЕ завидую!
# Писала нечитабильно и даже не оптимально!
#Входные данные -> внутри кода переписать транспонированно заданную матрицу.
# Да, буквально транспонированную.
#Уж извините, что не доведено до идеала. Удачи!

table = {
    'a1': [('-', '-'), ('a5', '-'), ('-', '-'), ('a1', 'w1')],
    'a2': [('-', 'w2'), ('-', '-'), ('-', 'w2'), ('a6', '-')],
    'a3': [('-', '-'), ('a5', 'w3'), ('a1', '-'), ('a1', '-')],
    'a4': [('-', '-'), ('a5', '-'), ('a2', '-'), ('a2', '-')],
    'a5': [('-', '-'), ('a2', '-'), ('a4', '-'), ('a4', '-')],
    'a6': [('a2', '-'), ('-', 'w1'), ('-', '-'), ('-', 'w2')],
    'a7': [('-', '-'), ('a6', '-'), ('a1', '-'), ('-', '-')],
    'a8': [('a7', '-'), ('-', '-'), ('-', 'w1'), ('a8', '-')],
    'a9': [('a6', '-'), ('a2', '-'), ('a1', '-'), ('a5', '-')]
}
# table = {
#     'a1': [('a2', 'w1'), ('-', 'w2'), ('a3', '-'), ('a2', 'w1')],
#     'a2': [('a3', 'w1'), ('a5', 'w2'), ('a2', 'w1'), ('-', '-')],
#     'a3': [('a3', 'w1'), ('a4', 'w2'), ('-', '-'), ('a5', 'w1')],
#     'a4': [('-', '-'), ('a1', 'w2'), ('a2', '-'), ('-', '-')],
#     'a5': [('-', '-'), ('-', '-'), ('a1', 'w2'), ('-', '-')]
# }

n = len(table)
m = len(table['a1'])




table_1 = {}    #заносим условия
pairs = {}      #запоминаем для каждой ячейки кто сослался
stack = []
for i in range(1, n):
    for j in range(i + 1, n + 1):
        table_1[(i, j)] = set()
        equival = True
        st1, st2 = 'a' + str(i), 'a' + str(j)
        for k in range(m):
            if table[st1][k][1] == '-' or table[st2][k][1] == '-' or table[st1][k][1] == table[st2][k][1]:
                continue
            else:
                equival = False
                break
        if equival:
            abs_eq = True
            for k in range(m):
                if table[st1][k][0] != '-' and table[st2][k][0] != '-' and table[st1][k][0] != table[st2][k][0]:
                    prev_st1, prev_st2 = table[st1][k][0], table[st2][k][0]
                    prev_idx1, prev_idx2 = int(prev_st1[1]), int(prev_st2[1])
                    prev_idx1, prev_idx2 = min(prev_idx1, prev_idx2), max(prev_idx1, prev_idx2)
                    table_1[(i, j)].add((prev_idx1, prev_idx2))
                    if (prev_idx1, prev_idx2) not in pairs:
                        pairs[(prev_idx1, prev_idx2)] = set()
                    pairs[(prev_idx1, prev_idx2)].add((i, j))
                    abs_eq = False
            if abs_eq:
                table_1[(i, j)].add('V')
        else:
            table_1[(i, j)].add('X')
            stack.append((i, j))

table_2 = {pair: set() for pair in table_1}
visited = set()
while stack:
    del_pair = stack.pop()
    table_2[del_pair].add('X')
    visited.add(del_pair)
    if del_pair in pairs:
        for p in pairs[del_pair]:
            if p not in visited:
                stack.append(p)

for pair in table_1:
    if not table_2[pair]:
        table_2[pair] = table_1[pair]



print('1. Нахождение совместимых пар состояний.')
print('Таблица, столбцы и строки которой сопоставляются состояниям автомата.')
print('Воспринимать координаты клеток как (x, y)')
for pair in table_1:
    print(pair, table_1[pair])

# print('Dop Table')
# for pair in pairs:
#     print((pair), pairs[pair])

# print('Stack')
# pprint.pprint(stack)
# table_2 = {
#     (2, 3): {'V'},
#     (2, 4): {'V'},
#     (2, 5): {'V'},
#     (3, 4): {'V'},
#     (3, 5): {'V'},
#     (4, 5): {'V'},
# }

print('Таблица после проверки условий совместимости')
for pair in table_2:
    print(pair, table_2[pair])


print('2. Нахождение списка максимальных классов совместимости.')
F = set()
auxiliary_F = set()
for i in range(n - 1, 0, -1):
    f = []
    for j in range(n, i, -1):
        #print(f'Now im here -> {i}, {j}')
        #Если состояния соместимы
        if 'X' not in table_2[(i, j)]:
            f.append(j)
    last_f = set(f)
    for el in last_f:
        auxiliary_F.add(tuple(sorted([i, el])))
    #print(f'last_f: {last_f}')
    for l in range(1, len(f) + 1):
        for p in permutations(f, l):
            #print(f'perm -> {p}')
            if p in auxiliary_F:
                if p in F:
                    F.remove(p)
                for aux_l in range(1, len(p)):
                    for aux_p in permutations(p, aux_l):
                        if tuple([i] + list(aux_p)) in F:
                            F.remove(tuple([i] + list(aux_p)))
                F.add(tuple([i] + list(p)))
                auxiliary_F.add(tuple([i] + list(p)))
                for el in p:
                    if el in last_f:
                        last_f.remove(el)
    for el in last_f:
        F.add(tuple(sorted([i, el])))
    #print(F)
print(F)


print('3. Составление списка простых классов совместимости.')
print('Левая колонка -- Классы совместимости, правая -- порожденные множества.')
print('Знак О обозначает пустое множество. '
      'Если оно есть где-то, где помимо него есть и другие элементы, то его не пишем! '
      'Пустое множество присустсвует в любом множестве')
dict_3 = defaultdict(set)
conditions = set()
for cl in F:
    for l in range(len(cl), 0, -1):
        for comb in combinations(cl, l):
            comb = tuple(sorted(comb))
            if len(comb) > 1:
                for p in permutations(comb, 2):
                    if p in table_2:
                        if 'V' not in table_2[p]:
                            for el in table_2[p]:
                                dict_3[comb].add(el)
                                conditions.add(el)
                        else:
                            dict_3[comb].add('O')

            else:
                if not dict_3[comb]:
                    dict_3[comb].add('O')
for k in sorted(dict_3):
    print(k,'\t\t\t', dict_3[k])

deleted_cls = set()
for k in dict_3:
    for l in range(len(k) - 1, 0, -1):
        for comb in combinations(k, l):
            comb = tuple(sorted(comb))
            if dict_3[k] == dict_3[comb]:
                deleted_cls.add(comb)
print(f'Вычеркиваем строки: {deleted_cls}')
for cl in deleted_cls:
    dict_3.pop(cl)
print('Получаем таблицу:')
pprint.pprint(dict_3)
print('В итоге имеет следующие условия:')
print(conditions)


print('4. Нахождение минимального замкнутого покрытия')
def help4(cond, cl):
    if {*cond} <= {*cl}:
        return 'x'
    if cond in dict_3[cl]:
        return 'o'
    return ''
dict_4 = defaultdict(dict)
for cl in dict_3:
    dict_4[cl] = {
        'Состояния': {i: '' if i not in cl else 'x' for i in range(1, n + 1)},
        'Условная совместимости': {cond: help4(cond, cl) for cond in conditions}
    }
for cl in dict_4:
    print(f'Простой класс: {cl}')
    pprint.pprint(dict_4[cl])


print('\nМИНИМАЛЬНОЕ ПОКРЫТИЕ ВЫБЕРЕТЕ, ПОЖАЛУЙСТА, САМИ. ЭТО НЕ СЛОЖНО, НО Я ЕБАЛА ЭТО ПИСАТЬ')
cover = set()
help_for_in = {i: k for i, k in enumerate(dict_4)}
pprint.pprint(help_for_in)
print('Вводите циферки, которые соответствуют выбранному простому классу. '
      'Когда захотите выйти из цикла, введите цифру, которой здесь нет')
print('Вводите -> ', end='')
n = int(input())
while n in help_for_in:
    cover.add(help_for_in[n])
    print('Вводите -> ', end='')
    n = int(input())
print(f'Ну, проверьте, правильно ли вы выбрали: {cover}')

print('5. Построение минимального автомата.')
def help5(i):
    for c in cover:
        if i in c:
            return c
    print('Эээ... дырявое какое-то покрытие попалось...')
    print('P.S.: После дебага выяснилось, что почему-то это говно работает, поэтому, ну, ладно... Но че то странно...')
    return '-'

def help_to_find(arr):
    for c in cover:
        enough = True
        for el in arr:
            if el not in c:
                enough = False
        if enough:
            return  c
    print('Хуевое покрытие')

another_helper = {i: help5(i) for i in range(1, n + 1)}
final_table = defaultdict(list)
for union in cover:
    column = []
    if len(union) == 1:
        for r in table['a' + str(union)]:
            a, w = table['a' + str(union)][r]
            idx = int(a[1:])
            a = another_helper[idx]
            column.append([a, w])
    else:
        for r in range(m):
            arr_a, arr_w = set(), set()
            for c in union:
                a, w = table['a' + str(c)][r]
                if a != '-':
                    arr_a.add(int(a[1:]))
                if w != '-':
                    arr_w.add(w)
            a, w = '-', '-'
            if len(arr_a) > 0:
                a = str(help_to_find(arr_a))
            if len(arr_w) > 1:
                print(f'Хуйня какая-то, не могу они склеится... {union}')
            elif len(arr_w) == 1:
                w = [el for el in arr_w][0]
            column.append([a, w])
    final_table[union] = column

pprint.pprint(final_table)

