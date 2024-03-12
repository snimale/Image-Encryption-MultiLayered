prime_1 = 3211891519                                              # choose p
prime_2 = 98765421103                                             # choose q
big_clock = prime_1 * prime_2  # = 317223818411189325457          # find n
small_clock = (prime_1-1) * (prime_2-1)                           # find m = (p-1) * (q-1)
public_key = 618596131                                            # find e
private_key = 291273621025443274195                               # find d

# Cipher = (data^e) mod n
# data = (Cipher^d) mod n

