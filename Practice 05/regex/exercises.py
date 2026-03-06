"""
Python RegEx Exercises Solutions
"""

import re


# 1. Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
def exercise_1(text):
    """
    Match a string that has an 'a' followed by zero or more 'b''s.
    Pattern: ab*
    """
    pattern = r'ab*'
    matches = re.findall(pattern, text)
    return matches


# 2. Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
def exercise_2(text):
    """
    Match a string that has an 'a' followed by two to three 'b'.
    Pattern: ab{2,3}
    """
    pattern = r'ab{2,3}'
    matches = re.findall(pattern, text)
    return matches


# 3. Write a Python program to find sequences of lowercase letters joined with a underscore.
def exercise_3(text):
    """
    Find sequences of lowercase letters joined with a underscore.
    Pattern: lowercase letters, underscore, lowercase letters (can repeat)
    """
    pattern = r'[a-z]+_[a-z_]*'
    matches = re.findall(pattern, text)
    return matches


# 4. Write a Python program to find the sequences of one upper case letter followed by lower case letters.
def exercise_4(text):
    """
    Find sequences of one upper case letter followed by lower case letters.
    Pattern: [A-Z][a-z]+
    """
    pattern = r'[A-Z][a-z]+'
    matches = re.findall(pattern, text)
    return matches


# 5. Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
def exercise_5(text):
    """
    Match a string that has an 'a' followed by anything, ending in 'b'.
    Pattern: a.*b
    """
    pattern = r'a.*b'
    matches = re.findall(pattern, text)
    return matches


# 6. Write a Python program to replace all occurrences of space, comma, or dot with a colon.
def exercise_6(text):
    """
    Replace all occurrences of space, comma, or dot with a colon.
    Pattern: [ ,.]
    """
    pattern = r'[ ,.]'
    result = re.sub(pattern, ':', text)
    return result


# 7. Write a python program to convert snake case string to camel case string.
def exercise_7(text):
    """
    Convert snake case string to camel case string.
    Example: snake_case_string -> snakeCaseString
    """
    components = text.split('_')
    # Keep the first component lowercase, capitalize the rest
    camel_case = components[0] + ''.join(x.title() for x in components[1:])
    return camel_case


# 8. Write a Python program to split a string at uppercase letters.
def exercise_8(text):
    """
    Split a string at uppercase letters.
    Pattern: (?=[A-Z]) - positive lookahead for uppercase letters
    """
    pattern = r'(?=[A-Z])'
    result = re.split(pattern, text)
    # Remove empty strings
    result = [x for x in result if x]
    return result


# 9. Write a Python program to insert spaces between words starting with capital letters.
def exercise_9(text):
    """
    Insert spaces between words starting with capital letters.
    Pattern: Add space before uppercase letters
    """
    pattern = r'([A-Z])'
    result = re.sub(pattern, r' \1', text)
    return result.strip()


# 10. Write a Python program to convert a given camel case string to snake case.
def exercise_10(text):
    """
    Convert camel case string to snake case.
    Example: camelCaseString -> camel_case_string
    """
    # Insert underscore before uppercase letters and convert to lowercase
    pattern = r'(?<!^)(?=[A-Z])'
    result = re.sub(pattern, '_', text).lower()
    return result


# Test all exercises
if __name__ == "__main__":
    print("Exercise 1: Match 'a' followed by zero or more 'b''s")
    print(exercise_1("ab abbb ab aabbbbbb a"))
    print()

    print("Exercise 2: Match 'a' followed by two to three 'b's")
    print(exercise_2("ab abb abbb abbbb aabb"))
    print()

    print("Exercise 3: Find lowercase sequences joined with underscore")
    print(exercise_3("hello_world this_is_a_test test"))
    print()

    print("Exercise 4: Find uppercase letter followed by lowercase letters")
    print(exercise_4("Hello World Python Example"))
    print()

    print("Exercise 5: Match 'a' followed by anything, ending in 'b'")
    print(exercise_5("aaaaab aaab acdb a1b"))
    print()

    print("Exercise 6: Replace space, comma, or dot with colon")
    print(exercise_6("Hello, world. This is a test."))
    print()

    print("Exercise 7: Convert snake_case to camelCase")
    print(exercise_7("hello_world_this_is_python"))
    print()

    print("Exercise 8: Split at uppercase letters")
    print(exercise_8("HelloWorldPythonExample"))
    print()

    print("Exercise 9: Insert spaces between capital letters")
    print(exercise_9("HelloWorldPythonExample"))
    print()

    print("Exercise 10: Convert camelCase to snake_case")
    print(exercise_10("helloWorldThisIsPython"))
    print()
