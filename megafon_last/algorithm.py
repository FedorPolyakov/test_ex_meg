import re

# КОНСТАНТЫ
ONE = 'одна'
TWO = 'две'
# словарь единиц
UNITS = {
    0: 'ноль', 1: 'один', 2: 'два', 3: 'три',
    4: 'четыре', 5: 'пять', 6: 'шесть', 7: 'семь',
    8: 'восемь', 9: 'девять'}
# словарь десятков
TENS = {
    10: 'десять', 11: 'одиннадцать',
    12: 'двенадцать', 13: 'тринадцать', 14: 'четырнадцать', 15: 'пятнадцать',
    16: 'шестнадцать', 17: 'семнадцать', 18: 'восемьнадцать', 19: 'девятнадцать',
    20: 'двадцать', 30: 'тридцать', 40: 'сорок', 50: 'пятьдесят',
    60: 'шестьдесят', 70: 'семьдесят', 80: 'вомемьдесят', 90: 'девяносто'
}
# словарь сотен
HUNDREDS = {
    100: 'сто', 200: 'двести', 300: 'триста',
    400: 'четыреста', 500: 'пятьсот', 600: 'шестьсот',
    700: 'семьсот', 800: 'восемьсот', 900: 'девятсот'
}
# словарь рублей
MONEY = ['рубля', 'рубль', 'рублей']
# словарь копеек
COINS = ['копейки', 'копейка', 'копеек']
# шкалы от тысячи до триллиона
SCALES = {
    1000: ['тысяча', 'тысячи', 'тысяч'],
    1000000: ['миллиона', 'миллион', 'миллионов'],
    1000000000: ['миллиарда', 'миллиард', 'миллиардов'],
    1000000000000: ['триллиона', 'триллион', 'триллионов']
}

def join_string_to_nums(string):
    new_str = string
    if ' ' in new_str:
        new_str.replace(' ', '')
    if ',' in new_str:
        new_str.replace(',', '.')
    return new_str


def nums_to_word_req(power, nums):
    """
    Рекурсивная функция составления числа прописью
    :param power: количество символов в числе
    :param nums: список символов чисел исходного числа
    :return: возвращает строку чисел прописью
    """
    if nums[0] == 0 and power != 1:
        nums.pop(0)
        return nums_to_word_req(power-1, nums)
    if power == 1:
        return f'{UNITS[nums.pop(0)]}'
    elif power == 2:
        if (nums[0]*10 + nums[-1]) in TENS:
            return f'{TENS[nums[0]*10 + nums[-1]]}'
        else:
            return (f'{TENS[nums.pop(0)*10]} '
                    f'{nums_to_word_req(power-1, nums)}')
    elif power == 3:
        if (nums[0]*100+nums[1]+nums[2]) in HUNDREDS:
            return f'{HUNDREDS[nums[0]*100]}'
        else:
            return (f'{HUNDREDS[nums.pop(0)*100]} '
                    f'{nums_to_word_req(power-1, nums)}')

    if power == 4:
        if nums[0] == 1:
            units = f'{ONE}'
            scales = f'{SCALES[1000][0]}'
        else:
            units = f'{TWO if nums[0] == 2 else UNITS[nums[0]]}'
            scales = f'{SCALES[1000][1] if (nums[0] <= 4 and nums[0] > 1) else SCALES[1000][2]}'
        hundreds = f'{nums_to_word_req(3, nums[1:]) if nums[1:] != [0,0,0] else ""}'
        return f'{units} {scales} {hundreds}'

    if power in [5, 8, 11, 14]:
        if nums[0]*10 + nums[1] in TENS:
            tens = f'{TENS[nums[0]*10 + nums[1]]} {SCALES[10**(power-2)][2]} ' \
                    f'{nums_to_word_req(power-2, nums[2:]) if nums[2:] != [0]*(power-2) else ""}'
        else:
            tens = f'{TENS[nums[0]*10]} {nums_to_word_req(power-1, nums[1:])}'
        return f'{tens}'
    if power in [6, 9, 12, 15]:
        return f'{HUNDREDS[nums[0]*100]} {SCALES[10**(power-3)][2]+" " if nums[1:3] == [0,0] else ""}' \
                f'{nums_to_word_req(power-1, nums[1:]) if nums[1:] != [0]*(power-1) else ""}'

    if power in [7, 10, 13]:
        units = f'{UNITS[nums[0]]}'
        hundreds = f'{nums_to_word_req(power-1, nums[1:]) if nums[1:] != [0]*(power-1) else ""}'
        if nums[0] == 1:
            return f'{units} ' \
                    f'{SCALES[10**(power-1)][1]} ' \
                    f'{hundreds}'
        else:
            return f'{units} ' \
                    f'{SCALES[10**(power-1)][0] if (nums[0]>1 and nums[0] <= 4) else SCALES[10**(power-1)][2]} ' \
                    f'{hundreds}'


def algo(input_number):
    """
    Главная функция алгоритма,
    :param input_number: принимает строку чисел
    :return: возвращает сформированную строку чисел прописью с обозначеним рублей и копеек
    """
    power = 0
    nums = []
    number = str(input_number)
    number_i = []
    number_f = []
    try:
        if '.' in number or ',' in number:
            try:
                number_i = (re.split('[.,]', number)[0])
                if ' ' in number_i:
                    number_i = int(number_i.replace(' ', ''))
                else:
                    number_i = int(number_i)
                number_f = (re.split('[.,]', number)[1])
                if ' ' in number_f:
                    number_f = str(number_f.replace(' ', ''))
                else:
                    number_f = str(number_f)
            except ValueError as e:
                return f'Введено неправильное значение'
        else:
            try:
                number_i = int(number)
                number_f = '00'
            except ValueError as e:
                return f'Введено неправильное значение'
        while True:
            try:
                number_i // 10
            except TypeError as e:
                return f'Введено неправильное значение'
            if number_i // 10 != 0:
                power += 1
                nums.append(number_i % 10)
                number_i = number_i // 10
            else:
                nums.append(number_i)
                power += 1
                nums.reverse()
                break
    except ValueError:
        power = 0
        nums.append(0)
    if power > 15:
        return f'Слишком большое число!'
    else:
        try:
            number_f = str(round(int(number_f) / (10 ** (len(number_f))), 2))[2:]
        except TypeError as e:
            return f'Введено неправильное значение'
        number_f = list(map(int, number_f))
        if len(number_f) < 2:
            number_f.append(0)
        try:
            if 10 * number_f[-2] + number_f[-1] > 9 and 10 * number_f[-2] + number_f[-1] < 20:
                string_coins = COINS[2]
            elif number_f[-1] == 1:
                string_coins = COINS[1]
            else:
                string_coins = COINS[0] if (number_f[-1] > 1 and number_f[-1] <= 4) else COINS[2]
        except IndexError as e:
            return f'Введено неправильное значение'

        number_f = "".join(list(map(str, number_f)))
        if len(nums) < 2:
            nums.insert(0, 0)
        try:
            if (10 * nums[-2] + nums[-1]) > 9 and (10 * nums[-2] + nums[-1]) < 20:
                string_money = MONEY[2]
            elif nums[-1] == 1:
                string_money = MONEY[1]
            else:
                string_money = MONEY[0] if (nums[-1] > 1 and nums[-1] <= 4) else MONEY[2]
            if nums[0] == 0:
                nums.pop(0)
            string_nums = nums_to_word_req(power, nums)
        except IndexError as e:
            return f'Введено неправильное значение'
    try:
        return f'{number} ({" ".join([string_nums])}) {" ".join([string_money, number_f, string_coins])}'
    except NameError as e:
        return f'Введено неправильное значение'


if __name__ == '__main__':
    print(algo('123.123'))
    print(algo('1.123'))
    print(algo('100101203123.123'))

