import numpy as np
from textblob import TextBlob

fichier = open("Elastic/send.txt", 'a')

tab_polarity = []
tab_subjectivity = []


def ecriture():
    temp = str("RedBull") + '; ' + str(np.absolute(np.mean(tab_polarity))) + '; '+str(1-np.absolute(np.mean(tab_polarity))) + '; '+ str(np.mean(tab_subjectivity))+ '; '+ str(1-np.mean(tab_subjectivity)) + "\n"
    print(temp)
    fichier.write(temp)
    fichier.close()




def sentiment(donnee):
    for i in donnee:
        test = TextBlob(i)
        polarity, subjectivity = test.sentiment
        tab_polarity.append(polarity)
        tab_subjectivity.append(subjectivity)
    ecriture()
