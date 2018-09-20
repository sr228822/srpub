// This snippet was prepared in response to this article:
// https://nathanleclaire.com/blog/2014/02/15/how-to-wait-for-all-goroutines-to-finish-executing-before-continuing/
package main

import (
    "fmt"
	"time"
	"math/rand"
)

type Result struct {
	body string
	idx int
}

func main() {
    things := []string{
		"apple",
		"banana",
		"carron",
		"dime",
    }

	rand.Seed(time.Now().UTC().UnixNano())
	results := make(chan Result)

    for idx, thing := range things {
        go func(thing string, idx int) {
			res := boring(thing, idx)
			results <- res
        }(thing, idx)
    }

	// Wait for jobs to finish
	orderedResults := make([]string, len(things))
    for i := 0; i < len(things); i++ {
		r := <-results
		orderedResults[r.idx] = r.body
    }

	for _, r := range orderedResults {
		fmt.Println(r)
	}
}

func boring(name string, idx int) Result {
	d := rand.Intn(10)
	time.Sleep(time.Duration(d) * time.Second)
	r := Result{
		body: fmt.Sprintf("%s slept %d", name, d),
		idx: idx,
	}
	return r
}
