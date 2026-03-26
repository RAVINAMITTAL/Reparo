Rfrom tokens import *

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0; #Cursor
        self.current_char = self.text[self.pos] if len(self.text)>0 else None

    # Function to advance cursor

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None


    def skip_whitespace(self):
        while self.current_char is not None and self.current_char in ' \t':
            self.advance()

    def extract_number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(T_NUMBER, result)

    def extract_word(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        keywords = ['if', 'else', 'return', 'print']
        if result in keywords:
            return Token(T_KEYWORD, result)
        
        return Token(T_IDENTIFIER, result)

        
    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char in ' \t':
                self.skip_whitespace()
                continue
            
            if self.current_char == '\n':
                self.advance()
                return Token(T_NEWLINE, '\n')

            if self.current_char in ['{', '}', '(', ')', ';', ',']:
                token_type = T_PARENTHESIS if self.current_char in '()' else T_PUNCTUATION
                token = Token(token_type, self.current_char) 
                self.advance()
                return token

            if self.current_char.isdigit():
                return self.extract_number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.extract_word()

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(T_OPERATOR, '==')
                return Token(T_OPERATOR, '=')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(T_OPERATOR, '!=')
                return Token(T_OPERATOR, '!')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(T_OPERATOR, '<=')
                return Token(T_OPERATOR, '<')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(T_OPERATOR, '>=')
                return Token(T_OPERATOR, '>')

            
            if self.current_char in ['+', '-', '*', '/', '&', '|', '%', '~', '^']:
                token = Token(T_OPERATOR, self.current_char)
                self.advance()
                return token

            raise Exception(f"Illegal character: {self.current_char}")
            self.advance()

        return Token(T_EOF, None)

    # Helper function to get all tokens at once
    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == T_EOF:
                break
        return tokens
