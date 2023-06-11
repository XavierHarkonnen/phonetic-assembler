def print_language(language, language_dictionary):
    grapheme_dictionary = language_dictionary[language][0]
    note = language_dictionary[language][2]
    print(f'Name: {language}\n')
    print(f'Note: {note}\n')
    print('| Grapheme | Phoneme |')
    print('|:---:|:---:|')
    for grapheme, phoneme in grapheme_dictionary.items():
        print(f'| ⟨{grapheme}⟩ | [{phoneme}] |')


def save_language(language, path, language_dictionary):
    import os
    grapheme_dictionary = language_dictionary[language][0]
    note = language_dictionary[language][2]

    file = open(os.path.join(path, f'{language}.md'), 'w')
    file.write(f'Name: {language}\n\n')
    file.write(f'Note: {note}\n\n')
    file.write('| Grapheme | Phoneme |\n')
    file.write('|:---:|:---:|\n')
    for grapheme, phoneme in grapheme_dictionary.items():
        file.write(f'| ⟨{grapheme}⟩ | [{phoneme}] |\n')
    file.close()


def file_to_phoneme_dictionary(file_path):
    import os
    if not os.path.isfile(file_path):
        print(f'{file_path} is not a file!')
        return -1

    file = open(file_path, 'r')
    table_dict = {}
    extension = file_path.split('.')[-1]

    if extension == 'md':
        first_line = file.readline()
        file.readline()
        second_line = file.readline()
        if first_line[:5].lower() != 'name:' or second_line[:5].lower() != 'note:':
            print('Markdown file is not formatted properly!')
            return -1
        name = first_line[5:].lower().strip()
        note = second_line[5:].strip()

        for row in file:
            if '|' in row:
                row = row.split('|')
                for x in range(len(row) - 1):
                    if row[x] != '' and row[x].strip()[0] == '⟨' and row[x].strip()[-1] == '⟩':
                        if row[x + 1] != '' and row[x + 1].strip()[0] == '[' and row[x + 1].strip()[-1] == ']':
                            table_dict[row[x].strip()[1:-1]] = row[x + 1].strip()[1:-1]

    elif extension == 'json':
        import json

        json_data = json.load(file)
        name = json_data.get('name')
        note = json_data.get('note')
        phonemes = json_data.get('phonemes')

        if name is None or note is None or phonemes is None:
            print('JSON file is not formatted properly!')
            return -1

        table_dict = phonemes

    elif extension == 'csv':
        import csv

        csv_reader = csv.reader(file)
        header = next(csv_reader)

        name = None
        note = None

        if 'grapheme' not in header or 'phoneme' not in header:
            print('CSV file is not formatted properly!')
            return -1

        for row in csv_reader:
            if len(row) == 1:
                if row[0].lower().startswith('name:'):
                    name = row[0][5:].strip()
                elif row[0].lower().startswith('note:'):
                    note = row[0][5:].strip()
            else:
                grapheme = row[header.index('grapheme')]
                phoneme = row[header.index('phoneme')]
                table_dict[grapheme] = phoneme
    else:
        print(f'.{extension} is not a valid file type!')
        return -1

    longest_grapheme_set = 1
    for key in table_dict:
        key_length = len(key)
        if key_length > longest_grapheme_set:
            longest_grapheme_set = key_length

    return name, table_dict, longest_grapheme_set, note
