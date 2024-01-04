from transformers import pipeline

MASK_WORD = "<mask>"


class TextSteganography:

    def __init__(self):
        self.mask_filler = pipeline("fill-mask", model="distilroberta-base")
        self.text_generator = pipeline("text-generation", model="gpt2", max_new_tokens=200)
        self.final_padding = 30

    def hide_message(self, list_word, list_position, subject):

        if len(list_word) != len(list_position):
            raise Exception()

        num_words = max(list_position) + self.final_padding

        text = subject
        words = text.split()

        while len(words) < num_words:
            output_text_generator = self.text_generator(text)

            text = output_text_generator[0]['generated_text']
            words = text.split()

        output = self.mask_filler("Paris es la " + MASK_WORD + " de Francia.")
        return text


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
