from os import listdir
import json

pythonFiles = [];
PERMISSION = 'Permission'
RESOURCE = 'Resource'
METHOD = 'Method'


# PYaml doesn't handle the AWS Functions well so we need to add them manually.

SOURCE_ARN = {"Fn::Join" : ["", ["arn:aws:execute-api:", { "Ref" : "AWS::Region"}, ":", { "Ref" : "AWS::AccountId"}, ":", { "Ref" : "RestApi" }, "/*"]]}
REST_API_ID = {"Ref" : "RestApi"}
LAMBDA_PERMISSION_ARN = {"Fn::Join" : ["", ["arn:aws:iam::", { "Ref" : "AWS::AccountId"}, ":role/pickPocketWriteAndSNS"]]}

for file in listdir():
    if file.endswith(".py") and file != "concat_files.py":
        pythonFiles.append(file)

parentyaml = {}
jsonOut = {}

for pythonFile in pythonFiles:
    with open('deploy_template.json') as templateFile:
        with open('api_gateway_template.json') as apiTemplateFile:
            with open(pythonFile) as appendFile:
                functionName = pythonFile.replace(".py", "") + "CLOUDFORM"

                tempJSON = json.load(templateFile)
                apiTemplateJSON = json.load(apiTemplateFile)

                jsonOut[functionName] = tempJSON['FunctionName']

                # Create Function
                propJson = jsonOut[functionName]["Properties"]
                codeJson = propJson["Code"]
                codeJson['ZipFile'] = appendFile.read()
                propJson['FunctionName'] = functionName
                propJson['Role'] = LAMBDA_PERMISSION_ARN

                # Add Permission
                permissionTemplate = apiTemplateJSON[PERMISSION]
                permissionName = PERMISSION + functionName
                jsonOut[permissionName] = permissionTemplate
                jsonOut[permissionName]['DependsOn'] = functionName
                jsonOut[permissionName]['Properties']['FunctionName'] = functionName
                jsonOut[permissionName]['Properties']['SourceArn'] = SOURCE_ARN

                # Add Resource
                resourceTemplate = apiTemplateJSON[RESOURCE]
                resourceName = RESOURCE + functionName
                jsonOut[resourceName] = resourceTemplate
                jsonOut[resourceName]['DependsOn'] = functionName
                # TODO pull path name from other JSON file
                jsonOut[resourceName]['Properties']['PathPart'] = functionName.replace("CLOUDFORM", "")

                # Add Method
                # TODO add way to tell whether this should be a GET or a POST
                methodTemplate = apiTemplateJSON[METHOD]
                methodName = METHOD + functionName
                jsonOut[methodName] = methodTemplate
                methodUri = { "Fn::Join" : ["", ["arn:aws:apigateway", ":", { "Ref" : "AWS::Region" }, ":","lambda:path/2015-03-31/functions/arn:aws:lambda", ":", { "Ref" : "AWS::Region" }, ":", { "Ref" : "AWS::AccountId" }, ":function:", functionName, "/invocations"]]}
                jsonOut[methodName]['Properties']['Integration']['Uri'] = methodUri
                jsonOut[methodName]['Properties']['RestApiId'] = REST_API_ID
                jsonOut[methodName]['Properties']['ResourceId'] = { "Ref": resourceName}
                jsonOut[methodName]['DependsOn'] = [functionName, resourceName, permissionName]

with open("deploy.json", "a") as f:
    with open("api_gateway_base.json") as baseTemplateFile:
        baseTemplateJSON = json.load(baseTemplateFile)
        jsonOut['RestApi'] = baseTemplateJSON['RestApi']
        parentyaml['Resources'] = jsonOut
        json.dump(parentyaml, f, indent=4, sort_keys=True)
