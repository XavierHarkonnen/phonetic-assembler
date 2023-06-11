import sys
import os
from background_scripts import language_dictionary, functions

default_phoneme_dictionaries_path = 'phoneme_dictionaries'
phoneme_dictionary_list = []

if os.path.isdir(default_phoneme_dictionaries_path):
    phoneme_dictionaries_path = default_phoneme_dictionaries_path
    for (_, _, filenames) in os.walk(phoneme_dictionaries_path):
        phoneme_dictionary_list = filenames
        break
else:
    print(
        'Phoneme dictionary folder could not be found.  Would you like to specify a location where your phoneme '
        'dictionaries are, or create a folder with the default dictionaries?  Enter \'y\' or \'yes\' to specify a '
        'directory, or enter \'n\', \'no\', or an empty field to create a new folder (input is case insensitive).'
    )
    while True:
        load_folder = input('Load folder? ')
        if load_folder.lower() in ('y', 'yes'):
            load_folder = True
            break
        elif load_folder.lower() in ('', 'n', 'no'):
            load_folder = False
            break
        else:
            print(
                'Not a valid answer.  Enter \'y\' or \'yes\' to specify a directory, or enter \'n\', \'no\', '
                'or an empty field to create a new folder (input is case insensitive).'
            )
    if load_folder:
        while True:
            phoneme_dictionaries_path = input('Path to phoneme dictionary folder: ')
            if os.path.isdir(phoneme_dictionaries_path):
                for (_, _, filenames) in os.walk(phoneme_dictionaries_path):
                    phoneme_dictionary_list = filenames
                break
            else:
                print('Not a valid path')
    else:
        phoneme_dictionaries_path = default_phoneme_dictionaries_path
        os.mkdir(phoneme_dictionaries_path)

        for language in language_dictionary.default_language_dictionary:
            functions.save_language(
                language, phoneme_dictionaries_path, language_dictionary.default_language_dictionary
            )

        for (_, _, filenames) in os.walk(phoneme_dictionaries_path):
            phoneme_dictionary_list = filenames
            break

phoneme_dictionary_list = [file for file in phoneme_dictionary_list if file.split('.')[-1] in ('md', 'json', 'csv')]

if not phoneme_dictionary_list:
    print(
        'No phoneme dictionary files were detected.  Enter \'y\' or \'yes\' to copy the default files into this '
        'directory, or enter \'n\', \'no\', or an empty field to exit (input is case insensitive).')
    while True:
        copy_defaults = input('Copy defaults? ')
        if copy_defaults.lower() in ('y', 'yes'):
            copy_defaults = True
            break
        elif copy_defaults.lower() in ('', 'n', 'no'):
            copy_defaults = False
            break
        else:
            print(
                'Not a valid answer.  Enter \'y\' or \'yes\' to copy the default files into this directory, '
                'or enter \'n\', \'no\', or an empty field to exit (input is case insensitive).'
            )
    if copy_defaults:
        for language in language_dictionary.default_language_dictionary:
            functions.save_language(
                language, phoneme_dictionaries_path, language_dictionary.default_language_dictionary
            )

        for (_, _, filenames) in os.walk(phoneme_dictionaries_path):
            phoneme_dictionary_list = filenames
            break
    else:
        sys.exit()

print('Available Languages:')
for file in phoneme_dictionary_list:
    language = '.'.join(file.split('.')[:-1])
    print(f'\t- {language}')

phoneme_dictionary_list = [os.path.join(phoneme_dictionaries_path, file) for file in phoneme_dictionary_list]

for file in phoneme_dictionary_list:
    dictionary = functions.file_to_phoneme_dictionary(file)
    language_dictionary.language_dictionary[dictionary[0]] = (dictionary[1], dictionary[2], dictionary[3])

while True:
    language_name = input('Language: ').lower().strip()
    if language_name in language_dictionary.language_dictionary:
        language = language_dictionary.language_dictionary[language_name]
        break
    else:
        print('Not a valid language!')

print(f'Note: {language[2]}')

while True:
    syllabic = input('Formatted with syllables? ')
    if syllabic.lower() in ('y', 'yes'):
        syllabic = True
        longest_grapheme_set = max(language[1], 2)
        phoneme_dictionary_path = {**language_dictionary.syllabic_characters, **language[0]}
        break
    elif syllabic.lower() in ('', 'n', 'no'):
        syllabic = False
        longest_grapheme_set = max(language[1], 1)
        phoneme_dictionary_path = {**language_dictionary.default_characters, **language[0]}
        break
    else:
        print(
            'Not a valid answer.  Enter \'y\' or \'yes\' to use syllabic notation, or enter \'n\', \'no\', or an empty '
            'field otherwise (input is case insensitive).'
        )

print(
    'Enter grapheme string below and press ctrl-d (Unix) or ctrl-z (Windows) to enter.  An empty field will print the '
    'language table.'
)

grapheme_string = sys.stdin.read().lower()
# string will not read lines that do not end with a '\n' on some terminals
# or EOF must be pressed twice
# input is fooked

if grapheme_string == '':
    functions.print_language(language_name, language_dictionary.language_dictionary)
else:
    phonetic_string = ''
    removed_characters = []
    i = 0
    while i < len(grapheme_string):
        j = min(len(grapheme_string) - i, longest_grapheme_set)
        while j > 0:
            if grapheme_string[i:i + j] in phoneme_dictionary_path:
                phonetic_string += phoneme_dictionary_path[grapheme_string[i:i + j]]
                i += j
                break
            elif j == 1:
                removed_characters.append(grapheme_string[i])
                i += 1
                break
            j -= 1

    print(f'\nPhonetic string:\n{phonetic_string}')
    if removed_characters:
        print(f'Removed {removed_characters[:-2]}')
