// This snippet was prepared in response to this article:
// https://nathanleclaire.com/blog/2014/02/15/how-to-wait-for-all-goroutines-to-finish-executing-before-continuing/
package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
	"time"
)

func main() {
    urls := []string{
        "http://www.reddit.com/r/aww.json",
        "http://www.reddit.com/r/funny.json",
        "http://www.reddit.com/r/programming.json",
    }

    resc, errc := make(chan string), make(chan error)

    for _, url := range urls {
        go func(url string) {
            body, err := fetch(url)
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
	fmt.Println("starting %s", url)
	time.Sleep(time.Second * 3)
    res, err := http.Get(url)
    if err != nil {
        return "", err
    }
    body, err := ioutil.ReadAll(res.Body)
    res.Body.Close()
    if err != nil {
        return "", err
    }
    return string(body), nil
}
