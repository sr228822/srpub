package main

import (
    "fmt"
	"time"
	"encoding/json"
)

type MyStruct struct {
	Dur time.Duration `json:"duration"`
}

func main() {

	ms := MyStruct{Dur: 10 * time.Hour}

	fmt.Printf("%v", ms)

	serial, err := json.Marshal(ms)
	if err != nil {
		fmt.Printf("oh no: %v", err)
	} else {
		fmt.Printf("%v", string(serial))
	}
}
