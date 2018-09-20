package main


import (
    "fmt"
)

var fruit = []string{"Apple", "banana", "organge"}
var veges = []string{"carrot", "peas"}

func main() {
    fmt.Println(fruit)
    fmt.Println(veges)
    produce := append(fruit, veges...)
    fmt.Println(produce)
}
