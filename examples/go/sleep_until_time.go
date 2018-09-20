package main

import (
    "fmt"
	"time"
)

func sleepUntil(h int) {
    t := time.Now()
    n := time.Date(t.Year(), t.Month(), t.Day(), h, 0, 0, 0, time.UTC)
    d := n.Sub(t)
    if d < 0 {
        n = n.Add(24 * time.Hour)
        d = n.Sub(t)
    }
	fmt.Printf("need to sleep %v", d)
	time.Sleep(d)
	fmt.Printf("ok its time now")
}

func main() {

	sleepUntil(12)
}
