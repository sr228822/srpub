package main

import (
	"fmt"
	"strings"
	"math/big"

	"github.com/satori/go.uuid"
)

var (
	NumBuckets *big.Int = big.NewInt(64)

	NumSamples = 100000
)

func main() {
	fmt.Printf("starting the test\n")

	baseUUID := uuid.Must(uuid.NewV4())
	fmt.Printf("base uuid is %s\n", baseUUID)

	res := map[int64]int64{}

	for i := 0; i < NumSamples; i++ {
		hostname := fmt.Sprintf("compute%d-sjc1", i)

		// Hash together a base-UUID with a hostname, using v5 (SHA1)
		hashedUUID := uuid.NewV5(baseUUID, hostname)

		// find the integer bucket of a UUID
		var i big.Int
		i.SetString(strings.Replace(hashedUUID.String(), "-", "", 4), 16)
		modulo := &big.Int{}
		modulo.Mod(&i, NumBuckets)
		bucket := modulo.Int64()

		//fmt.Printf("%s  %s %d\n", hostname, hashedUUID, bucket)

		// count hits per bucket
		if val, ok := res[bucket]; !ok {
			res[bucket] = 1
		} else {
			res[bucket] = val + 1
		}
	}

	// Compare how big various buckets are
	min := int64(999999)
	max := int64(0)
	sum := int64(0)
	for _, v := range res {
		//fmt.Printf("%d: %d\n", k, v)
		sum += v
		if v > max {
			max = v
		}
		if v < min {
			min = v
		}
	}

	fmt.Printf("\n")
	fmt.Printf("num-bucket: %d\n", len(res))
	fmt.Printf("expected  : %d\n", NumSamples / len(res))
	fmt.Printf("min-bucket: %d\n", min)
	fmt.Printf("avg-bucket: %d\n", sum / int64(len(res)))
	fmt.Printf("max-bucket: %d\n", max)
}

