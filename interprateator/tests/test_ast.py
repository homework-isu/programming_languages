from interpreter.ast import Number, BinOp, UnaryOp
from interpreter.token import Token, TokenType


class TestAst():
    def test_number_str(self):
        assert str(Number(Token(TokenType.NUMBER, "2"))) == "Number(Token(TokenType.NUMBER, 2))"

    def test_bin_op_str(self):
        assert str(BinOp(Number(2), Token(TokenType.OPERATOR, "+"), Number(2))) == "BinOp(+, Number(2), Number(2))"

    def test_unary_op_str(self):
        assert str(UnaryOp(Token(TokenType.OPERATOR, "-"), Number(2))) == "UnaryOp(-, Number(2))"
