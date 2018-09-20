package main

import (
	"context"
	"fmt"
	"time"
)

func longWork(ctx context.Context) error {
	fmt.Printf("I am starting my long work\n")
	for i := 0; i < 20; i++ {
		select {
		case <- time.After(1 * time.Second):
			fmt.Printf("work work\n")
		case <-ctx.Done():
			fmt.Printf("i am canceled\n")
			return ctx.Err()
		}
	}
	fmt.Printf("I finished my long work\n")
	return nil
}

func main() {
	// Pass a context with a timeout to tell a blocking function that it
	// should abandon its work after the timeout elapses.
	ctx, cancel := context.WithTimeout(context.Background(), 5 * time.Second)
	defer cancel()

	err := longWork(ctx)
	if err != nil {
		fmt.Printf("we errored: %v\n", err)
	}

	fmt.Printf("ending the function")

}
