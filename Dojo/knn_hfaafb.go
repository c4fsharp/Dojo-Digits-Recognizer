package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"log"
	"os"
	"strconv"
	"time"
)

func readData(filename string) ([][]int, error) {
	var result [][]int

	file, err := os.Open(filename)
	if err != nil {
		return result, err
	}
	defer file.Close()

	c := csv.NewReader(file)

	// skip header
	c.Read()

	for data := []int{}; ; data = []int{} {
		row, err := c.Read()
		if err == io.EOF {
			break
		} else if err != nil {
			return result, err
		}

		// convert elements to int
		for i := 0; i < len(row); i++ {
			v, _ := strconv.Atoi(row[i])
			data = append(data, v)
		}

		result = append(result, data)
	}

	return result, nil
}

func main() {
	start := time.Now()

	train, err := readData("trainingsample.csv")
	if err != nil {
		log.Fatal(err)
	}

	valid, err := readData("validationsample.csv")
	if err != nil {
		log.Fatal(err)
	}

	var (
		matches      int
		minimumSum   int
		minimumLabel int
		distance     int
		pxs          []int
		pys          []int
		t            int
	)

	for _, xs := range valid {
		minimumSum = 0
		minimumLabel = 0
		for _, ys := range train {
			distance = 0
			pxs = xs[1:]
			pys = ys[1:]
			for i := 0; i < len(pxs); i++ {
				t = pxs[i] - pys[i]
				distance += t * t
			}
			if minimumSum == 0 || distance < minimumSum {
				minimumSum = distance
				minimumLabel = ys[:1][0]
			}
		}
		if minimumLabel == xs[:1][0] {
			matches++
		}
	}

	r := float64(matches * 100.00 / len(valid))
	fmt.Printf("%f", r)
	fmt.Printf("Duration: %v", time.Since(start).Seconds())
}
