# Generate a Kitaev chain coupled to a Z2 gauge field
# The following comes from Aramthottil et al., Phys. Rev. B, L041101, 2022
# H = μ/2 Σ_{j=1}^{n-1} Z_jZ_{j+1} - Σ_{j=1}^n (t X_j + h Z_j)

from simuq.environment import Qubit
from simuq.qsystem import QSystem


def GenQS(a = 1.0, b=1.0, c=1.0, d=1.0, T=1):
    qs = QSystem()
    q = [Qubit(qs) for i in range(2)]

    H = 0
    H += a * q[0].Z 
    H += b * q[1].Z
    H += c * q[0].Z * q[1].Z
    H += d * q[0].X * q[1].X

    qs.add_evolution(H, T)
    return qs
