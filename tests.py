def thing():
    return True,'hi'


a = thing()
if thing()[0]:
    print('good')
