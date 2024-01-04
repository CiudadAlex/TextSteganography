from transformers import pipeline
from random import randint

MASK_WORD = "<mask>"


class TextSteganography:

    def __init__(self):
        self.mask_filler = pipeline("fill-mask", model="distilroberta-base")
        self.text_generator = pipeline("text-generation", model="gpt2", max_new_tokens=200)
        self.final_padding = 30
        self.min_separation = 7
        self.refinement_iterations = 10

    def hide_message_and_generate_list_positions(self, message_to_hide, subject):

        list_word = message_to_hide.split()
        list_separations = []

        for word in list_word:
            list_separations.append(randint(self.min_separation, 3 * self.min_separation))

        text = self.hide_message(list_word, list_separations, subject)
        list_positions = self.get_list_positions(list_separations)
        return text, list_positions

    def hide_message(self, list_word, list_separations, subject):

        if len(list_word) != len(list_separations):
            raise Exception("list_word and list_separations have different sizes: " + str(len(list_word)) + " != " + str(len(list_separations)))

        if min(list_separations) < self.min_separation:
            raise Exception("Min separation is below allowed: " + str(min(list_separations)) + " < " + str(self.min_separation))

        min_num_words = sum(list_separations) + self.final_padding
        text_initial = self.generate_initial_text(subject, min_num_words)

        print("___________________________________________")
        print(text_initial)
        print("___________________________________________")

        list_positions = self.get_list_positions(list_separations)
        text = text_initial

        for i in range(self.refinement_iterations):
            text = self.change_list_of_words_in_positions_and_surroundings(text, list_word, list_positions)
            print("Iter " + str(i))

        return text

    def generate_initial_text(self, subject, min_num_words):

        text = subject
        words = text.split()

        while len(words) < min_num_words:
            output_text_generator = self.text_generator(text)

            text = output_text_generator[0]['generated_text']
            words = text.split()

        text = ' '.join(words)

        return text

    def change_list_of_words_in_positions_and_surroundings(self, text, list_word, list_positions):

        text_mod = text

        for index in range(len(list_word)):
            word = list_word[index]
            position = list_positions[index]

            text_mod = self.change_word_in_position_and_surroundings(text_mod, word, position)

        return text_mod

    def change_word_in_position_and_surroundings(self, text, word, position):

        text_mod = self.change_word_in_position(text, word, position)

        for index in range(1, self.min_separation - 1):
            text_mod = self.generate_word_in_position(text_mod, position - index)
            text_mod = self.generate_word_in_position(text_mod, position + index)

        return text_mod

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
    def generate_word_in_position(self, text, position):

        text_mod = self.change_word_in_position(text, MASK_WORD, position)
        output = self.mask_filler(text_mod)
        generated_token = output[0]['token_str'].strip().split()[0]
        return text_mod.replace(MASK_WORD, generated_token)

    def change_word_in_position(self, text, word, position):

        list_text_words = text.split()

        list_text_words[position] = word

        text_mod = ' '.join(list_text_words)

        return text_mod


    def get_list_positions(self, list_separations):

        list_positions = []
        index = 0

        for separation in list_separations:
            index = index + separation
            list_positions.append(index)

        return list_positions


