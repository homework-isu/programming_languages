import pytest

from interpreter.parser import Parser
from interpreter.token import TokenType, Token


class TestParser:
    parser = Parser()

    def test_check_token_invalid_token_order(self):
        with pytest.raises(SyntaxError):
            self.parser.check_token(TokenType.NUMBER)

    def test_factor_invalid_factor(self):
        with pytest.raises(SyntaxError):
            self.parser.factor()

    def test_factor_invalid_factor_invalid_token_type(self):
        with pytest.raises(SyntaxError, match="Invalid factor"):
            self.parser._current_token = Token(TokenType.EOL, "EOL")
            self.parser.factor()

    def test_term_invalid_term(self):
        with pytest.raises(SyntaxError):
            self.parser.term()

    def test_expr_invalid_expr(self):
        with pytest.raises(SyntaxError):
            self.parser.expr()
