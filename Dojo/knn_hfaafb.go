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
 
	for data := []int{}; ; data = []int{} {
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
 
func main() {
	train := readData("trainingsample.csv")
	valid := readData("validationsample.csv")
	start := time.Now()
 
	var (
		match    int
		minSum   int
		minLabel int
		dist     int
		xsp      []int
		ysp      []int
		diff     int
	)
 
	for _, xs := range valid {
		minSum = 0
		minLabel = 0
		for _, ys := range train {
			dist = 0
			xsp = xs[1:]
			ysp = ys[1:]
			for i := 0; i < len(xsp); i++ {
				diff = xsp[i] - ysp[i]
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
 
	fmt.Printf("Match: %v%% \n", float64(match*100)/float64(len(valid)))
	fmt.Printf("Duration: %s \n", time.Since(start).String())
}
