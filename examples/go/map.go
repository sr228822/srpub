package main

import (
    "fmt"
)

func main() {
    query := map[string]string{
        "attrs": "these be attrs",
        "submap": "other",
        "relationships": "bork",
    }

	if res, ok := query["attrs"]; !ok {
		fmt.Println("lookup failed")
	} else {
		fmt.Println("lookup succeeded")
		fmt.Println(res)
	}

	if res, ok := query["nothere"]; !ok {
		fmt.Println("lookup failed")
	} else {
		fmt.Println("lookup succeeded")
		fmt.Println(res)
	}

	// Just doing it this way returns empty-string or nil for pointers
	res := query["alsonotthere"]
	if res == "" {
		fmt.Println("res was nil")
	} else {
		fmt.Println(res)
	}

	// For a list, its an empty list
	listmap := map[string][]string {
		"one": []string{"bork", "foo"},
	}
	fmt.Println(listmap["notthere"])
}
