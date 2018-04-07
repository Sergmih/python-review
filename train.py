import argparse
import re
import os
from sys import stdin


def func(str, lc, d):
    if lc:
        str = str.lower()
    words = re.findall(r'\w+', str)
    """Парсим строку, оставляем только буквы, приводим к нижнему регистру если нужно"""
    for x in range(0, len(words) - 1):
        """Составляем словарь с моделью, для каждого слова свой подсловарь в котором частота вхождений других слов после 
           текущего. Для каждого слова смотрим есть ли в словаре такой ключ, есть ли значения у ключа, для каждого 
           случая выполняем необходимые действия"""
        if not d.get(words[x]):
            d[words[x]] = {words[x+1]: 1}
        elif not d[words[x]].get(words[x+1]):
            d[words[x]][words[x+1]] = 1
        else:
            d[words[x]][words[x + 1]] += 1
    """Возвращаем последнее слово строки, чтобы связать его с первым словом следующей строки"""
    return words[len(words) - 1]


parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', dest='dir', default='stdin', help='directory path')
parser.add_argument('--model', dest='model',required=True, help='path to file with model')
parser.add_argument('--lc', action = 'store_true', help='is lowercase?')

dict = {}
if parser.parse_args().dir == 'stdin':
    tmp = ''
    for s in stdin:
        tmp = tmp + ' ' + s
        """Добавляем в начало строки последнее слово предыдущей, которое получили на прошлом шаге цикла если 
           цикл выполняется в первый раз, то добавится пробел, которые потом все равно обрежется. Вызываем функцию"""
        tmp = func(tmp, parser.parse_args().lc, dict)
else:
    for file in os.listdir(path=parser.parse_args().dir):
        """Перебираем файлы в директории, если это текстовый файл, то открываем его и построчно считываем"""
        if file[-4:] == ".txt":
            f = open(parser.parse_args().dir + '\\' + file)
            tmp = ''
            for s in f:
                tmp = tmp + ' ' + s
                tmp = func(tmp, parser.parse_args().lc, dict)
            f.close()
f = open(parser.parse_args().model, "w")
for x in dict:
    f.write(x + " ")
    for y in dict[x]:
        """Записываем в файл модель. Для каждого слова key идет строка вида key val_chis где val это слово которое
           встречалась после слова key, а chis это количество встречаний"""
        f.write(y + "_" + str(dict[x][y]) + " ")
    f.write("\n")
f.close()