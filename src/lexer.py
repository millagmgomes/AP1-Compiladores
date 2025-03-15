import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.line = 1

        self.reserved_words = {
            "begin": "BEGIN", "boolean": "BOOLEAN", "div": "DIV", "do": "DO",
            "else": "ELSE", "end": "END", "false": "FALSE", "if": "IF",
            "integer": "INTEGER", "mod": "MOD", "program": "PROGRAM",
            "read": "READ", "then": "THEN", "true": "TRUE", "not": "NOT",
            "var": "VAR", "while": "WHILE", "write": "WRITE"
        }

        self.token_patterns = [
            (r'[ \t\r]+', None),  # Ignorar espaços e tabulações
            (r'\n', self.handle_newline),  # Contar nova linha
            (r'//.*', None),  # Comentário de linha
            (r'\(\*[\s\S]*?\*\)', None),  # Comentário de bloco (* ... *)
            (r'\{[\s\S]*?\}', None),  # Comentário de bloco { ... }
            (r':=', 'ATRIBUICAO'),
            (r':', 'DOIS_PONTOS'),
            (r';', 'PONTO_VIRGULA'),
            (r'\.', 'PONTO_FINAL'),
            (r'\(', 'ABRE_PARENTESE'),
            (r'\)', 'FECHA_PARENTESE'),
            (r',', 'VIRGULA'),
            (r'<>|>=|<=|>|<|=', 'RELACIONAL'),
            (r'\+|-', 'ADICAO'),
            (r'\*|/', 'MULTIPLICACAO'),
            (r'\b(' + '|'.join(self.reserved_words.keys()) + r')\b', self.handle_reserved_word),
            (r'[a-zA-Z_][a-zA-Z0-9_]{0,19}', self.handle_identifier),
            (r'\d+', self.handle_number)
        ]

    def handle_reserved_word(self, lexeme):
        return (self.reserved_words[lexeme.lower()], lexeme, self.line)

    def handle_identifier(self, lexeme):
        return ('IDENTIFICADOR', lexeme, self.line)

    def handle_number(self, lexeme):
        return ('NUMERO', lexeme, self.line)

    def handle_newline(self, lexeme):
        self.line += 1
        return None

    def get_next_token(self):
        while self.position < len(self.source_code):
            substring = self.source_code[self.position:]
            for pattern, token_type in self.token_patterns:
                match = re.match(pattern, substring)
                if match:
                    lexeme = match.group(0)
                    self.position += len(lexeme)
                    if token_type is None:
                        break  # Continua o loop para o próximo caractere
                    if callable(token_type):
                        result = token_type(lexeme)
                        if result is None:
                            break  # Ignora tokens como quebras de linha e continua
                        return result
                    return (token_type, lexeme, self.line)
            else:
                erro_lexema = self.source_code[self.position]
                self.position += 1
                raise Exception(f"Erro léxico na linha {self.line}: caractere inválido '{erro_lexema}'")

        return ('EOF', 'EOF', self.line)
