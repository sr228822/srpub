package main

import (
    "fmt"
	"reflect"
)

func main() {
	a := map[string][]string{
		"key1": []string{"k1t1", "k1t2"},
		"key2": []string{"k2t1"},
	}

	b := map[string][]string{
		"key2": []string{"k2t1"},
		"key1": []string{"k1t1", "k1t2"},
	}

	if reflect.DeepEqual(a, b) {
		fmt.Println("Maps are equal")
	} else {
		fmt.Println("Maps are not equal")
	}
}
