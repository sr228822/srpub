package main

import (
    "fmt"
)

func foo() (int, error) {
	return 2, fmt.Errorf("oh no")
}

func main() {

    fmt.Println("Hello world!")

	var RETRIES = 3

    i := 0
    for {
        i++
		res, err := foo()
		if err != nil {
			if i >= RETRIES {
				fmt.Printf("out of retires, i die")
				return
			}
			continue
		}
		fmt.Printf("I am done, the result was %v", res)
		return
	}
}
