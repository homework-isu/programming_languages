import pytest
from interpreter import Interpreter
from interpreter.ast import Number, BinOp, UnaryOp
from interpreter.interpreter import NodeVisitor
from interpreter.token import Token, TokenType


@pytest.fixture(scope="function")
def interpreter():
    return Interpreter()


class TestInterpreter:
    interpreter = Interpreter()

    def test_add(self, interpreter):
        assert interpreter.eval("2+2") == 4

    def test_sub(self, interpreter):
        assert interpreter.eval("2-2") == 0

    def test_mul(self, interpreter):
        assert interpreter.eval("2*2") == 4

    def test_div(self, interpreter):
        assert interpreter.eval("2/2") == 1

    def test_add_with_letter(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("2+a")
        with pytest.raises(SyntaxError):
            interpreter.eval("t+2")

    def test_wrong_operator(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("2&3")

    def test_add_with_spaces(self, interpreter):
        assert interpreter.eval("2 + 2") == 4

    def test_unary_minus(self, interpreter):
        assert interpreter.eval("-1") == -1

    def test_unary_plus(self, interpreter):
        assert interpreter.eval("+1") == 1

    def test_unary_expression(self, interpreter):
        assert interpreter.eval("-(1+1)") == -2

    def test_visit_invalid_node(self, interpreter):
        node = "invalid"
        with pytest.raises(ValueError):
            interpreter.visit(node)

    def test_node_visitor_visit(self):
        nv = NodeVisitor()
        nv.visit()

    def test_interpreter_visit_bin_op_error(self, interpreter):
        with pytest.raises(ValueError):
            assert interpreter.visit(BinOp(Number(1), Token(TokenType.OPERATOR, "&"), Number(2)))

    def test_interpreter_visit_unary_op_error(self, interpreter):
        with pytest.raises(ValueError):
            assert interpreter.visit(UnaryOp(Token(TokenType.OPERATOR, "^"), Number(1)))
