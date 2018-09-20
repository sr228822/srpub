package main

import (
	"sort"
    "fmt"
)

type Foo struct {
	Name string
	Id int64
}

// Define custom sort
type ById []*Foo

func (s ById) Len() int {
	return len(s)
}

func (s ById) Swap(i, j int) {
	s[i], s[j] = s[j], s[i]
}

func (s ById) Less(i, j int) bool {
	return (s[i].Id < s[j].Id)
}

// Try it out

func main() {

	var foos []*Foo
	foos = append(foos, &Foo{Name: "bork five", Id: 5})
	foos = append(foos, &Foo{Name: "lol 3", Id: 3})
	foos = append(foos, &Foo{Name: "two two", Id: 2})
	foos = append(foos, &Foo{Name: "seveen", Id: 7})
	foos = append(foos, &Foo{Name: "sixteen", Id: 16})

	sort.Sort(ById(foos))

	for _, f := range foos {
		fmt.Println(f.Name)
	}
}
