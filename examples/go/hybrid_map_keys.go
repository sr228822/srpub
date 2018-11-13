package main

import (
    "fmt"
)

type Key struct {
	One string
	Two int64
	Three string
}

func main() {

	m := map[Key]string{}

	k1 := Key{One: "one", Two: 2, Three: "three"}

	m[k1] = "neat"

	k2 := Key{One: "one", Two: 2, Three: "three"}
	v, ok := m[k2]
	if ok {
		fmt.Printf("%v", v)
	} else {
		fmt.Printf("key not found")
	}
}
