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
if "{:?}" in bar:
    print("yes")

print(isinstance(foo, list))
print(isinstance(bar, str))