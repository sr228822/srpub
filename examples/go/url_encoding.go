package main

import (
	"fmt"
	"net/url"
)

func main() {

	// Standard QueryEscape call encodes a space with a "+" character.
	// This is because the specs allow either a "+" or "%20" for encoding
	// of a space character in URL Query strings and this function was
	// written for that purpose.

	myFirstString := "Hello world"
	myFirstEncodedString := url.QueryEscape(myFirstString)
	fmt.Println("URL QueryEscape:", myFirstEncodedString)

	// However, the logic for encoding a space using "%20" is build into
	// the net/url package, it is just not readily exposed. We can access
	// it by encoding a url path, where a space must be encoded as "%20"
	// according to spec.

	mySecondString := "Hello world"
	t := &url.URL{Path: mySecondString}
	mySecondEncodedString := t.String()
	fmt.Println("URL Path Encoded:", mySecondEncodedString)
	
	// Unfortunately, we are also supposed to encode "+" as "%2B", which
	// the url.URL{} trick doesn't do

	myThirdString := "Hello+world"
	t = &url.URL{Path: myThirdString}
	myThirdEncodedString := t.String()
	fmt.Println("URL Path Encoded:", myThirdEncodedString)
}
