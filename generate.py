import argparse
import random
import os
import sys
from collections import defaultdict


def upload_model(path, model_dict):
    """Функция принимает 2 аргумента:
       1) path - str, Путь до файла с моделью
       2) model_dict - defaultdict(dict), словарь с моделью
       Функция ничего не возвращает

       Создаем словарь с моделью, храним аналогичным образом, как в train.py. Первое слово в строке наш ключ, потом
       через пробел пара val_chis что значит что слово val встречалось после слова key  chis раз. Разделяем функцией
       split по '_' """
    f = open(path)
    for current_string in f:
        current_string = current_string.split()
        key = current_string[0]
        for i in range(1, len(current_string)):
            values = current_string[i].split('_')
            model_dict[key][values[0]] = values[1]


def generate_text(model_dict, current, lenght, output):
    """Функция генерирования, принимает 4 аргумента:
       1) model_dict - defaultdict(dict), словарь с моделью
       2) current - str, слово для которого мы ищем пару
       3) lenght - int, длина конечной последовательности
       4) output - str, либо 'stdout', либо путь до файла, в который записывать текст
       Функция ничего не возвращает

       для каждого слова составляем список, в котором с нужной частотой встречаются слова,которые могут идти
       после него в тексте. Далее функцией random.choise выбираеся следующее слово и сразу выводится"""
    if output != 'stdout':
        sys.stdout = open(output, 'w')
    else:
        print(current, ' ', end='')
    for i in range(1, lenght):
        generation_list = []
        for value in model_dict[current]:
            for j in range(int(model_dict[current][value])):
                generation_list.append(value)
        current = random.choice(generation_list)
        print(current, ' ', end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lenght', dest='lenght', type=int, help='lenght of generated text')
    parser.add_argument('--model', dest='model', required=True, help='path to file with model')
    parser.add_argument('--output', dest='output', default='stdout', help='path to output file')
    parser.add_argument('--seed', dest='seed', help='it is seed')

    model_dict = defaultdict(dict)
    """Вызываем функцию которая загружает модель, далее проверяем задано ли первое слово, если нет то выбираем его случайным
       образом среди всех ключей словаря, записываем в current. Вызываем функцию генератора текста"""
    upload_model(parser.parse_args().model, model_dict)
    if parser.parse_args().seed:
        current = parser.parse_args().seed
    else:
        """генерируем seed, если его не указали"""
        current = random.choice(list(model_dict.keys()))
    generate_text(model_dict, current, parser.parse_args().lenght, parser.parse_args().output)
