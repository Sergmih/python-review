import argparse
import random
import os
import sys
import pickle
from collections import defaultdict
import numpy


def upload_model(path):
    """Функция принимает 2 аргумента:
       1) path - str, Путь до файла с моделью
       Функция возвращает модель (defaultdict(dict))
       Считываем модель с помощью pickle """
    with open(path, 'rb') as input:
        model_dict = dict(pickle.load(input))
    return model_dict


def generate_text(model_dict, current, lenght, output, string_lenght):
    """Функция генерирования, принимает 4 аргумента:
       1) model_dict - defaultdict(dict), словарь с моделью
       2) current - str, слово для которого мы ищем пару
       3) lenght - int, длина конечной последовательности
       4) output - str, либо 'stdout', либо путь до файла, в
       который записывать текст Функция ничего не возвращает
       для каждого слова составляем список, в котором с нужной частотой
        встречаются слова,которые могут идти после него в тексте. Далее
        функцией random.choise выбираеся следующее слово и сразу выводится"""
    text = []
    if output != 'stdout':
        sys.stdout = open(output, 'w')
    print(current, ' ', end='')
    for i in range(1, lenght):
        while not model_dict.get(current):
            current = random.choice(list(model_dict.keys()))
        generation_list = list(model_dict[current].keys())
        frequency_list = list(model_dict[current].values())
        current = numpy.random.choice(generation_list, p=frequency_list)
        text.append(current)
        if len(text) > string_lenght:
            print(' '.join(text))
            text.clear()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Программа на основе заданной"
                                     " модели генерирует текст заданной длины."
                                     " Для текста можно указать начальное "
                                     "слово, иначе оно выберется "
                                     "автоматически")
    parser.add_argument('--lenght', dest='lenght', type=int, required=True,
                        help='lenght of generated text')
    parser.add_argument('--model', dest='model', required=True,
                        help='path to file with model')
    parser.add_argument('--output', dest='output', default='stdout',
                        help='path to output file')
    parser.add_argument('--seed', dest='seed', help='it is seed')
    parser.add_argument('--string-lenght', dest='str_lenght', default='10',
                        help='lenght of string in output, '
                        'if not set than it will be 10', type=int)

    """Вызываем функцию которая загружает модель, далее проверяем задано
    ли первое слово, если нет то выбираем его случайным образом среди всех
    ключей словаря, записываем в current. Вызываем функцию генератора текста"""
    model_dict = upload_model(parser.parse_args().model)
    if parser.parse_args().seed:
        current = parser.parse_args().seed
    else:
        """генерируем seed, если его не указали"""
        current = random.choice(list(model_dict.keys()))
    generate_text(model_dict, current, parser.parse_args().lenght,
                  parser.parse_args().output, parser.parse_args().str_lenght)
