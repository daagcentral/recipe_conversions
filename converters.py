import json
import csv
from pprint import pprint

def convertrecipes(jsonFile):
    recipeList = []
    recipeDict = {}
    idList = []
    jsonFile =  str(jsonFile) + '.json'
    with open(jsonFile) as f:
        dataNew = json.load(f)
        dataNew = dataNew["recipes"]
        print("new: " + str(len(dataNew)))
    with open('convrecipes.json') as g:
        dataExisting = json.load(g)
        dataExisting = dataExisting["recipes"]    
        print("Existing: " + str(len(dataExisting)))
    for i in dataExisting:
        idList += [i["id"]]

    for i in range(len(dataNew)):
        listOfFood = []
        listOfQty = []
        listOfSteps = []
        recipe = dataNew[i]
        recipes = {}
        if recipe["id"] not in idList:
            recipes['id'] = recipe["id"]
            recipes['name'] = recipe["title"]
            recipes['sourceName'] = recipe["sourceName"]
            recipes['sourceLink'] = recipe["sourceUrl"]
            recipes['imageUrl'] = recipe["image"]
            cookTime = recipe["readyInMinutes"]
            recipes['cookTimeMinutes'] = cookTime % 60
            recipes['cookTimeHours'] = cookTime//60
            ingredients = recipe["extendedIngredients"]
            
            for j in ingredients:
                listOfFood += [str(j["amount"]) + " " + str(j["unit"]) + " of " + j["name"]]
            recipes['ingredients'] = listOfFood

            analyzed_instruction = recipe["analyzedInstructions"]  
            step = analyzed_instruction[0]
            steps = step["steps"]
            for k in steps:
                listOfSteps += [k["step"]]
            recipes['instructions'] = listOfSteps   
            
            dataExisting += [recipes]
    recipeDict["recipes"] = dataExisting
    with open('convrecipes.json','w') as f:
        f.write(json.dumps(recipeDict, sort_keys=True, indent =2))    

    print("we now have: " + str(len(dataExisting)))

def extractCsv():

    with open('plu_codes.csv', 'r') as csvfile:
        rawPlu = csv.reader(csvfile)
        data = [r for r in rawPlu]
        with open('plus.json') as f:
            data1 = json.load(f)
        print(data[1][0])    
        for i in data:
            pprint(i)
            data1[str(i[0])] = i[1]
    print(data1)
    with open('plus.json','w') as f:
        f.write(json.dumps(data1, sort_keys=True, indent =2))    

            
def getFoodsFromRecipe():
    with open('convrecipes.json') as f:
        data = json.load(f)
        data = data["recipes"]
        Foods = []
        string = " of "

        for i in range(1):

            recipe = data[i]
            ingredients = recipe["ingredients"]

            for j in range(len(ingredients)):
                
                food = ingredients[j]
                food = food.partition(string)[2]
                if food not in Foods:
                    Foods += [ food ]

        Foods.sort()
        str1 = "foods.add(new Food(\""
        str2 = "\"));"
        for k in Foods:
            print(str1 + k + str2)


def readBarcode():
    with open('barcode.json') as f:
        barcode = json.load(f)
    return barcode
def saveBarcode(code, item):
    barcodes = readBarcode()
    if code not in barcodes:
        barcodes[code] = item
        with open('barcode.json', 'w') as f:
            f.write(json.dumps(barcodes, sort_keys=True, indent=2))
            return item
    return ''