try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


class teste:
     def __init__(self, val1, val2) -> None:
         self.val1 = val1
         self.val2 = val2

# objetos = [teste(1,2) , teste(3,4) , teste(5,6)]

# save_object( objetos, "teste.pkl")

with open('teste.pkl', 'rb') as inp:
    objetos = pickle.load(inp)

for i in objetos:
    print(i.val1)
    print(i.val2)