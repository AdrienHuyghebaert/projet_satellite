#Ce script contient plusieurs fonctions permettant de s'assurer
# que le format de donnée que l'utilisateur rentre est le bon.

'''Flottant'''

def get_float_input(prompt):
    while True:
        # Constantly check if a value was entered followed by Enter
        try:
            # Put the value entered by user in "entree"
            entree = input(prompt)
            # Try to transform it into a float, if it cannot, we go to "except"
            value = float(entree)
            break
        except ValueError:
            # If input is not a float we get a ValueError
            print("Invalid input, please try again.")
    return value



'''Entier'''

def get_int_input(prompt):
    while True:
        # Constantly check if a value was entered followed by Enter
        try:
            # Put the value entered by user in "entree"
            entree = input(prompt)
            # Try to transform it into an int, if it cannot, we go to "except"
            value = int(entree)
            break
        except ValueError:
            # If input is not a float we get a ValueError
            print("Invalid input, please try again.")
    return value


'''Chaine de caractère'''

def get_str_input(prompt):
    while True:
        # Constantly check if a value was entered followed by Enter
        try:
            # Put the value entered by user in "entree"
            entree = input(prompt)
            # Try to transform it into a str, if it cannot, we go to "except"
            value = str(entree)
            break
        except ValueError:
            # If input is not a float we get a ValueError
            print("Invalid input, please try again.")
    return value
