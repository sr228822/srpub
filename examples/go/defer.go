package main

import (
    "fmt"
	"time"
)

func bar() {
    fmt.Println("Hello world!")
	ts := time.Now()
	fmt.Printf("The time is %v\n", ts)
	defer func() {fmt.Printf("it has been %v", time.Since(ts))}()
	time.Sleep(3 * time.Second)
}

func foo() {
    fmt.Println("Hello world!")
	defer fmt.Println("Goodbye World")

	fmt.Println("=== I am the meat ===")
}

func main() {
	bar()
}
