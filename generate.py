import argparse
import random
import os
from sys import stdin


def uploadmodel(path, d):
    """Создаем словарь с моделью, храним аналогичным образом, как в train.py. Первое слово в строке наш ключ, потом
       через пробел пара val_chis что значит что слово val встречалось после слова key  chis раз. Разделяем функцией
       split по _"""
    f = open(path)
    for x in f:
        x = x.split()
        key = x[0]
        for i in range(1, len(x)):
            symb = x[i].split('_')
            if not d.get(key):
                d[key] = {symb[0]: symb[1]}
            else:
                d[key][symb[0]] = symb[1]



def generate(d, current, lenght, output):
    """Функция генерирования, для каждого слова составляем список, в котором с нужной частотой встречаются слова,
    которые могут идти после него в тексте. Далее функцией random.choise выбираеся следующее слово и сразу выводится"""
    if output != 'stdout':
        f = open(output, "w")
    print(current, ' ', end='')
    for i in range(1, lenght):
        lst = []
        for x in d[current]:
            for j in range(int(d[current][x])):
                lst.append(x)
        current = random.choice(lst)
        if(output == 'stdout'):
            print(current, ' ', end='')
        else:
            f.write(current + ' ')


parser = argparse.ArgumentParser()
parser.add_argument('--lenght', dest='lenght', type=int, help='lenght of generated text')
parser.add_argument('--model', dest='model', required=True, help='path to file with model')
parser.add_argument('--output', dest='output', default='stdout', help='path to output file')
parser.add_argument('--seed', dest='seed', help='it is seed')

dict= {}
"""Вызываем функцию которая загружает модель, далее проверяем задано ли первое слово, если нет то выбираем его случайным
   образом среди всех ключей словаря, записываем в current. Вызываем функцию генератора текста"""
uploadmodel(parser.parse_args().model, dict)
if parser.parse_args().seed:
    current = parser.parse_args().seed
else:
    """if no seed then random"""
    current = random.choice(list(dict.keys()))
generate(dict, current, parser.parse_args().lenght, parser.parse_args().output)
