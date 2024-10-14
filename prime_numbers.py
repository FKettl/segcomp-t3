import random

# Função para calcular o símbolo de Jacobi (a/n)
# Implementado e adaptado de: https://en.wikipedia.org/wiki/Jacobi_symbol#cite_ref-4
def jacobi(a, n):
    if a == 0:
        return 0
    result = 1
    if a < 0:
        a = -a
        if n % 4 == 3:
            result = -result
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 == 3 or n % 8 == 5:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    else:
        return 0

# Função para verificar se um número é primo usando o teste Solovay-Strassen
def solovay_strassen(n, k=40):
    if n < 2:
        return False
    if n != 2 and n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(1, n - 1)
        jacobian = jacobi(a, n) % n
        mod_exp = pow(a, (n - 1) // 2, n)

        if jacobian == 0 or mod_exp != jacobian:
            return False

    return True


def miller_rabin(n, k=40):
    """Realiza o Teste de Miller-Rabin para verificar se n é primo."""
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    # Encontre s e d, tal que (n-1) / 2^s = d
    # tal que s seja a maior potencia de 2 que divide n-1
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # Realiza k testes
    for _ in range(k):
        a = random.randint(2, n - 2)  # Escolhe um número aleatório no intervalo [2, n-2]
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Se não encontrou um testemunho, n é composto

    return True  # n é provavelmente primo

# Exemplo de uso
"""
n = 791801032056296568081676934676877732481832594908851493678435945178634118993181279848550027104280075850144997291533874352637462272474884578251930419875230966316199007265661300734331391846961039594126673838276446624910362478491105294884920038502491912077139348317088046565523619354325835441132309291965564522502768559557681478828469165549528970341866340560377788008449081775335300066419564346512352703264977526310786426693122349001608700455507696233425713585892748430422220138808456756209639968492469552466732671140815963439235895905999756902700103986627861290376526564217332697382323929693051971798013006726216940115616634097340795491453949252763773802849790155682725882496760808704639652741702100016740353904974956799501102931009958005481998557371320008579294629351952585779473651625362355266625747412204712477646765126493003113919772205975713228255595165862074961368188032063195609225287621768796414907529343627009813648887912304131077040851136260401781900994769679207230960330821828885342523613797306484415993250728821491577516457987443171792629221037258360500569308853873861490741666314135356991869953311207144646257115019011429215466700024462882130730186094399925380945229984254169988761773003476796659956461049419894577616684141  # Número a ser testado

if solovay_strassen(n):
    print(f"{n} é provavelmente primo.")
else:
    print(f"{n} é composto.")

print(f"O número {n} é {'primo' if miller_rabin(n) else 'composite'}.")
"""
