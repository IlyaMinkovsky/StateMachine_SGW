import pprint
from itertools import *
from collections import defaultdict

#Тому, кто собрался читать этот код, максимально НЕ завидую!
# Писала нечитабильно и даже не оптимально!
#Входные данные -> внутри кода переписать транспонированно заданную матрицу.
# Да, буквально транспонированную.
#Уж извините, что не доведено до идеала. Удачи!

# table = {
#     'a1': [('-', '-'), ('a5', '-'), ('-', '-'), ('a1', 'w1')],
#     'a2': [('-', 'w2'), ('-', '-'), ('-', 'w2'), ('a6', '-')],
#     'a3': [('-', '-'), ('a5', 'w3'), ('a1', '-'), ('a1', '-')],
#     'a4': [('-', '-'), ('a5', '-'), ('a2', '-'), ('a2', '-')],
#     'a5': [('-', '-'), ('a2', '-'), ('a4', '-'), ('a4', '-')],
#     'a6': [('a2', '-'), ('-', 'w1'), ('-', '-'), ('-', 'w2')],
#     'a7': [('-', '-'), ('a6', '-'), ('a1', '-'), ('-', '-')],
#     'a8': [('a7', '-'), ('-', '-'), ('-', 'w1'), ('a8', '-')],
#     'a9': [('a6', '-'), ('a2', '-'), ('a1', '-'), ('a5', '-')]
# }
table = {
    'a1': [('a5', '-'), ('a1', 'w1'), ('-', '-'), ('-', '-')],
    'a2': [('-', '-'), ('a6', '-'), ('-', 'w1'), ('-', '-')],
    'a3': [('a5', '-'), ('-', 'w1'), ('-', '-'), ('a1', 'w1')],
    'a4': [('a5', 'w2'), ('-', '-'), ('-', '-'), ('a2', '-')],
    'a5': [('a2', '-'), ('a1', '-'), ('-', '-'), ('a4', '-')],
    'a6': [('a1', 'w1'), ('-', 'w2'), ('a2', '-'), ('-', '-')],
    'a7': [('a9', '-'), ('-', '-'), ('-', '-'), ('a1', '-')],
    'a8': [('-', '-'), ('a8', '-'), ('a6', '-'), ('-', '-')],
    'a9': [('a2', '-'), ('a5', '-'), ('a7', '-'), ('a1', '-')]
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
    # print('Эээ... дырявое какое-то покрытие попалось...')
    # print('P.S.: После дебага выяснилось, что почему-то это говно работает, поэтому, ну, ладно... Но че то странно...')
    return '-'

def help_to_find(arr):
    #print(f'cover == {cover}')
    for c in cover:
        enough = True
        for el in arr:
            if el not in c:
                enough = False
        if enough:
            return c
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
                print(f'Хуйня какая-то, не могут они склеится... {union}')
            elif len(arr_w) == 1:
                w = [el for el in arr_w][0]
            column.append([a, w])
    final_table[union] = column

print('Получаем вот такую таблицу, но НЕ СПЕШИТЕ ПЕРЕПИСЫВАТЬ:')
pprint.pprint(final_table)

print('Хотите добавить какой-нибудь столбец? Это нужно, если у вас где-то есть None... То есть столбец, который ни с кем не склеивается.')
print('\tДа - 1\n\tНет - 2')
choice = int(input())
while choice not in {1, 2}:
    print('Выберете что-то другое')
    choice = int(input())
if choice == 1:
    print('Введите номер столбца в исходной таблице')
    print('Если что, программа написана так, что добавить можно еще только один столбец')
    c = int(input())
    if c < 1 or c > len(table):
        print('Такого столбца нет')
    for k in final_table:
        if c in k:
            print(f'Так у вас есть эта колонка в склейке {k}')
    new_c = (c, )
    c = f'a{c}'
    final_table[new_c] = []
    for r in table[c]:
        new_r = []
        st, w = r[0], r[1]
        #print(f'Proba row is {int(st[1:])}, {w}')
        if st == '-':
            new_r.append(st)
        else:
            new_r.append(str(help_to_find([int(st[1:])])))
        new_r.append(w)
        final_table[new_c].append(new_r)
        #print(f'New row is {new_r}')
    for k in final_table:
        for i in range(len(final_table[k])):
            if final_table[k][i][0] == 'None':
                final_table[k][i][0] = str(new_c)
    print('Теперь табличка выглядит вот так:')
    pprint.pprint(final_table)

rename_states = {str(k): f'b{i + 1}' for i, k in enumerate(sorted(final_table.keys()))}
print(f'Заменим кортежи следущим образом:\n{rename_states}')

new_table = defaultdict(list)
output_signals = set()
for k in final_table.keys():
    new_table[rename_states[str(k)]] = []
    for row in final_table[k]:
        output_signals.add(row[1])
        new_table[rename_states[str(k)]].append([rename_states[row[0]] if row[0] != '-' else row[0], row[1]])

print(f'В итоге получаем вот такую табличку (ОБРАТИТЕ ВНИМАНИЕ, ЧТО СТОЛБЦЫ НАПИСАНЫ В ДРУГОМ ПОРЯДКЕ, ЧЕМ ВЫШЕ!!!):')
pprint.pprint(new_table)



print(f'6. Кодирование конечного автомата')
def find_power_2(x):
    power = 1
    while 2 ** power < x:
        power += 1
    return power

input_signals = {f'z{i + 1}' for i in range(len(table['a1']))}
input_codes = {f'x{i + 1}' for i in range(find_power_2(len(input_signals)))}
input_table = defaultdict(dict)
total = len(input_codes)
for i in range(find_power_2(len(input_signals))):
    x = f'x{i + 1}'
    total -= 1
    limit = 2 ** total
    cnt = 0
    cur_val = 0
    for j in range(len(table['a1'])):
        z = f'z{j + 1}'
        if 'code' not in input_table[z]:
            input_table[z]['code'] = ''
        input_table[z]['code'] += str(cur_val)
        cnt += 1
        input_table[z][x] = cur_val
        if cnt == limit:
            cur_val = (cur_val + 1) % 2
            cnt = 0
print('Таблица закодированных входных сигналов:')
pprint.pprint(input_table)


states = {st for st in rename_states.values()}
states_codes = {f'tau{i + 1}' for i in range(find_power_2(len(states)))}
states_table = defaultdict(dict)
total = len(states_codes)
for i in range(find_power_2(len(states))):
    tau = f'tau{i + 1}'
    total -= 1
    limit = 2 ** total
    cnt = 0
    cur_val = 0
    for j in range(len(states)):
        st = f'b{j + 1}'
        if 'code' not in states_table[st]:
            states_table[st]['code'] = ''
        states_table[st]['code'] += str(cur_val)
        cnt += 1
        states_table[st][tau] = cur_val
        if cnt == limit:
            cur_val = (cur_val + 1) % 2
            cnt = 0
print('Таблица закодированных состояний:')
pprint.pprint(states_table)

if '-' in output_signals:
    output_signals.remove('-')
output_codes = {f'y{i + 1}' for i in range(find_power_2(len(output_signals)))}
output_table = defaultdict(dict)
total = len(output_codes)
for i in range(find_power_2(len(output_signals))):
    y = f'y{i + 1}'
    total -= 1
    limit = 2 ** total
    cnt = 0
    cur_val = 0
    for j in range(len(output_signals)):
        w = f'w{j + 1}'
        if 'code' not in output_table[w]:
            output_table[w]['code'] = ''
        output_table[w]['code'] += str(cur_val)
        cnt += 1
        output_table[w][y] = cur_val
        if cnt == limit:
            cur_val = (cur_val + 1) % 2
            cnt = 0
print('Таблица закодированных выходных сигналов:')
pprint.pprint(output_table)
print('Верхние три таблицы передирайте без поля code. Оно мне в коде нужно')

table_jump_states = defaultdict(dict)
table_jump_outputs = defaultdict(dict)
for i in range(len(new_table)):
    st = f'b{i + 1}'
    for j in range(len(new_table[st])):
        w = f'z{j + 1}'
        row = new_table[st][j]
        new_st, new_out = row[0], row[1]
        table_jump_states[states_table[st]['code']][input_table[w]['code']] = states_table[new_st]['code'] if new_st != '-' else new_st
        table_jump_outputs[states_table[st]['code']][input_table[w]['code']] = output_table[new_out]['code'] if new_out != '-' else new_out

print('Таблица переходов для состояний (КОЛОНКИ СТОЯТ СООТВЕТСТВЕННО ПОСЛЕДНЕЙ ВЫВЕДЕННОЙ ТАБЛИЦЕ, ТИПА ГДЕ УЖЕ ЗАМЕНА НА БУКОВКИ ПРОИЗОШЛА):')
print('Как воспринимать и переписывать формат табличек?')
print('Первый ключ -- состояние, bi')
print('Второй ключ -- входной сигнал zi')
print('Иначе говорят, формат такой же как и все предыдущее время, просто закодированный')
print('Обходим по колонкам. Каждую колонку обходим сверху вниз. Вот и все.')
pprint.pprint(table_jump_states)

print('Таблица переходов для выходных сигналов:')
pprint.pprint(table_jump_outputs)

def get_T_trigger():
    T_trigger = {
        0: {0: 0, 1: 1},
        1: {1: 0, 0: 1}
    } #tau_исх: {tau_пер: phi}

    T_phi_table = defaultdict(dict)
    for st in table_jump_states:
        for z in table_jump_states[st]:
            new_st = table_jump_states[st][z]
            T_phi_table[st][z] = ''
            if new_st == '-':
                T_phi_table[st][z] += '-'
            else:
                for i in range(len(st)):
                    T_phi_table[st][z] += str(T_trigger[int(st[i])][int(new_st[i])])
    print('Таблица функций возбуждения памяти для T-триггера:')
    pprint.pprint(T_phi_table)
    return T_phi_table

def get_D_trigger():
    print('Для D-триггера таблица функций возбуждения памяти полностью совпадает с таблицей переходов для состояний')
    D_phi_table = table_jump_states.copy()
    pprint.pprint(D_phi_table)
    return D_phi_table

def get_RS_trigger():
    RS_trigger = {
        0: {
            0: {'phiR': '-', 'phiS': '0', 'code': '-0'},
            1: {'phiR': '0', 'phiS': '1', 'code': '01'}
        },
        1: {
            0: {'phiR': '1', 'phiS': '0', 'code': '10'},
            1: {'phiR': '0', 'phiS': '-', 'code': '0-'}
        }
    }
    RS_phi_table = defaultdict(dict)
    for st in table_jump_states:
        for z in table_jump_states[st]:
            new_st = table_jump_states[st][z]
            RS_phi_table[st][z] = ''
            if new_st == '-':
                RS_phi_table[st][z] += '-'
            else:
                for i in range(len(st)):
                    if i > 0:
                        RS_phi_table[st][z] += ' '
                    RS_phi_table[st][z] += str(RS_trigger[int(st[i])][int(new_st[i])]['code'])
    print('Таблица функций возбуждения памяти для RS-триггера:')
    pprint.pprint(RS_phi_table)
    for st in RS_phi_table:
        for z in RS_phi_table[st]:
            if RS_phi_table[st][z].find(' ') > -1:
                RS_phi_table[st][z] = RS_phi_table[st][z].replace(" ", '')
    #pprint.pprint(RS_phi_table)
    return RS_phi_table

print('Выберите триггер:\n\tT -- 1\n\tD -- 2\n\tRS -- 3')
trigger_number = int(input())
while trigger_number not in {1, 2, 3}:
    print('Не то выбрали, выберете еще раз')
    trigger_number = int(input())
trigger = None
if trigger_number == 1:
    trigger = get_T_trigger()
elif trigger_number == 2:
    trigger = get_D_trigger()
else:
    trigger = get_RS_trigger()

print('Для функций первая цифра в названии -- индекс сверху, вторая -- индекс снизу')
print('Не хочу гуглить, как сделать черту сверху, поэтому запись типа _х1 воспринимайте как х1 с чертой, т е отрицание х1')

def convert_by_symbol(code, sym):
    new_code = ''
    for i in range(len(code)):
        if int(code[i]) == 0:
            new_code += '_'
        new_code += sym
        new_code += str(i)
    return new_code

yij = defaultdict(str)
J = len(output_table['w1']['code'])
I = 2
for j in range(J):
    for i in range(I):
        yij[f'y{i}{j + 1}'] = ''
for st in table_jump_outputs:
    for z in table_jump_outputs[st]:
        w = table_jump_outputs[st][z]
        if w == '-':
            for j in range(J):
                i = 1
                if len(yij[f'y{i}{j + 1}']) > 0:
                    yij[f'y{i}{j + 1}'] += ' V '
                yij[f'y{i}{j + 1}'] += st
                yij[f'y{i}{j + 1}'] += z
        else:
            for j in range(J):
                for i in range(I):
                    if w[j] == '1' or (w[j] == '-' and i == 1):
                        if len(yij[f'y{i}{j + 1}']) > 0:
                            yij[f'y{i}{j + 1}'] += ' V '
                        yij[f'y{i}{j + 1}'] += st
                        yij[f'y{i}{j + 1}'] += z
for j in range(J):
    for i in range(I):
        yij[f'y{i}{j + 1}'] += ' =\n = '
for st in table_jump_outputs:
    for z in table_jump_outputs[st]:
        w = table_jump_outputs[st][z]
        if w == '-':
            for j in range(J):
                i = 1
                if yij[f'y{i}{j + 1}'][-2] != '=':
                    yij[f'y{i}{j + 1}'] += ' V '
                yij[f'y{i}{j + 1}'] += convert_by_symbol(st, 'τ')
                yij[f'y{i}{j + 1}'] += convert_by_symbol(z, 'x')
        else:
            for j in range(J):
                for i in range(I):
                    if w[j] == '1' or (w[j] == '-' and i == 1):
                        if yij[f'y{i}{j + 1}'][-2] != '=':
                            yij[f'y{i}{j + 1}'] += ' V '
                        yij[f'y{i}{j + 1}'] += convert_by_symbol(st, 'τ')
                        yij[f'y{i}{j + 1}'] += convert_by_symbol(z, 'x')
for j in range(J):
    for i in range(I):
        yij[f'y{i}{j + 1}'] = f'y{i}{j + 1} = ' + yij[f'y{i}{j + 1}']
print('Полученные функции для выходных сигналов:')
for y in yij:
    print(yij[y])

phiij = defaultdict(str)
J = len(states_table['b1']['code'])
I = 2
K = 0
if trigger_number == 3:
    K = 2
for j in range(J):
    for i in range(I):
        if K == 0:
            phiij[f'phi{i}{j + 1}'] = ''
        else:
            phiij[f'phi{i}{j + 1}{"R"}'] = ''
            phiij[f'phi{i}{j + 1}{"S"}'] = ''
for st in trigger:
    for z in trigger[st]:
        new_st = trigger[st][z]
        if new_st == '-':
            for j in range(J):
                i = 1
                if K == 0:
                    if len(phiij[f'phi{i}{j + 1}']) > 0:
                        phiij[f'phi{i}{j + 1}'] += ' V '
                    phiij[f'phi{i}{j + 1}'] += st
                    phiij[f'phi{i}{j + 1}'] += z
                else:
                    if len(phiij[f'phi{i}{j + 1}{"R"}']) > 0:
                        phiij[f'phi{i}{j + 1}{"R"}'] += ' V '
                    phiij[f'phi{i}{j + 1}{"R"}'] += st
                    phiij[f'phi{i}{j + 1}{"R"}'] += z

                    if len(phiij[f'phi{i}{j + 1}{"S"}']) > 0:
                        phiij[f'phi{i}{j + 1}{"S"}'] += ' V '
                    phiij[f'phi{i}{j + 1}{"S"}'] += st
                    phiij[f'phi{i}{j + 1}{"S"}'] += z
        else:
            if K == 0:
                for j in range(J):
                    for i in range(I):
                        if new_st[j] == '1' or (new_st[j] == '-' and i == 1):
                            if len(phiij[f'phi{i}{j + 1}']) > 0:
                                phiij[f'phi{i}{j + 1}'] += ' V '
                            phiij[f'phi{i}{j + 1}'] += st
                            phiij[f'phi{i}{j + 1}'] += z
            else:
                for j in range(J):
                    for i in range(I):
                        idx = K * j
                        if new_st[idx] == '1' or (new_st[idx] == '-' and i == 1):
                            if len(phiij[f'phi{i}{j + 1}{"R"}']) > 0:
                                phiij[f'phi{i}{j + 1}{"R"}'] += ' V '
                            phiij[f'phi{i}{j + 1}{"R"}'] += st
                            phiij[f'phi{i}{j + 1}{"R"}'] += z
                        idx += 1
                        if new_st[idx] == '1' or (new_st[idx] == '-' and i == 1):
                            if len(phiij[f'phi{i}{j + 1}{"S"}']) > 0:
                                phiij[f'phi{i}{j + 1}{"S"}'] += ' V '
                            phiij[f'phi{i}{j + 1}{"S"}'] += st
                            phiij[f'phi{i}{j + 1}{"S"}'] += z
for phi in phiij:
    phiij[phi] += ' =\n = '
for st in trigger:
    for z in trigger[st]:
        new_st = trigger[st][z]
        if new_st == '-':
            for j in range(J):
                i = 1
                if K == 0:
                    if phiij[f'phi{i}{j + 1}'][-2] != '=':
                        phiij[f'phi{i}{j + 1}'] += ' V '
                    phiij[f'phi{i}{j + 1}'] += convert_by_symbol(st, 'τ')
                    phiij[f'phi{i}{j + 1}'] += convert_by_symbol(z, 'x')
                else:
                    if phiij[f'phi{i}{j + 1}{"R"}'][-2] != '=':
                        phiij[f'phi{i}{j + 1}{"R"}'] += ' V '
                    phiij[f'phi{i}{j + 1}{"R"}'] += convert_by_symbol(st, 'τ')
                    phiij[f'phi{i}{j + 1}{"R"}'] += convert_by_symbol(z, 'x')

                    if phiij[f'phi{i}{j + 1}{"S"}'][-2] != '=':
                        phiij[f'phi{i}{j + 1}{"S"}'] += ' V '
                    phiij[f'phi{i}{j + 1}{"S"}'] += convert_by_symbol(st, 'τ')
                    phiij[f'phi{i}{j + 1}{"S"}'] += convert_by_symbol(z, 'x')
        else:
            if K == 0:
                for j in range(J):
                    for i in range(I):
                        if new_st[j] == '1' or (new_st[j] == '-' and i == 1):
                            if phiij[f'phi{i}{j + 1}'][-2] != '=':
                                phiij[f'phi{i}{j + 1}'] += ' V '
                            phiij[f'phi{i}{j + 1}'] += convert_by_symbol(st, 'τ')
                            phiij[f'phi{i}{j + 1}'] += convert_by_symbol(z, 'x')
            else:
                for j in range(J):
                    for i in range(I):
                        idx = K * j
                        if new_st[idx] == '1' or (new_st[idx] == '-' and i == 1):
                            if phiij[f'phi{i}{j + 1}{"R"}'][-2] != '=':
                                phiij[f'phi{i}{j + 1}{"R"}'] += ' V '
                            phiij[f'phi{i}{j + 1}{"R"}'] += convert_by_symbol(st, 'τ')
                            phiij[f'phi{i}{j + 1}{"R"}'] += convert_by_symbol(z, 'x')
                        idx += 1
                        if new_st[idx] == '1' or (new_st[idx] == '-' and i == 1):
                            if phiij[f'phi{i}{j + 1}{"S"}'][-2] != '=':
                                phiij[f'phi{i}{j + 1}{"S"}'] += ' V '
                            phiij[f'phi{i}{j + 1}{"S"}'] += convert_by_symbol(st, 'τ')
                            phiij[f'phi{i}{j + 1}{"S"}'] += convert_by_symbol(z, 'x')
for phi in phiij:
    phiij[phi] = f'φ{phi[3:]} = ' + phiij[phi]
print('Полученные функции для внутренних сигналов:')
for phi in phiij:
    print(phiij[phi])

print('7. Минимизация с помощью карт Карно.')
print('Ниже приведены сами карты. Без последующей минимизации. Минимизировать по картам легко. В худшем случае есть инет.')
def get_terms(s):
    return s.split(" V ")

def get_parts(term):
    idx = term.find("x")
    if idx == -1 or idx == 0:
        print("Хуйня какая-то")
        return
    if term[idx - 1] == "_":
        idx -= 1
    return term[:idx], term[idx:]

J = len(output_table['w1']['code'])
I = 2
for j in range(J):
    y0, y1 = f'y{0}{j + 1}', f'y{1}{j + 1}'
    print(f'Карта карно для y{j + 1}:')
    terms0 = get_terms(yij[y0][yij[y0].rfind(" = ") + len(" = "):])
    terms1 = get_terms(yij[y1][yij[y1].rfind(" = ") + len(" = "):])
    Carno_map = defaultdict(dict)
    uniq_xs, uniq_taus = set(), set()
    for term in terms0:
        tau, x = get_parts(term)
        uniq_taus.add(tau)
        uniq_xs.add(x)
    for term in terms1:
        tau, x = get_parts(term)
        uniq_taus.add(tau)
        uniq_xs.add(x)
    for tau in uniq_taus:
        for x in uniq_xs:
            Carno_map[tau][x] = ''
            if tau + x in terms0 and tau + x in terms1:
                Carno_map[tau][x] = '1'
            elif tau + x in terms1:
                Carno_map[tau][x] = '*'
    pprint.pprint(Carno_map)


J = len(states_table['b1']['code'])
I = 2
K = 0
if trigger_number == 3:
    K = 2
for j in range(J):
    if K == 0:
        phi0, phi1 = f'phi{0}{j + 1}', f'phi{1}{j + 1}'
        print(f'Карта карно для φ{j + 1}:')
        terms0 = get_terms(phiij[phi0][phiij[phi0].rfind(" = ") + len(" = "):])
        terms1 = get_terms(phiij[phi1][phiij[phi1].rfind(" = ") + len(" = "):])
        Carno_map = defaultdict(dict)
        uniq_xs, uniq_taus = set(), set()
        for term in terms0:
            tau, x = get_parts(term)
            uniq_taus.add(tau)
            uniq_xs.add(x)
        for term in terms1:
            tau, x = get_parts(term)
            uniq_taus.add(tau)
            uniq_xs.add(x)
        for tau in uniq_taus:
            for x in uniq_xs:
                Carno_map[tau][x] = ''
                if tau + x in terms0 and tau + x in terms1:
                    Carno_map[tau][x] = '1'
                elif tau + x in terms1:
                    Carno_map[tau][x] = '*'
        pprint.pprint(Carno_map)
    else:
        for t in "R", "S":
            phi0, phi1 = f'phi{0}{j + 1}{t}', f'phi{1}{j + 1}{t}'
            print(f'Карта карно для φ{j + 1}{t}:')
            terms0 = get_terms(phiij[phi0][phiij[phi0].rfind(" = ") + len(" = "):])
            terms1 = get_terms(phiij[phi1][phiij[phi1].rfind(" = ") + len(" = "):])
            Carno_map = defaultdict(dict)
            uniq_xs, uniq_taus = set(), set()
            for term in terms0:
                tau, x = get_parts(term)
                uniq_taus.add(tau)
                uniq_xs.add(x)
            for term in terms1:
                tau, x = get_parts(term)
                uniq_taus.add(tau)
                uniq_xs.add(x)
            for tau in uniq_taus:
                for x in uniq_xs:
                    Carno_map[tau][x] = ''
                    if tau + x in terms0 and tau + x in terms1:
                        Carno_map[tau][x] = '1'
                    elif tau + x in terms1:
                        Carno_map[tau][x] = '*'
            pprint.pprint(Carno_map)


