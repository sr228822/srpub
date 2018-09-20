package main

import (
    "fmt"
)

func foo(i int) {
	fmt.Printf("foo %v", i)
}

func main() {
	idx := 0

	foo(++i)

	fmt.Printf("done and i is %v", i)
}
