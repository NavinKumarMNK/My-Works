package main

import (
	"errors"
	"fmt"
	"math/rand/v2"
	"strings"
	"sync"
	"time"
	"unicode/utf8"
)

/* function overloading is not supported in GO
func print(printValue String) {
	fmt.Println("String : " + printValue)
}
*/

func print(myObj ...interface{}) {
	fmt.Println(myObj...)
}

func intDivision(numerator int, denominator int) (int, int, error) {
	if denominator == 0 {
		return 0, 0, errors.New("Cannot Divide by zero")
	}
	var result int = numerator / denominator
	var remainder int = numerator % denominator
	return result, remainder, nil
}

func timeloop(slice []int, n int) time.Duration {
	// append n elements to the slice and return the duration of this opperation
	var t0 = time.Now()
	for len(slice) < n {
		slice = append(slice, 1)
	}
	return time.Since(t0)
}

type ownerInfo struct {
	name string
}

type gasEngine struct {
	mpg       uint8
	gallons   uint8
	ownerInfo ownerInfo
}

type electricEngine struct {
	mpkwh     uint8
	kwh       uint8
	ownerInfo ownerInfo
}

// notice the struct obj is passed before declaring the function name
func (e gasEngine) milesLeft() uint8 {
	return e.gallons * e.mpg
}

func (e electricEngine) milesLeft() uint8 {
	return e.mpkwh * e.kwh
}

func squareSlice(slice *[]float32) {
	for i := range *slice {
		(*slice)[i] = (*slice)[i] * (*slice)[i]
	}
}

// declare genric function with Type T parameters which can represent int21 or float21
// which takes an input slice of type T slice and returns type T value
func sumSlice[T int | float32](slice []T) T {
	var sum T
	for _, v := range slice {
		sum += v
	}
	return sum
}

var dbData = []string{"id1", "id2", "id3", "id4"} // database
var wg = sync.WaitGroup{}                         // wait Group
var results1 = []string{}

// plain dbCall simulation
func dbCall(i int) {
	var delay float32 = rand.Float32() * 200
	time.Sleep(time.Duration(delay) * time.Millisecond)
	fmt.Println("Result : ", dbData[i])
	results1 = append(results1, dbData[i])
	wg.Done()
}

// dbCall simulation - with single mutex
var m1 = sync.Mutex{}

func dbCallSingleMutex(value int) {
	var delay float32 = rand.Float32() * 300 // (0, 1) * 300
	time.Sleep(time.Duration(delay) * time.Millisecond)
	fmt.Println("Result : ", dbData[value])
	m1.Lock()
	results1 = append(results1, dbData[value])
	m1.Unlock()
	wg.Done()
}

// dbCall Simulation - read and write lock()
var mRW = sync.RWMutex{}

func dbCallRWMutex(i int) {
	var delay float32 = rand.Float32() * 2000
	time.Sleep(time.Duration(delay) * time.Millisecond)
	save(dbData[i])
	log()
	wg.Done()
}

func save(result string) {
	mRW.Lock() // write lock
	results1 = append(results1, result)
	mRW.Unlock()
}

func log() {
	mRW.RLock()
	print("The current results are: ", results1)
	mRW.RUnlock()
}

func putChannel(c chan int) {
	c <- 123
}

func putIterChannel(c chan int) {
	defer close(c) // close the channel before function ends else there will be a deadlock
	for i := 0; i < 3; i++ {
		c <- i
	}
}

func main() {
	// DataTypes
	var intNum int
	var floatNum float32
	intNum += 1
	fmt.Println(intNum)
	floatNum += 3.1
	fmt.Println(floatNum)

	var resultFloat float32 = float32(intNum) + floatNum
	fmt.Println(resultFloat)

	var myRune rune = 'a' // Rune is a char
	fmt.Println(myRune)
	var myString string = "Hello" + " " + `World
	!`
	fmt.Println(utf8.RuneCountInString(myString))
	fmt.Println(len(myString))

	var myBoolean bool = false // Default bool value is false
	fmt.Println(myBoolean)

	myVar := "text" // Assigning Datatype Automatically
	fmt.Println(myVar)

	var1, var2 := 1, 2
	fmt.Println(var1, var2)

	const myConst string = "const value" // Cannot change the value

	// functions
	print(myConst)
	var result, remainder, err = intDivision(5, 0)
	if err != nil {
		fmt.Println(err.Error())
	} else {
		fmt.Printf("Result = %v %v %v \n", result, remainder, err)
	}

	// switch cases
	switch {
	case err != nil:
		fmt.Println(err.Error())
	default:
		fmt.Println(result)
	}

	switch remainder {
	case 0:
		fmt.Println("The divison was exact")
	}

	// arrays
	var intArr [3]int
	// var intArr [3]int = [3]int32{1, 2, 3} or intArr := [...]int32{1, 2, 3}
	intArr[0] = 1
	fmt.Println(intArr[0:3])
	fmt.Println(&intArr[0]) // returns address of first element

	// slice
	var intSlice = []int32{8, 9}
	var intSlice2 = []int32{1, 3}
	fmt.Println(len(intSlice), cap(intSlice), &intSlice[0])
	intSlice = append(intSlice, 7)
	intSlice = append(intSlice, intSlice2...)
	fmt.Println(intSlice)

	// make slice
	var intSlice3 []int32 = make([]int32, 4, 6) // make(type, length, capacity)
	fmt.Println(intSlice3)

	// map
	var myMap map[string]uint8 = map[string]uint8{"Foo": 23, "Bar": 32}
	var myMap2 = make(map[string]uint8, 5)
	fmt.Println(myMap, myMap2)
	fmt.Println(myMap["Foo"], myMap["Ran"]) // returns zero if the key is not found

	// handling missing values
	var value, ok = myMap["Ran"]
	if ok {
		fmt.Println("The age is", value)
	} else {
		fmt.Println("Invalid Name")
	}

	// iterator - for - atmost two parameter need for the iterator
	for name, value := range myMap {
		fmt.Println(name, value)
	}

	// while
	var i = 0
	for i < 5 {
		print(i)
		i += 1
	}

	// Importance of preallocation
	var n = 1000000
	var testSlice = []int{}
	var testSlice2 = make([]int, 0, n)
	fmt.Println("Time without & with pre allocation", timeloop(testSlice, n), timeloop(testSlice2, n))

	// Strings & rune ; string is immutable
	var myString1 = "résumé" // utf-8
	var indexed = myString1[1]
	print(indexed, len(myString1))
	for i, v := range myString1 {
		print(i, v)
	}

	var myString2 = []rune("résumé") // utf-8
	var indexed1 = myString2[1]
	print(indexed1, len(myString2))
	for i, v := range myString2 {
		print(i, v)
	}

	// String Builder
	var strSlice = []string{"a", "b", "c"}
	var strBuilder strings.Builder
	for i := range strSlice {
		strBuilder.WriteString(strSlice[i])
	}
	catStr := strBuilder.String()
	fmt.Println(catStr)

	// Structs
	var myEngine = gasEngine{mpg: 24, ownerInfo: ownerInfo{"Alex"}}
	myEngine.gallons = 10
	fmt.Println(myEngine)

	// Anonymous struct
	var myEngine2 = struct {
		mpg     uint8
		gallons uint8
	}{25, 18}
	fmt.Println(myEngine2)

	fmt.Println(myEngine.milesLeft())
	// fmt.Println(myEngine2.milesLeft()) - Error because only gasEngine and electricEngine are accepted as parameters in the function definition.

	// pointers
	var p *int32 = new(int32) // allocated a space
	*p = 100
	fmt.Println(p, *p)

	var p1 *int32 // currently assigned nil
	fmt.Println(p1)
	var il int32
	p1 = &il
	*p1 = 4
	fmt.Println(p1)

	// call by address
	var slice = []float32{1, 2, 3, 4}
	fmt.Printf("%p \n", &slice)
	squareSlice(&slice)
	fmt.Println(slice)

	// Generics
	var intSlice1 = []int{1, 2, 3}
	var floatSlice1 = []float32{1, 2, 3}
	fmt.Println(sumSlice[int](intSlice1))
	fmt.Println(sumSlice[float32](floatSlice1))

	// go routines
	t0 := time.Now()
	for i := 0; i < len(dbData); i++ {
		wg.Add(1)
		// didn't wait to finish & move on after spaning go routines
		// without mutex we will get different results. because many write happens to
		// an entity at the same time
		// go dbCall(i)
		// use mutex to get rid of unexpected results
		// go dbCallSingleMutex(i)
		// To prevent reading from blocking writing operations, we use RWMutex().
		// This allows us to define separate read locks and write locks, ensuring proper
		// synchronization in the correct context.
		go dbCallRWMutex(i)
	}
	wg.Wait()
	fmt.Println("Execution Time : ", time.Since(t0))
	fmt.Println("Results : ", results1)

	// channels - {Hold Data, Thread Safe, Listen for Data}
	/* var c = make(chan int)
	c <- 1  // puts the value into unbuffered c and blocks for something to read
	var i2 = <-c
	print(i2)  fatal error: all goroutines are asleep - deadlock!
	*/

	var c = make(chan int)
	go putChannel(c)
	res := <-c
	fmt.Println(res)

	go putIterChannel(c)
	for i := range c {
		fmt.Println(i)
	}
}
