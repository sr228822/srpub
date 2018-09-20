package main

import (
    "fmt"
)

type Foo struct {
	Count int
	Name string
}

func main() {
	a := &Foo{Count: 1, Name:"hello"}

	// copy a to b
	b := *a

	// update a
	a.Count = 7

	// print both
    fmt.Println(a)
	fmt.Println(b)
}
