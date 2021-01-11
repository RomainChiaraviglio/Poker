from random import sample
from collections import Counter
import csv

deck = [(2, "coeur"), (2, "pique"), (2, "trefle"), (2, "carreau"),
		(3, "coeur"), (3, "pique"), (3, "trefle"), (3, "carreau"),
		(4, "coeur"), (4, "pique"), (4, "trefle"), (4, "carreau"),
		(5, "coeur"), (5, "pique"), (5, "trefle"), (5, "carreau"),
		(6, "coeur"), (6, "pique"), (6, "trefle"), (6, "carreau"),
		(7, "coeur"), (7, "pique"), (7, "trefle"), (7, "carreau"),
		(8, "coeur"), (8, "pique"), (8, "trefle"), (8, "carreau"),
		(9, "coeur"), (9, "pique"), (9, "trefle"), (9, "carreau"),
		(10, "coeur"), (10, "pique"), (10, "trefle"), (10, "carreau"),
		(11, "coeur"), (11, "pique"), (11, "trefle"), (11, "carreau"),
		(12, "coeur"), (12, "pique"), (12, "trefle"), (12, "carreau"),
		(13, "coeur"), (13, "pique"), (13, "trefle"), (13, "carreau"),
		(14, "coeur"), (14, "pique"), (14, "trefle"), (14, "carreau")]


def flush(couleur):
	return max(couleur.count("coeur"), couleur.count("pique"), couleur.count("trefle"), couleur.count("carreau"))>=5

def quinte(cartes):
	cartes = sorted(cartes, key=lambda x:x[0])
	dict_cartes = {}

	for i, c in enumerate(cartes):
		if c[0]-i not in dict_cartes:
			dict_cartes[c[0]-i] = [c]
		else:
			dict_cartes[c[0]-i].append(c)

	suite = dict_cartes[max(dict_cartes, key= lambda x: len(dict_cartes[x]))]
	if len(suite) >= 5:
		coul = [x[1] for x in suite]
		num = [x[0] for x in suite]
		if flush(coul) and 10 in num and 11 in num and 12 in num and 13 in num and 14 in num:
			return 200
		if flush(coul):
			return 180 + max(num)
		return 90 + max(num)
	return None


def carre(num):
	for n in set(num):
		if num.count(n) == 4:
			return n
	return None

def brelan(num):
	list_brelan = []
	for n in set(num):
		if num.count(n) == 3:
			list_brelan.append(n)
	if len(list_brelan) == 2:
		return [max(list_brelan), min(list_brelan)]
	elif len(list_brelan) == 1:
		return list_brelan
	return None

def paire(num):
	list_paire = []
	for n in set(num):
		if num.count(n) == 2:
			list_paire.append(n)
	if len(list_paire) > 1:
		return [sorted(list_paire)[-1], sorted(list_paire)[-2]]
	elif len(list_paire) == 1:
		return list_paire
	return None

def score(cartes, j):
	num = [x[0] for x in cartes]
	couleur = [x[1] for x in cartes]

	# Si quinte, quinte flush ou quinte flush royale
	resultat = quinte(cartes)
	if resultat:
		return resultat

	# Si couleur
	if flush(couleur):
		return 110 + max([i[0] for i in cartes if i[1]==max(Counter(couleur))])

	# Si carré
	if carre(num):
		return 160 + carre(num)

	# Si full ou brelan
	brelan_temp = brelan(num)
	paire_temp = paire(num)
	if brelan_temp:
		if len(brelan_temp)==2:
			return 130 + sum(brelan_temp)
		if paire_temp:
			return 130 + brelan_temp[0] + paire_temp[0]
		return 70 + brelan_temp[0] + max([x[0] for x in j])

	# Si deux ou une paire
	if paire_temp:
		if len(paire_temp)>1:
			return 40 + sum(paire_temp) + max([x[0] for x in j])
		return 20 + paire_temp[0] + max([x[0] for x in j])

	# Figure haute
	return max(num) + max([x[0] for x in j])


with open('poker_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Joueur1", "Joueur2", "Commun", "Score1", "Score2", "J1 win ?"])
    for i in range(50000):
    	jeu = sample(deck, 9)
    	joueur1 = jeu[:2]+jeu[-5:]
    	joueur2 = jeu[2:]

    	s1 = score(joueur1, jeu[:2])
    	s2 = score(joueur2, jeu[2:4])

    	writer.writerow([joueur1[:2], joueur2[:2], joueur1[-5:], s1, s2, s1>s2])