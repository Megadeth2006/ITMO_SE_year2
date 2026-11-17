from __future__ import annotations
import math
from typing import Callable

EPSILON = 1e-4

def is_equidistant(xs: list[float]) -> bool:
    if len(xs) < 2: return True
    h = xs[1] - xs[0]
    for i in range(1, len(xs) - 1):
        if abs((xs[i + 1] - xs[i]) - h) > EPSILON:
            return False
    return True

def compute_finite_differences(ys: list[float]) -> list[list[float]]:
    n = len(ys)
    table = [[0.0] * n for _ in range(n)]
    
    for i in range(n): 
        table[i][0] = ys[i]
        
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = table[i + 1][j - 1] - table[i][j - 1]
    return table

def compute_divided_differences(xs: list[float], ys: list[float]) -> list[list[float]]:
    n = len(xs)
    table = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        table[i][0] = ys[i]
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (xs[i + j] - xs[i])
    return table

def build_lagrange(xs: list[float], ys: list[float]) -> Callable[[float], float]:
    n = len(xs)
    def evaluate(x: float) -> float:
        result = 0.0
        for i in range(n):
            term = ys[i]
            for j in range(n):
                if i != j:
                    term *= (x - xs[j]) / (xs[i] - xs[j])
            result += term
        return result
    return evaluate

def build_newton_divided(xs: list[float], ys: list[float]) -> Callable[[float], float]:
    n = len(xs)
    diffs = compute_divided_differences(xs, ys)
    def evaluate(x: float) -> float:
        result = diffs[0][0]
        term = 1.0
        for i in range(1, n):
            term *= (x - xs[i - 1])
            result += term * diffs[0][i]
        return result
    return evaluate

def build_gauss(xs: list[float], ys: list[float]) -> Callable[[float], float]:
    if not is_equidistant(xs): raise ValueError("Нужен равномерный шаг")
    n = len(xs)
    diffs = compute_finite_differences(ys)
    h = xs[1] - xs[0]
    center_idx = n // 2

    def evaluate(x: float) -> float:
        t = (x - xs[center_idx]) / h
        result = diffs[center_idx][0]
        term = 1.0
        
        if t >= 0:
          
            for k in range(1, n):
                
                term *= (t + (k // 2)) if k % 2 == 1 else (t - (k // 2))
                
                offset = k // 2
                idx = center_idx - offset
                if 0 <= idx < n - k:
                    result += (term / math.factorial(k)) * diffs[idx][k]
                else: break
        else:
         
            for k in range(1, n):
               
                term *= (t - (k // 2)) if k % 2 == 1 else (t + (k // 2))
                
                offset = (k + 1) // 2 if k % 2 == 1 else k // 2
                idx = center_idx - offset
                if 0 <= idx < n - k:
                    result += (term / math.factorial(k)) * diffs[idx][k]
                else: break
                
        return result
    return evaluate

def stirling_term(t: float, order: int) -> float:
    if order == 1: return t
    if order == 2: return t * t
    term = t * t if order % 2 == 0 else t
    limit = (order // 2 - 1) if order % 2 == 0 else ((order - 1) // 2)
    for i in range(1, limit + 1):
        term *= (t * t - i * i)
    return term

def build_stirling(xs: list[float], ys: list[float]) -> Callable[[float], float]:
    if not is_equidistant(xs): raise ValueError("Нужен равномерный шаг")
    if len(xs) % 2 == 0: raise ValueError("Требует нечетного количества узлов")
    n = len(xs)
    diffs = compute_finite_differences(ys)
    h = xs[1] - xs[0]
    center_idx = n // 2

    def evaluate(x: float) -> float:
        t = (x - xs[center_idx]) / h
        result = diffs[center_idx][0]
        for k in range(1, n):
            term = stirling_term(t, k)
            if k % 2 == 0:
                m = k // 2
                idx = center_idx - m
                if 0 <= idx < n - k:
                    result += (term * diffs[idx][k]) / math.factorial(k)
                else: break
            else:
                m = (k - 1) // 2
                idx1, idx2 = center_idx - m - 1, center_idx - m
                if 0 <= idx1 < n - k and 0 <= idx2 < n - k:
                    dy = (diffs[idx1][k] + diffs[idx2][k]) / 2.0
                    result += (term * dy) / math.factorial(k)
                else: break
        return result
    return evaluate

def bessel_term(t: float, order: int) -> float:
    if order == 1: return t - 0.5
    if order == 2: return t * (t - 1.0)
    term = t * (t - 1.0) if order % 2 == 0 else (t - 0.5) * t * (t - 1.0)
    m = order // 2
    for i in range(2, m + 1):
        term *= (t - i) * (t + i - 1.0)
    return term

def build_bessel(xs: list[float], ys: list[float]) -> Callable[[float], float]:
    if not is_equidistant(xs): raise ValueError("Нужен равномерный шаг")
    if len(xs) % 2 != 0: raise ValueError("Требует четного количества узлов")
    n = len(xs)
    diffs = compute_finite_differences(ys)
    h = xs[1] - xs[0]
    idx0 = n // 2 - 1

    def evaluate(x: float) -> float:
        t = (x - xs[idx0]) / h
        result = (diffs[idx0][0] + diffs[idx0 + 1][0]) / 2.0
        for k in range(1, n):
            term = bessel_term(t, k)
            if k == 1:
                if 0 <= idx0 < n - k:
                    result += term * diffs[idx0][k]
                else: break
            elif k % 2 == 0:
                m = k // 2
                idxA, idxB = idx0 - m, idx0 - m + 1
                if 0 <= idxA < n - k and 0 <= idxB < n - k:
                    dy = (diffs[idxA][k] + diffs[idxB][k]) / 2.0
                    result += (term * dy) / math.factorial(k)
                else: break
            else:
                m = (k - 1) // 2
                idx = idx0 - m
                if 0 <= idx < n - k:
                    result += (term * diffs[idx][k]) / math.factorial(k)
                else: break
        return result
    return evaluate