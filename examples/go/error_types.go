package main

import (
    "fmt"
)

type AlphaError struct {
	error
}

func NewAlphaError(err error) AlphaError {
	return AlphaError{err}
}

type BetaError struct {
	error
}

func NewBetaError(err error) BetaError {
	return BetaError{err}
}


func foo(x int) error {
	if x == 0 {
		return NewAlphaError(fmt.Errorf("I am alpha error"))
	} else if x == 1 {
		return NewBetaError(fmt.Errorf("I am beta error"))
	} else if x == 2 {
		return fmt.Errorf("I am vanilla error")
	} else {
		return nil
	}
}

func bar(x int) {
	err := foo(x)

	switch err.(type) {
	case AlphaError:
		fmt.Println("bar got an alpha error")
		fmt.Println(err)
	case BetaError:
		fmt.Println("bar got an beta error")
		fmt.Println(err)
	case nil:
		fmt.Println("No Error")
	default:
		fmt.Println("bar got an unknown error")
		fmt.Println(err)
	}
}

func main() {
    fmt.Println("Hello world!")
	bar(0)
	bar(1)
	bar(2)
	bar(3)
}
