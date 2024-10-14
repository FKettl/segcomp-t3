from datetime import datetime
import random
import timeit


class LaggedFibonacciGenerator:
    """
    O Lagged Fibonacci Generator (LFG) é um método para gerar números
    pseudoaleatórios que utiliza uma combinação de valores passados da
    sequência com um atraso (lag). Esse algoritmo é eficaz em produzir
    sequências longas de números pseudoaleatórios e é uma variante dos
    geradores de Fibonacci.

        S(n) = (S(n-1)+S(n-2)) mod m

    ref: https://en.wikipedia.org/wiki/Lagged_Fibonacci_generator
    Funcionamento:
    - Inicialização:
      - A classe é inicializada com parâmetros que definem o tamanho da
        sequência (`k`), o atraso (`j`), um valor de módulo (`modulus`)
        e uma semente inicial (`seed`).
      - O gerador começa a sequência com a semente e gera `k-1` números
        iniciais usando uma fórmula linear simples (similar ao gerador
        de congruência linear implementado abaixo).

    - Geração de Números:
      - Para gerar o próximo número na sequência, o método `next()`
        combina dois números da sequência que estão atrasados por `j` e
        `k` posições, utilizando a fórmula acima.
      - O novo número gerado é adicionado à sequência, enquanto o valor
        mais antigo é removido para manter o tamanho da sequência
        constante em `k`.

    - Geração em Massa:
      - O método `generate(n)` permite gerar uma lista de `n` números
        pseudoaleatórios chamando o método `next()` repetidamente.
    """
    def __init__(self, j=24, k=55, modulus=2**2, seed=1):
        self.j = j
        self.k = k
        self.modulus = modulus
        self.sequence = []

        # Inicializa a sequência com a semente
        self.sequence.append(seed)
        for _ in range(1, k):
            value = random.randint(0, modulus - 1)  # Gera um valor aleatório dentro do módulo
            self.sequence.append(value)

        # Tentei utilizar os numeros 1103515245 e 12345 para iniciar as sequências pois são mencionados no artigo, porém eles só estavam gerando resultados impares
        # ref: S. K. Park and K. W. Miller. 1988. Random number generators: good ones are hard to find. Commun. ACM 31, 10 (Oct. 1988), 1192–1201. https://doi.org/10.1145/63039.63042
        #for _ in range(1, k):
        #    next_value = (self.sequence[-1] * 1103515245 + 12345) % self.modulus  # Um passo similar ao anterior para "bootstrap"
        #    self.sequence.append(next_value)

    def next(self):
        # Calcula o próximo valor da sequência usando (X_k = (X_(k-j) + X_(k-k)) % m)
        next_value = (self.sequence[-self.j] + self.sequence[-self.k]) % self.modulus
        self.sequence.append(next_value)

        # Remove o valor mais antigo para manter o tamanho da sequência
        self.sequence.pop(0)
        return next_value

    def generate(self, n = 1):
        # Gera uma lista com `n` valores pseudoaleatórios
        return [self.next() for _ in range(n)]

class LinearCongruentialGenerator:
    """
    O Gerador Congruencial Linear é um método simples e amplamente utilizado para gerar números pseudoaleatórios.
    O algoritmo é definido pela seguinte relação de recorrência:

        X_{n+1} = (a * X_n + c) mod m

    ref: https://www.columbia.edu/~ks20/4106-18-Fall/Simulation-LCG.pdf

    onde:
    - X_n é o número atual na sequência,
    - a é o multiplicador (um inteiro positivo),
    - c é a constante aditiva (um inteiro não negativo),
    - m é o módulo (um inteiro positivo que define o limite superior da sequência),
    - X_0 é a semente inicial (valor de início).

    O LCG tem algumas propriedades que o tornam fácil de implementar, mas sua qualidade estatística pode variar
    dependendo dos parâmetros escolhidos (a, c, m). Para melhores resultados, é comum utilizar:
    - a como um número ímpar (geralmente um número primo),
    - c como um número relativamente pequeno em comparação a m,
    - m como uma potência de 2, que simplifica a aritmética.

    ref: https://en.wikipedia.org/wiki/Linear_congruential_generator
.
    """
    def __init__(self, seed=1, a=1664525, c=1013904223, modulus=2**4096):
        """
        Inicializa o LCG com os parâmetros fornecidos.

        :param seed: Semente inicial para a geração de números.
        :param a: Multiplicador (comum: 1664525).
        :param c: Constante aditiva (comum: 1013904223).
        :param modulus: Módulo (comum: 2**32).
        ref: https://medium.com/@chanakapinfo/simulations-and-random-number-generation-exploring-linear-congruential-generator-9ba6fbc73939
        """
        self.seed = seed
        self.a = a  # Multiplicador
        self.c = c  # Constante aditiva
        self.modulus = modulus  # Módulo
        self.current = seed  # Valor atual da sequência

    def next(self):
        """
        Gera o próximo número pseudoaleatório na sequência.
        """
        self.current = (self.a * self.current + self.c) % self.modulus
        return self.current

    def generate(self, n=1, seed=None):
        """
        Gera uma lista de `n` números pseudoaleatórios.

        :param n: Número de valores a serem gerados.
        :return: Lista de números gerados.
        """
        if seed is not None:
            self.current = seed
        return [self.next() for _ in range(n)]

"""
modulos = 2**4096

lcg = LinearCongruentialGenerator(seed=123456, modulus=modulos)  # Inicializa com uma semente
random_numbers = lcg.generate(10)  # Gera 10 números pseudoaleatórios
print("Numeros gerados com lcg", random_numbers)

lfg = LaggedFibonacciGenerator(seed=123456, modulus=modulos)
random_numbers = lfg.generate(10)
print("Numeros gerados com lfg",random_numbers)
number = 100
execution_time = timeit.timeit(lfg.generate, number=number)
print("Tempo de execução LFG:", execution_time/number)

number = 100
execution_time = timeit.timeit(lcg.generate, number=number)
print("Tempo de execução LCG:", execution_time/number)
"""
