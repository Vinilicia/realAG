import numpy as np
import pandas as pd
import math
import random

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

def selecionaPais(pop, nPop, fit):
    pais = []
    invertFit = fit.copy()
    for i in range(nPop):
        if invertFit[i] == 0:
            invertFit[i] = 0.000001
        invertFit[i] = 1/invertFit[i]
    for i in range(0, nPop, 2):
        p1 = random.choices(pop, weights=invertFit, k=1)
        p2 = random.choices(pop, weights=invertFit, k=1)
        while np.array_equal(p1, p2):
            p2 = random.choices(pop, weights=invertFit, k=1)
        pais.append(p1)
        pais.append(p2)
    return pais

def cruzamentoPorBLXab(pais, pop, nPop, Pc, d, xMin, xMax):
    popIntermed = pop.copy()
    alpha = 0.75
    beta = 0.25
    for i in range(0, nPop, 2):
        r = np.random.uniform(0, 1)
        if r < Pc:
            x = None
            y = None
            if funcaoObjetivo(pais[i], d) < funcaoObjetivo(pais[i+1], d):
                x = pais[i][0]
                y = pais[i+1][0]
            else:
                x = pais[i+1][0]
                y = pais[i][0]
            for j in range(d):
                dist = abs(x[j]-y[j])
                if(x[j] <= y[j]):
                    u1 = np.random.uniform(x[j]-alpha*dist, y[j]+beta*dist)
                    if u1 < xMin: u1 = xMin
                    elif u1 > xMax: u1 = xMax
                    u2 = np.random.uniform(x[j]-alpha*dist, y[j]+beta*dist)
                    if u2 < xMin: u2 = xMin
                    elif u2 > xMax: u2 = xMax
                    x[j] = u1
                    y[j] = u2
                else:
                    u1 = np.random.uniform(y[j]-beta*dist, x[j]+alpha*dist)
                    if u1 < xMin: u1 = xMin
                    elif u1 > xMax: u1 = xMax
                    u2 = np.random.uniform(y[j]-beta*dist, x[j]+alpha*dist)
                    if u2 < xMin: u2 = xMin
                    elif u2 > xMax: u2 = xMax
                    x[j] = u1
                    y[j] = u2
            popIntermed[i] = x
            popIntermed[i+1] = y
    return popIntermed

def cruzamentoPorMedia(pais, pop, nPop, Pc, d):
    popIntermed = pop.copy()
    for i in range(nPop-1):
        r = np.random.uniform(0, 1)
        if r < Pc:
            for j in range(d):
                popIntermed[i][j] = (pais[i][0][j] + pais[i+1][0][j])/2
    for j in range(d):
        popIntermed[nPop-1][j] = (pais[0][0][j] + pais[nPop-1][0][j])/2
    return popIntermed

def mutacao(pop, nPop, Pm, d, xMin, xMax):
    for i in range(nPop):
        for j in range(d):
            r = np.random.uniform(0, 1)
            if r < Pm:
                pop[i][j] = np.random.uniform(xMin, xMax)

def elitismo(pop, popi, nPop, fit):
    elite = min(fit)
    elite = fit.index(elite)
    r = np.random.randint(0, nPop)
    popi[r] = pop[elite]
    return popi

def realAG(nPop, nGer, cruzamento, Pc, Pm, elit):
    nPop = 100
    dimFunc = 2
    nGer = 100
    xMin = -2
    xMax = 2
    pop = np.random.uniform(xMin, xMax, (nPop, dimFunc))
    Pc = 1
    Pm = 0.1
    melhor = funcaoObjetivo(pop[0], dimFunc)
    for i in range(nGer):
        fit, melhor = avaliaPopulacao(pop, nPop, dimFunc, melhor)
        pais = selecionaPais(pop, nPop, fit)
        if cruzamento == 0:
            popIntermed = cruzamentoPorBLXab(pais, pop, nPop, Pc, dimFunc, xMin, xMax)
        else:
            popIntermed = cruzamentoPorMedia(pais, pop, nPop, Pc, dimFunc)
        mutacao(popIntermed, nPop, Pm, dimFunc, xMin, xMax)
        if elit == 1:
            elitismo(pop, popIntermed, nPop, fit)
        pop = popIntermed.copy()
        #print(f"Geração {i+1} | Melhor fit = {melhor:.20f}")
    return melhor

pops = [25, 50, 100]
nGers = [25, 50, 100]
cruzamento = [0, 1]
taxasCruz = [0.6, 0.8, 1.0]
taxasMut = [0.01, 0.05, 0.1]
elits = [0, 1]
resultados = []
for pop in pops:
    for nGer in nGers:
        for cruz in cruzamento:
            for taxaCruz in taxasCruz:
                for taxaMut in taxasMut:
                    for elit in elits:
                        fits = []
                        for i in range(20):
                            fit = realAG(pop, nGer, cruzamento, taxaCruz, taxaMut, elit)
                            fits.append(fit)
                        media = np.mean(fits)
                        desvio = np.std(fits)
                        melhor = np.min(fits)

                        resultados.append({
                            "População": pop,
                            "Gerações": nGer,
                            "Cruzamento": cruz,
                            "TaxaCruz": taxaCruz,
                            "TaxaMut": taxaMut,
                            "Elitismo": elit,
                            "Média": media,
                            "Desvio": desvio,
                            "Melhor": melhor
                        })

                        print(resultados[-1])

tabela = pd.DataFrame(resultados)
print(tabela)
