package main

import (
	"fmt"
)

type logme func(string) string

func getALogMe(in string) logme {
	l := fmt.Sprintf("yeah! %v", in)
	
	return func(s string) string {
		return fmt.Sprintf("in a logme: %v and %v\n", l, s)
	}
}

func main() {
	
	logme := getALogMe("woot")
	
	fmt.Println(logme("toot"))
}
