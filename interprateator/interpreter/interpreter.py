from .parser import Parser
from .ast import Number, BinOp, UnaryOp, Assign, Var, ComplexStatement, EmptyNode, Block


class NodeVisitor:
    def visit(self, node):  # pragma: no cover
        pass


class Interpreter(NodeVisitor):

    def __init__(self):
        self.parser = Parser()
        self.scope = {}

    def visit(self, node):
        if isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, BinOp):
            return self.visit_binop(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unaryop(node)
        elif isinstance(node, Assign):
            return self.visit_assign(node)
        elif isinstance(node, Var):
            return self.visit_var(node)
        elif isinstance(node, ComplexStatement):
            return self.visit_complex_statement(node)
        elif isinstance(node, EmptyNode):
            return None
        elif isinstance(node, Block):
            return self.visit(node.complex_statement)
        else:
            raise ValueError("Invalid node")

    def visit_assign(self, node):
        v_name = node.left.value
        v_value = self.visit(node.right)
        self.scope[v_name] = v_value

    def visit_var(self, node):
        v_name = node.token.value
        v_value = self.scope.get(v_name)
        if v_value is None:
            raise ValueError(f"Unknown variable {v_name}")
        return v_value

    def visit_number(self, node):
        return float(node.token.value)

    def visit_unaryop(self, node):
        match node.op.value:
            case "-":
                return -self.visit(node.number)
            case "+":
                return self.visit(node.number)
            case _:
                raise ValueError("Invalid operator")

    def visit_binop(self, node):
        match node.op.value:
            case "+":
                return self.visit(node.left) + self.visit(node.right)
            case "-":
                return self.visit(node.left) - self.visit(node.right)
            case "*":
                return self.visit(node.left) * self.visit(node.right)
            case "/":
                return self.visit(node.left) / self.visit(node.right)
            case _:
                raise ValueError("Invalid operator")

    def visit_complex_statement(self, node):
        for child in node.children:
            self.visit(child)

    def eval(self, code):
        tree = self.parser.parse(code)
        self.visit(tree)
        return self.scope