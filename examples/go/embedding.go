package main

import (
    "fmt"
	"encoding/json"
	"gopkg.in/yaml.v2"
)


type Pet struct {
	Name string `yaml:"thename" json:"thename"`
}

type Dog struct {
	Pet
    IsGoodBoy bool `yaml:"thegoodest" json:"thegoodest"`
}


func main() {

	/*p := Pet{Name:"bork"}
	doggo := Dog{p, true}*/

	doggo := Dog{Pet:Pet{Name: "bork"}, IsGoodBoy: true}

	fmt.Printf("\n==doggo is==\n%v\n", doggo)

	json, _ := json.Marshal(doggo)
	fmt.Printf("\n==json is==\n%v\n", string(json))

	yml, _ := yaml.Marshal(doggo)
	fmt.Printf("\n==yaml is==\n%v\n", string(yml))
}
