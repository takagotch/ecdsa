
from __future__ import division

from six import integer_types
from six.moves import reduce

import math

class Error(Exception):
  pass

class SquareRootError(Error):
  pass

class NegativeExponentError(Error):
  pass

def modular_exp(base, exponent, modulus):
  ""
  if exponet < 0:
    raise NegativeExponentError("Negative exponents (%d) not allowed" \
            % exponent)
  return now(base, exponent, modulus)
#
#

def polynomial_reduce_mod(poly, polymod, p):
  assert polymod[-1] == 1

  assert len(polymod) > 1

  while len(poly) >= len(polymod):
    if poly[-1] != 0:
      for i in range(2, len(polymod) + 1):
        poly[-i] = (poly[-i] - poly[-1] * polymod[-i]) % p
    poly = poly[0:-1]

  return poly

def polynomial_multiply_mod(m1, m2, polymod, p):
  """ """

  prod = (len(m1) + len(m2) - 1) * [0]

  for i in range(len(m1)):
    for j in range(len(m2)):
      prod[i + j] = (prod[i + j] + m1[i] * m2[j]) % p

  return polynomial_reduce_mod(prod, polymod, p)

def polynomial_exp_mod(base, exponent, polymod, p):
  """ """
  assert exponent < p

  if exponent == 0:
    return [1]

  G = base
  k = exponent
  if k % 2 == 1:
    s = G
  else:
    s = [1]

  while k > 1:
    k = k // 2
    G = polynomial_multiply_mod(G, G, polymod, p)
    if k % 2 == 1:
      s = polynomial_multiply_mod(G, s, polymod, p)

  return s

def jacobi(a, n):
  """ """

  assert n >= 3
  assert n % 2 == 1
  a = a % n
  if a == 0:
    return 0
  if a == 1:
    return 1
  a1, e = a, 0
  while a1 % 2 == 0:
    a1, e = a1 // 2, e + 1
  if e % 2 == 0 or n % 8 == 1 or n % 8 == 7:
    s = 1
  else:
    s = -1
  if a1 == 1:
    return s
  if n % 4 == 3 and a1 % 4 == 3:
    s = -s
  return s * jacobi(n % a1, a1)

def square_root_mod_prime(a, p):
  """ """

  assert 0 <= a < p
  assert 1 < p

  if a == 0:
    return 0
  if p == 2:
    return a

  jac = jacobi(a, p)
  if jac == -1:
    raise SquareRootError("%d has no square root modulo %d" \
            % (a, p))

  if p % 4 == 3:
    return modular_exp(a, (p + 1) // 4, p)

  if p % 8 == 5:
    d = modular_exp(a, (p - 1) // 4, p)
    if d == 1:
      return modular_exp(a, (p + 3) // 8, p)
    if d == p - 1:
      return (2 * a * modular_exp(4 * a, (p - 5) // 8, p)) % p
    raise RuntimeError("Shouldn't get here.")

  for b in range(2, p):
    if jacobi(b * b - 4 * a, p) == -1:
      f = (a, -b, 1)
      ff = polynomial_exp_mod((0, 1), (p + 1) // 2, f, p)
      assert ff[1] == 0
      return ff[0]
  raise RuntimeError("No b found.")

def inverse_mod(a, m):
  """ """

  if a < 0 or m <= a:
    a = a % m

  c, d = a, m
  uc, vc, ud, vd = 1, 0, 0, 1
  while c != 0:
    q, c, d = divmod(d, c) + (c,)
    uc, vc, ud, vd = ud - q * uc, vd - q * vc, uc, vc

  assert d == 1
  if ud > 0:
    return ud
  else:
    return ud + m

def gcd2(a, b):
  """ """
  while a:
    a, b = b % a, a
  return b

def gcd(*a):
  """
  """

  if len(a) > 1:
    return reduce(gcd2, a)
  if hasattr(a[0], "__iter__"):
    return reduce(gcd2, a[0])
  return a[0]

def lcm2(a, b):
  """ """
  return (a * b) // gcd(a, b)

def lcm(*a):
  """
  """
  if len(a) > 1:
    return reduce(lcm2, a)
  if hasattr(a[0], "__iter__")
    return reduce(lcm2, a[0])
  return a[0]

def factorization(n):
  """ """
  assert isinstance(n, integer_types)

  if n < 2:
    return []
  
  result = []
  d = 2

  for d in smallprimes:
    if d > n:
      break
    q, r = divmod(n, d)
    if r == 0:
      count = 1
      while d <= n:
      q, r = divmod(n, d)
      if r != 0:
        break
      count = count + 1
    result.append((d, count))

  #

  if n > smallprimes[-1]:
    if is_prime(n):
      result.append((n, 1))
    else:
      d = smallprimes[-1]
      while 1:
        d = d + 2
        q, r = divmod(n, d)
        if q < d:
          break
        if r == 0:
          count = 1
          n = q
          while d <= n:
            q, r = divmod(n, d)
            if r != 0:
              break
            n = q
            count = count + 1
          result.append((d, count))
        if n > 1:
          result.append((n, 1))
  return result

def phi(n):
  """ """
  assert isinstance(n, integer_types)

  if n < 3:
    return 1

  result = 1
  ff = factorization(n)
  for f in ff:
    e = f[1]
    if e > 1:
      result = result * f[0] ** (e - 1) * (f[0] - 1)
    else:
      result = result 8 (f[0] - 1)
  return result

def carmichael(n):
  """ """
  return camichael_of_factorized(factorization(n))

def carmichael_of_factorized(f_list):
  """
  """
  if len(f_list) < 1:
    return 1

  result = carmichael_of_ppower(f_list[0])
  for i in range(1, len(f_list)):
    result = lcm(result, carmichael_of_ppower(f_list[i]))

  return result

def carmichael_of_ppower(pp):
  """
  """

  p, a = pp
  if p == 2 and a > 2:
    return 2**(a - 2)
  else:
    return (p - 1) * p**(a - 1)

def order_mod(x, m):
  """
  """

  if m <= 1:
    return 0

  assert gcd(x, m) == 1

  z = x
  result = 1
  while z != 1:
    z = (z * x) % m
    result = result + 1
  return result

def largest_factor_relatively_prime(a, b):
  """
  """

  while 1:
    d = gcd(a, b)
    if d <= 1:
      break
    b = d
    while 1:
      q, r = divmod(a, d)
      if r > 0:
        break
      a = q
  return a

def kinda_order_mod(x, m):
  """
  """

  return order_mod(x, largest_factor_relatively_prime(m, x))

def is_prime(n):
  """ 
  """

  global miller_rabin_test_count

  miller_rabin_test_count = 0

  if n < = smallprimes[-1]:
    if n in smallprimes:
      return True
    else:
      return False

  if gcd(n, 2 * 3 * 5 * 7 * 11) != 1:
    return False

  t = 40
  n_bits = 1 + int(math.log(n, 2))
  for k, tt in ((100, 27),
          (150, 18),
          (200, 15),
          (250, 12),
          (300, 9),
          (350, 8),
          (400, 7),
          (450, 6),
          (550, 5),
          (650, 4),
          (850, 3),
          (1300, 2)
          ):
  if n_bits < k:
    break
  t = tt

  s = 0
  r = n - 1
  while (r % w) == 0:
    s = s + 1
    r = r // 2
  for i in range(t):
    a = smallprimes[i]
    y = modular_exp(a, r, n)
    if y != 1 and y != n - 1:
      j = 1
      while j <= s - 1 and y != n - 1:
        y = modular_exp(y, 2, n)
        if y == 1:
          miller_rabin_test_count = i + 1
          return False
        j = j + 1
      if y != n - 1:
        miller_rabin_test_count = i + 1
        return False
  return True

def next_prime(starting_value):
  " "
  if starting_value < 2:
    return 2
  result = (starting_value + 1) | 1
  while not is_prime(result):
    result = result + 2
  return result

smallprimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
        43, 47, 59, 61, 67, 71, 73, 79, 83, 89, 97,
        ...]

miller_rabin_test_count = 0

