import numpy as np
import math

def funcaoObjetivo(indv, d):
    e = math.e
    sum1 = np.sum(np.square(indv))
    sum2 = np.sum(np.cos(2 * np.pi * np.array(indv)))
    f = -20*e**(-0.2*np.sqrt(sum1/d)) -e**((1/d)*sum2) + 20 + e
    return f

def avaliaPopulacao(pop, nPop, d, melhor):
    fits = []
    for i in range(nPop):
        fit = funcaoObjetivo(pop[i], d)
        fits.append(fit)
        if fit < melhor:
            melhor = fit
    return fits, melhor

def selecionaPais(nPop, fit):
    pais = []
    pv = 0.9
    for i in range(nPop):
        p1 = np.random.randint(0, nPop)
        p2 = np.random.randint(0, nPop)
        while p1 == p2:
            p2 = np.random.randint(0, nPop)
        r = np.random.uniform(0, 1)
        if fit[p1] < fit[p2]:
            if r > pv or (i > 0 and pais[i-1] == p1):
                pais.append(p2)
            else:
                pais.append(p1)
        else:
            if r < pv or (i > 0 and pais[i-1] == p1):
                pais.append(p2)
            else:
                pais.append(p1)
    return pais

def cruzamento(pais, pop, nPop, Pc, p, d):
    popIntermed = pop.copy()
    for i in range(0,nPop,2):
        r = np.random.uniform(0, 1)
        if r < Pc:
            r = np.random.randint(1, p)
            for j in range(d):
                temp = popIntermed[pais[i]][j][:r].copy()
                popIntermed[pais[i]][j][:r] = popIntermed[pais[i+1]][j][:r]
                popIntermed[pais[i+1]][j][:r] = temp
    return popIntermed

def mutacao(pop, nPop, Pm, p, d):
    for i in range(nPop):
        for j in range(d):
            for k in range(p):
                r = np.random.uniform(0, 1)
                if r < Pm:
                    pop[i][j][k] = 1 - pop[i][j][k]

def elitismo(pop, popi, fit, ne):
    elite_idx = sorted(range(len(fit)), key=lambda i: fit[i])[:ne]
    elite = [pop[i] for i in elite_idx]
    popi[:ne] = elite
    return popi

def genericAG():
    nPop = 100
    dimFunc = 2
    nGer = 100
    nElite = 2
    xMin = -10
    xMax = 10
    pop = np.random.uniform(xMin, xMax, (nPop, dimFunc))
    Pc = 1
    Pm = 0.1
    melhor = funcaoObjetivo(pop[0], dimFunc)
    for i in range(nGer):
        fit, melhor = avaliaPopulacao(pop, nPop, dimFunc, melhor)
        pais = selecionaPais(nPop, fit)
        popIntermed = cruzamento(pais, pop, nPop, Pc, precisao, dimFunc)
        mutacao(popIntermed, nPop, Pm, precisao, dimFunc)
        elitismo(pop, popIntermed, fit, nElite)
        pop = popIntermed.copy()
        print("Geracao " + str(i+1) + " Melhor fit = " + str(melhor))
    return melhor

melhor = genericAG()
print(melhor)
