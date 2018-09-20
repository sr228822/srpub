package main

import (
    "fmt"
	"regexp"
)


func main() {

	s := regexp.MustCompile("(-|_)").Split("this-is-a_thing_to-split", -1)
	for idx, e := range s {
		fmt.Printf("%d  %v\n", idx, e)
	}
}
