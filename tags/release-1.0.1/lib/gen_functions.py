import math
import string
import random

#funciones = [    lambda x,direccion: direccion*20*math.sin(x/2),
                 #lambda x,direccion: direccion*20*math.cos(x/2),
                 #lambda x,direccion: direccion*x,
                 #lambda x,direccion: direccion*x**2/6,
                 #lambda x,direccion: -direccion*x**2/6,
                 ##lambda x,d: math.log(x)*x+math.sin(x),
                 #lambda x,d: (x**2*math.cos(x)/5) / 15,
                 #lambda x,d: math.sin(x) * 25]




funciones = [
    lambda x,d: math.sin(x*.05) * 50,
    lambda x,direccion: direccion*1.5*x,
    lambda x,direccion: direccion*10*x**2/200,
    lambda x,direccion: -1*7*x**2/200,
    lambda x,d: x*2*math.sin(x*.05),
]



for n, f in zip(string.letters, funciones):
    print '%s = {' % n,
    for x in xrange(6000):
        print "%i:%f," % (x,f(math.radians(x)*50,1))
    print '}'

print "functions=[" + ", ".join(["%s" % x for x in string.letters[:len(funciones)]]) + "]"
