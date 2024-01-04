from TextSteganography import TextSteganography

textSteganography = TextSteganography()

message_to_hide = "Paris is in danger send the planes"
subject = "In France the "
text, list_positions = textSteganography.hide_message_and_generate_list_positions(message_to_hide, subject)

print("___________________________________________")
print(text)
print("___________________________________________")

words = text.split()

for index in list_positions:
    print(words[index])
