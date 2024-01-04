from TextSteganography import TextSteganography

textSteganography = TextSteganography()

list_word = [
    'Paris',
    'is',
    'in',
    'danger',
    'send',
    'the',
    'planes'
]

list_separations = [
    7,
    8,
    12,
    9,
    14,
    17,
    7
]
subject = "The number 42 "
output = textSteganography.hide_message(list_word, list_separations, subject)

print("___________________________________________")
print(output)
print("___________________________________________")

list_positions = textSteganography.get_list_positions(list_separations)
words = output.split()
index = 0

for index in list_positions:
    print(words[index])
