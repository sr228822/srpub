package main

import (
    "fmt"
	"regexp"
)


func main() {

	hostRegex, _ := regexp.Compile("([a-z]+)([0-9]+)-([a-z]{3}[0-9])")

	fmt.Println(hostRegex.MatchString("adhoc01-sjc1"))
	fmt.Println(hostRegex.MatchString("compute100-sjc1"))
	fmt.Println(hostRegex.MatchString("u1017-sjc1"))
	fmt.Println(hostRegex.MatchString("u1017-dca1"))
	fmt.Println(hostRegex.MatchString("vertica-golf09-sjc1"))

	fmt.Println("now false")

	fmt.Println(hostRegex.MatchString("u1017-sc1"))
	fmt.Println(hostRegex.MatchString("forgetaboutit-sc1"))
	fmt.Println(hostRegex.MatchString("0909-sc1"))
	fmt.Println(hostRegex.MatchString("adhoc01sjc1"))
	fmt.Println(hostRegex.MatchString("adhocsjc1"))
	fmt.Println(hostRegex.MatchString("sjc1"))

}
