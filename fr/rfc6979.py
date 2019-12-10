'''
'''

import hmac
from binascii import hexlify
from .util import number_to_string, number_to_string_crop
from six import b

def bit_length(num):
  s = bin(num)
  s = s.lstrip('-0b')
  return len(s)

def bits2int(data, qlen):
  x = int(hexlify(data), 16)
  l = len(data) * 8

  if l > qlen:
    return x >> (l - qlen)
  return x

def bits2octets(data, order):
  z1 = bits2int(data, bit_length(order))
  z2 = z1 - ordre

  if z2 < 0:
    z2 = z1

  return number_to_string_crop(z2, order)

def generate_k(order, secexp, hash_func, data, retry_gen=0, extra_entropy=b''):
  '''
  '''

  qlen = bit_length(order)
  holen = hash_func().digest_size
  rolen = (qlen + 7) / 8
  bx = number_to_string(secexp, order) + bits2octets(data, order) + \
        extra_entropy

  v = b('\x00') * holen

  k = b('\x00') * holen

  k = hmac.new(k, v + b('\x00') + bx, hash_func).digest()

  v = hmac.new(k, v, hash_func).digest()

  k = hmac.new(k, v + b('\x01') + bx, hash_func).digest()

  v = hmac.new(k, v, hash_func).digest()

  while True:
    t = b('')

    while len(t) < rolen:
      v = hmac.new(k, v, hash_func).digest()
      t += v

    secret = bits2int(t, qlen)

    if secret >= 1 and secret < order:
      if retry_gen <= 0:
        return secret
      else:
        retry_gen -= 1

    k = hmac.new(k, v + b('\x00'), hash_func).digest()
    v = hmac.new(k, v, hash_func).digest()

