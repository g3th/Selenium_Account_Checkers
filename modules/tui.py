from titles.main_title import title

def options():
    while True:
        print("\x1bc")
        title()
        print("\n+------------------------+")
        print("|Pick a Service or Quit: |")
        print("+------------------------+")
        print("|    1) Dazn             |")
        print("|    2) Disney           |")
        print("|    3) HBO              |")
        print("|    4) ESPN+            |")
        print("|    5) Paramount        |")
        print("|    6) Direct TV        |")
        print("|    7) Quit             |")
        print("+------------------------+")
        try:
            option = int(input("> "))
            # Non-Inclusive
            if option not in range(1, 8):
                print("Invalid Option.")
                input("Press Enter to continue...")
            elif option == 7:
                print("Goodbye.")
                break
            else:
                return option
        except ValueError as e:
            print("Not a numeric value.")
            print("Press Enter to continue...")
            input()
