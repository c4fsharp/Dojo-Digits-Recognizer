package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"log"
	"os"
	"runtime"
	"strconv"
	"time"
)

func readData(filename string) [][]int {
	var rows [][]int

	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	c := csv.NewReader(file)

	// skip header
	c.Read()

	for {
		data := []int{}
		row, err := c.Read()
		if err == io.EOF {
			break
		} else if err != nil {
			log.Fatal(err)
		}

		// convert elements to int
		for i := 0; i < len(row); i++ {
			v, _ := strconv.Atoi(row[i])
			data = append(data, v)
		}

		rows = append(rows, data)
	}

	return rows
}

func calcGoodCount(begin int, end int, images [][]int, samples [][]int, c chan int) {
	match := 0

	for i := begin; i < end; i++ {
		xs := images[i]
		minSum := 0
		minLabel := 0
		for _, ys := range samples {
			dist := 0
			xsp := xs[1:]
			ysp := ys[1:]
			for i := 0; i < len(xsp); i++ {
				diff := xsp[i] - ysp[i]
				dist += diff * diff
			}
			if minSum == 0 || dist < minSum {
				minSum = dist
				minLabel = ys[:1][0]
			}
		}
		if minLabel == xs[:1][0] {
			match++
		}
	}

	c <- match
}

func main() {
	train := readData("trainingsample.csv")
	valid := readData("validationsample.csv")

	numCpu := runtime.NumCPU()
	runtime.GOMAXPROCS(numCpu)

	start := time.Now()

	inputSize := len(valid)
	chunkSize := inputSize / numCpu
	c := make(chan int, numCpu)

	i := 0
	begin := 0
	end := 0

	numGoroutines := 0
	for i = 0; i < numCpu; i++ {
		begin = i * chunkSize
		end = (i + 1) * chunkSize
		go calcGoodCount(begin, end, valid, train, c)
		numGoroutines += 1
	}

	if end < inputSize {
		go calcGoodCount(end, inputSize, valid, train, c)
		numGoroutines += 1
	}

	match := 0
	for i := 0; i < numGoroutines; i++ {
		matches := <-c
		match += matches
	}

	fmt.Printf("Match: %d %.2f%% \n", match, float64(match*100)/float64(len(valid)))
	fmt.Printf("Duration: %s \n", time.Since(start).String())
}
