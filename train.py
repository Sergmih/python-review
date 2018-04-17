import argparse
import re
import os
from sys import stdin
from collections import defaultdict


def create_model(current_str, islow, model_dict):
    """Функция создания модели, принимает на вход 3 агрумента:
       1) current_str - str, переменная в котрой хранится последнее слово предыдущей строки
       2) islow - bool, проверка нужно ли приводить к нижнему регистру, True - если нужно
       3) model_dict - defaultdict(defaultdict(int)), словарь с моделью
       Функция возвращает последнее слово в текущей строке (str)
       """
    if islow:
        current_str = current_str.lower()
    words = re.findall(r'\w+', current_str)
    """Парсим строку, оставляем только буквы, приводим к нижнему регистру если нужно"""
    for x in range(0, len(words) - 1):
        """Составляем словарь с моделью, для каждого слова свой подсловарь в котором частота вхождений других слов после 
           текущего. Записываем эту частоту"""
        model_dict[words[x]][words[x + 1]] += 1
    """Возвращаем последнее слово строки, чтобы связать его с первым словом следующей строки"""
    return words[len(words) - 1]


parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', dest='dir', default='stdin', help='directory path')
parser.add_argument('--model', dest='model',required=True, help='path to file with model')
parser.add_argument('--lc', action = 'store_true', help='is lowercase?')

model_dict = defaultdict(lambda: defaultdict(int))
if parser.parse_args().dir == 'stdin':
    new_string = ''
    for current_string in stdin:
        new_string = ' ' + current_string
        """Добавляем в начало строки последнее слово предыдущей, которое получили на прошлом шаге цикла если 
           цикл выполняется в первый раз, то добавится пробел, которые потом все равно обрежется. Вызываем функцию"""
        new_string = create_model(new_string, parser.parse_args().lc, model_dict)
else:
    for file in os.listdir(path=parser.parse_args().dir):
        """Перебираем файлы в директории, если это текстовый файл, то открываем его и построчно считываем"""
        if file[-4:] == ".txt":
            f = open(parser.parse_args().dir + '\\' + file)
            new_string = ''
            for current_string in f:
                new_string += ' ' + current_string
                new_string = create_model(new_string, parser.parse_args().lc, model_dict)
            f.close()
f = open(parser.parse_args().model, "w")
for x in model_dict:
    f.write(x + " ")
    for y in model_dict[x]:
        """Записываем в файл модель. Для каждого слова key идет строка вида key val_chis где val это слово которое
           встречалась после слова key, а chis это количество встречаний"""
        f.write(y + "_" + str(model_dict[x][y]) + " ")
    f.write("\n")
f.close()