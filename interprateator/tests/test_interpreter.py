import pytest
from interpreter import Interpreter
from interpreter.ast import Number, BinOp, UnaryOp
from interpreter.interpreter import NodeVisitor
from interpreter.token import Token, TokenType


def make_pascal_code(exp):
    return f"BEGIN\nx:={exp};\nEND."


class TestInterpreter:
    interpreter = Interpreter()

    def test_add(self):
        assert self.interpreter.eval(make_pascal_code("2+2")) == {"x": 4}

    def test_sub(self):
        assert self.interpreter.eval(make_pascal_code("2-2")) == {"x": 0}

    def test_mul(self):
        assert self.interpreter.eval(make_pascal_code("2*2")) == {"x": 4}

    def test_div(self):
        assert self.interpreter.eval(make_pascal_code("2/2")) == {"x": 1}

    def test_add_with_letter(self):
        with pytest.raises(ValueError):
            self.interpreter.eval(make_pascal_code("2+a"))
        with pytest.raises(ValueError):
            self.interpreter.eval(make_pascal_code("a+2"))

    def test_wrong_operator(self):
        with pytest.raises(SyntaxError):
            self.interpreter.eval(make_pascal_code("1$2"))

    def test_add_with_spaces(self):
        codes = [
            "2 + 2",
            " 2+ 2 ",
            " 2+2",
            "   2 +       2"
        ]
        for code in codes:
            assert self.interpreter.eval(make_pascal_code(code)) == {"x": 4}

    def test_unary_minus(self):
        assert self.interpreter.eval(make_pascal_code("-1")) == {"x": -1}

    def test_unary_plus(self):
        assert self.interpreter.eval(make_pascal_code("+1")) == {"x": 1}

    def test_unary_expression(self):
        assert self.interpreter.eval(make_pascal_code("-(2-1)")) == {"x": -1}

    def test_visit_invalid_node(self):
        node = None
        with pytest.raises(ValueError):
            self.interpreter.visit(node)

    def test_interpreter_visit_bin_op_error(self):
        with pytest.raises(ValueError):
            self.interpreter.visit(BinOp(Number(1), Token(TokenType.OPERATOR, "&"), Number(2)))

    def test_interpreter_visit_unary_op_error(self):
        with pytest.raises(ValueError):
            self.interpreter.visit(UnaryOp(Token(TokenType.OPERATOR, "^"), Number(1)))
