package lib

import (
	"errors"
	"testing"
)

func TestParseString(t *testing.T) {
	tests := []struct {
		Name      string
		Inp       string
		Out       []string
		WaitError bool
		ExpectErr error
	}{
		{
			Name: "1",
			Inp:  "+ - 2 3 4",
			Out:  []string{"+", "-", "2", "3", "4"},
		},
		{
			Name: "2",
			Inp:  "+ 1 2",
			Out:  []string{"+", "1", "2"},
		},
	}
	for _, test := range tests {
		t.Run(test.Name, func(t *testing.T) {
			result := ParceStirng(test.Inp)
			if len(result) != len(test.Out) {
				t.Errorf("invalid len of result, wait: %d, got: %d", len(test.Out), len(result))
			}

			for i := range result {
				if test.Out[i] != result[i] {
					t.Errorf("invalid elemnt, wait: %s, got: %s", test.Out[i], result[i])
				}
			}
		})
	}
}

func TestIsOperator(t *testing.T) {
	tests := []struct{
		Name string
		Inp string
		Out bool
	}{
		{
			Name: "+",
			Inp: "+",
			Out: true,
		},
		{
			Name: "-",
			Inp: "/",
			Out: true,
		},
		{
			Name: "*",
			Inp: "/",
			Out: true,
		},
		{
			Name: "/",
			Inp: "/",
			Out: true,
		},
		{
			Name: "invalid char 1",
			Inp: "12",
			Out: true,
		},
		{
			Name: "invalid char 2",
			Inp: "++",
			Out: false,
		},
	}

	for _, test := range tests {
		t.Run(test.Name, func(t *testing.T) {
			ok := isOperator(test.Inp)
			if ok != test.Out {
				t.Errorf("invalid result, waited: %v, got: %v", test.Out, ok)
				return
			}
		})
	}
}

func TestValidateChars(t *testing.T) {
	tests := []struct {
		Name      string
		Inp       []string
		WaitError bool
		Err       error
	}{
		{
			Name:      "all right",
			Inp:       []string{"+", "-", "2", "3", "-", "4", "5"},
			WaitError: false,
			Err:       nil,
		},
		{
			Name:      "invalid char 1",
			Inp:       []string{"+", "--", "*", "2", "3", "4", "5"},
			WaitError: true,
			Err:       ErrorInvalidChar,
		},
		{
			Name:      "invalid char 2",
			Inp:       []string{"+", "-", "*", "2", "3", "4", "i"},
			WaitError: true,
			Err:       ErrorInvalidChar,
		},
		{
			Name:      "invalid postion of char 1",
			Inp:       []string{"+", "2", "*", "2", "3", "-", "4"},
			WaitError: true,
			Err:       ErrorInvalidPosition,
		},
		{
			Name:      "invalid postion of char 2",
			Inp:       []string{"1", "-", "*", "3", "4"},
			WaitError: true,
			Err:       ErrorInvalidPosition,
		},
		{
			Name:      "invalid len of operands and operators 1",
			Inp:       []string{"+", "*", "-", "3", "4"},
			WaitError: true,
			Err:       ErrorInvalidCountOperandsAndOperators,
		},
		{
			Name:      "invalid len of operands and operators 2",
			Inp:       []string{"+", "*", "2", "3", "4", "1"},
			WaitError: true,
			Err:       ErrorInvalidCountOperandsAndOperators,
		},
	}

	for _, test := range tests {
		t.Run(test.Name, func(t *testing.T) {
			err := ValidateChars(test.Inp)
			if test.WaitError {
				if err == nil {
					t.Error("waited error, got ok")
					return
				}

				if !errors.Is(err, test.Err) {
					t.Error("waited other error")
					return
				}
			}
		})
	}
}

func TestMakeInfix(t *testing.T) {
	tests := []struct {
		Name             string
		InpChars         []string
		IntOperandsCount int
		Out              string
	}{
		{
			Name:             "all right 1",
			InpChars:         []string{"+", "-", "*", "2", "3", "4", "5"},
			IntOperandsCount: 3,
			Out:              "((2 * 3) - 4) + 5",
		},
		{
			Name:             "all right 2",
			InpChars:         []string{"/", "4", "5"},
			IntOperandsCount: 1,
			Out:              "4 / 5",
		},
	}

	for _, test := range tests {
		t.Run(test.Name, func(t *testing.T) {
			result := MakeInfix(test.InpChars,)
			if result != test.Out {
				t.Errorf("invalid result, waited: %s, got %s", test.Out, result)
				return
			}
		})
	}
}
