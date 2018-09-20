package main

import (
    "fmt"
)


func main() {

	a := []int{2, 8, 9}
	b := []int{13, 14, 15}

	for _, v := range a {
		for _, x := range b {
			fmt.Printf("v = %v, x = %v\n", v, x)
			if x == 14 {
				break
			}
		}
	}


}
