package main

import (
    "fmt"
    "log"
    "net/http"
	"strings"
	"io/ioutil"
)

// formatRequest generates ascii representation of a request
func formatRequest(r *http.Request) string {
 // Create return string
 var request []string
 // Add the request string
 url := fmt.Sprintf("%v %v %v", r.Method, r.URL, r.Proto)
 request = append(request, url)
 // Add the host
 request = append(request, fmt.Sprintf("Host: %v", r.Host))
 // Loop through headers
 for name, headers := range r.Header {
   name = strings.ToLower(name)
   for _, h := range headers {
     request = append(request, fmt.Sprintf("%v: %v", name, h))
   }
 }
 
 // If this is a POST, add post data
 if r.Method == "POST" {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		request = append(request, fmt.Sprintf("error reading request body"))
	} else {
		request = append(request, fmt.Sprintf("Body: %s", string(body)))
	}
 } 

  // Return the request as a string
  return strings.Join(request, "\n")
}

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hi there, I love %s!", r.URL.Path[1:])
	fmt.Println(formatRequest(r))
}

func main() {
    http.HandleFunc("/neat", handler)
    log.Fatal(http.ListenAndServe(":12345", nil))
}
