import src.lexer as Lexer


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        """Exibe uma mensagem de erro detalhada."""
        print(f"Erro sintático: {message} na linha {self.current_token[2]}")
        exit(1)

    def consume(self, token_type, expected=None):
        """Consome o token atual se ele corresponder ao esperado."""
        if self.current_token[0] == token_type and (expected is None or self.current_token[1] == expected):
            print(f"Linha: {self.current_token[2]} - atomo: {self.current_token[0]} lexema: {self.current_token[1]}")
            self.current_token = self.lexer.get_next_token()
        else:
            expected_str = f"{token_type} {expected}" if expected else token_type
            self.error(f"esperado [{expected_str}], encontrado [{self.current_token[0]} {self.current_token[1]}]")

    def program(self):
        """Analisa a estrutura principal do programa."""
        self.consume('PROGRAM')
        self.consume('IDENTIFICADOR')
        self.consume('PONTO_VIRGULA')
        self.block()
        self.consume('PONTO_FINAL')

    def block(self):
        """Analisa o bloco principal, incluindo declarações e comandos."""
        if self.current_token[0] == 'VAR':
            self.variable_declarations()
        self.compound_command()

    def variable_declarations(self):
        """Analisa as declarações de variáveis."""
        self.consume('VAR')
        while self.current_token[0] == 'IDENTIFICADOR':
            self.declaration()
            self.consume('PONTO_VIRGULA')

    def declaration(self):
        """Analisa uma única declaração de variável."""
        self.identifier_list()
        self.consume('DOIS_PONTOS')
        self.variable_type()

    def identifier_list(self):
        """Analisa uma lista de identificadores."""
        self.consume('IDENTIFICADOR')
        while self.current_token[0] == 'VIRGULA':
            self.consume('VIRGULA')
            self.consume('IDENTIFICADOR')

    def variable_type(self):
        """Verifica o tipo de variável."""
        if self.current_token[0] in ('INTEGER', 'BOOLEAN'):
            self.consume(self.current_token[0])
        else:
            self.error(f"tipo inválido [{self.current_token[1]}]")

    def compound_command(self):
        """Analisa comandos compostos."""
        self.consume('BEGIN')
        while self.current_token[0] not in ('END', 'ELSE'):
            self.command()
            if self.current_token[0] == 'PONTO_VIRGULA':
                self.consume('PONTO_VIRGULA')
            else:
                break
        if self.current_token[0] == 'END':
            self.consume('END')

    def command(self):
        """Identifica e analisa o tipo de comando."""
        if self.current_token[0] == 'IDENTIFICADOR':
            self.assignment()
        elif self.current_token[0] == 'IF':
            self.if_command()
        elif self.current_token[0] == 'WHILE':
            self.while_command()
        elif self.current_token[0] == 'READ':
            self.read_command()
        elif self.current_token[0] == 'WRITE':
            self.write_command()
        elif self.current_token[0] == 'BEGIN':
            self.compound_command()
        else:
            self.error(f"comando inválido [{self.current_token[1]}]")

    def assignment(self):
        """Analisa um comando de atribuição."""
        self.consume('IDENTIFICADOR')
        self.consume('ATRIBUICAO')
        self.expression()

    def if_command(self):
        """Analisa um comando condicional IF."""
        self.consume('IF')
        self.expression()
        self.consume('THEN')

        self.command()

        # Consome o ELSE corretamente, se existir
        if self.current_token[0] == 'ELSE':
            self.consume('ELSE')
            self.command()

    def while_command(self):
        """Analisa um comando de repetição WHILE."""
        self.consume('WHILE')
        self.expression()
        self.consume('DO')
        self.command()

    def read_command(self):
        """Analisa um comando de entrada (READ)."""
        self.consume('READ')
        self.consume('ABRE_PARENTESE')
        self.identifier_list()
        self.consume('FECHA_PARENTESE')

    def write_command(self):
        """Analisa um comando de saída (WRITE)."""
        self.consume('WRITE')
        self.consume('ABRE_PARENTESE')
        self.expression()
        while self.current_token[0] == 'VIRGULA':
            self.consume('VIRGULA')
            self.expression()
        self.consume('FECHA_PARENTESE')

    def expression(self):
        """Analisa expressões."""
        self.simple_expression()
        if self.current_token[0] == 'RELACIONAL':
            self.consume('RELACIONAL')
            self.simple_expression()

    def simple_expression(self):
        """Analisa expressões simples."""
        self.term()
        while self.current_token[0] in ('ADICAO', 'OR'):
            self.consume(self.current_token[0])
            self.term()

    def term(self):
        """Analisa termos de uma expressão."""
        self.factor()
        while self.current_token[0] in ('MULTIPLICACAO', 'DIV', 'MOD', 'AND'):
            self.consume(self.current_token[0])
            self.factor()

    def factor(self):
        """Analisa fatores de uma expressão."""
        if self.current_token[0] == 'IDENTIFICADOR':
            self.consume('IDENTIFICADOR')
        elif self.current_token[0] == 'NUMERO':
            self.consume('NUMERO')
        elif self.current_token[0] == 'TRUE':
            self.consume('TRUE')
        elif self.current_token[0] == 'FALSE':
            self.consume('FALSE')
        elif self.current_token[0] == 'NOT':
            self.consume('NOT')
            self.factor()
        elif self.current_token[0] == 'ABRE_PARENTESE':
            self.consume('ABRE_PARENTESE')
            self.expression()
            self.consume('FECHA_PARENTESE')
        else:
            self.error(f"fator inválido [{self.current_token[1]}]")
