package lib

import "errors"

var (
	ErrorInvalidChar                      = errors.New("invalid char")
	ErrorInvalidPosition                  = errors.New("invalid position for char")
	ErrorInvalidCountOperandsAndOperators = errors.New("invalid number of operands and operators")
)
