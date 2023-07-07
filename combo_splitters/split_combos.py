class ComboSplitter:

    def __init__(self, combo_dir, combo_name):

        self.combo_directory = combo_dir
        self.combo_name = combo_name
        self.user = []
        self.password = []
        self.error = 0

    def split_file(self):
        try:
            with open(self.combo_directory, 'r') as combos:
                for line in combos.readlines():
                    self.user.append(line.split(":")[0])
                    self.password.append(line.split(":")[1].split(" ")[0].strip())
            return self.user, self.password
        except FileNotFoundError:
            self.error = 1
            return 1
        except IndexError:
            self.error = 2
            return 1


    def return_error(self):
        match self.error:
            case 1:
                print("\nNo combo-list found.\n")
                print("Add one, and name it '" + self.combo_name + "' before starting the program.")
                print("\nEnding.\n")
            case 2:
                print("\nThere is something wrong with the combo-list\n\n")
                print("Please check:\n\n1) There are no invalid characters\n")
                print("2) There are no extra lines in the file (i.e. ASCII graphics etc)\n")
                print("3) There is no extra information (i.e. made by) at the top/bottom of the file\n")
                print("4) There are no extra spaces at the top or bottom of the file\n")
