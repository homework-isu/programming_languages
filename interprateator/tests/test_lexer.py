import pytest
from interpreter.lexer import Lexer
from interpreter.token import TokenType


class TestLexer:
    lexer = Lexer()

    def test_lex_number(self):
        lexer = self.lexer
        lexer.init("123.45")
        result = lexer.number()
        assert result == "123.45"

    def test_lex_colon_assign(self):
        lexer = self.lexer
        lexer.init(":=")
        result = lexer.colon()
        assert result.type_ == TokenType.ASSIGN

    def test_lex_colon_no_assign(self):
        lexer = self.lexer
        lexer.init(":")
        result = lexer.colon()
        assert result.type_ == TokenType.COLON

    def test_lex_keyword(self):
        lexer = self.lexer
        lexer.init("BEGIN")
        result = lexer.keyword()
        assert result.type_ == TokenType.BEGIN

    def test_lex_operator(self):
        lexer = self.lexer
        lexer.init("+")
        result = lexer.next()
        assert result.type_ == TokenType.OPERATOR

    def test_lex_operator_complex(self):
        lexer = self.lexer
        lexer.init("+-*/")
        results = [lexer.next() for _ in range(4)]
        expected_types = [TokenType.OPERATOR] * 4
        assert [result.type_ for result in results] == expected_types


    def test_lex_next(self):
        lexer = self.lexer
        lexer.init("BEGIN x := 10; END.")

        results = []
        while lexer._current_char:
            results += [lexer.next()]
        expected_types = [TokenType.BEGIN, TokenType.ID, TokenType.ASSIGN, TokenType.NUMBER,
                          TokenType.SEMICOLON, TokenType.END, TokenType.DOT]
        assert [result.type_ for result in results] == expected_types


