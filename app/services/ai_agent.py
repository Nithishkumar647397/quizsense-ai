"""
QuizSense AI - Intelligent Quiz Agent
Works with Learning Agent for personalized experience!
"""

import random
from typing import List, Dict
from datetime import datetime


class QuizAgent:
    def __init__(self):
        print("🤖 Quiz Agent Ready!")
        self.question_bank = self._load_questions()
    
    def _load_questions(self) -> Dict:
        """Load comprehensive question bank"""
        
        return {
            "Variables and Data Types": {
                "easy": [
                    {"question": "Which is a valid Python variable name?", "options": {"A": "2name", "B": "my_var", "C": "my-var", "D": "class"}, "correct_answer": "B", "explanation": "Variable names can have letters, numbers, underscores but can't start with number or be reserved words."},
                    {"question": "What type is x = 5.5?", "options": {"A": "int", "B": "float", "C": "str", "D": "double"}, "correct_answer": "B", "explanation": "Decimal numbers are float type in Python."},
                    {"question": "What is type(True)?", "options": {"A": "int", "B": "str", "C": "bool", "D": "bit"}, "correct_answer": "C", "explanation": "True and False are boolean (bool) type."},
                    {"question": "How to create a string?", "options": {"A": "x = Hello", "B": "x = 'Hello'", "C": "x = (Hello)", "D": "string Hello"}, "correct_answer": "B", "explanation": "Strings need quotes - single or double."},
                    {"question": "What does None mean?", "options": {"A": "Zero", "B": "Empty", "C": "No value", "D": "Error"}, "correct_answer": "C", "explanation": "None represents absence of value."},
                    {"question": "Comment symbol in Python?", "options": {"A": "//", "B": "#", "C": "/*", "D": "--"}, "correct_answer": "B", "explanation": "# is used for comments."},
                    {"question": "What is type('123')?", "options": {"A": "int", "B": "str", "C": "float", "D": "num"}, "correct_answer": "B", "explanation": "Anything in quotes is string."},
                    {"question": "What is type([1,2,3])?", "options": {"A": "array", "B": "tuple", "C": "list", "D": "set"}, "correct_answer": "C", "explanation": "Square brackets create a list."},
                ],
                "medium": [
                    {"question": "What happens with '5' + 5?", "options": {"A": "10", "B": "'55'", "C": "TypeError", "D": "55"}, "correct_answer": "C", "explanation": "Cannot concatenate str and int directly."},
                    {"question": "What is bool('')?", "options": {"A": "True", "B": "False", "C": "Error", "D": "None"}, "correct_answer": "B", "explanation": "Empty string is considered False."},
                    {"question": "Convert '42' to integer?", "options": {"A": "integer('42')", "B": "int('42')", "C": "num('42')", "D": "parse('42')"}, "correct_answer": "B", "explanation": "int() function converts to integer."},
                    {"question": "What creates a tuple?", "options": {"A": "[1,2]", "B": "{1,2}", "C": "(1,2)", "D": "<1,2>"}, "correct_answer": "C", "explanation": "Parentheses create tuple."},
                    {"question": "Mutable data type?", "options": {"A": "str", "B": "tuple", "C": "list", "D": "int"}, "correct_answer": "C", "explanation": "Lists can be changed after creation."},
                ],
                "hard": [
                    {"question": "What is 0.1 + 0.2 == 0.3?", "options": {"A": "True", "B": "False", "C": "Error", "D": "0.3"}, "correct_answer": "B", "explanation": "Floating point precision causes this to be False."},
                    {"question": "What does id(x) return?", "options": {"A": "Type", "B": "Value", "C": "Memory address", "D": "Name"}, "correct_answer": "C", "explanation": "id() returns unique identifier (memory address)."},
                    {"question": "Difference: is vs ==?", "options": {"A": "Same", "B": "is=identity, ===value", "C": "is=value, ===identity", "D": "Speed only"}, "correct_answer": "B", "explanation": "'is' checks identity, '==' checks value equality."},
                ],
            },
            "Operators": {
                "easy": [
                    {"question": "What is 10 % 3?", "options": {"A": "3", "B": "1", "C": "0", "D": "3.33"}, "correct_answer": "B", "explanation": "% gives remainder. 10÷3 = 3 remainder 1."},
                    {"question": "What does ** do?", "options": {"A": "Multiply", "B": "Power", "C": "Comment", "D": "Pointer"}, "correct_answer": "B", "explanation": "** is exponentiation (power)."},
                    {"question": "What is 7 // 2?", "options": {"A": "3.5", "B": "3", "C": "4", "D": "2"}, "correct_answer": "B", "explanation": "// is floor division, gives integer."},
                    {"question": "What is 2 ** 4?", "options": {"A": "8", "B": "16", "C": "6", "D": "24"}, "correct_answer": "B", "explanation": "2 to the power 4 = 16."},
                    {"question": "What does += do?", "options": {"A": "Add only", "B": "Add and assign", "C": "Compare", "D": "Increment 1"}, "correct_answer": "B", "explanation": "x += 5 means x = x + 5."},
                    {"question": "What is 10 / 4?", "options": {"A": "2", "B": "2.5", "C": "2.0", "D": "3"}, "correct_answer": "B", "explanation": "/ gives float result."},
                ],
                "medium": [
                    {"question": "What does 'in' operator check?", "options": {"A": "Type", "B": "Membership", "C": "Equality", "D": "Size"}, "correct_answer": "B", "explanation": "'in' checks if element exists in sequence."},
                    {"question": "Result of 'abc' * 2?", "options": {"A": "Error", "B": "'abcabc'", "C": "'abc2'", "D": "6"}, "correct_answer": "B", "explanation": "* repeats string."},
                    {"question": "What is not True?", "options": {"A": "True", "B": "False", "C": "Error", "D": "None"}, "correct_answer": "B", "explanation": "'not' reverses boolean."},
                    {"question": "5 > 3 and 2 > 4?", "options": {"A": "True", "B": "False", "C": "Error", "D": "None"}, "correct_answer": "B", "explanation": "'and' needs both True."},
                ],
                "hard": [
                    {"question": "What is ^ operator?", "options": {"A": "Power", "B": "XOR", "C": "AND", "D": "NOT"}, "correct_answer": "B", "explanation": "^ is bitwise XOR."},
                    {"question": "What is 5 & 3?", "options": {"A": "8", "B": "1", "C": "15", "D": "2"}, "correct_answer": "B", "explanation": "Bitwise AND: 101 & 011 = 001 = 1."},
                ],
            },
            "Control Flow": {
                "easy": [
                    {"question": "Keyword for condition?", "options": {"A": "when", "B": "if", "C": "check", "D": "test"}, "correct_answer": "B", "explanation": "'if' starts conditional statement."},
                    {"question": "What is 'else' for?", "options": {"A": "Loop", "B": "When if is False", "C": "Error", "D": "End"}, "correct_answer": "B", "explanation": "'else' runs when 'if' condition is False."},
                    {"question": "What does 'elif' mean?", "options": {"A": "end if", "B": "else if", "C": "element if", "D": "error if"}, "correct_answer": "B", "explanation": "'elif' is short for 'else if'."},
                    {"question": "Result of 5 > 3?", "options": {"A": "5", "B": "3", "C": "True", "D": "False"}, "correct_answer": "C", "explanation": "5 is greater than 3, so True."},
                    {"question": "Equality operator?", "options": {"A": "=", "B": "==", "C": "===", "D": "eq"}, "correct_answer": "B", "explanation": "== checks equality."},
                    {"question": "Not equal operator?", "options": {"A": "<>", "B": "!=", "C": "=/=", "D": "ne"}, "correct_answer": "B", "explanation": "!= means not equal."},
                ],
                "medium": [
                    {"question": "What is ternary operator?", "options": {"A": "Three values", "B": "One-line if-else", "C": "Loop", "D": "Function"}, "correct_answer": "B", "explanation": "x if condition else y - one line conditional."},
                    {"question": "True or False?", "options": {"A": "True", "B": "False", "C": "Error", "D": "None"}, "correct_answer": "A", "explanation": "'or' returns True if any is True."},
                    {"question": "True and False?", "options": {"A": "True", "B": "False", "C": "Error", "D": "None"}, "correct_answer": "B", "explanation": "'and' returns False if any is False."},
                ],
                "hard": [
                    {"question": "What is short-circuit evaluation?", "options": {"A": "Error handling", "B": "Stop when result known", "C": "Fast loop", "D": "Memory save"}, "correct_answer": "B", "explanation": "Python stops evaluating when result is determined."},
                ],
            },
            "Loops": {
                "easy": [
                    {"question": "Loop for fixed iterations?", "options": {"A": "while", "B": "for", "C": "do", "D": "repeat"}, "correct_answer": "B", "explanation": "'for' loop runs fixed number of times."},
                    {"question": "What does 'break' do?", "options": {"A": "Pause", "B": "Exit loop", "C": "Skip", "D": "Restart"}, "correct_answer": "B", "explanation": "'break' exits the loop immediately."},
                    {"question": "What does 'continue' do?", "options": {"A": "Exit", "B": "Skip to next iteration", "C": "Pause", "D": "Restart"}, "correct_answer": "B", "explanation": "'continue' skips rest of current iteration."},
                    {"question": "What is range(5)?", "options": {"A": "1-5", "B": "0-5", "C": "0-4", "D": "1-4"}, "correct_answer": "C", "explanation": "range(5) gives 0,1,2,3,4."},
                    {"question": "Infinite loop?", "options": {"A": "for i in range(10)", "B": "while True", "C": "for i in []", "D": "while False"}, "correct_answer": "B", "explanation": "'while True' runs forever."},
                    {"question": "range(3) runs how many times?", "options": {"A": "2", "B": "3", "C": "4", "D": "1"}, "correct_answer": "B", "explanation": "0, 1, 2 = 3 iterations."},
                ],
                "medium": [
                    {"question": "range(2, 10, 2) gives?", "options": {"A": "2,4,6,8,10", "B": "2,4,6,8", "C": "2,3,4,5,6,7,8,9", "D": "4,6,8"}, "correct_answer": "B", "explanation": "Start 2, stop before 10, step 2."},
                    {"question": "What is enumerate()?", "options": {"A": "Count items", "B": "Index and value", "C": "Sort", "D": "Filter"}, "correct_answer": "B", "explanation": "enumerate() gives both index and value."},
                    {"question": "Nested loop is?", "options": {"A": "Fast loop", "B": "Loop inside loop", "C": "Broken loop", "D": "No loop"}, "correct_answer": "B", "explanation": "A loop inside another loop."},
                ],
                "hard": [
                    {"question": "What is list comprehension?", "options": {"A": "List method", "B": "Concise list creation", "C": "List type", "D": "List copy"}, "correct_answer": "B", "explanation": "[x for x in items] creates list concisely."},
                    {"question": "for-else in Python?", "options": {"A": "Error", "B": "else runs if no break", "C": "Always runs", "D": "Never runs"}, "correct_answer": "B", "explanation": "'else' after 'for' runs if loop completes without break."},
                ],
            },
            "Strings": {
                "easy": [
                    {"question": "Get string length?", "options": {"A": "str.length", "B": "len(str)", "C": "str.size()", "D": "size(str)"}, "correct_answer": "B", "explanation": "len() returns length."},
                    {"question": "Convert to uppercase?", "options": {"A": "str.upper()", "B": "str.UP()", "C": "upper(str)", "D": "str.caps()"}, "correct_answer": "A", "explanation": ".upper() method converts to uppercase."},
                    {"question": "First character of 'Hello'?", "options": {"A": "'Hello'[1]", "B": "'Hello'[0]", "C": "'Hello'.first()", "D": "first('Hello')"}, "correct_answer": "B", "explanation": "Index 0 is first character."},
                    {"question": "Join strings?", "options": {"A": "str1 & str2", "B": "str1 + str2", "C": "str1.add(str2)", "D": "join(str1,str2)"}, "correct_answer": "B", "explanation": "+ concatenates strings."},
                    {"question": "Remove edge spaces?", "options": {"A": "trim()", "B": "strip()", "C": "clean()", "D": "remove()"}, "correct_answer": "B", "explanation": "strip() removes leading/trailing whitespace."},
                ],
                "medium": [
                    {"question": "'hello'.split('l')?", "options": {"A": "['he','o']", "B": "['he','','o']", "C": "['hello']", "D": "error"}, "correct_answer": "B", "explanation": "Splits at each 'l', empty between two l's."},
                    {"question": "What is f-string?", "options": {"A": "Fast string", "B": "Formatted string", "C": "Float string", "D": "File string"}, "correct_answer": "B", "explanation": "f'Hello {name}' embeds variables."},
                    {"question": "Replace in string?", "options": {"A": "str.swap()", "B": "str.replace()", "C": "str.change()", "D": "replace(str)"}, "correct_answer": "B", "explanation": ".replace(old, new) replaces text."},
                ],
                "hard": [
                    {"question": "What is string interning?", "options": {"A": "Compression", "B": "Reusing same string objects", "C": "Encryption", "D": "Parsing"}, "correct_answer": "B", "explanation": "Python reuses identical immutable strings."},
                ],
            },
            "Lists and Tuples": {
                "easy": [
                    {"question": "Create empty list?", "options": {"A": "()", "B": "[]", "C": "{}", "D": "<>"}, "correct_answer": "B", "explanation": "[] creates empty list."},
                    {"question": "Add to end of list?", "options": {"A": "list.add()", "B": "list.append()", "C": "list.push()", "D": "list.insert()"}, "correct_answer": "B", "explanation": "append() adds to end."},
                    {"question": "First element index?", "options": {"A": "1", "B": "0", "C": "-1", "D": "first"}, "correct_answer": "B", "explanation": "Indexing starts at 0."},
                    {"question": "Last element?", "options": {"A": "list[last]", "B": "list[-1]", "C": "list[0]", "D": "list.last()"}, "correct_answer": "B", "explanation": "-1 index is last element."},
                    {"question": "List vs Tuple?", "options": {"A": "Same", "B": "List mutable, tuple not", "C": "Tuple mutable", "D": "Speed only"}, "correct_answer": "B", "explanation": "Lists can change, tuples cannot."},
                    {"question": "Get list length?", "options": {"A": "list.length", "B": "len(list)", "C": "list.size()", "D": "count(list)"}, "correct_answer": "B", "explanation": "len() returns length."},
                ],
                "medium": [
                    {"question": "Remove and return last?", "options": {"A": "remove()", "B": "pop()", "C": "delete()", "D": "last()"}, "correct_answer": "B", "explanation": "pop() removes and returns last element."},
                    {"question": "Slice list[2:5]?", "options": {"A": "Index 2,3,4,5", "B": "Index 2,3,4", "C": "Index 2 to 5", "D": "Error"}, "correct_answer": "B", "explanation": "End index is excluded."},
                    {"question": "extend() vs append()?", "options": {"A": "Same", "B": "extend adds each item", "C": "append adds each item", "D": "Speed"}, "correct_answer": "B", "explanation": "extend() adds each element, append() adds as one item."},
                ],
                "hard": [
                    {"question": "List unpacking?", "options": {"A": "Compression", "B": "Assign to multiple vars", "C": "Extract", "D": "Copy"}, "correct_answer": "B", "explanation": "a, b, c = [1, 2, 3] unpacks list."},
                ],
            },
            "Dictionaries": {
                "easy": [
                    {"question": "Create empty dict?", "options": {"A": "[]", "B": "{}", "C": "()", "D": "dict[]"}, "correct_answer": "B", "explanation": "{} creates empty dictionary."},
                    {"question": "Access value by key 'name'?", "options": {"A": "dict.name", "B": "dict['name']", "C": "dict(name)", "D": "dict->name"}, "correct_answer": "B", "explanation": "dict['key'] accesses value."},
                    {"question": "Get all keys?", "options": {"A": "dict.values()", "B": "dict.keys()", "C": "dict.items()", "D": "dict.all()"}, "correct_answer": "B", "explanation": "keys() returns all keys."},
                    {"question": "Can keys be duplicate?", "options": {"A": "Yes", "B": "No", "C": "Sometimes", "D": "Only strings"}, "correct_answer": "B", "explanation": "Dictionary keys must be unique."},
                    {"question": "Add new key-value?", "options": {"A": "dict.add(k,v)", "B": "dict[k] = v", "C": "dict.put(k,v)", "D": "dict.insert(k,v)"}, "correct_answer": "B", "explanation": "Direct assignment adds new pair."},
                ],
                "medium": [
                    {"question": "Access non-existent key?", "options": {"A": "None", "B": "Error", "C": "0", "D": "Empty"}, "correct_answer": "B", "explanation": "KeyError is raised."},
                    {"question": "dict.get('key', 'default')?", "options": {"A": "Always default", "B": "Value or default", "C": "Error", "D": "None"}, "correct_answer": "B", "explanation": "get() returns value or default if missing."},
                ],
                "hard": [
                    {"question": "Dictionary comprehension?", "options": {"A": "Method", "B": "{k:v for...}", "C": "Loop only", "D": "Not possible"}, "correct_answer": "B", "explanation": "{k:v for k,v in items} creates dict."},
                ],
            },
            "Functions": {
                "easy": [
                    {"question": "Define function keyword?", "options": {"A": "function", "B": "def", "C": "func", "D": "define"}, "correct_answer": "B", "explanation": "'def' defines a function."},
                    {"question": "Call function 'greet'?", "options": {"A": "call greet", "B": "greet()", "C": "run greet", "D": "greet"}, "correct_answer": "B", "explanation": "functionname() calls function."},
                    {"question": "No return statement returns?", "options": {"A": "0", "B": "None", "C": "Error", "D": "Empty"}, "correct_answer": "B", "explanation": "Functions return None by default."},
                    {"question": "What is parameter?", "options": {"A": "Return value", "B": "Input to function", "C": "Function name", "D": "Output"}, "correct_answer": "B", "explanation": "Parameters receive input values."},
                    {"question": "What does return do?", "options": {"A": "Print", "B": "Send value back", "C": "End program", "D": "Loop"}, "correct_answer": "B", "explanation": "return sends value to caller."},
                ],
                "medium": [
                    {"question": "What is *args?", "options": {"A": "Required args", "B": "Variable positional args", "C": "Keyword args", "D": "Error"}, "correct_answer": "B", "explanation": "*args accepts any number of positional arguments."},
                    {"question": "What is **kwargs?", "options": {"A": "Positional args", "B": "Keyword arguments", "C": "Required args", "D": "Error"}, "correct_answer": "B", "explanation": "**kwargs accepts keyword arguments."},
                    {"question": "What is lambda?", "options": {"A": "Loop", "B": "Anonymous function", "C": "Class", "D": "Module"}, "correct_answer": "B", "explanation": "lambda creates small anonymous functions."},
                    {"question": "Default parameter value?", "options": {"A": "Required", "B": "Optional with preset", "C": "Error", "D": "First only"}, "correct_answer": "B", "explanation": "def func(x=5) has default value."},
                ],
                "hard": [
                    {"question": "What is closure?", "options": {"A": "End function", "B": "Function with outer scope access", "C": "Error handler", "D": "Loop"}, "correct_answer": "B", "explanation": "Closure remembers variables from enclosing scope."},
                    {"question": "What is decorator?", "options": {"A": "Comment", "B": "Function modifier", "C": "Variable", "D": "Class"}, "correct_answer": "B", "explanation": "@decorator modifies function behavior."},
                ],
            },
            "OOP Basics": {
                "easy": [
                    {"question": "Create class keyword?", "options": {"A": "def", "B": "class", "C": "object", "D": "new"}, "correct_answer": "B", "explanation": "'class' keyword defines a class."},
                    {"question": "What is self?", "options": {"A": "Class name", "B": "Current instance", "C": "Parent", "D": "Module"}, "correct_answer": "B", "explanation": "self refers to current instance."},
                    {"question": "What is __init__?", "options": {"A": "Destructor", "B": "Constructor", "C": "Static", "D": "Private"}, "correct_answer": "B", "explanation": "__init__ initializes new objects."},
                    {"question": "Create object of Car class?", "options": {"A": "new Car()", "B": "Car()", "C": "create Car", "D": "Car.new()"}, "correct_answer": "B", "explanation": "ClassName() creates object."},
                    {"question": "What is an object?", "options": {"A": "Class", "B": "Instance of class", "C": "Function", "D": "Variable"}, "correct_answer": "B", "explanation": "Object is an instance of a class."},
                ],
                "medium": [
                    {"question": "What is inheritance?", "options": {"A": "Copy code", "B": "Derive from parent class", "C": "Share memory", "D": "Link files"}, "correct_answer": "B", "explanation": "Child class inherits from parent class."},
                    {"question": "What is encapsulation?", "options": {"A": "Compression", "B": "Bundle data and methods", "C": "Encryption", "D": "Hiding only"}, "correct_answer": "B", "explanation": "Encapsulation bundles data with methods."},
                ],
                "hard": [
                    {"question": "What is polymorphism?", "options": {"A": "Multiple classes", "B": "Same interface different behavior", "C": "Inheritance", "D": "Encapsulation"}, "correct_answer": "B", "explanation": "Same method name, different implementations."},
                ],
            },
            "Exception Handling": {
                "easy": [
                    {"question": "Handle exceptions keyword?", "options": {"A": "catch", "B": "try", "C": "handle", "D": "error"}, "correct_answer": "B", "explanation": "'try' block handles exceptions."},
                    {"question": "What catches exceptions?", "options": {"A": "try", "B": "except", "C": "finally", "D": "catch"}, "correct_answer": "B", "explanation": "'except' catches exceptions."},
                    {"question": "Division by zero error?", "options": {"A": "ValueError", "B": "ZeroDivisionError", "C": "TypeError", "D": "MathError"}, "correct_answer": "B", "explanation": "ZeroDivisionError for divide by zero."},
                    {"question": "What is finally?", "options": {"A": "Optional", "B": "Always executes", "C": "Error only", "D": "Success only"}, "correct_answer": "B", "explanation": "'finally' always runs."},
                ],
                "medium": [
                    {"question": "Raise custom exception?", "options": {"A": "throw", "B": "raise", "C": "error", "D": "exception"}, "correct_answer": "B", "explanation": "'raise' throws exceptions."},
                    {"question": "Multiple except blocks?", "options": {"A": "Not allowed", "B": "Allowed", "C": "Max 2", "D": "Max 1"}, "correct_answer": "B", "explanation": "Can have multiple except blocks."},
                ],
                "hard": [
                    {"question": "Create custom exception?", "options": {"A": "Function", "B": "Inherit from Exception", "C": "String", "D": "Dict"}, "correct_answer": "B", "explanation": "class MyError(Exception): pass"},
                ],
            },
            "Recursion": {
                "easy": [
                    {"question": "What is recursion?", "options": {"A": "Loop", "B": "Function calling itself", "C": "Class", "D": "Error"}, "correct_answer": "B", "explanation": "Recursion is function calling itself."},
                    {"question": "What is base case?", "options": {"A": "First call", "B": "Stop condition", "C": "Main case", "D": "Error case"}, "correct_answer": "B", "explanation": "Base case stops recursion."},
                    {"question": "No base case causes?", "options": {"A": "Fast execution", "B": "Infinite recursion", "C": "Error message", "D": "Nothing"}, "correct_answer": "B", "explanation": "Infinite recursion and stack overflow."},
                    {"question": "Factorial of 0?", "options": {"A": "0", "B": "1", "C": "Error", "D": "Undefined"}, "correct_answer": "B", "explanation": "0! = 1 by definition."},
                ],
                "medium": [
                    {"question": "Factorial formula?", "options": {"A": "n + f(n-1)", "B": "n * f(n-1)", "C": "n - f(n-1)", "D": "n / f(n-1)"}, "correct_answer": "B", "explanation": "n! = n × (n-1)!"},
                    {"question": "Fibonacci recursive?", "options": {"A": "f(n-1)", "B": "f(n-1) + f(n-2)", "C": "f(n) * 2", "D": "f(n+1)"}, "correct_answer": "B", "explanation": "fib(n) = fib(n-1) + fib(n-2)"},
                ],
                "hard": [
                    {"question": "What is memoization?", "options": {"A": "Memory cleanup", "B": "Caching results", "C": "Memorizing code", "D": "Memory allocation"}, "correct_answer": "B", "explanation": "Storing computed results to avoid recalculation."},
                ],
            },
            "File Handling": {
                "easy": [
                    {"question": "Open file in Python?", "options": {"A": "file()", "B": "open()", "C": "read()", "D": "load()"}, "correct_answer": "B", "explanation": "open() function opens files."},
                    {"question": "Mode for reading?", "options": {"A": "'w'", "B": "'r'", "C": "'a'", "D": "'x'"}, "correct_answer": "B", "explanation": "'r' mode for reading."},
                    {"question": "Mode for writing?", "options": {"A": "'r'", "B": "'w'", "C": "'read'", "D": "'write'"}, "correct_answer": "B", "explanation": "'w' mode for writing."},
                    {"question": "Close file?", "options": {"A": "file.end()", "B": "file.close()", "C": "close(file)", "D": "file.stop()"}, "correct_answer": "B", "explanation": "close() method closes file."},
                ],
                "medium": [
                    {"question": "'with' statement for files?", "options": {"A": "Faster", "B": "Auto-closes file", "C": "Read-only", "D": "Write-only"}, "correct_answer": "B", "explanation": "'with' automatically closes file."},
                    {"question": "'w' vs 'a' mode?", "options": {"A": "Same", "B": "'w' overwrites, 'a' appends", "C": "'a' overwrites", "D": "Speed"}, "correct_answer": "B", "explanation": "'w' overwrites, 'a' appends to end."},
                ],
                "hard": [
                    {"question": "What is seek()?", "options": {"A": "Search text", "B": "Move file pointer", "C": "Find file", "D": "Close file"}, "correct_answer": "B", "explanation": "seek() moves read/write position."},
                ],
            },
            # Web Development Topics
            "HTML Basics": {
                "easy": [
                    {"question": "HTML stands for?", "options": {"A": "Hyper Text Markup Language", "B": "High Tech ML", "C": "Home Tool ML", "D": "Hyper Transfer ML"}, "correct_answer": "A", "explanation": "HyperText Markup Language."},
                    {"question": "Largest heading tag?", "options": {"A": "<h6>", "B": "<h1>", "C": "<head>", "D": "<header>"}, "correct_answer": "B", "explanation": "<h1> is largest heading."},
                    {"question": "Link tag?", "options": {"A": "<link>", "B": "<a>", "C": "<href>", "D": "<url>"}, "correct_answer": "B", "explanation": "<a href=''> creates links."},
                    {"question": "Image tag?", "options": {"A": "<image>", "B": "<img>", "C": "<pic>", "D": "<photo>"}, "correct_answer": "B", "explanation": "<img src=''> displays images."},
                    {"question": "Paragraph tag?", "options": {"A": "<para>", "B": "<p>", "C": "<text>", "D": "<paragraph>"}, "correct_answer": "B", "explanation": "<p> creates paragraph."},
                ],
                "medium": [
                    {"question": "<div> vs <span>?", "options": {"A": "Same", "B": "div=block, span=inline", "C": "span=block", "D": "No difference"}, "correct_answer": "B", "explanation": "div is block, span is inline."},
                    {"question": "Form submit method?", "options": {"A": "GET and POST", "B": "SEND and RECEIVE", "C": "UP and DOWN", "D": "IN and OUT"}, "correct_answer": "A", "explanation": "GET and POST are form methods."},
                ],
                "hard": [
                    {"question": "What is semantic HTML?", "options": {"A": "Colored HTML", "B": "Meaningful tags", "C": "Fast HTML", "D": "New HTML"}, "correct_answer": "B", "explanation": "Tags that describe content meaning."},
                ],
            },
            "CSS Fundamentals": {
                "easy": [
                    {"question": "CSS stands for?", "options": {"A": "Cascading Style Sheets", "B": "Computer Style System", "C": "Creative Style Sheets", "D": "Code Style System"}, "correct_answer": "A", "explanation": "Cascading Style Sheets."},
                    {"question": "Select by ID?", "options": {"A": ".id", "B": "#id", "C": "id", "D": "@id"}, "correct_answer": "B", "explanation": "# selects by ID."},
                    {"question": "Select by class?", "options": {"A": "#class", "B": ".class", "C": "class", "D": "@class"}, "correct_answer": "B", "explanation": ". selects by class."},
                    {"question": "Change text color?", "options": {"A": "text-color", "B": "color", "C": "font-color", "D": "text"}, "correct_answer": "B", "explanation": "color property changes text color."},
                ],
                "medium": [
                    {"question": "What is box model?", "options": {"A": "3D boxes", "B": "Content+Padding+Border+Margin", "C": "Box layout", "D": "Container"}, "correct_answer": "B", "explanation": "Box model: content, padding, border, margin."},
                    {"question": "Center element horizontally?", "options": {"A": "center: true", "B": "margin: 0 auto", "C": "align: center", "D": "horizontal: center"}, "correct_answer": "B", "explanation": "margin: 0 auto centers block elements."},
                ],
                "hard": [
                    {"question": "What is specificity?", "options": {"A": "Speed", "B": "Rule priority system", "C": "Accuracy", "D": "Order"}, "correct_answer": "B", "explanation": "Determines which CSS rules apply."},
                ],
            },
            "JavaScript Basics": {
                "easy": [
                    {"question": "Declare variable?", "options": {"A": "var x", "B": "variable x", "C": "v x", "D": "declare x"}, "correct_answer": "A", "explanation": "var, let, or const declare variables."},
                    {"question": "Single line comment?", "options": {"A": "#", "B": "//", "C": "/*", "D": "--"}, "correct_answer": "B", "explanation": "// for single line comments."},
                    {"question": "Print to console?", "options": {"A": "print()", "B": "console.log()", "C": "log()", "D": "output()"}, "correct_answer": "B", "explanation": "console.log() prints to console."},
                    {"question": "String in JS?", "options": {"A": "Only ''", "B": "'' or \"\"", "C": "Only \"\"", "D": "`` only"}, "correct_answer": "B", "explanation": "Both single and double quotes work."},
                ],
                "medium": [
                    {"question": "== vs ===?", "options": {"A": "Same", "B": "=== checks type too", "C": "== checks type", "D": "Speed"}, "correct_answer": "B", "explanation": "=== checks both value and type."},
                    {"question": "What is undefined?", "options": {"A": "Error", "B": "Variable declared but no value", "C": "Null", "D": "Zero"}, "correct_answer": "B", "explanation": "undefined means no value assigned."},
                ],
                "hard": [
                    {"question": "What is closure?", "options": {"A": "End function", "B": "Function with outer scope", "C": "Loop", "D": "Error"}, "correct_answer": "B", "explanation": "Function that remembers outer variables."},
                ],
            },
            "DOM Manipulation": {
                "easy": [
                    {"question": "DOM stands for?", "options": {"A": "Document Object Model", "B": "Data Object Model", "C": "Digital Object Model", "D": "Display Object Model"}, "correct_answer": "A", "explanation": "Document Object Model."},
                    {"question": "Get element by ID?", "options": {"A": "getById()", "B": "getElementById()", "C": "findId()", "D": "selectId()"}, "correct_answer": "B", "explanation": "document.getElementById()"},
                    {"question": "Change element text?", "options": {"A": "element.text", "B": "element.innerHTML", "C": "element.value", "D": "element.content"}, "correct_answer": "B", "explanation": "innerHTML or textContent changes text."},
                ],
                "medium": [
                    {"question": "Add event listener?", "options": {"A": "onClick()", "B": "addEventListener()", "C": "addEvent()", "D": "onEvent()"}, "correct_answer": "B", "explanation": "addEventListener('click', func)"},
                    {"question": "What is event bubbling?", "options": {"A": "Animation", "B": "Event goes child to parent", "C": "Event goes parent to child", "D": "Error"}, "correct_answer": "B", "explanation": "Events propagate up the DOM tree."},
                ],
                "hard": [
                    {"question": "innerHTML vs textContent?", "options": {"A": "Same", "B": "innerHTML parses HTML", "C": "textContent parses HTML", "D": "Speed"}, "correct_answer": "B", "explanation": "innerHTML renders HTML, textContent is plain text."},
                ],
            },
            "APIs and REST": {
                "easy": [
                    {"question": "API stands for?", "options": {"A": "Application Programming Interface", "B": "Automated Program Interface", "C": "Application Process Integration", "D": "Auto Programming Interface"}, "correct_answer": "A", "explanation": "Application Programming Interface."},
                    {"question": "HTTP method to GET data?", "options": {"A": "POST", "B": "GET", "C": "FETCH", "D": "RETRIEVE"}, "correct_answer": "B", "explanation": "GET retrieves data."},
                    {"question": "HTTP method to send data?", "options": {"A": "GET", "B": "POST", "C": "SEND", "D": "PUSH"}, "correct_answer": "B", "explanation": "POST sends data."},
                ],
                "medium": [
                    {"question": "REST stands for?", "options": {"A": "Representational State Transfer", "B": "Remote State Transfer", "C": "Request State Transfer", "D": "Response State Transfer"}, "correct_answer": "A", "explanation": "Representational State Transfer."},
                    {"question": "JSON stands for?", "options": {"A": "JavaScript Object Notation", "B": "Java Standard Object Notation", "C": "JavaScript Online Notation", "D": "Java Simple Object Notation"}, "correct_answer": "A", "explanation": "JavaScript Object Notation."},
                ],
                "hard": [
                    {"question": "PUT vs PATCH?", "options": {"A": "Same", "B": "PUT=full update, PATCH=partial", "C": "PATCH=full update", "D": "Speed"}, "correct_answer": "B", "explanation": "PUT replaces entire resource, PATCH updates part."},
                ],
            },
            # Data Structures
            "Arrays": {
                "easy": [
                    {"question": "Array access time complexity?", "options": {"A": "O(n)", "B": "O(1)", "C": "O(log n)", "D": "O(n²)"}, "correct_answer": "B", "explanation": "Array access by index is O(1)."},
                    {"question": "Arrays store elements in?", "options": {"A": "Random memory", "B": "Contiguous memory", "C": "Linked nodes", "D": "Tree structure"}, "correct_answer": "B", "explanation": "Arrays use contiguous memory."},
                ],
                "medium": [
                    {"question": "Insert at beginning complexity?", "options": {"A": "O(1)", "B": "O(n)", "C": "O(log n)", "D": "O(n²)"}, "correct_answer": "B", "explanation": "Need to shift all elements."},
                ],
                "hard": [
                    {"question": "What is dynamic array?", "options": {"A": "Fixed size", "B": "Auto-resizing array", "C": "Linked list", "D": "Tree"}, "correct_answer": "B", "explanation": "Dynamic arrays resize automatically."},
                ],
            },
            "Linked Lists": {
                "easy": [
                    {"question": "Linked list node contains?", "options": {"A": "Only data", "B": "Data and next pointer", "C": "Only pointer", "D": "Index"}, "correct_answer": "B", "explanation": "Node has data and next pointer."},
                    {"question": "First node is called?", "options": {"A": "Root", "B": "Head", "C": "Start", "D": "First"}, "correct_answer": "B", "explanation": "First node is head."},
                ],
                "medium": [
                    {"question": "Doubly linked list has?", "options": {"A": "One pointer", "B": "Next and previous pointers", "C": "Two data", "D": "Array"}, "correct_answer": "B", "explanation": "Has both next and previous pointers."},
                ],
                "hard": [
                    {"question": "Search time complexity?", "options": {"A": "O(1)", "B": "O(n)", "C": "O(log n)", "D": "O(n²)"}, "correct_answer": "B", "explanation": "Must traverse nodes, O(n)."},
                ],
            },
            "Stacks": {
                "easy": [
                    {"question": "Stack follows which principle?", "options": {"A": "FIFO", "B": "LIFO", "C": "Random", "D": "Priority"}, "correct_answer": "B", "explanation": "Last In First Out."},
                    {"question": "Add to stack operation?", "options": {"A": "Add", "B": "Push", "C": "Insert", "D": "Enqueue"}, "correct_answer": "B", "explanation": "Push adds to top."},
                    {"question": "Remove from stack?", "options": {"A": "Remove", "B": "Pop", "C": "Delete", "D": "Dequeue"}, "correct_answer": "B", "explanation": "Pop removes from top."},
                ],
                "medium": [
                    {"question": "Stack overflow means?", "options": {"A": "Empty stack", "B": "Stack exceeds limit", "C": "Stack error", "D": "Fast stack"}, "correct_answer": "B", "explanation": "Stack exceeds memory limit."},
                ],
                "hard": [
                    {"question": "Call stack in recursion?", "options": {"A": "Not used", "B": "Stores function calls", "C": "Stores variables only", "D": "Memory heap"}, "correct_answer": "B", "explanation": "Stores function calls and local variables."},
                ],
            },
            "Queues": {
                "easy": [
                    {"question": "Queue follows which principle?", "options": {"A": "LIFO", "B": "FIFO", "C": "Random", "D": "Priority"}, "correct_answer": "B", "explanation": "First In First Out."},
                    {"question": "Add to queue operation?", "options": {"A": "Push", "B": "Enqueue", "C": "Add", "D": "Insert"}, "correct_answer": "B", "explanation": "Enqueue adds to rear."},
                    {"question": "Remove from queue?", "options": {"A": "Pop", "B": "Dequeue", "C": "Remove", "D": "Delete"}, "correct_answer": "B", "explanation": "Dequeue removes from front."},
                ],
                "medium": [
                    {"question": "Circular queue advantage?", "options": {"A": "Faster", "B": "Reuses empty space", "C": "Unlimited size", "D": "No advantage"}, "correct_answer": "B", "explanation": "Reuses space when front moves."},
                ],
                "hard": [
                    {"question": "Priority queue?", "options": {"A": "Fast queue", "B": "Elements ordered by priority", "C": "VIP queue", "D": "First come"}, "correct_answer": "B", "explanation": "Dequeue by priority, not order."},
                ],
            },
            "Trees": {
                "easy": [
                    {"question": "Topmost node is called?", "options": {"A": "Head", "B": "Root", "C": "Top", "D": "First"}, "correct_answer": "B", "explanation": "Root is topmost node."},
                    {"question": "Nodes with no children?", "options": {"A": "Root", "B": "Leaf", "C": "Branch", "D": "Empty"}, "correct_answer": "B", "explanation": "Leaf nodes have no children."},
                ],
                "medium": [
                    {"question": "Binary tree max children?", "options": {"A": "1", "B": "2", "C": "3", "D": "Unlimited"}, "correct_answer": "B", "explanation": "Binary tree: max 2 children per node."},
                ],
                "hard": [
                    {"question": "Inorder traversal?", "options": {"A": "Root, Left, Right", "B": "Left, Root, Right", "C": "Left, Right, Root", "D": "Right, Root, Left"}, "correct_answer": "B", "explanation": "Inorder: Left, Root, Right."},
                ],
            },
            "Graphs": {
                "easy": [
                    {"question": "Graph has vertices and?", "options": {"A": "Lines", "B": "Edges", "C": "Points", "D": "Nodes"}, "correct_answer": "B", "explanation": "Graphs have vertices and edges."},
                    {"question": "Directed graph has?", "options": {"A": "No direction", "B": "Edges with direction", "C": "Only nodes", "D": "Cycles"}, "correct_answer": "B", "explanation": "Edges have direction in directed graph."},
                ],
                "medium": [
                    {"question": "Adjacency list stores?", "options": {"A": "All vertices", "B": "Neighbors of each vertex", "C": "All edges", "D": "Distances"}, "correct_answer": "B", "explanation": "List of neighbors for each vertex."},
                ],
                "hard": [
                    {"question": "BFS time complexity?", "options": {"A": "O(V)", "B": "O(E)", "C": "O(V+E)", "D": "O(V×E)"}, "correct_answer": "C", "explanation": "BFS visits all vertices and edges."},
                ],
            },
            "Hash Tables": {
                "easy": [
                    {"question": "Average lookup time?", "options": {"A": "O(n)", "B": "O(1)", "C": "O(log n)", "D": "O(n²)"}, "correct_answer": "B", "explanation": "Hash tables have O(1) average lookup."},
                    {"question": "Hash function does?", "options": {"A": "Sort data", "B": "Map key to index", "C": "Search data", "D": "Delete data"}, "correct_answer": "B", "explanation": "Converts key to array index."},
                ],
                "medium": [
                    {"question": "Hash collision is?", "options": {"A": "Error", "B": "Two keys same index", "C": "Full table", "D": "Empty table"}, "correct_answer": "B", "explanation": "Different keys map to same index."},
                ],
                "hard": [
                    {"question": "Chaining handles collision by?", "options": {"A": "Rehashing", "B": "Linked list at index", "C": "New table", "D": "Ignoring"}, "correct_answer": "B", "explanation": "Store multiple items in linked list."},
                ],
            },
            # Algorithms
            "Sorting": {
                "easy": [
                    {"question": "Bubble sort complexity?", "options": {"A": "O(n)", "B": "O(n²)", "C": "O(log n)", "D": "O(n log n)"}, "correct_answer": "B", "explanation": "Bubble sort is O(n²)."},
                    {"question": "Stable sort means?", "options": {"A": "Fast", "B": "Maintains relative order", "C": "No errors", "D": "In-place"}, "correct_answer": "B", "explanation": "Equal elements keep original order."},
                ],
                "medium": [
                    {"question": "Quick sort average case?", "options": {"A": "O(n)", "B": "O(n²)", "C": "O(n log n)", "D": "O(log n)"}, "correct_answer": "C", "explanation": "Quick sort averages O(n log n)."},
                ],
                "hard": [
                    {"question": "Quick sort worst case?", "options": {"A": "O(n log n)", "B": "O(n²)", "C": "O(n)", "D": "O(log n)"}, "correct_answer": "B", "explanation": "Worst case O(n²) with bad pivot."},
                ],
            },
            "Searching": {
                "easy": [
                    {"question": "Linear search complexity?", "options": {"A": "O(1)", "B": "O(n)", "C": "O(log n)", "D": "O(n²)"}, "correct_answer": "B", "explanation": "Checks each element, O(n)."},
                    {"question": "Binary search requires?", "options": {"A": "Unsorted data", "B": "Sorted data", "C": "Linked list", "D": "Hash table"}, "correct_answer": "B", "explanation": "Binary search needs sorted data."},
                ],
                "medium": [
                    {"question": "Binary search complexity?", "options": {"A": "O(n)", "B": "O(log n)", "C": "O(n²)", "D": "O(1)"}, "correct_answer": "B", "explanation": "Binary search is O(log n)."},
                ],
                "hard": [
                    {"question": "Interpolation search best for?", "options": {"A": "Any data", "B": "Uniformly distributed", "C": "Small data", "D": "Unsorted"}, "correct_answer": "B", "explanation": "Works best on uniformly distributed data."},
                ],
            },
            "Dynamic Programming": {
                "easy": [
                    {"question": "DP stands for?", "options": {"A": "Data Processing", "B": "Dynamic Programming", "C": "Direct Programming", "D": "Digital Programming"}, "correct_answer": "B", "explanation": "Dynamic Programming."},
                    {"question": "DP uses?", "options": {"A": "Random values", "B": "Stored subproblem results", "C": "Brute force", "D": "Sorting"}, "correct_answer": "B", "explanation": "Stores results of subproblems."},
                ],
                "medium": [
                    {"question": "Two approaches in DP?", "options": {"A": "Fast and slow", "B": "Top-down and bottom-up", "C": "Left and right", "D": "In and out"}, "correct_answer": "B", "explanation": "Memoization (top-down) and tabulation (bottom-up)."},
                ],
                "hard": [
                    {"question": "Optimal substructure means?", "options": {"A": "Best data structure", "B": "Optimal from optimal subproblems", "C": "Fastest", "D": "Smallest"}, "correct_answer": "B", "explanation": "Solution built from optimal subproblem solutions."},
                ],
            },
            "Greedy Algorithms": {
                "easy": [
                    {"question": "Greedy algorithm does?", "options": {"A": "Random choice", "B": "Locally optimal choice", "C": "Global search", "D": "Backtrack"}, "correct_answer": "B", "explanation": "Makes best choice at each step."},
                    {"question": "Greedy always optimal?", "options": {"A": "Yes", "B": "No, depends on problem", "C": "Always", "D": "Never"}, "correct_answer": "B", "explanation": "Not always optimal for all problems."},
                ],
                "medium": [
                    {"question": "Fractional knapsack uses?", "options": {"A": "DP", "B": "Greedy", "C": "Brute force", "D": "Backtracking"}, "correct_answer": "B", "explanation": "Fractional knapsack solved greedily."},
                ],
                "hard": [
                    {"question": "Greedy choice property?", "options": {"A": "Random", "B": "Local optimal → Global optimal", "C": "Backtrack", "D": "Exhaustive"}, "correct_answer": "B", "explanation": "Local optimal choices lead to global optimal."},
                ],
            },
        }
    
    async def generate_quiz(self, subject: str, topic: str, difficulty: str, num_questions: int, previous_questions: List[str] = []) -> Dict:
        """Generate quiz from question bank"""
        
        print(f"🤖 Agent generating: {topic} ({difficulty}) - {num_questions} questions")
        
        questions = []
        
        # Get questions for topic
        if topic in self.question_bank:
            topic_qs = self.question_bank[topic]
            
            # Get requested difficulty
            if difficulty in topic_qs:
                available = topic_qs[difficulty].copy()
                random.shuffle(available)
                questions.extend(available)
            
            # Add from other difficulties if needed
            if len(questions) < num_questions:
                for diff in ["easy", "medium", "hard"]:
                    if diff != difficulty and diff in topic_qs:
                        extra = topic_qs[diff].copy()
                        random.shuffle(extra)
                        for q in extra:
                            if q not in questions:
                                questions.append(q)
                            if len(questions) >= num_questions:
                                break
        
        # If still not enough, get from any topic
        if len(questions) < num_questions:
            for top_qs in self.question_bank.values():
                for diff in ["easy", "medium", "hard"]:
                    if diff in top_qs:
                        for q in top_qs[diff]:
                            if q not in questions:
                                questions.append(q)
                            if len(questions) >= num_questions:
                                break
                if len(questions) >= num_questions:
                    break
        
        # Shuffle and limit
        random.shuffle(questions)
        questions = questions[:num_questions]
        
        # Format
        formatted = []
        for i, q in enumerate(questions):
            formatted.append({
                "q_id": f"q{i+1}",
                "question": q["question"],
                "options": q["options"],
                "correct_answer": q["correct_answer"],
                "topic": topic,
                "sub_topic": topic,
                "difficulty": difficulty,
                "explanation": q.get("explanation", "")
            })
        
        print(f"✅ Generated {len(formatted)} questions")
        return {"questions": formatted}
    
    async def generate_weekly_report(self, user_name: str, performance_data: Dict) -> Dict:
        """Generate weekly report"""
        
        accuracy = performance_data.get('overall_accuracy', 0)
        weak = performance_data.get('weak_topics', [])
        strong = performance_data.get('strong_topics', [])
        
        if accuracy >= 80:
            summary = f"🌟 Excellent work, {user_name}! You're mastering these concepts!"
        elif accuracy >= 60:
            summary = f"👍 Good progress, {user_name}! Keep practicing daily."
        else:
            summary = f"💪 Keep going, {user_name}! Every expert was once a beginner."
        
        return {
            "summary": summary,
            "strong_topics": strong,
            "weak_topics": weak,
            "improved_topics": [],
            "declined_topics": [],
            "patterns": [],
            "focus_topics": weak[:3] if weak else ["Continue practicing"],
            "recommendations": [
                "Practice weak topics first",
                "Review explanations for wrong answers",
                "Take daily quizzes for consistency"
            ],
            "full_report": f"# Weekly Report\n\nAccuracy: {accuracy}%\n\nKeep learning! 🚀"
        }
    
    async def analyze_performance(self, attempts: List[Dict], historical_data: Dict) -> Dict:
        return {"overall_accuracy": 0, "topics": {}, "patterns": [], "message": "Done"}