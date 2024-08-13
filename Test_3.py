import os
import shutil

class save:
    def __init__(self):
        self.filepath = "Data/config/path.txt"
        with open(self.filepath, "r") as f:
            self.content = f.read()
        self.content = self.content.split("|")

    def convert_to_scsp(self):
        with open("Data/temp/temp.scsp", "w") as f:
            f.write("init()\nvariable.init()\nmodule.init()\nmotor.init()\nsensor.init()\ncalibration.init()\nai.init()\ngenerate_ab(new_function)\n")
            for i in self.content:
                match i:
                    case 1:
                        f.write("    drive(10)")
                    case 2:
                        f.write("    tank(180)")
                    case 3:
                        f.write("    drive(-10)")
                    case 4:
                        f.write("    tank(-180)")
            f.write("main.init()\nswitch()\ncalibrate()\nai.run({'Calibration': calibration, 'Akku': 85, 'Wheelusage': 0.95})")
        pass