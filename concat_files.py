from os import listdir
import yaml

pythonFiles = [];

for file in listdir():
    if file.endswith(".py") and file != "concat_files.py":
        pythonFiles.append(file)

parentyaml = {}
yamls = {}

for pythonFile in pythonFiles:
    with open('deploy_template.yaml') as templateFile:
        with open(pythonFile) as appendFile:
            functionName = pythonFile.replace(".py", "") + "CLOUDFORM"

            tempYaml = yaml.load(templateFile)
            yamls[functionName] = tempYaml['FunctionName']

            propYaml = yamls[functionName]["Properties"]
            codeYaml = propYaml["Code"]
            codeYaml['ZipFile'] = appendFile.read()
            propYaml['FunctionName'] = functionName


with open("deploy.yaml", "a") as f:
    parentyaml['Resources'] = yamls
    yaml.dump(parentyaml, f)
