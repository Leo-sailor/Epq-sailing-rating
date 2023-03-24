import pandas
import tabula
import cProfile
def findandreplace(inp,find,replace):
    if type(inp) == str:
        findlength = len(find)
        locations = []
        replaceletters = list(replace)
        for x in range(0,len(inp)-findlength):
            if inp[x: x + findlength] == find:
                locations.append(list(range(x, x + findlength)))
        letters = list(inp)
        for x in range(len(locations) - 1,-1,-1):
            for y in range(len(locations[x]) - 1,-1,-1):
                letters.pop(locations[x][y])
            for z in range(len(replaceletters)):
                letters.insert(locations[x][y+z],replaceletters[z])

        return ''.join(letters)

    elif type(inp) == list:
        out = []
        for item in inp:
            out.append(findandreplace(item,find,replace))
        return out
    elif type(inp) == float or type(inp) == int:
        return findandreplace(str(inp),find,replace)
    else:
        raise TypeError('Expected type list or str not ' + str(type(inp)))

def megatablefrompdf(file):
    tables = tabula.read_pdf(file, pages="all")
    table = pandas.concat(tables)
    lists = table.values.tolist()
    head = [(table.columns.tolist())]
    for row in lists:
        head.append(row)
    head = findandreplace(head,"\r"," ")
    return head


