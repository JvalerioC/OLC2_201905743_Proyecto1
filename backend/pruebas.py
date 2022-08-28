'''s = 'fun {} {} {}'
c = '{}'
print(s.find(c))

s = 'fun {} {} {}'
c = '{}'
lst = []
for pos,char in enumerate(s):
    if(char == c):
        lst.append(pos)

print(lst)
x = ["my", "unlimited", "sadness"]
for i in range(len(x)-1, -1, -1):
    print(i, x[i])'''
import string
from tokenize import String
from xml.etree.ElementInclude import include


foo = []
bar = "{:?}"
print(bar)
a = 100.0

if a > 50.0:
    a = a/2 +20
    print(a)

bar1 = str(bar)
print(bar, bar1)

print(isinstance(foo, list))
print(False or False)

for i in "hola":
    print(i)