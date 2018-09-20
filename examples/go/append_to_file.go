package main

import (
    "fmt"
	"time"
	"os"
)

func appendToFile(fpath string, line string) {
    // write it to a file
    f, err := os.OpenFile(fpath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0600)
    if err != nil {
        fmt.Printf("failed to open data file: %v", err)
    } else {
        defer f.Close()
        if _, err = f.WriteString(line + "\n"); err != nil {
            panic(err)
        }
    }

}

func main() {
    fmt.Println("Hello world!")

	appendToFile("/tmp/neat.txt", fmt.Sprintf("oh helloooooo %v", time.Now()))

	fmt.Println("done")
}
