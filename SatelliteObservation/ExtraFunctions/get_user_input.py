# ==========================================================================================
# Auteurs: Groupe 5
# Date : 02/07/24
# Fonction: Ce script contient plusieurs fonctions permettant de s'assurer
# # que le format de donnée que l'utilisateur rentre est le bon.
# ==========================================================================================

import SatelliteObservation

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


'''Booleen'''

def get_boolean_input(prompt):

    while True:
        user_input = SatelliteObservation.get_str_input(prompt).strip().lower()
        if user_input == 'true':
            return True
        elif user_input == 'false':
            return False
        else:
            print("Entrée invalide. Réessayez en répondant par 'True' ou 'False'")

