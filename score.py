from colorama import Fore, Back, Style, init
import time
import os

init(autoreset=True)

os.system('cls' if os.name == 'nt' else 'clear')

# Stylish Border
border = Fore.CYAN + Style.BRIGHT + "═" * 50
print(border)

# Text Animation
text = "🌙✨ KHAIR MUBARAK MADAM ✨🌙"

print("\n")

for char in text:
    print(Fore.MAGENTA + Style.BRIGHT + char, end="", flush=True)
    time.sleep(0.06)

print("\n\n")

# Footer Style
print(border)
print(Fore.YELLOW + Style.BRIGHT + "✨ Wishing You Endless Happiness & Blessings ✨")
print(border)

# Glow Effect Lines
for i in range(3):
    print(Fore.GREEN + "✨ " * 20)
    time.sleep(0.3)