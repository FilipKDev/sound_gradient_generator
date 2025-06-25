from ui_elements import *

def generate_test_image(*args):
    if len(args) < 2:
        raise ValueError("Minimum arguments required: Width, Height")
    win = Window(args[0], args[1], args[2], args[3])
    win.run()

def main():
    #params = input("Enter parameters: ")
    params = "1000 1000 0 100"
    generate_test_image(*params.split())
    print("Complete!")

main()