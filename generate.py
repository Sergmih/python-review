import argparse
import random
import os
from sys import stdin


def upload_model(path, model_dict):
    """Создаем словарь с моделью, храним аналогичным образом, как в train.py. Первое слово в строке наш ключ, потом
       через пробел пара val_chis что значит что слово val встречалось после слова key  chis раз. Разделяем функцией
       split по _"""
    f = open(path)
    for current_string in f:
        current_string = current_string.split()
        key = current_string[0]
        for i in range(1, len(current_string)):
            values = current_string[i].split('_')
            if not model_dict.get(key):
                model_dict[key] = {values[0]: values[1]}
            else:
                model_dict[key][values[0]] = values[1]



def generate(d, current, lenght, output):
    """Функция генерирования, для каждого слова составляем список, в котором с нужной частотой встречаются слова,
    которые могут идти после него в тексте. Далее функцией random.choise выбираеся следующее слово и сразу выводится"""
    if output != 'stdout':
        f = open(output, "w")
        f.write(current + ' ')
    else:
        print(current, ' ', end='')
    for i in range(1, lenght):
        generation_list = []
        for value in d[current]:
            for j in range(int(d[current][value])):
                generation_list.append(value)
        current = random.choice(generation_list)
        if(output == 'stdout'):
            print(current, ' ', end='')
        else:
            f.write(current + ' ')


parser = argparse.ArgumentParser()
parser.add_argument('--lenght', dest='lenght', type=int, help='lenght of generated text')
parser.add_argument('--model', dest='model', required=True, help='path to file with model')
parser.add_argument('--output', dest='output', default='stdout', help='path to output file')
parser.add_argument('--seed', dest='seed', help='it is seed')

model_dict = {}
"""Вызываем функцию которая загружает модель, далее проверяем задано ли первое слово, если нет то выбираем его случайным
   образом среди всех ключей словаря, записываем в current. Вызываем функцию генератора текста"""
upload_model(parser.parse_args().model, model_dict)
if parser.parse_args().seed:
    current = parser.parse_args().seed
else:
    """if no seed then random"""
    current = random.choice(list(model_dict.keys()))
generate(model_dict, current, parser.parse_args().lenght, parser.parse_args().output)
