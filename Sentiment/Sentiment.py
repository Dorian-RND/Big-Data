import numpy as np
from textblob import TextBlob

fichier = open("Elastic/send.txt", 'a')

tab_polarity = []
tab_subjectivity = []


def ecriture(polarity, subjectivity):
    for polarite in (polarity):
        polarite=float(polarite)
        if polarite < -0.5:
            polarite = "tres negatif"
        elif -0.5 <= polarite < 0.0:
            polarite = "negatif"
        elif polarite==0.0:
            polarite="neutre"
        elif 0.0 < polarite < 0.5:
            polarite = "positif"
        else:
            polarite = "tres positif"

        for j in subjectivity:
            subjectivite=j


        temp = str("RedBull") + '; ' + polarite + '; ' + str(subjectivite) + "\n"
        print("ecriture dans le fichier send")
        fichier.write(temp)
    fichier.close()


def sentiment(donnee):
    for i in donnee:
        test = TextBlob(i)
        polarity, subjectivity = test.sentiment
        tab_polarity.append(polarity)
        tab_subjectivity.append(subjectivity)
    ecriture(tab_polarity, tab_subjectivity)
