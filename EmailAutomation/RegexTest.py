import re

text_to_search = '''
abcdefghijklmnopqrstuvxz
ABCDEFGHIJKLMNOPQRSTUVXZ
1234567890

Ha HaHa

389.987.678-32

Mr. Gama
Mr Smith
Ms Davis
Mrs. Robson
Mr. T

'''
sentence = 'Start a sequence and then bring it to an end'

#pattern = re.compile(r'.')
#pattern = re.compile(r'\d')
'''
. - Any character except New Line
\d - Digit (0-9)
\D - Not a Digit (0-9)
\w - Word character (a-z, A-Z, 0-9, _)
\W - Not a world Character
\s - Whitespace (space, tab, newline)
\S - Not a whitespace (space, tab, newline)
\b - word Boundary
\B - Not a word Boundary
^ - Beginning of a String
$ - End of a String
[] - Matches Characters in brackets
[^ ] - Matches Characters Not in

| - Either or
() - Group

QUANTIFIERS

* - 0 or More
+ - 1 or More
? - 0 or One
{3} - Exact Number
{3,4} - Range of Numbers (Minimum, Maximum)

'''

#pattern = re.compile(r'\d\d\d.\d\d\d.\d\d\d.\d\d')
#pattern = re.compile(r'\d{3}.\d{3}.\d{3}.\d{2}')
#pattern = re.compile(r'Mr\.?\s[A-Z]\w*')
#pattern = re.compile(r'M(r|s|rs)\.?\s[A-Z]\w*')
#pattern = re.compile(r'start', re.IGNORECASE) Ignorar case sensitive

pattern = re.compile(r'M(r|s|rs)\.?\s[A-Z]\w*')
matches = pattern.finditer(text_to_search)

for match in matches:
    print(match.group(0))