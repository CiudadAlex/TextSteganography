from transformers import pipeline

MASK_WORD = "<mask>"


class TextSteganography:

    def __init__(self):
        self.maskFiller = pipeline("fill-mask", model="distilroberta-base")

    def hide_message(self, list_tuples_word_position):
        output = self.maskFiller("Paris is the " + MASK_WORD + " of France.")
        return output[0]


'''

output of the maskFiller:

[
    {'score': 0.6790179014205933, 'token':   812, 'token_str':    ' capital', 'sequence':    'Paris is the capital of France.'},
    {'score': 0.0517798401415348, 'token': 32357, 'token_str': ' birthplace', 'sequence': 'Paris is the birthplace of France.'},
    {'score': 0.0382528081536293, 'token':  1144, 'token_str':      ' heart', 'sequence':      'Paris is the heart of France.'}, 
    {'score': 0.0243489351123571, 'token': 29778, 'token_str':       ' envy', 'sequence':       'Paris is the envy of France.'}, 
    {'score': 0.0228512510657310, 'token':  1867, 'token_str':    ' Capital', 'sequence':    'Paris is the Capital of France.'}
]
'''
