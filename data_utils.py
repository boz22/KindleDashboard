"""
Converts a list of objects to a csv string
The list of the columns for the resulting csv is obtained by taking the first object in the list and retrieving
the names of its attributes.
It is therefore assumed that objects in this list are of the same type (i.e.: same number of attributes with the same names)
If an element has a missing value for one of its attributes, it will be empty in the csv.
If the list is empty or the objects contained in the list do not have a public attribute (i.e: not startig with _ ) an empty
string will be returned.
"""
def objects_list_to_csv(objList):
    columnNames = [];
    if len(objList) > 0:
        #Get names of the attributes
        referenceObj = objList[0]
        for attrName in dir(referenceObj):
            if not attrName.startswith("_"):
                columnNames.append(attrName)
    else:
        print('The list is empty. Cannot convert an empty list into a csv since there is no way to figure out column names')
        return ""

    if len(columnNames) == 0:
        print('The number of columns is 0. Cannot build a csv with no column')
        return ""
    #Building the columns rows of the csv
    header = ""
    for col in columnNames:
        header = header + col + ","
    #At the end, we need to remove the comma at the end
    header = header[:-1]

    csvBody=""
    #Now iterating through list and create rows of csv
    for obj in objList:
        csvRow = ""
        for col in columnNames:
            csvRow = csvRow + getattr(obj,col) + ","
        csvRow = csvRow[:-1]
        csvBody = csvBody + csvRow + '\n'


    return header + '\n' + csvBody
