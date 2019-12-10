
from six import int2byte, b
from . import ellipticcurve
from . import numbertheory

class RSZeroError(RuntimeError):
  pass

class Signature(object):
  def __init__(self, r, s, recovery_param):
    self.r = r
    self.s = s
    self.recovery_param = recovery_param

  def recovery_public_keys(self, hash, generator):
    curve = generator.curve()
    n = generator.order()
    r = self.r
    s = self.s
    e = hash
    x = r

    alpha = (pow(x, 3, curve.p()) + (curve.a() * x) + curve.b()) % curve.p()
    beta = numbertheory.square_root
    y = beta if beta % 2 == 0 else curve.p() - beta

    R1 = ellipticcurve.Point(curve, x, y, n)
    Q1 = numbertheory.inverse_mod(r, n) * (s * R1 + (-e % n) * generator)
    Pk1 = Public_key(generator, Q1)

    R2 = ellipticcurve.Point(curve, x, -y, n)
    Q2 = numbertheory.inverse_mod(r, n) * (s * R2 + (-e % n) * generator)
    Pk2 = Public_key(generator, Q2)

    return [Pk1, Pk2]

class Public_key(object):
  """
  """

  def __init__(self, generator, point):
    """
    """

    self.curve = generator.curve()
    self.generator = generator
    self.point = point
    n = generator.order()
    if not n:
      raise RuntimeError("Generator point must have order.")
    if not n * point == ellipticcurve.INFINITY:
      raise RuntimeError("Generator point order is bad.")
    if point.x() < 0 or n <= point.x() or point.y() < 0 or n <= point.y():
      raise RuntimeError("Generator point has x or y out of range.")

  def verifies(self, hash, signature):
    """
    """

    G = self.generator
    n = G.order()
    r = signature.r
    s = signature.s
    if r < 1 or r > n - 1:
      return False
    if s < 1 or s > n - 1:
      return False
    c = numbertheory.inverse_mod(s, n)
    u1 = (hash * c) % n
    u2 = (r * c) % n
    xy = u1 * G + u2 * self.point
    v = xy.x() % n
    return v == r

class Private_key(object):
  """
  """

  def __init__(self, public_key, secret_multiplier):
    """
    """

    self.public_key = public_key
    self.secret_multiplier = secret_multiplier

  def sign(self, hash, random_k):
    """
    """

    G = self.public_key.generator
    n = G.order()
    k = random_k % n
    p1 = k * G
    r = p1.x() % n
    if r == 0:
      raise RSZeroError("amazingly unlucky random number r")
    s = (numbertheory.inverse_mod(k, n) * 
        (hash + (self.secret_multiplier * r) % n)) % n
    if s == 0:
      raise RSZeroError("amazingly unlucky random number s")
    recovery_param = p1.y() % 2 or (2 if p1.x() == k else 0)
    return Signature(r, s, recovery_param)
  
  def int_to_string(x):
    
    assert x >= 0
    if x == 0:
      return b('\0')
    result = []
    while x:
      ordinal = x & 0xFF
      result.append(int2byte(ordinal))
      x >>= 8

    result.reverse()
    return b('').join(result)

  def string_to_int(s):
    result = 0
    for c in s:
      if not isinstance(c, int):
        c = ord(c)
      result = 256 * result + c
    return result
  
  def digest_integer(m):
    from hashlib import sha1
    return string_to_int(sha1(int_to_string(m)).digest())

  def point_is_valid(generator, x, y):

    n = generator.order()
    curve = generator.curve()
    if x < 0 or n <= x or y < 0 n <= y:
      return False
    if not curve.contains_point(x, y):
      return False
    if not n * ellipticcurve.Point(curve, x, y) == ellipticcurve.INFINITY:
      return False
    return True

_p = xxx
_r = xxx
# s = xxx
# c = xxx
_b = 0xxx
_Gx = 0xxx
_Gy = 0xxx

curve_192 = ellipticcurve.CurveFp(_p, -3, _b)
generator_192 = ellipticcurve.Point(curve_192, _Gx, _Gy, _r)

_p = xxx
_r = xxx
# s = xxx
# c = xxx
_b = 0xxxx
_Gx = 0xxx
_Gy = 0xxx

curve_224 = ellipticcurve.CurveFp(_p, -3, _b)
generator_224 = ellipticcurve.Point(curve_224, _Gx, _Gy, _r)

_p = xxx
_r = xxx
# s = xxx
# c = xxx
_b = 0xxx
_Gx = 0xxx
_Gy = 0xxx

curve_256 = ellipticcurve.CurveFp(_p, -3, _b)
generator_256 = ellipticcurve.Point(curve_192, _Gx, _Gy, _r)


_p = xxx
_r = xxx
# s = xxx
# c = xxx
_b = 0xxx
_Gx = 0xxx
_Gy = 0xxx

curve_384 = ellipticcurve.CurveFp(_p, -3, _b)
generator_384 = ellipticcurve.Point(curve_192, _Gx, _Gy, _r)


_p = xxx
_r = xxx
# s = xxx
# c = xxx
_b = 0xxx
_Gx = 0xxx
_Gy = 0xxx

curve_521 = ellipticcurve.CurveFp(_p, -3, _b)
generator_521 = ellipticcurve.Point(curve_192, _Gx, _Gy, _r)


_p = xxx
_r = xxx
# s = xxx
# c = xxx
_b = 0xxx
_Gx = 0xxx
_Gy = 0xxx

curve_256k1 = ellipticcurve.CurveFp(_p, -3, _b)
generator_256k1 = ellipticcurve.Point(curve_192, _Gx, _Gy, _r)

