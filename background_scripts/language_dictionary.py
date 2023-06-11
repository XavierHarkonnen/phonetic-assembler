from background_scripts.default_phoneme_dictionaries import *

# format: '<language identifier>': (<phoneme dictionary>, <longest grapheme> , '<note>'),

default_language_dictionary = {
    'german': (
        german_phonemes, 3, 'No notes'
    ),
    'latin': (
        latin_phonemes, 3, 'Consonant \'i\' must be represented as \'j\' and vowel \'v\' must be represented as \'u\''
    ),
    'osserian': (
        osserian_phonemes, 1, 'Not fully implemented'
    ),
    # 'high tairen': (high_tairen_phonemes, 1, 'Not implemented'),
    # 'low tairen': (low_tairen_phonemes, 1, 'Not implemented'),
    # 'antenorian': (antenorian_phonemes, 1, 'Not implemented'),
    # 'nemelian': (nemelian_phonemes, 1, 'Not implemented'),
    # 'hyrkothalian': (hyrkothalian_phonemes, 1, 'Not implemented'),
}

language_dictionary = {}

default_characters = {
    ' ': ' ',
    '. ': '\n',
    '\'': '',
    '\n': '\n\n'
}

syllabic_characters = {
    ' ': ' ',
    'ˈ': 'ˈ',  # Primary stress (appears before stressed syllable)
    '\'': 'ˈ',  # Primary stress (ASCII)
    'ˌ': 'ˌ',  # Secondary stress (appears before stressed syllable)
    ',': 'ˌ',  # Secondary stress (ASCII)
    '.': '.',  # Syllable break (internal boundary)
    '‿': '‿',  # Linking (lack of a boundary; a phonological word)
    '_': '‿',  # Linking (ASCII)
    '|': '|',  # Minor or foot break
    '‖': '‖',  # Major or intonation break
    '||': '‖',  # Major or intonation break (ASCII)
    '↗': '↗',  # Global rise
    '/': '↗',  # Global rise (ASCII)
    '↘': '↘',  # Global fall
    '\\': '↘',  # Global fall (ASCII)
    'ꜛ': 'ꜛ',  # Upstep
    '^': 'ꜛ',  # Upstep (ASCII)
    'ꜜ': 'ꜜ',  # Downstep
    '~': 'ꜜ',  # Downstep (ASCII)
    '\n': '\n'
}
