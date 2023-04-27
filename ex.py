import json
import sys

print(sys.argv[1:3])


print(len(sys.argv))

print(sys.argv, '\n\n')

if len(sys.argv) == 1:
    print('nada foi digitado')