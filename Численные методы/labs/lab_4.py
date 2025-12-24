import math


def mat_copy(A):
    return [row[:] for row in A]


def mat_mul(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    C = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            s = 0.0
            for k in range(p):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C


def mat_vec_mul(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def vec_dot(u, v):
    return sum(ui * vi for ui, vi in zip(u, v))


def norm2(v):
    return math.sqrt(sum(x * x for x in v))


def gauss_solve(A, b):
    n = len(A)
    M = [[float(A[i][j]) for j in range(n)] + [float(b[i])] for i in range(n)]
    for k in range(n):
        piv_row = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[piv_row][k]) < 1e-14:
            raise ValueError("Матрица вырождена при Гауссе")
        if piv_row != k:
            M[k], M[piv_row] = M[piv_row], M[k]
        pivot = M[k][k]
        for j in range(k, n + 1):
            M[k][j] /= pivot
        for i in range(n):
            if i == k:
                continue
            factor = M[i][k]
            if abs(factor) > 0:
                for j in range(k, n + 1):
                    M[i][j] -= factor * M[k][j]
    return [M[i][n] for i in range(n)]


def determinant(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    det = 0.0
    for j in range(n):
        minor = [[M[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += ((-1) ** j) * M[0][j] * determinant(minor)
    return det


def inverse_matrix(matrix):
    M = [[float(x) for x in row] for row in matrix]
    n = len(M)
    det = determinant(M)
    if abs(det) < 1e-14:
        raise ValueError("Матрица вырождена")

    adj = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = []
            for ii in range(n):
                if ii == i:
                    continue
                row = []
                for jj in range(n):
                    if jj == j:
                        continue
                    row.append(M[ii][jj])
                minor.append(row)
            cofactor = ((-1) ** (i + j)) * determinant(minor)
            adj[j][i] = cofactor
    return [[adj[i][j] / det for j in range(n)] for i in range(n)]


def fmt(x):
    if abs(x) < 0.00005:
        x = 0.0
    return f"{x:0.4f}"


def print_matrix_A(A):
    for row in A:
        print("  " + "  ".join(fmt(x) for x in row))


def print_matrix_A_original():
    rows = [
        ["3", "1,7", "1,6", "5,5"],
        ["1,7", "1", "2", "4,5"],
        ["1,6", "2", "3", "1,5"],
        ["5,5", "4,5", "1,5", "1"],
    ]
    for row in rows:
        print("  " + "  ".join(row))


# полиномы: представление коэффициентами
def poly_add(p, q):
    m = max(len(p), len(q))
    r = [0.0] * m
    for i in range(m):
        if i < len(p):
            r[i] += p[i]
        if i < len(q):
            r[i] += q[i]
    return r


def poly_sub(p, q):
    m = max(len(p), len(q))
    r = [0.0] * m
    for i in range(m):
        if i < len(p):
            r[i] += p[i]
        if i < len(q):
            r[i] -= q[i]
    return r


def poly_mul_scalar(p, a):
    return [a * ci for ci in p]


def poly_eval_asc(p, x):
    s = 0.0
    xp = 1.0
    for c in p:
        s += c * xp
        xp *= x
    return s


def poly_compose_linear_t_to_x(coeffs_t, alpha, beta):
    res = [0.0]
    power = [1.0]
    base = [beta, alpha]
    for j in range(len(coeffs_t)):
        res = poly_add(res, poly_mul_scalar(power, coeffs_t[j]))
        power = poly_mul(power, base)
    return res


def poly_mul(p, q):
    r = [0.0] * (len(p) + len(q) - 1)
    for i in range(len(p)):
        for j in range(len(q)):
            r[i + j] += p[i] * q[j]
    return r


def prepare_data_N_equals_11():
    N = 11
    base_xs = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    xs = [b + 0.1 * N for b in base_xs]
    ys_expr = [
        lambda N: 0.5913,
        lambda N: 0.63 + N / 17.0,
        lambda N: 0.7162,
        lambda N: 0.8731,
        lambda N: 0.9574,
        lambda N: 1.8 - math.cos(N / 11.0),
        lambda N: 1.3561,
        lambda N: 1.2738,
        lambda N: 1.1 + N / 29.0,
        lambda N: 1.1672,
    ]
    ys = [f(N) for f in ys_expr]
    return xs, ys


# дискретные ортогональные чебышевы полиномы
def build_discrete_orthogonal_polynomials(t_nodes, deg=3):
    def inner(p, q):
        s = 0.0
        for ti in t_nodes:
            s += poly_eval_asc(p, ti) * poly_eval_asc(q, ti)
        return s

    basis = []
    for k in range(deg + 1):
        p = [0.0] * k + [1.0]
        basis.append(p)

    T = []
    for k in range(deg + 1):
        q = basis[k][:]
        for j in range(k):
            denom = inner(T[j], T[j])
            if abs(denom) < 1e-14:
                raise ValueError("Нулевая норма при построении ортогональных полиномов")
            num = inner(q, T[j])
            q = poly_sub(q, poly_mul_scalar(T[j], num / denom))
        T.append(q)
    return T


def least_squares_discrete_chebyshev(xs, ys, deg=3):
    a = xs[0]
    b = xs[-1]
    alpha = 2.0 / (b - a)
    beta = -(a + b) / (b - a)

    def to_t(x):
        return alpha * x + beta

    t_nodes = [to_t(x) for x in xs]
    Tpolys = build_discrete_orthogonal_polynomials(t_nodes, deg=deg)

    ck = []
    for k in range(deg + 1):
        num = 0.0
        den = 0.0
        for i in range(len(xs)):
            Tk = poly_eval_asc(Tpolys[k], t_nodes[i])
            num += ys[i] * Tk
            den += Tk * Tk
        if abs(den) < 1e-14:
            raise ValueError("Нулевая норма Tk при вычислении коэффициентов")
        ck.append(num / den)

    P_t = [0.0]
    for k in range(deg + 1):
        P_t = poly_add(P_t, poly_mul_scalar(Tpolys[k], ck[k]))

    P_x = poly_compose_linear_t_to_x(P_t, alpha, beta)

    h = xs[1] - xs[0]
    return {
        "t_nodes": t_nodes,
        "Tpolys": Tpolys,
        "ck": ck,
        "P_t": P_t,
        "P_x": P_x,
        "h": h,
    }


# Данилевский
def swap_rows_cols(M, i, j):
    n = len(M)
    B = [row[:] for row in M]
    B[i], B[j] = B[j], B[i]
    for r in range(n):
        B[r][i], B[r][j] = B[r][j], B[r][i]
    return B


def frobenius_type(F, tol=1e-8):
    n = len(F)
    superdiag = all(abs(F[i][i + 1] - 1.0) < tol for i in range(n - 1))
    subdiag = all(abs(F[i + 1][i] - 1.0) < tol for i in range(n - 1))
    if superdiag:
        return "super"
    if subdiag:
        return "sub"
    return "none"


def leverrier_charpoly(A):
    n = len(A)
    coeffs = [0.0] * (n + 1)
    coeffs[0] = 1.0
    B_prev = [[0.0] * n for _ in range(n)]
    for k in range(1, n + 1):
        if k == 1:
            s_k = sum(A[i][i] for i in range(n))
        else:
            AB = mat_mul(A, B_prev)
            s_k = sum(AB[i][i] for i in range(n))
        c_k = -s_k / k
        coeffs[k] = c_k
        if k == 1:
            B_prev = [[A[i][j] for j in range(n)] for i in range(n)]
            for i in range(n):
                B_prev[i][i] += c_k
        else:
            B_prev = mat_mul(A, B_prev)
            for i in range(n):
                B_prev[i][i] += c_k
    return coeffs


def charpoly_from_frobenius(F):
    n = len(F)
    t = frobenius_type(F)
    if t == "super":
        last = F[n - 1]
        c0_to_cnm1 = [-last[j] for j in range(n)]
        return [1.0] + [c0_to_cnm1[n - 1 - k] for k in range(n)]
    if t == "sub":
        first = F[0]
        c1_to_cn = [-first[j] for j in range(n)]
        return [1.0] + c1_to_cn
    return leverrier_charpoly(F)


def danilevski_strict(A):
    n = len(A)
    M = mat_copy(A)
    tol = 1e-14
    for p in range(n - 1, 0, -1):
        r = p - 1
        s = p
        alpha = M[s][r]
        if abs(alpha) < tol:
            found = False
            for i in range(r):
                if abs(M[s][i]) > tol:
                    M = swap_rows_cols(M, i, r)
                    found = True
                    break
            if not found:
                raise ValueError(
                    "Не удалось найти ненулевой элемент для шага Данилевского"
                )
            alpha = M[s][r]

        P = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        for j in range(n):
            P[r][j] = M[s][j] / alpha

        P_inv = inverse_matrix(P)
        M = mat_mul(P_inv, mat_mul(M, P))

    A_fro = M
    coeffs = charpoly_from_frobenius(A_fro)
    return A_fro, coeffs


# Корни
def poly_eval_desc(coeffs_desc, x):
    s = 0.0
    for a in coeffs_desc:
        s = s * x + a
    return s


def gershgorin_bound(A):
    n = len(A)
    mx = 0.0
    for i in range(n):
        s = 0.0
        for j in range(n):
            s += abs(A[i][j])
        mx = max(mx, s)
    return mx + 1.0


def bisection_root(coeffs_desc, a, b, tol=1e-12):
    fa = poly_eval_desc(coeffs_desc, a)
    fb = poly_eval_desc(coeffs_desc, b)
    if fa == 0.0:
        return a
    if fb == 0.0:
        return b
    for _ in range(200):
        m = 0.5 * (a + b)
        fm = poly_eval_desc(coeffs_desc, m)
        if abs(fm) < tol or abs(b - a) < tol:
            return m
        if fa * fm < 0:
            b = m
            fb = fm
        else:
            a = m
            fa = fm
    return 0.5 * (a + b)


def find_real_roots_scan(coeffs_desc, bound_R, n_roots=4):
    for M in [2000, 5000, 10000, 20000]:
        xs = [-bound_R + (2.0 * bound_R) * i / M for i in range(M + 1)]
        vals = [poly_eval_desc(coeffs_desc, x) for x in xs]
        intervals = []
        for i in range(M):
            f1 = vals[i]
            f2 = vals[i + 1]
            if f1 == 0.0:
                intervals.append((xs[i] - 1e-6, xs[i] + 1e-6))
            elif f1 * f2 < 0:
                intervals.append((xs[i], xs[i + 1]))

        roots = []
        for a, b in intervals:
            r = bisection_root(coeffs_desc, a, b, tol=1e-12)
            ok = True
            for rr in roots:
                if abs(r - rr) < 1e-6:
                    ok = False
                    break
            if ok:
                roots.append(r)
        roots.sort()
        if len(roots) >= n_roots:
            return roots[:n_roots]
    return roots


# Собственные векторы (A - λI) v = 0
def nullspace_vector(M):
    n = len(M)
    A = [row[:] for row in M]
    row = 0
    piv_cols = []
    tol = 1e-10

    for col in range(n):
        sel = None
        for r in range(row, n):
            if abs(A[r][col]) > tol:
                sel = r
                break
        if sel is None:
            continue
        A[row], A[sel] = A[sel], A[row]
        pivot = A[row][col]
        A[row] = [val / pivot for val in A[row]]
        for r in range(n):
            if r != row:
                fac = A[r][col]
                if abs(fac) > tol:
                    A[r] = [A[r][c] - fac * A[row][c] for c in range(n)]
        piv_cols.append(col)
        row += 1
        if row == n:
            break

    free_cols = [c for c in range(n) if c not in piv_cols]
    if not free_cols:
        return [0.0] * n

    free = free_cols[0]
    v = [0.0] * n
    v[free] = 1.0

    for r_idx in range(len(piv_cols) - 1, -1, -1):
        c = piv_cols[r_idx]
        s = 0.0
        for j in free_cols:
            s += A[r_idx][j] * v[j]
        v[c] = -s

    nrm = norm2(v)
    if nrm == 0:
        return v
    return [vi / nrm for vi in v]


# Степенной метод
def power_method(A, eps=0.001, max_iter=10000):
    n = len(A)
    x = [1.0] * n
    r = norm2(x)
    x = [xi / r for xi in x]
    lam = 0.0
    for _ in range(max_iter):
        Ax = mat_vec_mul(A, x)
        lam_new = vec_dot(Ax, x)
        normAx = norm2(Ax)
        if normAx == 0:
            return 0.0, x
        x_new = [ai / normAx for ai in Ax]
        if abs(lam_new - lam) < eps:
            return lam_new, x_new
        lam = lam_new
        x = x_new
    return lam, x


def main():
    xs, ys = prepare_data_N_equals_11()
    print("Задание 1: узлы x и значения y (N=11):")
    for x, y in zip(xs, ys):
        print("  " + f"x={x:0.4f}" + "  " + f"y={y:0.4f}")
    print("")

    res1 = least_squares_discrete_chebyshev(xs, ys, deg=3)

    print("Коэффициенты разложения по формуле c_k = (Σ y_i T_k(t_i)) / (Σ T_k(t_i)^2):")
    for k, ck in enumerate(res1["ck"]):
        print(f"c_{k} = {fmt(ck)}")
    print("")

    print("Многочлен P_3 в степенной базе по x: P(x)=c0+c1 x+c2 x^2+c3 x^3")
    P_x = res1["P_x"]
    for i in range(4):
        ci = P_x[i] if i < len(P_x) else 0.0
        print(f"c_{i} = {fmt(ci)}")
    print("")

    h = res1["h"]
    print("Проверка в промежуточных точках x_i + h/2:")
    for x in xs:
        xm = x + h / 2.0
        Pxm = poly_eval_asc(P_x, xm)
        print(f"x_mid={xm:0.4f}\tP(x_mid)={fmt(Pxm)}")
    print("")

    print("Разложение через полиномы Чебышева (дискретные T_k):")
    for k, ck in enumerate(res1["ck"]):
        print(f"c_{k} = {fmt(ck)}")
    print("")

    A = [
        [1.6, 1.6, 1.7, 1.8],
        [1.6, 2.6, 1.3, 1.3],
        [1.7, 1.3, 3.6, 1.4],
        [1.8, 1.3, 1.4, 4.6],
    ]

    print("Задание 2: матрица A:")
    print_matrix_A_original()
    print("")

    A_fro, coeffs = danilevski_strict(A)
    print("Финальная Фробениусова форма (A_fro):")
    t = frobenius_type(A_fro)
    if t == "super":
        print("----")
    elif t == "sub":
        print("----")
    else:
        print("(коэффициенты через Леверрье)")
    print_matrix_A(A_fro)
    print("")

    print(
        "Коэффициенты характеристического многочлена (lambda^n + c1*lambda^{n-1} + ... + c_n):"
    )
    for i, c in enumerate(coeffs):
        print(f"c[{i}] = {fmt(c)}")
    print("")

    R = gershgorin_bound(A)
    roots = find_real_roots_scan(coeffs, R, n_roots=4)

    print("Собственные значения (корни):")
    for r in roots:
        print(fmt(r))
    print("")

    if roots:
        print("Собственные векторы:")
        for lamr in roots:
            n = len(A)
            M = [
                [A[i][j] - (lamr if i == j else 0.0) for j in range(n)]
                for i in range(n)
            ]
            v = nullspace_vector(M)

            print(f"lambda={lamr:0.4f}")
            for val in v:
                print("v = " + fmt(val))
            print("")

    print("Задание 3: степенной метод")
    lam_est, v_est = power_method(A, eps=0.001)
    print("Оценка спектрального радиуса:")
    print(f"lambda ≈ {fmt(lam_est)}")
    print("\nПриближенный собственный вектор:")
    for val in v_est:
        print(fmt(val))

    try:
        import numpy as np

        Anp = np.array(A, dtype=float)
        w, V = np.linalg.eigh(Anp)

        print("\nСравнение с numpy:")
        print("Собственные значения numpy:")
        for wi in w:
            print(fmt(float(wi)))
        print("")

        print("Собственные векторы numpy (по одному на собственное значение):")
        for i in range(len(w)):
            lam = float(w[i])
            vec = V[:, i]
            print(f"lambda={lam:0.4f}")
            for k in range(len(vec)):
                print("v = " + fmt(float(vec[k])))
            print("")
    except Exception:
        pass


if __name__ == "__main__":
    main()
