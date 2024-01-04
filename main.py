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

list_position = [
    4,
    25,
    32,
    55,
    62,
    78,
    92
]
subject = "The number 42"
output = textSteganography.hide_message(list_word, list_position, subject)

print("___________________________________________")
print(output)
print("___________________________________________")

words = output.split()

for index in list_position:
    print(words[index])
