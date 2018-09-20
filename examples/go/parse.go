package main

import (
	"fmt"
	"strings"
	"regexp"
	"strconv"
	"errors"
	//"time"
)

const FAILURE_FALLBACK = 18000

// This maps funcitons to the arg-index of their span
var functionsWithSpan = map[string]int{
	"summarize": 1,
	"smartSummarize": 1,
	"movingAverage": 1,
	"movingMedian": 1,
	"hitcount": 1,
	"sustainedAbove": 2,
	"sustainedBelow": 2,
}

func imax(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

func parseTimeString(s string) (int, error) {
	s = strings.TrimSpace(strings.Replace(strings.Replace(s, "'", "", -1), "\"", "", -1))

	// Look for well formatted integers with units
	r := regexp.MustCompile("[0-9]+[s,m,h,d]")
	match := r.FindString(s)
	if match != "" {
		unit := match[len(match)-1:]
		val, err := strconv.Atoi(match[0:len(match)-1])
		if err != nil {
			return 0, err
		}
		switch {
		case unit == "s":
			return val, nil
		case unit == "m":
			return 60 * val, nil
		case unit == "h":
			return 3600 * val, nil
		case unit == "d":
			return 86400 * val, nil
		}
	}

	// Default interpretation of integers is 10s buckets
	val, err := strconv.Atoi(s)
	if err == nil {
		return 10 * val, nil
	}

	return 0, errors.New("Failed to parse time string : " + s)
}

func splitFunction(query string) (string, []string) {
	// Split based on first parenthesis
	split := strings.SplitN(query, "(", 2)
	if len(split) != 2 {
		// Does not contain a function to parse
		return "", []string{}
	}
	function :=  split[0]
	argstring := split[1]
	argstring = argstring[0:len(argstring)-1] // remove trailing parenthesis

	// Loop through argstring splitting on commas not nested inside other functions or brackets
	args := []string{}
	bracketDepth := 0
	startIdx := 0
	for idx, r := range argstring {
		c := string(r)
		if c == "(" || c == "{" {
			bracketDepth += 1
		} else if c == ")" || c == "}" {
			bracketDepth -= 1
		} else if (c == "," && bracketDepth == 0) {
			args = append(args, strings.TrimSpace(argstring[startIdx:idx]))
			startIdx = idx+1
		}
	}
	args = append(args, strings.TrimSpace(argstring[startIdx:len(argstring)]))

	fmt.Println(function)
	for _, a := range args {
		fmt.Println("   " + a)
	}

	return function, args
}

func parseSpan(query string) (int, error) {
	span := 0

	function, args := splitFunction(query)
	if function == "" {
		// Not having a function is okay, just means we reached
		// The bottom level of recursion
		return 0, nil
	}

	// Lookup this function in our list
	if argIdx, ok := functionsWithSpan[function]; ok {
		if argIdx >= len(args) {
			return 0, errors.New("Incorrectly formatted query : " + query)
		}
		thisSpan, err := parseTimeString(args[argIdx])
		if err != nil {
			return 0, err
		}
		span = imax(span, thisSpan)
	}

	// TODO add a whitelist of functions we can safely ignore

	for _, arg := range args {
		thisSpan, err := parseSpan(arg)
		if err != nil {
			return 0, err
		}
		span = imax(span, thisSpan)
	}
	return span, nil
}

func main() {
	fmt.Println("====  expect 300 ==== ")
	fmt.Println(parseSpan("divideSeries(stats.sjc1.timers.abcdef, movingMedian(stats.sjc1.timers.zyx, '5min'))"))
	fmt.Println("====  expect 40 ==== ")
	fmt.Println(parseSpan("movingMedian(alias(transformNull(stats.*.counts.whatever, 0), 'mything'), 4)"))
	fmt.Println("====  expect 1860  ==== ")
	fmt.Println(parseSpan("movingMedian(alias(summarize(transformNull(stats.{sjc1,dca1}.counts.whatever, 0), '31min', 'sum', False), 'mything'), '21s')"))
	fmt.Println("====  expect 120  ==== ")
	fmt.Println(parseSpan("scale(summarize(divideSeries(offset(transformNull(sumSeries(stats.dca1.counts.disco.production.rt-disco*.rt-pod06.typed-request-client.blacklist-sirvice-client.v1.rpc.weights.statusCode.200),0),20),offset(transformNull(sumSeries(stats.dca1.counts.disco.production.rt-disco*.rt-pod06.typed-request-client.blacklist-sirvice-client.v1.rpc.weights.statusCode.*),0),20)),'2min'),100)"))
	//fmt.Println(a)
	fmt.Println("====  expect errors ==== ")
	fmt.Println(parseSpan("movingMedian(alias(transformNull(stats.*.counts.whatever, 0), 'mything'), 'bork')"))
	fmt.Println(parseSpan("movingMedian(alias(transformNull(stats.*.counts.whatever, 0), 'mything'))"))
}
