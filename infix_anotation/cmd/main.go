package main

import (
	"bufio"
	"fmt"
	"infix/lib"
	"os"
)

func main() {
	fmt.Println("Insert string")
	reader := bufio.NewReader(os.Stdin)

	inp, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("Error reading input:", err)
		return
	}

	chars := lib.ParceStirng(inp)

	err = lib.ValidateChars(chars)
	if err != nil {
		panic(err)
	}

	fmt.Println(lib.MakeInfix(chars))

}
