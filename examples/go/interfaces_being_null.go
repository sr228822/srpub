package main

import (
    "fmt"
)

func foo(obj interface{}) {
	if obj == nil {
		fmt.Printf("That obj is nill\n")
		return
	}
	fmt.Printf("That object is not nil, it is... %v\n", obj)
}

func main() {
	var i *int
	if i == nil {
		fmt.Printf("i is nil\n")
	}
	foo(i)
}
