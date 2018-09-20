package main

import (
    "fmt"
	"time"
)

func main() {


	s := 5 * time.Second
	t := 500 * time.Millisecond
	v := int(s / t)
	fmt.Printf("%v", v)
}
