package main

import (
    "fmt"
)

type Foo struct {
	// primitives work great
	Count int
	Name string

	// pointers and complex structures aren't deep copies tho
	StringPointer *string
	MyMap map[string]string
}

func main() {
	neat := "neat"
	a := &Foo{Count: 1, Name:"hello", StringPointer: &neat, MyMap: map[string]string{"one": "1111", "two": "2222"}}

	// copy a to b
	b := *a

	// update a
	a.Count = 7

	// print both
    fmt.Println(a)
	fmt.Println(b)

	// updating complex fields in A updates b
	*a.StringPointer = "updated"
	a.MyMap["three"] = "33333"
	fmt.Printf("these fields are shared between a and b\n")
	fmt.Println(b.MyMap)
	fmt.Println(*b.StringPointer)
}
