package lib

import (
	"errors"
	"fmt"
	"regexp"
	"strings"
)

func wrapError(err error, messes ...interface{}) error {
	return errors.Join(err, fmt.Errorf("%v", messes))
}

func ParceStirng(inp string) []string {
	inp = strings.TrimSpace(inp)
	return strings.Fields(inp)
}

func ValidateChars(chars []string) error {
	var (
		operands  int
		operators int
	)
	operatorsCompiler, _ := regexp.Compile(`[+\-*\/]`)

	operandsCompiler, _ := regexp.Compile(`\d`)

	for _, c := range chars {

		flag := operatorsCompiler.MatchString(c)
		if flag {
			if len(c) != 1 {
				return wrapError(ErrorInvalidChar, c)
			}
			operators++
			continue
		}
		flag = operandsCompiler.MatchString(c)
		if flag {
			operands++
			continue
		}
		return wrapError(ErrorInvalidChar, c)
	}
	if operands-1 != operators {
		return wrapError(ErrorInvalidCountOperandsAndOperators, operands, operators)
	}

	stack := []string{}
	for i := len(chars) - 1; i >= 0; i-- {
		if isOperator(chars[i]) {
			if len(stack) < 2 {
				return wrapError(ErrorInvalidPosition, chars[i])
			}
			stack = stack[:len(stack)-2]
			stack = append(stack, " ")
		} else {
			stack = append(stack, chars[i])
		}
	}
	if len(stack) != 1 {
		return fmt.Errorf("%v", stack)
	}
	return nil
}

func isOperator(c string) bool {
	switch c {
	case "+", "-", "/", "*":
		return true
	default:
		return false
	}
}

func MakeInfix(chars []string) string {
	stack := []string{}
	for i := len(chars) - 1; i >= 0; i-- {
		if isOperator(chars[i]) {
			operand1 := stack[len(stack)-1]
			stack = stack[:len(stack)-1]

			operand2 := stack[len(stack)-1]
			stack = stack[:len(stack)-1]

			infixExpr := fmt.Sprintf("(%s %s %s)", operand1, chars[i], operand2)
			stack = append(stack, infixExpr)
		} else {
			stack = append(stack, chars[i])
		}
	}
	return stack[0][1:len(stack[0])-1]
}
