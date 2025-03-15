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
            (r'\:=', 'ATRIBUICAO'),
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
            (r'[a-zA-Z_][a-zA-Z0-9_]*', self.handle_identifier),
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
    
    def handle_invalid_identifier(self, lexeme):
        return ('ERRO_LEXICO', f"Erro léxico na linha {self.line}: identificador inválido ' {lexeme}'", self.line)

    def handle_invalid_character(self, lexeme):
        return ('ERRO_LEXICO', f"Erro léxico na linha {self.line}: identificador inválido ' {lexeme}'", self.line)

    def get_next_token(self):
        while self.position < len(self.source_code):
            for pattern, action in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(self.source_code, self.position)
                if match:
                    lexeme = match.group(0)
                    self.position += len(lexeme)
                    if action:
                        token = action(lexeme) if callable(action) else (action, lexeme, self.line)
                        if token: 
                            return token
                        
                    break

        return ('EOF', 'EOF', self.line)        