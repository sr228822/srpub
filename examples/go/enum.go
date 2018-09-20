package main

import "fmt"

const (
    // EventUnknown -
    EventUnknown = 0
    // EventRollback -
    EventRollback
    // EventRestart -
    EventRestart
    // EventRollout -
    EventRollout
)

func main() {
	fmt.Printf("EventUnknown %v\n", EventUnknown)
	fmt.Printf("EventRollback %v\n", EventRollback)
	fmt.Printf("EventRestart %v\n", EventRestart)
}
