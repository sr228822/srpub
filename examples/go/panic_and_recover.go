package main

import "fmt"

func main() {
    f()
    fmt.Println("Returned normally from f.")
}

func f() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered in f from panic:", r)
        }
    }()
    fmt.Println("Calling g.")
    g()
    fmt.Println("back in F, Returned normally from g.")
}

func g() {
	fmt.Println("entering g")
	panic("boom")
    fmt.Println("exiting g, Never makes it here")
}
