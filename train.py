import argparse
import re
import os
import pickle
import sys
from collections import defaultdict


def create_model(current_str, islow, model_dict):
    """Функция создания модели, принимает на вход 3 агрумента:
       1) current_str - str, переменная в котрой хранится последнее слово предыдущей строки
       2) islow - bool, проверка нужно ли приводить к нижнему регистру, True - если нужно
       3) model_dict - defaultdict(defaultdict(int)), словарь с моделью
       Функция возвращает последнее слово в текущей строке (str)"""
    if islow:
        current_str = current_str.lower()
    words = re.findall(r'\w+', current_str)
    """Парсим строку, оставляем только буквы, приводим к нижнему регистру если нужно"""
    for x in range(0, len(words) - 1):
        """Составляем словарь с моделью, для каждого слова свой подсловарь в котором 
        частота вхождений других слов после текущего. Записываем эту частоту"""
        model_dict[words[x]][words[x + 1]] += 1
    """Возвращаем последнее слово строки, чтобы связать его с первым словом следующей строки"""
    return words[len(words) - 1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Программа которая на основе заданных текстов составляет модель, "
                                                 "с помощью которой работает generate.py. Тексты можно писать в "
                                                 "консоль, либо указывать путь до директории с файлами, из которой "
                                                 "будут проанализированны все файлы с расширением '.txt'. Можно "
                                                 "опционально приводить тексты в нижнему регистру.")
    parser.add_argument('--input-dir', dest='dir', default='stdin', help='directory path')
    parser.add_argument('--model', dest='model',required=True, help='path to file with model')
    parser.add_argument('--lc', action = 'store_true', help='is lowercase?')

    model_dict = defaultdict(lambda: defaultdict(int))

    list = []
    if parser.parse_args().dir != 'stdin':
        for file in os.listdir(path=parser.parse_args().dir):
            if file[-4:] == ".txt":
                list.append(file)
    else:
        list.append(sys.stdin)
    for file in list:
        try:
            f = open(parser.parse_args().dir + '\\' + file)
        except:
            f = file
        new_string = ''
        for current_string in f:
            new_string += ' ' + current_string
            new_string = create_model(new_string, parser.parse_args().lc, model_dict)
    with open(parser.parse_args().model, 'wb') as output:
        pickle.dump(dict(model_dict), output)
