import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pickle
from keras.models import load_model
import json
import random
import numpy as np

lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

detected_tags = []
symptoms_list = []
detected_rules = []


symptoms = [
    'Hard to chew',  # 1
    'Swelling  or inflammation  of the gums',  # 2
    'Shaky Teeth',  # 3
    'Swelling of the jaw',  # 4
    'Fever',  # 5
    'Swollen lymph nodes around jaw or neck',  # 6
    'Bad Breath',  # 7
    'Pain or tenderness around the gums',  # 8
    'Severe pain for several days after tooth extraction',  # 9
    'Bones seen in socket',  # 10
    'Teeth feel painful and sensitive',  # 11
    'Eroded tooth',  # 12
    'Headache',  # 13
    'Insomnia or feeling restless',  # 14
    'The sound of teeth crunching during sleep',  # 15
    'Gums bleed easily',  # 16
    'The shape of the gum is round',  # 17
    'The consistency of the gums becomes soft',  # 18
    'Gum or suppurating teeth',  # 19
    'Tooth aches or throbbing',  # 20
    'Redness on the corners of the mouth',  # 21
    'The corner of the mouth feel painful',  # 22
    'Scaly mouth corners',  # 23
    'Ulcer (wound in the corner of the mouth)',  # 24
    'Dentin Seen',  # 25
    'Cavity',  # 26
    'Infected pulp/inflammation of the pulp',  # 27
    'Throbbing pain without stimulation',  # 28
    'White spots on teeth',  # 29
    'White patches on tongue',  # 30
    'White patches on the oral cavity',  # 31
    'Plaque deposits',  # 32
    'There is Tartar',  # 33
    'Tooth decay',  # 34
    'Pulp is numb',  # 35
    'The pulp chamber is open',  # 36
    'Red gum'  # 37
]

rules = [
    ['1', '2', '3'],  # Disease 1
    ['7', '1', '4', '8', '5', '6'],  # disease 2
    ['7', '9', '10'],
    ['11', '12'],
    ['11', '13', '14', '15'],
    ['2', '16', '17', '18'],
    ['2', '5', '6', '19', '20'],
    ['7', '1', '4', '8', '2'],
    ['21', '22', '23', '24'],
    ['26', '25', '11'],
    ['25', '26', '27', '28'],
    ['26', '29'],
    ['7', '30', '31'],
    ['7', '16', '32', '33'],
    ['26', '34', '35', '36'],
    ['7', '16', '2', '19', '37']
]

diseases = [
    'Periodontal Abscess',
    'Peripical Abscess',
    'Alveolar Osteitis',
    'Dental Abrasion',
    'Bruxism',
    'Gingivitis',
    'Infected Teeth',
    'Pain at the rear teeth',
    'Angular Ceilitis',
    'Caries Media',
    'Caries Profunda',
    'Caries Superficial',
    'Candidiasis',
    'Calculus (dental)',
    'Pulp Necrosis',
    'Periodontitis',
]

symptoms = [" ".join(x.lower().split()) for x in symptoms]
diseases = [" ".join(x.lower().split()) for x in diseases]


def clean_up_sentence(sentence):
    stopWords = set(stopwords.words('english'))
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [word for word in sentence_words if word.isalnum()]
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in sentence_words]

    filtered_words = []
    for w in sentence_words:
        if w not in stopWords:
            filtered_words.append(w)

    bigrm = nltk.bigrams(filtered_words)

    result = map(lambda x: ' '.join(x), list(bigrm))

    filtered_words.extend(list(result))
    print(filtered_words)
    return filtered_words


def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bags = []
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag = [0]*len(words)
                bag[i] = 1
                bags.append(bag)
                if show_details:
                    print('found in bag: %s' % w)
    return(np.array(bags))


def predict_class(sentence, model):
    bags = bow(sentence, words)
    results = []
    for bag in bags:
        res = model.predict(np.array([bag]))[0]
        ERROR_THRESHOLD = 0.25
        PROBABILITY_THRESHOLD = 0.8
        result = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        result.sort(key=lambda x: x[1], reverse=True)
        results.append(result)

    print("results", results)
    return_list = []
    for result in results:
        for r in result:
            if (r[1] > PROBABILITY_THRESHOLD):
                return_list.append(
                    {"intent": classes[r[0]], "probability": str(r[1])})
    # print("r", r)
    # print("results", results)
    # print("res", res)
    # print("symptoms", symptoms)
    print("return list", return_list)
    return return_list


def getPrediction(ints):
    print('ints', ints)
    data_intents = {}
    for intent in ints:
        tag = intent['intent'].lower()
        if(tag != ''):  # dump every 'tag' which determines which intents the user's input match into the list symptoms_list
            detected_tags.append(tag)
            if any(tag in symptom for symptom in symptoms):
                if(tag not in symptoms_list):
                    symptoms_list.append(tag)
                    detected_rules.append(symptoms.index(tag) + 1)

            detected_diseases = []
            for detected_rule in detected_rules:
                for rule in rules:
                    if str(detected_rule) in rule:
                        detected_diseases.append(
                            diseases[rules.index(rule)])
                        temp = list(set(detected_diseases))

            if 'temp' in locals():
                detected_disease_probabilities = []
                for index, disease in enumerate(temp, start=1):
                    disease_index = diseases.index(disease)
                    rules_list = rules[disease_index]
                    total_rules = len(rules_list)
                    matched_rules = 0
                    for rule in rules_list:
                        for detected_rule in detected_rules:
                            if str(detected_rule) in rule:
                                matched_rules += 1
                    rule_probability = matched_rules / total_rules
                    # detected_disease_probabilities.append(
                    #     {'disease': disease, 'probability': rule_probability * detected_diseases.count(disease)/len(detected_diseases), 'index': index})  # Algorithm for Probability goes here
                    detected_disease_probabilities.append(
                        {'disease': disease, 'probability': rule_probability, 'index': diseases.index(disease)})  # Algorithm for Probability goes here
                detected_disease_probabilities = sorted(
                    detected_disease_probabilities, key=lambda x: x['probability'], reverse=True)

        data_intents['detected_tags'] = detected_tags
        data_intents['symptoms_list'] = symptoms_list
        data_intents['detected_rules'] = detected_rules
        data_intents['detected_diseases'] = detected_diseases

    print("Tags: ", detected_tags)
    print("Symptoms: ", symptoms_list)
    print("Rules: ", detected_rules)
    print("Detected Disease: ", detected_diseases)

    if 'detected_disease_probabilities' in locals():
        data_intents['temp'] = temp
        data_intents['detected_disease_probabilities'] = detected_disease_probabilities
        print("Diseases: ", temp)
        print("Probabilities: ", detected_disease_probabilities)

    return data_intents


def getResponse(ints):
    prediction = getPrediction(ints)
    list_of_intents = intents['intents']
    result = ints[-1]['intent']
    for i in list_of_intents:
        if(i['tag'] == result):
            if(len(symptoms_list) < 3):
                result = random.choice(i['responses'])
            elif(result == "no_other_symptoms" or len(symptoms_list) >= 3):
                index_highest_disease_probability = prediction[
                    'detected_disease_probabilities'][0]['index']
                for rule in rules[index_highest_disease_probability]:
                    if(int(rule) not in detected_rules):
                        result = "Mmm, based on my data, people that have your symptoms are also have " + symptoms[int(
                            rule) - 1] + ", do you also feel it? symptoms no: " + rule
                        print(result)
                        user_input = input().lower().strip()
                        if 'yes' in user_input:
                            ints.append(predict_class(symptoms[int(
                                rule) - 1], model))
                        # print("Based on my data, people that have your symptoms are also have ", symptoms[int(
                        #     rule) - 1], ", do you also feel it? symptoms no:", rule)  # Bot will ask questions related to the symptoms
                        # user_input = input("yes or no?")
                        # if (user_input == "yes"):

                # result = "I have diagnosed your symptoms and I guess you are having "
                # result += prediction[
                #     'detected_disease_probabilities'][0]['disease'] + "."
                # for ds in detected_disease_probabilities:
                #     if ds['probability'] >= 0.3:
                #         result += ds['disease'] + ", "

            # for key, value in i.items():
            #     if(key == "tag" and value == result):
            #         print()
            #     i['tag'].index(result)
            # for t in i['tag']:
            #     if(t == detected_tags[-1]):
            #         result = random.choice(i['responses'])
            #         print(result)

            # for i in list_of_intents:
            #     # when user input 'no' wll trigger this if section, which detect all rules that matches and detect if any disease matched
            #     if(i['tag'] == 'no_other_symptoms'):
            #         temp_rule = []
            #         s = 0
            #         result = random.choice(i['responses'])
            #         # print("No hahahahhaha")
            #         for s_list in symptoms_list:
            #             temp = 0
            #             for symptom in symptoms:
            #                 temp += 1
            #                 if all(item in s_list for item in symptom):
            #                     temp_rule.append(temp)
            #                 else:
            #                     continue
            #         print("temp rule: ", temp_rule)
            #         for rule in rules:
            #             s += 1
            #             if all(item in str(temp_rule) for item in rule):
            #                 detected_disease = diseases[s]
            #                 tag = detected_disease
            #                 if(detected_disease == ''):
            #                     tag = 'cant_find_disease'
            #             else:
            #                 continue
            #         # print(detected_disease)
            #     elif(i['tag'] == tag):  # if user keeps input any thing other than 'no'
            #         break
            # # print(tag)
            # result = random.choice(i['responses'])
            # # print(symptoms_list)
    return result


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints)
    return(res)


print("You can start interact with the chatbot now.")
while True:
    user_input = input().lower().strip()
    # user_input = "i have bad breathe, fever, cannot sleep, headache"
    if(user_input != ""):
        print("You: ============================================================================>>>", user_input)
        print("Bot: ============================================================================>>>",
              chatbot_response(user_input))
