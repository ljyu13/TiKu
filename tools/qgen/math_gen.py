#!/usr/bin/env python3
"""数学题目生成器：小学（1-6）、初中（7-9）、高中（10-12）。
全部为参数化题目，答案由程序精确计算，可无限生成且不重复。
"""
from fractions import Fraction

from .core import fmt_num, pick_distractors


def _int_mc(b, text, ans, analysis, kps, span=8, difficulty=2):
    opts = pick_distractors(b.rng, ans, "int", span=max(2, abs(ans) // 2 + 3))
    b.choice(text, fmt_num(ans), opts, analysis, kps, difficulty=difficulty)


# ---------------- 小学 ----------------
def p_add(b):
    hi = {1: 10, 2: 50, 3: 200, 4: 1000, 5: 10000, 6: 100000}[b.grade]
    a = b.rng.randint(1, hi)
    c = b.rng.randint(1, hi)
    _int_mc(b, "%d + %d = ？" % (a, c), a + c,
            "相同数位对齐相加：%d + %d = %d。" % (a, c, a + c), ["加法运算"])


def p_sub(b):
    hi = {1: 10, 2: 50, 3: 200, 4: 1000, 5: 10000, 6: 100000}[b.grade]
    a = b.rng.randint(2, hi)
    c = b.rng.randint(1, a - 1)
    _int_mc(b, "%d − %d = ？" % (a, c), a - c,
            "从 %d 里减去 %d：%d − %d = %d。" % (a, c, a, c, a - c), ["减法运算"])


def p_mul(b):
    if b.grade <= 2:
        a, c = b.rng.randint(2, 9), b.rng.randint(2, 9)
    else:
        a, c = b.rng.randint(2, 99), b.rng.randint(2, 12)
    _int_mc(b, "%d × %d = ？" % (a, c), a * c,
            "用乘法计算：%d × %d = %d。" % (a, c, a * c), ["乘法运算"], span=a + c)


def p_div(b):
    c = b.rng.randint(2, 12)
    q = b.rng.randint(2, 30)
    a = c * q
    _int_mc(b, "%d ÷ %d = ？" % (a, c), q,
            "因为 %d × %d = %d，所以 %d ÷ %d = %d。" % (c, q, a, a, c, q), ["除法运算"])


def p_div_rem(b):
    c = b.rng.randint(3, 9)
    q = b.rng.randint(2, 20)
    r = b.rng.randint(1, c - 1)
    a = c * q + r
    ans = "%d……%d" % (q, r)
    opts = ["%d……%d" % (q + 1, r), "%d……%d" % (q, r + 1),
            "%d……%d" % (q - 1, r)]
    b.choice("%d ÷ %d 的商和余数分别是多少？" % (a, c), ans, opts,
             "%d ÷ %d = %d 余 %d，因为 %d×%d+%d=%d。" % (a, c, q, r, c, q, r, a),
             ["有余数的除法"], difficulty=3)


def p_mixed(b):
    a = b.rng.randint(2, 20)
    c = b.rng.randint(2, 9)
    d = b.rng.randint(1, 15)
    if b.rng.random() < 0.5:
        ans = a + c * d
        text = "%d + %d × %d = ？" % (a, c, d)
        ana = "先算乘法 %d×%d=%d，再算加法 %d+%d=%d。" % (c, d, c * d, a, c * d, ans)
    else:
        val = a + d
        ans = val - c * d if val >= c * d else a
        text = "%d − %d × %d = ？" % (val, c, d) if val >= c * d else "%d + %d − %d = ？" % (a, c, d)
        if val >= c * d:
            ana = "先算乘法 %d×%d=%d，再算减法 %d−%d=%d。" % (c, d, c * d, val, c * d, ans)
        else:
            ans = a + c - d
            ana = "同级运算从左到右：%d+%d=%d，再减 %d 得 %d。" % (a, c, a + c, d, ans)
    _int_mc(b, text, ans, ana, ["四则混合运算"], difficulty=3)


def p_frac(b):
    den = b.rng.choice([2, 3, 4, 5, 6, 8, 10])
    x = b.rng.randint(1, den - 1)
    y = b.rng.randint(1, den - 1)
    if b.rng.random() < 0.5:
        res = Fraction(x, den) + Fraction(y, den)
        op = "+"
    else:
        if x < y:
            x, y = y, x
        res = Fraction(x, den) - Fraction(y, den)
        op = "−"
    ans = "%s" % res
    opts = ["%s" % (res + Fraction(1, den)), "%s" % (res + Fraction(1, 2)),
            "%s" % abs(res - Fraction(1, den))]
    b.choice("计算 %d/%d %s %d/%d = ？" % (x, den, op, y, den), ans, opts,
             "分母相同，分子直接相加减：%d/%d %s %d/%d = %s。" % (x, den, op, y, den, ans),
             ["分数加减法"], difficulty=2)


def p_decimal(b):
    a = round(b.rng.uniform(1, 50), 1)
    c = round(b.rng.uniform(1, 20), 1)
    if b.rng.random() < 0.5:
        ans = round(a + c, 2)
        op = "+"
    else:
        if a < c:
            a, c = c, a
        ans = round(a - c, 2)
        op = "−"
    opts = pick_distractors(b.rng, ans, "decimal", span=5)
    b.choice("计算 %.1f %s %.1f = ？" % (a, op, c), fmt_num(ans), opts,
             "小数加减要把小数点对齐：%.1f %s %.1f = %s。" % (a, op, c, fmt_num(ans)),
             ["小数加减法"])


def p_unit(b):
    kind = b.rng.choice(["长度", "质量", "时间", "面积"])
    tables = {
        "长度": [("1米", "100厘米"), ("1分米", "10厘米"), ("1厘米", "10毫米"), ("1千米", "1000米")],
        "质量": [("1千克", "1000克"), ("1吨", "1000千克")],
        "时间": [("1小时", "60分钟"), ("1分钟", "60秒"), ("1天", "24小时"), ("1周", "7天")],
        "面积": [("1平方米", "100平方分米"), ("1平方分米", "100平方厘米"), ("1公顷", "10000平方米")],
    }
    big, small = b.rng.choice(tables[kind])
    n = b.rng.randint(2, 12)
    ratio = {"米": 100, "分米": 10, "厘米": 10, "千米": 1000, "千克": 1000, "吨": 1000,
             "小时": 60, "分钟": 60, "天": 24, "周": 7, "平方米": 100, "平方分米": 100,
             "公顷": 10000}
    bigname = big.lstrip("0123456789")
    smallname = small.lstrip("0123456789")
    r = ratio.get(bigname, 10)
    ans = n * r
    opts = pick_distractors(b.rng, ans, "int", span=r)
    b.choice("%d %s 等于多少 %s？" % (n, bigname, smallname),
             fmt_num(ans), opts,
             "1 %s = %d %s，所以 %d %s = %d %s。" % (bigname, r, smallname, n, bigname, ans, smallname),
             ["单位换算", kind])


def p_perimeter(b):
    shape = b.rng.choice(["正方形", "长方形"])
    if shape == "正方形":
        s = b.rng.randint(2, 30)
        ans = 4 * s
        b.choice("一个正方形的边长是 %d 厘米，它的周长是多少厘米？" % s,
                 fmt_num(ans), pick_distractors(b.rng, ans, "int", span=s),
                 "正方形周长 = 边长×4 = %d×4 = %d 厘米。" % (s, ans), ["正方形周长"])
    else:
        l = b.rng.randint(3, 40)
        w = b.rng.randint(2, l - 1)
        ans = 2 * (l + w)
        b.choice("一个长方形的长是 %d 厘米、宽是 %d 厘米，它的周长是多少厘米？" % (l, w),
                 fmt_num(ans), pick_distractors(b.rng, ans, "int", span=l),
                 "长方形周长 = (长+宽)×2 = (%d+%d)×2 = %d 厘米。" % (l, w, ans), ["长方形周长"])


def p_area(b):
    shape = b.rng.choice(["正方形", "长方形"])
    if shape == "正方形":
        s = b.rng.randint(2, 20)
        ans = s * s
        b.choice("一个正方形的边长是 %d 厘米，它的面积是多少平方厘米？" % s,
                 fmt_num(ans), pick_distractors(b.rng, ans, "int", span=s * 2),
                 "正方形面积 = 边长×边长 = %d×%d = %d 平方厘米。" % (s, s, ans), ["正方形面积"])
    else:
        l = b.rng.randint(3, 25)
        w = b.rng.randint(2, l - 1)
        ans = l * w
        b.fill("一个长方形的长是 %d 厘米、宽是 %d 厘米，面积是___平方厘米。" % (l, w),
               fmt_num(ans), "长方形面积 = 长×宽 = %d×%d = %d 平方厘米。" % (l, w, ans), ["长方形面积"])


def p_percent(b):
    total = b.rng.choice([100, 200, 500, 1000, 50, 80])
    pct = b.rng.choice([10, 20, 25, 30, 40, 50, 60, 75, 80])
    ans = total * pct // 100
    b.choice("%d 的 %d%% 是多少？" % (total, pct), fmt_num(ans),
             pick_distractors(b.rng, ans, "int", span=total // 10 + 1),
             "%d × %d%% = %d×%s = %d。" % (total, pct, total, fmt_num(pct / 100), ans),
             ["百分数"], difficulty=2)


def p_factor(b):
    n = b.rng.randint(12, 100)
    if b.rng.random() < 0.5:
        # 判断因数
        d = b.rng.randint(2, 12)
        ok = (n % d == 0)
        b.judge("%d 是 %d 的因数。" % (d, n), ok,
                "%d ÷ %d = %s，%s整除，所以 %d %s是 %d 的因数。" %
                (n, d, fmt_num(n / d), "能" if ok else "不能", d, "" if ok else "不", n),
                ["因数与倍数"])
    else:
        # 最小质数/最大因数等
        ans = n
        b.fill("%d 的最大因数是___。" % n, fmt_num(ans),
               "一个数的最大因数是它本身，所以是 %d。" % n, ["因数与倍数"])


def p_word(b):
    kind = b.rng.choice(["购物", "行程", "工程"])
    if kind == "购物":
        price = b.rng.randint(5, 60)
        cnt = b.rng.randint(2, 15)
        paid = b.rng.randint(cnt * price, cnt * price + 100)
        ans = paid - cnt * price
        b.calc("小明买了 %d 件商品，每件 %d 元，付了 %d 元，应找回多少元？" % (cnt, price, paid),
               "%d元" % ans,
               "总价 = %d×%d = %d 元，找回 = %d − %d = %d 元。" % (cnt, price, cnt * price, paid, cnt * price, ans),
               ["应用题", "购物"], difficulty=2)
    elif kind == "行程":
        v = b.rng.randint(30, 90)
        t = b.rng.randint(2, 8)
        ans = v * t
        b.calc("一辆汽车每小时行驶 %d 千米，行驶 %d 小时一共行驶多少千米？" % (v, t),
               "%d千米" % ans,
               "路程 = 速度×时间 = %d×%d = %d 千米。" % (v, t, ans), ["应用题", "行程"])
    else:
        total = b.rng.randint(20, 60)
        per = b.rng.randint(2, 6)
        ans = total // per
        b.fill("把 %d 个苹果平均分给 %d 个小朋友，每人分到___个。" % (total, per),
               fmt_num(ans), "%d ÷ %d = %d，每人分到 %d 个。" % (total, per, ans, ans),
               ["应用题", "平均分"])


PRIMARY_FNS = [p_add, p_sub, p_mul, p_div, p_div_rem, p_mixed, p_frac, p_decimal,
               p_unit, p_perimeter, p_area, p_percent, p_factor, p_word]


# ---------------- 初中 ----------------
def j_rational(b):
    a = b.rng.randint(-20, 20)
    c = b.rng.randint(-20, 20)
    op = b.rng.choice(["+", "−", "×"])
    if op == "+":
        ans = a + c
    elif op == "−":
        ans = a - c
    else:
        ans = a * c
    _int_mc(b, "计算 (%d) %s (%d) = ？" % (a, op, c), ans,
            "有理数运算：%s。" % fmt_num(ans), ["有理数运算"])


def j_abs(b):
    x = b.rng.randint(-30, 30)
    b.choice("|%d| 的值是？" % x, fmt_num(abs(x)),
             pick_distractors(b.rng, abs(x), "int", span=6),
             "绝对值表示到原点的距离，|%d| = %d。" % (x, abs(x)), ["绝对值"])


def j_linear_eq(b):
    a = b.rng.randint(2, 9)
    x = b.rng.randint(-10, 10)
    c = b.rng.randint(-15, 15)
    rhs = a * x + c
    b.choice("解方程 %dx + %d = %d，x = ？" % (a, c, rhs), fmt_num(x),
             pick_distractors(b.rng, x, "int", span=5),
             "%dx = %d − (%d) = %d，x = %d÷%d = %d。" % (a, rhs, c, rhs - c, rhs - c, a, x),
             ["一元一次方程"])


def j_system(b):
    x = b.rng.randint(-8, 8)
    y = b.rng.randint(-8, 8)
    a = b.rng.randint(1, 5)
    d = b.rng.randint(1, 5)
    s1 = x + y
    s2 = a * x - d * y if a != d else a * x + y
    # 保证可解：这里用简单形式 x+y=s1, x-y=s2
    s2 = x - y
    b.calc("解方程组：x + y = %d，x − y = %d。" % (s1, s2),
           "x = %d，y = %d" % (x, y),
           "两式相加得 2x = %d，x = %d；相减得 2y = %d，y = %d。" % (s1 + s2, x, s1 - s2, y),
           ["二元一次方程组"])


def j_inequality(b):
    a = b.rng.randint(2, 9)
    c = b.rng.randint(-10, 10)
    b.choice("解不等式 %dx + %d > 0，x 的取值范围是？" % (a, c),
             "x > %s" % fmt_num(-c / a),
             ["x < %s" % fmt_num(c / a), "x > %s" % fmt_num(c / a), "x > %s" % fmt_num(-c / a - 1)],
             "%dx > %d，x > %s。" % (a, -c, fmt_num(-c / a)), ["一元一次不等式"], difficulty=3)


def j_power(b):
    base = b.rng.randint(2, 6)
    m = b.rng.randint(2, 4)
    n = b.rng.randint(1, 3)
    ans = base ** (m + n)
    b.choice("计算 %d^%d × %d^%d = ？" % (base, m, base, n), fmt_num(ans),
             pick_distractors(b.rng, ans, "int", span=ans // 2 + 2),
             "同底数幂相乘，指数相加：%d^(%d+%d) = %d^%d = %d。" % (base, m, n, base, m + n, ans),
             ["幂的运算"])


def j_radical(b):
    k = b.rng.randint(2, 12)
    b.choice("化简 √%d 的结果是？" % (k * k), fmt_num(k),
             [fmt_num(k + 1), fmt_num(k * k), fmt_num(k - 1)],
             "√%d = %d，因为 %d² = %d。" % (k * k, k, k, k * k), ["二次根式"])


def j_quadratic(b):
    r1 = b.rng.randint(-8, 8)
    r2 = b.rng.randint(-8, 8)
    # (x-r1)(x-r2) = x^2 -(r1+r2)x + r1r2
    coef_b = -(r1 + r2)
    coef_c = r1 * r2
    text = "一元二次方程 x² %s %dx %s %d = 0 的两根是？" % (
        "+" if coef_b >= 0 else "−", abs(coef_b), "+" if coef_c >= 0 else "−", abs(coef_c))
    ans = "%d 和 %d" % (r1, r2)
    b.choice(text, ans,
             ["%d 和 %d" % (-r1, -r2), "%d 和 %d" % (r1 + 1, r2 - 1), "%d 和 %d" % (r2, r1 + 2)],
             "因式分解得 (x−(%d))(x−(%d))=0，两根为 %d 和 %d。" % (r1, r2, r1, r2),
             ["一元二次方程"], difficulty=3)


def j_function(b):
    k = b.rng.randint(2, 9)
    c = b.rng.randint(-10, 10)
    x0 = b.rng.randint(1, 8)
    ans = k * x0 + c
    b.choice("一次函数 y = %dx + %d，当 x = %d 时 y = ？" % (k, c, x0), fmt_num(ans),
             pick_distractors(b.rng, ans, "int", span=k),
             "代入 x=%d：y = %d×%d + (%d) = %d。" % (x0, k, x0, c, ans), ["一次函数"])


def j_pythagoras(b):
    m = b.rng.randint(2, 12)
    n = b.rng.randint(2, 12)
    c2 = m * m + n * n
    # 找勾股数
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
    a1, b1, c1 = b.rng.choice(triples)
    k = b.rng.randint(1, 3)
    a1, b1, c1 = a1 * k, b1 * k, c1 * k
    b.choice("直角三角形两直角边分别为 %d 和 %d，斜边是？" % (a1, b1), fmt_num(c1),
             [fmt_num(c1 + k), fmt_num(a1 + b1), fmt_num(c1 - k)],
             "由勾股定理 c² = %d² + %d² = %d，c = %d。" % (a1, b1, c1 * c1, c1),
             ["勾股定理"])


def j_angle(b):
    x = b.rng.randint(20, 80)
    y = b.rng.randint(20, 80)
    third = 180 - x - y
    if third <= 0:
        x = y = 40
        third = 100
    b.choice("三角形的两个内角分别是 %d° 和 %d°，第三个内角是？" % (x, y),
             "%d°" % third,
             ["%d°" % (third + 10), "%d°" % (third - 10), "%d°" % (180 - x)],
             "三角形内角和为 180°，第三个角 = 180°−%d°−%d° = %d°。" % (x, y, third),
             ["三角形内角和"])


def j_prob(b):
    total = b.rng.choice([6, 8, 10, 12, 20])
    good = b.rng.randint(1, total - 1)
    from fractions import Fraction as F
    ans = F(good, total)
    b.choice("一个袋子里有 %d 个球，其中 %d 个红球，随机摸一个，摸到红球的概率是？" % (total, good),
             "%s" % ans,
             ["%s" % F(total - good, total), "%s" % F(good + 1, total), "%s" % F(good, total + 2)],
             "概率 = 红球数÷总数 = %d/%d = %s。" % (good, total, ans), ["简单概率"])


def j_fraction_simplify(b):
    a = b.rng.randint(2, 9)
    c = b.rng.randint(2, 9)
    k = b.rng.randint(2, 6)
    from fractions import Fraction as F
    ans = F(a, c)
    b.choice("化简分式 %d/%d 的结果是？" % (a * k, c * k), "%s" % ans,
             ["%d/%d" % (a * k + 1, c * k), "%s" % F(c, a), "%d/%d" % (a, c * k)],
             "分子分母同除以 %d 得 %d/%d = %s。" % (k, a, c, ans), ["分式化简"])


JUNIOR_FNS = [j_rational, j_abs, j_linear_eq, j_system, j_inequality, j_power, j_radical,
              j_quadratic, j_function, j_pythagoras, j_angle, j_prob, j_fraction_simplify,
              p_frac, p_percent, p_word]


# ---------------- 高中 ----------------
def h_set(b):
    A = set(b.rng.sample(range(1, 10), 4))
    B = set(b.rng.sample(range(1, 10), 4))
    inter = sorted(A & B)
    ans = "{" + ",".join(map(str, inter)) + "}" if inter else "空集"
    sa = "{" + ",".join(map(str, sorted(A))) + "}"
    sb = "{" + ",".join(map(str, sorted(B))) + "}"
    union = "{" + ",".join(map(str, sorted(A | B))) + "}"
    b.choice("已知集合 A=%s，B=%s，则 A∩B = ？" % (sa, sb), ans,
             [union, "{1,2}", "空集"],
             "交集取公共元素 A∩B = %s。" % ans, ["集合运算"])


def h_function_domain(b):
    k = b.rng.randint(1, 12)
    b.choice("函数 f(x)=√(x−%d) 的定义域是？" % k, "x ≥ %d" % k,
             ["x > %d" % k, "x ≤ %d" % k, "全体实数"],
             "二次根式要求 x−%d ≥ 0，即 x ≥ %d。" % (k, k), ["函数定义域"])


def h_exponent(b):
    base = b.rng.randint(2, 6)
    e = b.rng.randint(1, 4)
    ans = base ** e
    b.choice("计算 log_%d(%d) 的值是？" % (base, ans), fmt_num(e),
             [fmt_num(e + 1), fmt_num(base), fmt_num(ans)],
             "因为 %d^%d = %d，所以 log_%d(%d) = %d。" % (base, e, ans, base, ans, e),
             ["对数运算"], difficulty=3)


def h_arith_seq(b):
    a1 = b.rng.randint(-10, 10)
    d = b.rng.randint(2, 8)
    n = b.rng.randint(5, 15)
    ans = a1 + (n - 1) * d
    b.choice("等差数列中 a₁=%d，公差 d=%d，则 a%d = ？" % (a1, d, n), fmt_num(ans),
             pick_distractors(b.rng, ans, "int", span=d * 2),
             "aₙ = a₁+(n−1)d = %d+(%d−1)×%d = %d。" % (a1, n, d, ans), ["等差数列"])


def h_geo_seq(b):
    a1 = b.rng.randint(1, 5)
    q = b.rng.randint(2, 4)
    ans = a1 * (q ** 3)
    b.choice("等比数列中 a₁=%d，公比 q=%d，则 a₄ = ？" % (a1, q), fmt_num(ans),
             pick_distractors(b.rng, ans, "int", span=a1 * q),
             "a₄ = a₁·q³ = %d×%d³ = %d。" % (a1, q, ans), ["等比数列"])


def h_trig(b):
    import math
    ang = b.rng.choice([0, 30, 45, 60, 90])
    fn = b.rng.choice(["sin", "cos"])
    rad = math.radians(ang)
    val = math.sin(rad) if fn == "sin" else math.cos(rad)
    ans = fmt_num(round(val, 4))
    table = {"sin": {0: "0", 30: "1/2", 45: "√2/2", 60: "√3/2", 90: "1"},
             "cos": {0: "1", 30: "√3/2", 45: "√2/2", 60: "1/2", 90: "0"}}
    b.choice("%s%d° 的值是？" % (fn, ang), table[fn][ang],
             [table["cos" if fn == "sin" else "sin"][ang], "1", "0"],
             "特殊角三角函数值：%s%d° = %s。" % (fn, ang, table[fn][ang]),
             ["特殊角三角函数"], difficulty=2)


def h_vector(b):
    x1, y1 = b.rng.randint(-8, 8), b.rng.randint(-8, 8)
    x2, y2 = b.rng.randint(-8, 8), b.rng.randint(-8, 8)
    ans = x1 * x2 + y1 * y2
    b.choice("已知向量 a=(%d,%d)，b=(%d,%d)，则 a·b = ？" % (x1, y1, x2, y2), fmt_num(ans),
             pick_distractors(b.rng, ans, "int", span=10),
             "数量积 a·b = %d×%d + %d×%d = %d。" % (x1, x2, y1, y2, ans), ["向量数量积"])


def h_complex(b):
    a, c = b.rng.randint(-8, 8), b.rng.randint(-8, 8)
    d, e = b.rng.randint(-8, 8), b.rng.randint(-8, 8)
    real = a * d - c * e
    imag = a * e + c * d
    ans = "%d%s%di" % (real, "+" if imag >= 0 else "−", abs(imag))
    b.choice("计算 (%d+%di)(%d+%di) = ？" % (a, c, d, e), ans,
             ["%d+%di" % (real, abs(imag) + 1), "%d−%di" % (real, abs(imag)),
              "%d+%di" % (real + 1, imag)],
             "展开：%d·%d−%d·%d = %d，虚部 %d·%d+%d·%d = %d。" %
             (a, d, c, e, real, a, e, c, d, imag), ["复数运算"], difficulty=3)


def h_derivative(b):
    a = b.rng.randint(1, 8)
    n = b.rng.randint(2, 5)
    x0 = b.rng.randint(1, 5)
    ans = a * n * (x0 ** (n - 1))
    b.choice("设 f(x)=%dx^%d，则 f'(%d) = ？" % (a, n, x0), fmt_num(ans),
             pick_distractors(b.rng, ans, "int", span=a * n),
             "f'(x) = %d·%d·x^%d，代入 x=%d 得 %d。" % (a, n, n - 1, x0, ans),
             ["导数运算"], difficulty=3)


def h_permutation(b):
    n = b.rng.randint(4, 9)
    m = b.rng.randint(2, min(4, n))
    import math
    ans = math.factorial(n) // math.factorial(n - m)
    b.choice("从 %d 个不同元素中取出 %d 个排列，共有多少种？" % (n, m), fmt_num(ans),
             pick_distractors(b.rng, ans, "int", span=ans // 2 + 1),
             "A(%d,%d) = %d!/(%d−%d)! = %d。" % (n, m, n, n, m, ans),
             ["排列组合"], difficulty=3)


def h_prob(b):
    import math
    n = b.rng.randint(5, 10)
    k = b.rng.randint(2, n - 1)
    ans = math.comb(n, k)
    b.choice("从 %d 人中选 %d 人组成小组，共有多少种选法？" % (n, k), fmt_num(ans),
             pick_distractors(b.rng, ans, "int", span=ans // 2 + 1),
             "组合数 C(%d,%d) = %d。" % (n, k, ans), ["组合数"], difficulty=3)


def h_quadratic_func(b):
    a = b.rng.choice([1, -1, 2, -2])
    h = b.rng.randint(-5, 5)
    k = b.rng.randint(-6, 6)
    b.fill("二次函数 y=%d(x−(%d))²+%d 的顶点坐标是 (___,___)。" % (a, h, k),
           "(%d,%d)" % (h, k),
           "顶点式为 y=a(x−h)²+k，顶点为 (h,k) = (%d,%d)。" % (h, k),
           ["二次函数顶点"], difficulty=2)


def h_line(b):
    k = b.rng.randint(-6, 6)
    c = b.rng.randint(-8, 8)
    # 点到直线距离从略，改为求与x轴交点
    if k == 0:
        k = 2
    x0 = -c / k
    b.choice("直线 y=%dx+(%d) 与 x 轴交点的横坐标是？" % (k, c), fmt_num(x0),
             [fmt_num(c / k), fmt_num(-c), fmt_num(-k / c) if c else "0"],
             "令 y=0：%dx+(%d)=0，x = %s。" % (k, c, fmt_num(x0)), ["直线方程"], difficulty=2)


SENIOR_FNS = [h_set, h_function_domain, h_exponent, h_arith_seq, h_geo_seq, h_trig,
              h_vector, h_complex, h_derivative, h_permutation, h_prob, h_quadratic_func,
              h_line, j_quadratic, j_function]


def generate(builder):
    """根据年级选择题型工厂，循环生成直至满 1000 题。"""
    g = builder.grade
    if g <= 6:
        fns = PRIMARY_FNS
    elif g <= 9:
        fns = JUNIOR_FNS
    else:
        fns = SENIOR_FNS
    target = 1000
    stall = 0
    while len(builder.items) < target:
        before = len(builder.items)
        fn = builder.rng.choice(fns)
        fn(builder)
        if len(builder.items) == before:
            stall += 1
            if stall > 400:
                # 兜底：参数化四则运算，保证能填满
                a = builder.rng.randint(1, 999)
                c = builder.rng.randint(1, 99)
                builder.fill("计算 %d + %d = ___。" % (a, c), fmt_num(a + c),
                             "%d + %d = %d。" % (a, c, a + c), ["四则运算"])
        else:
            stall = 0
