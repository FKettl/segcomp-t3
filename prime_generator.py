from pseudo_random_numbers import LinearCongruentialGenerator
from prime_numbers import solovay_strassen, miller_rabin
from datetime import datetime
import timeit

modulos = 2**1024
lcg = LinearCongruentialGenerator(seed=int(datetime.now().timestamp()), modulus=modulos)  # Inicializa com uma semente

""" Código para encontrar um número primo utilizando os geradores de números pseudoaleatórios e os testes de primalidade """
def find_prime1():
    random_numbers = lcg.generate(1)  # Gera 10 números pseudoaleatórios
    while not miller_rabin(random_numbers[0]):
        random_numbers = lcg.generate(1)

    print("ACHOU", random_numbers[0])
    return random_numbers[0]

def find_prime2():
    random_numbers = lcg.generate(1)  # Gera 10 números pseudoaleatórios
    while not solovay_strassen(random_numbers[0]):
        random_numbers = lcg.generate(1)

    print("ACHOU", random_numbers[0])
    return random_numbers[0]



execution_time = timeit.timeit(find_prime1, number=1)
print("Tempo de execução miller_rabin:", execution_time)

execution_time = timeit.timeit(find_prime2, number=1)
print("Tempo de execução solovay_strassen:", execution_time)
