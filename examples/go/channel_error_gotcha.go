package main

import (
    "fmt"
)

type res struct {
	val int32
	err error
}

func main() {

	input := []int32{1, 5, 3, 11, 4, 2, 9, 6}
	//input := []int32{1, 5, 3, 11, 13, 7, 9}

	myChan := make(chan res)

	for _, val := range input {
		if val % 2 == 0 {
			myChan <- res{err: fmt.Errorf("i dont like even numbers")}
			continue
		}

		// This is example, so lets do it in a go-routine
		go func(int32) {
			square := val * val
			myChan <- res{val: square}
		}(val)
	}

	for range input {
		r := <-myChan
		if r.err == nil {
			fmt.Printf("A result %v\n", r.val)
		} else {
			fmt.Printf("An error %v\n", r.err)
		}
	}
}
