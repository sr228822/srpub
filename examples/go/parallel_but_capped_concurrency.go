// This snippet was prepared in response to this article:
// https://nathanleclaire.com/blog/2014/02/15/how-to-wait-for-all-goroutines-to-finish-executing-before-continuing/
package main

import (
    "fmt"
	"time"
)

func main() {
    urls := []string{
        "http://www.reddit.com/r/aww.json",
        "http://www.reddit.com/r/funny.json",
        "http://www.reddit.com/r/programming.json",
        "http://www.reddit.com/r/2",
        "http://www.reddit.com/r/3",
        "http://www.4.com",
        "http://www.5.com",
        "http://www.6.com",
        "http://www.7.com",
        "http://www.89.com",
    }

    resc, errc := make(chan string), make(chan error)

	// limit concurrency to 3
	sem := make(chan bool, 3)

    for _, url := range urls {
        go func(url string) {
			sem <- true
            body, err := fetch(url)
			<-sem
            if err != nil {
                errc <- err
                return
            }
            resc <- string(body)
        }(url)
    }

    for i := 0; i < len(urls); i++ {
        select {
        case res := <-resc:
            fmt.Println(res)
        case err := <-errc:
            fmt.Println(err)
        }
    }
}

func fetch(url string) (string, error) {
	fmt.Printf("starting %s\n", url)
	time.Sleep(time.Second * 3)
	fmt.Printf("  ...finished %s\n", url)
    return "bork", nil
}
