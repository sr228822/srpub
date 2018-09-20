package main

import (
    "fmt"
)

func xor(items ...bool) bool {
	found := 0
	for _, item := range items {
		if item {
			found++
		}
	}
	return (found == 1)
}

func main() {

	fmt.Printf("should be true\n")
	fmt.Printf("%v\n", xor(true, false, false))
	fmt.Printf("%v\n", xor(false, false, true))

	fmt.Printf("should be false\n")

	fmt.Printf("%v\n", xor(true, false, true))
	fmt.Printf("%v\n", xor(true, true, false))
	fmt.Printf("%v\n", xor(false, false, false))
	fmt.Printf("%v\n", xor(true, true, true))
}
