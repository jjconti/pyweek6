import math

funciones = [lambda x,direccion: direccion*20*math.sin(x/2),
                 lambda x,direccion: direccion*20*math.cos(x/2),
                 lambda x,direccion: direccion*x,
                 lambda x,direccion: direccion*x**2/6,
                 lambda x,direccion: -direccion*x**2/6]

for n, f in zip('abcde', funciones):
    print '%s = {' % n,
    for x in xrange(6000):
        print "%i:%f," % (x,f(math.radians(x)*50,1))
    print '}'