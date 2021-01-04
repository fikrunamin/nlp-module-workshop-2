import json

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
    ['1', '2', '3'],
    ['7', '1', '4', '8', '5', '6'],
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

# JSON Pattern
# "intents":
# [
#     {
#         "tag": "greeting",
#         "patterns": [
#             "Hi there",
#             "Hello",
#             "What's up",
#             "Good day",
#             "Yo"
#         ],
#         "responses": [
#             "Hi",
#             "Hello",
#             "Hi there, can I help you?"
#         ],
#         "context": [
#             ""
#         ]
#     },
#     {
#         "tag": "Swelling or inflammation of the gums",
#         "patterns": [
#             "Swelling or inflammation of the gums",
#             "gums are swelling",
#             "swelling of gums",
#             "gum is getting big"
#         ],
#         "responses": [
#             "Can you please tell us more about your symptoms? If there is no other symptoms, kindly type 'NO'."
#         ],
#         "context": [
#             ""
#         ]
#     },
#     {
#         "tag": "Peripical Abscess",
#         "patterns": [
#             ""
#         ],
#         "responses": [
#             "You MAY suffer from Peripical Abscess, A collection of pus at the root of a tooth, usually caused by an infection that has spread from a tooth to the surrounding tissues."
#         ],
#         "context": [
#             ""
#         ]
#     },
# ]

intents = []

for index, rule in enumerate(rules, start=0):
    x = {
        "tag": diseases[index],
        "patterns": rule,
        "responses": "You may suffer " + diseases[index]
    }
    intents.append(x)

print(intents)
