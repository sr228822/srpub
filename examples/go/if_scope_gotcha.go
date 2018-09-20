package main

import (
	"fmt"
)

func foo() (int, error) {
	return 2, nil
}

func main() {

	a := 1
	if a, err := foo(); err == nil {
		// a is scoped locally here
		fmt.Printf("inside a is %v\n", a)
	}
	// a will be 1 outside
	fmt.Printf("outside a is %v\n", a)
}
