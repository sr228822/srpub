package main

import "fmt"

type Cat struct {
    name  string
    skill string
}

func main() {

    cat1 := &Cat{name: "Toonces", skill: "driving"}
    cat2 := *cat1
	
    cat2.name = "Felix"

    fmt.Println(cat1.name, "is good at", cat1.skill)
    fmt.Println(cat2.name, "is good at", cat2.skill)

}
