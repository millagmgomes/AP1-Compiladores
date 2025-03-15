from src.lexer import Lexer
from src.parser import Parser

if __name__ == "__main__":

    code_error_lexer = """ 
    program exemplo;
        var
            numero: integer;
        begin
            numero := 10;
            numero := 20#; 
        end.
    """

    code_error_sintax = """
    program exemplo;
    var
        numero: integer;
    begin
        numero := ; 
    end.
    """
    code_clean = """
    program exemplo;
    var
        numero: integer;
        resultado: integer;
    begin
        numero := 10;
        resultado := numero * 2;
        
        if resultado > 15 then
            write(resultado)
        else
            write(0);
            
        read(numero);
    end.

    """

    lexer = Lexer(code_error_sintax)
    parser = Parser(lexer)
    
    try:
        parser.program()
        print("Programa analisado com sucesso!")
    except SystemExit:
        print("Erro durante a análise do programa.")
        