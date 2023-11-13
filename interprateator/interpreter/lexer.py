from .token import Token, TokenType

KEYWORDS = {
    "BEGIN": Token(TokenType.BEGIN, "BEGIN"),
    "END": Token(TokenType.END, "END"),
}


class Lexer:
    def __init__(self):
        self._pos = 0
        self._text = ""
        self._current_char = None

    def init(self, text):
        self._text = text
        self._pos = 0
        self._current_char = self._text[self._pos]

    def advance(self):
        self._pos += 1
        self._current_char = self._text[self._pos] if self._pos < len(self._text) else None

    def skip_whitespace(self):
        while self._current_char is not None and self._current_char.isspace():
            self.advance()

    def number(self):
        result = []
        while self._current_char is not None and (self._current_char.isdigit() or self._current_char == "."):
            result.append(self._current_char)
            self.advance()
        return "".join(result)

    def colon(self):
        self.advance()
        while self._current_char is not None and self._current_char.isspace():
            self.advance()  # pragma: no cover
        if self._current_char == "=":
            self.advance()
            return Token(TokenType.ASSIGN, ":=")
        return Token(TokenType.COLON, ":")

    def keyword(self):
        result = ''
        while self._current_char is not None and self._current_char.isalnum():
            result += self._current_char
            self.advance()
        return KEYWORDS.get(result, Token(TokenType.ID, result))

    def operator_token(self, operator_type):
        op = self._current_char
        self.advance()
        return Token(operator_type, op)

    def next(self):
        while self._current_char:
            if self._current_char.isspace():
                self.skip_whitespace()
                continue

            match self._current_char:
                case "+" | "-" | "/" | "*":
                    return self.operator_token(TokenType.OPERATOR)
                case "(":
                    return self.operator_token(TokenType.LPAREN)
                case ")":
                    return self.operator_token(TokenType.RPAREN)
                case ".":
                    return self.operator_token(TokenType.DOT)
                case ":":
                    return self.colon()
                case ";":
                    return self.operator_token(TokenType.SEMICOLON)
                case "=":
                    return self.operator_token(TokenType.ASSIGN)
                case ",":
                    return self.operator_token(TokenType.COMMA)
                case char if char.isalpha():
                    return self.read_keyword()
                case char if char.isdigit():
                    return Token(TokenType.NUMBER, self.number())

            raise SyntaxError("Bad token")