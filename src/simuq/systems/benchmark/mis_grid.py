# The Maximal-independent-set Hamiltonian
# H(t) = Δ(t)Σ_j n_j + Ω(t)/2 Σ_j X_j + α Σ_{(j, k)\in E} n_j n_k
# Here Δ(t) changes linearly from -U to U, E is a grid lattice
# HML discretizes it into D segments

import numpy as np

from simuq.environment import Qubit
from simuq.qsystem import QSystem


def GenQS(k=3, T=1, U=1, Omega=4, alpha=4):

    qs = QSystem()
    n = k * k
    link = []
    for i in range(k):
        for j in range(k):
            if j < k - 1:
                link.append((i * k + j, i * k + j + 1))
            if i < k - 1:
                link.append((i * k + j, (i + 1) * k + j))
    q = [Qubit(qs) for i in range(n)]
    noper = [(q[i].I - q[i].Z) / 2 for i in range(n)]
    H = 0
    for q0, q1 in link:
        H += alpha * noper[q0] * noper[q1]
    for i in range(n):
        H += Omega / 2 * q[i].X

    for i in range(n):
        H += -U * noper[i]

    qs.add_evolution(H, T)
    return qs
