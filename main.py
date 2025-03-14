from src.lexer import Lexer
from src.parser import Parser

if __name__ == "__main__":
    code = """
    program exemplo;
    var
        x, y: integer;
    begin
        if x > y then
        begin
            x := y;
            write(x);
        end
        else
        begin
            y := x;
            write(y);
        end;
    end.


    """

    lexer = Lexer(code)
    parser = Parser(lexer)
    
    try:
        parser.program()
        print("Programa analisado com sucesso!")
    except SystemExit:
        print("Erro durante a análise do programa.")
        