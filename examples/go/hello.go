package main

import (
    "fmt"
	"time"
)

func foo(x int) int {
    if (x == 7) {
        return 77
    }
    return (x + 2)
}

func main() {
    fmt.Println("Hello world!")

	time.Sleep(10 * time.Second)

	fmt.Println("done")
}
