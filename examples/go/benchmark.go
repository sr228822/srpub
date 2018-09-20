package main

import (
	"fmt"
	"time"
)

func optionA()  {
	return
}

func main() {

	t0 := time.Now()
	for i := 0; i < 10000; i++ {
		optionA()
	}
	t1 := time.Now()
	fmt.Printf("%v", (t1 - t0))
}
