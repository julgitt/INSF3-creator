"""Function providing type hint support."""
from typing import List, Callable


def calc_h(x: List[float]) -> List[float]:
    """Calculate list of h, where h_k = x_k - x_(k-1)"""
    h: List[float] = [0.0] + [
        x[i] - x[i - 1]
        for i in range(1, len(x))
    ]
    return h


def calc_lambdas(h: List[float]) -> List[float]:
    """Calculate list of lambdas, where lambda_k = h_k / (h_k + h_(k+1))"""
    lambdas: List[float] = [0.0] + [
        h[i] / (h[i] + h[i + 1])
        for i in range(1, len(h) - 1)
    ]
    return lambdas


def calc_d(x: List[float], y: List[float]) -> List[float]:
    """Calculate list of d, where d_k = 6 * f[x_(k-1), x_k, x(k+1)]"""
    d: List[float] = [0.0] + [
        6 * (
            (
                (y[i + 1] - y[i]) / (x[i + 1] - x[i])
            ) - (
                (y[i] - y[i - 1]) / (x[i] - x[i - 1])
            )
        ) / (x[i + 1] - x[i - 1])
        for i in range(1, len(x) - 1)
    ]
    return d


def calc_moments(x: List[float], y: List[float]) -> List[float]:
    """recursive computation of consecutive moments"""
    p: List[float] = [0.0]
    q: List[float] = [0.0]
    v: float = 0.0

    h: List[float] = calc_h(x)
    lambdas: List[float] = calc_lambdas(h)
    d: List[float] = calc_d(x, y)

    for i in range(1, len(lambdas)):
        v = lambdas[i] * p[i - 1] + 2.0
        p.append((lambdas[i] - 1.0) / v)
        q.append((d[i] - lambdas[i] * q[i - 1]) / v)

    m: List[float] = [q[-1], 0.0]

    for i in range(len(q) - 2, -1, -1):
        m.insert(0, p[i] * m[0] + q[i])

    return m


def get_calc_nifs3_k(x: List[float], y: List[float],
                h: List[float], m: List[float],
                k: int) -> Callable[[float], float]:
    """Returns nifs3 function for x and y coordinates list, list of h, moments and k value."""
    return (lambda u: (1.0 / h[k]) * (
            ((1.0 / 6.0) * m[k - 1] * (x[k] - u) ** 3) +
            ((1.0 / 6.0) * m[k] * (u - x[k - 1]) ** 3) +
            (y[k - 1] - ((1.0 / 6.0) * m[k - 1] * h[k] ** 2)) * (x[k] - u) +
            (y[k] - ((1.0 / 6.0) * m[k] * h[k] ** 2)) * (u - x[k - 1])
        ))
       

def calc_nifs3(x: List[float], y: List[float]) -> tuple[List[float], List[float]]:
    """Calculate nifs3 for x and y coordinates list"""
    M: int = 3000
    n: int = len(x)

    # time array
    t: List[float] = [k / (n - 1) for k in range(n)]

    m_x: List[float] = calc_moments(t, x)
    m_y: List[float] = calc_moments(t, y)

    h: List[float] = calc_h(t)

    x_list: List[Callable[[float], float]] = [
        get_calc_nifs3_k(t, x, h, m_x, k) for k in range(1, n)]
    y_list: List[Callable[[float], float]] = [
        get_calc_nifs3_k(t, y, h, m_y, k) for k in range(1, n)]

    s_x: List[float] = []
    s_y: List[float] = []
    index: int = 1
    for k in range(M + 1):
        u = k / M
        if (index < (len(x) + 1) and u > t[index]):
            index += 1
        s_x.append(x_list[index - 1](u))
        s_y.append(y_list[index - 1](u))

    return s_x, s_y
