from __future__ import division
from formatter import money, number


NUMBERS = [
    ['um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez', 'onze', 'doze', 'treze', 'quatorze', 'quinze', 'dezesseis', 'dezesete', 'dezoito', 'dezenove'],
    ['dez', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa'],
    ['cem', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos']
]

power = {
    'mil': 0,
    'milhao': 1,
    'milhoes': 1,
    'bilhao': 2,
    'bilhoes': 2,
    'trilhao': 3,
    'trilhoes': 3,
    'quadrilhao': 4,
    'quadrilhoes': 4,
    'quintalhao': 5,
    'quintalhoes': 5,
}

units = {
    'reais': (1, money),
    'centavos': (100, money),
}


class R(object):
    def __init__(self):
        self.text = []

    def __add__(self, other):
        if isinstance(other, N):
            if other.value > 0:
                self.text.append(str(other))
                other.value = 0
                other.format = number
        else:
            self.text.append(other)
        return self

    def __str__(self):
        return ' '.join(self.text)


class N(object):
    def __init__(self, value=0, type=None, base=None, format=number):
        self.value = value
        self.type = type
        self.base = base
        self.format = format

    def fix(self, base, format):
        self.value /= base
        self.base = base
        self.format = format

    def sum(self, other):
        if self.type == other.type and self.base > other.base:
            self.value += other.value
            return True
        return False

    def reset(self):
        copy = N(self.value, self.type, self.base, self.format)
        self.value = 0
        self.type = None
        self.format = None
        return copy

    def __add__(self, other):
        self.value += other
        return self

    def __str__(self):
        return self.format(self.value)


def numbers(text):
    wrds = text.split(' ')
    resp = R()
    total = N()
    temp = 0
    prev = 0
    keep = None
    run = False
    for word in wrds:
        for i, sequence in enumerate(NUMBERS):
            if word in sequence:
                calc = 10 ** i * (sequence.index(word) + 1)
                if calc > prev > 0:
                    resp += total + temp
                    temp = 0
                prev = calc
                temp += calc
                run = True
                break
        else:
            if run:
                if word in power:
                    total += 1000 ** (power[word] + 1) * temp
                    temp, prev = 0, 0
                elif word in units:
                    total += temp
                    temp = 0
                    total.fix(*units[word])
                    if keep and not total.sum(keep):
                        resp += keep
                        resp += 'e'
                    keep = total.reset()
                elif word != 'e':
                    resp += total + temp
                    resp += word
                    temp, prev = 0, 0
                    run = False
            else:
                resp += word
    if keep:
        resp += keep
    resp += total + temp
    return str(resp)
