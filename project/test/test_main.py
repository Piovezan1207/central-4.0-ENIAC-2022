import json

jsonTeste = {
            "type" : "assemble",
            "properties" : [{
                "id" : "10",
                "color" : "BLACK",
            }],
        }


for i in jsonTeste:
    print(jsonTeste[i])


if "type" not in jsonTeste or "properties" not in jsonTeste: print("erro 1")

typesList = ["assemble" , "storage"]
if  jsonTeste["type"] not in typesList: print("erro 2")

propertiesList = {
    "assemble" : ["id"  ],
    "storage" : [["id" ] , ["color"]],
    }


listOfMandatoryProperties = ["id"]
listOfOptionalProperties = ["color"]
propertiesList = listOfMandatoryProperties + listOfOptionalProperties
colorsList = ["BLACK" , "SILVER" , "RED"]



for i in listOfMandatoryProperties:
    if i not in jsonTeste["properties"][0]:
        print("erro 3")

for i in jsonTeste["properties"][0]:
    if i not in propertiesList: print("erro 4")

if jsonTeste["type"] == "assemble" and "color" not in jsonTeste["properties"][0]: print("erro 5")