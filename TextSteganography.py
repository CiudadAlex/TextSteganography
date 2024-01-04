from transformers import pipeline

MASK_WORD = "<mask>"


class TextSteganography:

    def __init__(self):
        self.mask_filler = pipeline("fill-mask", model="distilroberta-base")
        self.text_generator = pipeline("text-generation", model="gpt2", max_new_tokens=200)
        self.final_padding = 30
        self.min_separation = 7

    def hide_message(self, list_word, list_separations, subject):

        if len(list_word) != len(list_separations):
            raise Exception("list_word and list_separations have different sizes: " + str(len(list_word)) + " != " + str(len(list_separations)))

        if min(list_separations) < self.min_separation:
            raise Exception("Min separation is below allowed: " + str(min(list_separations)) + " < " + str(self.min_separation))

        num_words = max(list_separations) + self.final_padding

        text = subject
        words = text.split()

        while len(words) < num_words:
            output_text_generator = self.text_generator(text)

            text = output_text_generator[0]['generated_text']
            words = text.split()

        text = ' '.join(words)

        list_positions = self.get_list_positions(list_separations)
        text = self.change_words_in_positions_and_surroundings(text, list_word, list_positions)

        return text

    def change_words_in_positions_and_surroundings(self, text, list_word, list_positions):

        for index in range(len(list_word)):
            word = list_word[index]
            position = list_positions[index]

            text = self.change_word_in_position(text, word, position)

        # output = self.mask_filler(text)
        # FIXME finish self.min_separation

        return text

    def change_word_in_position(self, text, word, position):

        list_text_words = text.split()

        list_text_words[position] = word

        new_text = ' '.join(list_text_words)

        return new_text


    def get_list_positions(self, list_separations):

        list_positions = []
        index = 0

        for separation in list_separations:
            index = index + separation
            list_positions.append(index)

        return list_positions

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
