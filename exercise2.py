#IMPORTING PACKAGES
import spacy
import es_core_news_sm
from collections import Counter 

#LOADING AND PROCESSING THE DATA
#We define the file path of the dataset
corpus_path = './es_corpus.txt'

#We open the dataset file and assign it to a new variable
with open(corpus_path, 'r') as file:
   #We use the .replace() method to replace the line break symbol (\n) with spaces
  corpus = file.read().replace('\n', ' ')

#We apply the SpaCy model to our dataset
nlp = spacy.load('es_core_news_sm')
doc=nlp(corpus)

#CAPTURING NOUNS THAT CAN DENOTE INFORMATIONAL CONTENT
#We first create a handmade list of adjectives denoting informational content
propositional_predicates = ['verdadero', 'falso', 'plausible', 'implausible', 'cierto',
                            'verídico', 'veraz', 'sincero', 'fáctico', 'infinito',
                            'interminable', 'perpetuo', 'imperecedero']
#We create an empty list that will be filled with the nouns that fulfill the conditions
nouns_info_cont = []
#We specify our conditions in the following loop
for token in doc:
  if token.head.dep_ == "acl" and token.tag_ == "NOUN" and token.dep_ == "nsubj" and token.head.head.pos_ == "NOUN":
    nouns_info_cont.append(token.head.head.lemma_)
  if token.dep_ == "amod" and token.tag_=="ADJ" and token.lemma_ in propositional_predicates and token.head.pos_ == "NOUN" or token.dep_ == "ROOT" and token.tag_ == "ADJ" and token.lemma_ in propositional_predicates and token.head.pos_ == "NOUN":
    nouns_info_cont.append(token.head.lemma_)

#Then we use the set() function to remove duplicates and we print our results
print('Nouns that can denote informational content:', set(nouns_info_cont))
print('\n')

#CAPTURING NOUNS THAT CAN DENOTE EVENTUALITY
#We first create a handmade list of adjectives denoting eventuality
eventive_pred = ["duradero", "perdurable", "eterno", "inacabable", "indefinido",
                 "inextinguible", "inmemorial", "inmortal", "perenne", "persistente",
                 "prolongado", "sempiterno"]
#We create another handmade list of nouns that usually modify a noun alongside with a numeral and denote eventuality
eventive_pp = ["hora", "minuto", "año", "mes", "segundo", "semana"]

#We create another handmade list of verbs that denote eventuality
eventive_verbs = ["durar", "comenzar", "empezar", "terminar", "iniciar", "continuar",
                  "finalizar", "acabar", "inaugurar", "prolongarse", "demorar",
                  "prolongar", "transcurrir", "abarcar", "culminar", "mantener", "permanecer"]

#We create an empty list that will be filled with the nouns that fulfill the conditions
nouns_ev = []
#We specify our conditions in the following loop
for token in doc:
  if token.dep_ == "amod" and token.tag_=="ADJ" and token.lemma_ in eventive_pred and token.head.pos_ == "NOUN":
    nouns_ev.append(token.head.lemma_)
  if token.tag_ == "NUM" and token.head.dep_ == "nmod" and token.head.lemma_ in eventive_pp and token.head.head.tag_ == "NOUN" and token.head.head.pos_ == "NOUN":
    nouns_ev.append(token.head.head.text)
  if token.lemma_ in eventive_verbs and token.head.dep_ == "nsubj" and token.head.pos_ == "NOUN":
    nouns_ev.append(token.head.lemma_)

#Then we use the set() function to remove duplicates and we print our results
print('Nouns that can denote eventuality:', set(nouns_ev))
print('\n')

#CAPTURING COINCIDENCES BETWEEN THE TWO CLASSES
#We create an empty list and fill it only with the coincidences of the two lists
coincidences = []
for token in nouns_info_cont:
  if token in nouns_ev:
    coincidences.append(token)

#Then we use the set() function to remove duplicates and we print our results
print('Intersections between these classes:', set(coincidences))
print('\n')

#MEASURING THE FREQUENCY OF THE COINCIDENCES IN EACH LIST
#We use the Counter function to measure the list of each element in each list
freq_info_cont = Counter(nouns_info_cont)
freq_ev = Counter(nouns_ev)

#Then we define a function to filter each frequency list by the coincidences of both lists
def my_filtering_function(pair):
    #We define the words that we want to maintain in each frequency list
    wanted_keys = ['vida', 'guerra', 'libro']
    key, value = pair
    if key in wanted_keys:
        #Keep the pair in the list
        return True
    else:
        #Deletes the pair out of the list
        return False

#We apply the defined function to each list
coincidences_info_cont = dict(filter(my_filtering_function, freq_info_cont.items()))
coincidences_ev = dict(filter(my_filtering_function, freq_ev.items()))

#We print our results
print('Frequency of intersections with informational content:', coincidences_info_cont)
print('Frequency of intersections with eventual content:', coincidences_ev)
