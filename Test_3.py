import os
import shutil

class save:
    def __init__(self):
        self.filepath = "Data/config/path.txt"
        with open(self.filepath, "r") as f:
            self.content = f.read()
        self.content = self.content.split("|")
        self.convert_to_scsp()

    def convert_to_scsp(self):
        generate_ab_function = 0
        with open("Data/temp/temp.scsp", "w") as f:
            f.write("init()\nvariable.init()\nmodule.init()\nmotor.init()\nsensor.init()\ncalibration.init()\nai.init()\ngenerate_ab(new_function)\n")
            for i in self.content:
                match i:
                    case "1":
                        f.write("drive(5)\n")
                    case "2":
                        f.write("tank(90)\n")
                    case "3":
                        f.write("drive(-5)\n")
                    case "4":
                        f.write("tank(-90)\n")
                    case "5":
                        f.write(f"generate_ab({generate_ab_function})")
                        generate_ab_function += 1
            f.write("main.init()\nswitch()\ncalibrate()\nai.run({'Calibration': calibration, 'Akku': 85, 'Wheelusage': 0.95})\n")
            for i in range(generate_ab_function):
                f.write(f"switch()\n")
                f.write(f"generate_ab({i})\n")
            f.write("main.run()")


if __name__ == "__main__":
    save()