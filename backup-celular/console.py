# ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"  # Resets the color

def print_error(text: str) -> None:
   print(f"{RED}{text}{RESET}") 

def print_success(text: str) -> None:
   print(f"{GREEN}{text}{RESET}") 

def print_warning(text: str) -> None:
   print(f"{YELLOW}{text}{RESET}")

def print_info(text: str) -> None:
   print(f"{BLUE}{text}{RESET}")  