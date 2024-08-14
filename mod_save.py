import os
import shutil
import sys
import json
import zipfile
from datetime import datetime

content_compile = []
last_function = "False"
file_name = ""
conf_file = "Data/config/conf.json"
llsp3_file_path = 'Projekt.llsp3'
extracted_folder = llsp3_file_path + 'projectbody.json'

with open(conf_file, "r") as file:
    content = json.load(file)
    calibrate = content["calibrate"]
    __version__ = content["version"]
    module = content["module"]
    motor = content["motor"]
    sensor = content["sensor"]
    variables = content["variables"]
    ai = content["ai"]
    switch = content["switch"]

class Save:
    def __init__(self):
        self.filepath = "Data/config/path.txt"
        with open(self.filepath, "r") as f:
            self.content = f.read()
        self.content = self.content.split("|")
        self.convert_to_scsp()
        self.compile("Data/temp/temp.scsp")
        self.main()

    def convert_to_scsp(self):
        generate_ab_function = 1
        generate_ab_function_names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
        with open("Data/temp/temp.scsp", "w") as f:
            f.write("init()\nvariable.init()\nmodule.init()\nmotor.init()\nsensor.init()\ncalibration.init()\nai.init()\ngenerate_ab(zero)\n")
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
                        f.write(f"generate_ab({generate_ab_function_names[generate_ab_function]})\n")
                        generate_ab_function += 1
            f.write("main.init()\nswitch()\ncalibrate()\nai.run({'Calibration': calibration, 'Akku': 85, 'Wheelusage': 0.95})\n")
            f.write("switch()\n")
            f.write("call(new_function)\n")
            for i in range(generate_ab_function):
                f.write(f"switch()\n")
                f.write(f"call({generate_ab_function_names[i]})\n")
            f.write("main.run()")

    def compile(self, file):
        global content_compile
        if file.endswith(".scsp"):
            with open(file, "r") as f:
                content = f.readlines()
                for line in content:
                    content_compile.append(line)
        else:
            print(f"Error: The file {file} is not a valid file type.")

    def get_active_function(self, line):
        function, variable = line.split("(")
        variable = variable.replace("(", "").replace(")", "").replace("\n", "")
        return function, variable

    def write_function(self, function,file,value=False):
        """
        Writes the specified function and its value to a Python file.

        Parameters:
            function (str): The function to write.
            file (str): The name of the file to write to.
            value (str, optional): The value associated with the function. Defaults to False.
        """
        global last_function
        print(f"Writing {function} function...")
        file_name = file.split(".")
        file_name = file_name[0]
        with open(f"{os.path.join(os.getcwd() + "\\Data\\temp", file_name)}.py", "a") as f:
            match function:
                case "log":
                    if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                        f.write(f"\n  print('{str(value)}')")
                    elif last_function == "switch":
                        f.write(f"\n    print('{str(value)}')")
                    else:
                        f.write(f"\nprint('{str(value)}')")
                case "sleep":
                    sleep_out = f"\ntime.sleep({str(value)})"
                    f.write(sleep_out)
                case "init":
                    init_out = f"\nimport force_sensor, distance_sensor, motor, motor_pair\nfrom hub import port\nimport time\nfrom app import linegraph as ln\nimport runloop\nfrom math import *\nimport random\nimport math\n"
                    f.write(init_out)
                case "ai.init":
                    ai_content = ai
                    for line in ai_content:
                        f.write(line)
                case "module.init":
                    for line in module:
                        f.write(line)
                case "motor.init":
                    for line in motor:
                        f.write(line)
                case "sensor.init":
                    for line in sensor:
                        f.write(line)
                case "calibration.init":
                    for line in calibrate:
                       f.write(line)
                case "variable.init":
                    for line in variables:
                        f.write(line)
                case "switch.init":
                    for line in switch:
                        f.write("\n")
                        f.write(line)
                case "drive":
                    if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                        f.write(f"\n  await drive({value})")
                    elif last_function == "switch":
                        f.write(f"\n    await drive({value})")
                    else:
                        f.write(f"\n  await drive({value})")
                case "tank":
                    if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                        f.write(f"\n  await tank({value})")
                    elif last_function == "switch":
                        f.write(f"\n    await tank({value})")
                    else:
                        f.write(f"\n  await tank({value})")
                case "obstacle":
                    if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                        f.write(f"\n  await obstacle({value})")
                    elif last_function == "switch":
                        f.write(f"\n    await obstacle({value})")
                    else:
                        f.write(f"\n  await obstacle({value})")
                case "module":
                    if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                        f.write(f"\n  await module({value})")
                    elif last_function == "switch":
                        f.write(f"\n    await module({value})")
                    else:
                        f.write(f"\n  await module({value})")
                case "calibrate":
                    if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                        f.write("\n  await calibrate()")
                    elif last_function == "switch":
                        f.write("\n    await calibrate()")
                    else:
                        f.write("\n  await calibrate()")
                case "main.init":
                    f.write("\nasync def main():")
                case "main.run":
                    f.write("\nrunloop.run(main())")
                case "switch":
                    if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                        f.write("\n  if await switch():")
                    elif last_function == "switch":
                        pass
                    else:
                        f.write("\n  if await switch():")
                case "call":
                    if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                        f.write(f"\n  await {value}()")
                    elif last_function == "switch":
                        f.write(f"\n    await {value}()")
                case "generate_ab":
                    f.write(f"\nasync def {value}():") # async dev (value) <- function_name()
                case "ai.run":
                    if last_function == "main.init" or last_function == "generate_ab" or last_function == "module" or last_function == "drive" or last_function == "tank" or last_function == "obstacle" or last_function == "ai.run" or last_function == "calibrate" :
                        f.write("\n  global calibration")
                        f.write(f"\n  new_data_point = {value}") # {'Kalibrierung': calibration, 'Batterieladestand': 85, 'Reifennutzung': 0.95}
                        f.write("\n  calibration = knn_predict(data, new_data_point, k=3)")
                        f.write("\n  print(f'Vorhergesagte Multiplikation: {calibration}')")
                    elif last_function == "switch":
                        f.write("\n    global calibration")
                        f.write(f"\n    new_data_point = {value}") # {'Kalibrierung': calibration, 'Batterieladestand': 85, 'Reifennutzung': 0.95}
                        f.write("\n    calibration = knn_predict(data, new_data_point, k=3)")
                        f.write("\n    print(f'Vorhergesagte Multiplikation: {calibration}')")
                case _:
                    if function == "//" or function == "#":
                        f.write(f"\n# {value}")
                    else:
                        print(f"Error: The function {function} does not exist.")
                        sys.exit(1)
            last_function = function
            print(f"{last_function} function written...")

    def compile_llsp3(self, file, directory, project_name):
        os.makedirs(directory, exist_ok=True)
        projectbody_data = {
            "main": ""
        }
        icon_svg_content = """
        <svg width="60" height="60" xmlns="http://www.w3.org/2000/svg">
            <g fill="none" fill-rule="evenodd">
                <g fill="#D8D8D8" fill-rule="nonzero">
                    <path d="M34.613 7.325H15.79a3.775 3.775 0 00-3.776 3.776v37.575a3.775 3.775 0 003.776 3.776h28.274a3.775 3.775 0 003.776-3.776V20.714a.8.8 0 00-.231-.561L35.183 7.563a.8.8 0 00-.57-.238zm-.334 1.6l11.96 12.118v27.633a2.175 2.175 0 01-2.176 2.176H15.789a2.175 2.175 0 01-2.176-2.176V11.1c0-1.202.973-2.176 2.176-2.176h18.49z"/>
                    <path d="M35.413 8.214v11.7h11.7v1.6h-13.3v-13.3z"/>
                </g>
                <path fill="#0290F5" d="M23.291 27h13.5v2.744h-13.5z"/>
                <path fill="#D8D8D8" d="M38.428 27h4.32v2.744h-4.32zM17 27h2.7v2.7H17zM17 31.86h2.7v2.744H17zM28.151 31.861h11.34v2.7h-11.34zM17 36.72h2.7v2.7H17zM34.665 36.723h8.1v2.7h-8.1z"/>
                <path fill="#0290F5" d="M28.168 36.723h4.86v2.7h-4.86z"/>
            </g>
        </svg>
        """
        projectbody_path = os.path.join(directory, 'projectbody.json')
        with open(os.path.join("Data\\temp", file), 'r') as file:
            projectbody_data['main'] = file.read()
        with open(projectbody_path, 'w') as file:
            json.dump(projectbody_data, file)
        icon_svg_path = os.path.join(directory, 'icon.svg')
        with open(icon_svg_path, 'w') as file:
            file.write(icon_svg_content)
        current_datetime = datetime.utcnow().isoformat() + 'Z'
        manifest_data = {
            "type": "python",
            "appType": "llsp3",
            "autoDelete": False,
            "created": current_datetime,
            "id": "wJI4suuRFvcs",
            "lastsaved": current_datetime,
            "size": 1004,
            "name": project_name,
            "slotIndex": 0,
            "workspaceX": 120,
            "workspaceY": 120,
            "zoomLevel": 0.5,
            "hardware": {
                "python": {
                    "type": "flipper"
                }
            },
            "state": {
                "canvasDrawerOpen": True
            },
            "extraFiles": []
        }
        manifest_path = os.path.join(directory, 'manifest.json')
        with open(manifest_path, 'w') as file:
            json.dump(manifest_data, file)
        llsp3_file_path = os.path.join(project_name + '.llsp3')
        with zipfile.ZipFile(llsp3_file_path, 'w') as zip_ref:
            for foldername, subfolders, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, directory)
                    zip_ref.write(file_path, arcname)

        if os.path.exists(llsp3_file_path):
            os.remove(manifest_path)
            os.remove(icon_svg_path)
            os.remove(projectbody_path)
            os.rmdir(directory)
            os.remove(os.path.join("Data\\temp", project_name + '.py')) # Remove this File if you want to debug the app / if the .llsp3 file is not working

    def main(self):
        global content_compile
        file = "temp.scsp"
        file_name = file.split(".")[0]
        file_dir = os.getcwd() + "\\Data\\temp\\llsp3"
        os.makedirs(file_dir, exist_ok=True)
        with open(f"{os.path.join("Data\\temp", file_name)}.py", "w") as f:
            f.write("")
        for line in content_compile:
            function, value = self.get_active_function(line)
            self.write_function(function, file, value)
        self.compile_llsp3(file_name + ".py", file_dir, file_name)