import sys
import time

prompt = "Prompt:"
for x in range(10):
    inputStr = input(prompt).lower()
    print('\033[1A'+'\033[K')
    print(inputStr)

