package main

import (
    "fmt"
	"reflect"
)


type MyStruct struct {
	FieldOne int64
	FieldTwo int64
	FieldThree int64
}


func main() {
    fmt.Println("Hello world!")

	mys := MyStruct{FieldOne: 11, FieldTwo: 22, FieldThree: 33}

    v := reflect.ValueOf(mys)
    for i := 0; i < v.NumField(); i++ {
        name := v.Type().Field(i).Name
        val := v.Field(i).Interface().(int64)
		fmt.Printf("%d: %s: %v\n", i, name, val)
    }

	fmt.Println("done")
}
