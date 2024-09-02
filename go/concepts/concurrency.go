package main

import (
	"fmt"
	"strconv"
	"sync"
	"time"
)

func main() {
	exampleSyncCode(); // This runs the sync code 
	exampleGoCoroutineCode(); // This function creates a go routine
	exampleCompleteGoCoroutineCode() // This complete function is go coroutine
	exampleWaitGroupCode() // This function adds wait group to wait for coroutine to complete
	exampleStringChannel() // This function defines a channel to communicate with go routines
	exampleBlockingChannelCode(1) // This function defines send & receive sequential which causes deadlock 
	exampleChannelCommunication() // This function runs two go routines and communicate between them through channel 
	exampleChannelSelect() // This function explains the importance of channel
	exampleWorkerPools() // This function defines how multiple concurrent worker pulls items from the queue
}

func exampleWorkerPools() {
	jobs := make(chan int, 100)
	results := make(chan int, 100)

	// 4 workers
	go worker(jobs, results)
	go worker(jobs, results)
	go worker(jobs, results)
	go worker(jobs, results)

	for i := 0; i < 100; i++ {
		jobs <- i 
	}
	close(jobs)

	for i := 0; i < 100; i++ {
		fmt.Println(<-results)
	}
	close(results)
}

func worker(jobs <-chan int, results chan<- int) {
	for n := range jobs {
		results <- calculateFibonacci(n)
	}
}

func calculateFibonacci(n int) int {
	if n <= 1 {
		return n
	}
	return calculateFibonacci(n-1) + calculateFibonacci(n-2)
}

func exampleChannelSelect() {
	c1 := make(chan string)
	c2 := make(chan string)

	go func() {
		for {
			c1 <- "Every 100s"
			time.Sleep(time.Millisecond * 100)
		}
	}()

	go func() {
		for {
			c1 <- "Every 500s"
			time.Sleep(time.Millisecond * 500)
		}
	}()

	for {
		/*  // Code gets blocked on v2 for 2 sec making the c1 to wait so here we need to use select statement
			fmt.Println(<-c1)
			fmt.Println(<-c2)
		*/	
		select {
		case msg1 := <- c1:
			fmt.Println(msg1)
		case msg2 := <- c2:
			fmt.Println(msg2)
		}
	}
}

func exampleChannelCommunication() {
	c := make(chan int)
	var w sync.WaitGroup
	w.Add(2)
	go func() {
		sendChannel(&c, 10)
		w.Done()
	}()
	go func() {
		recvChannel(&c)
		w.Done()
	}()
	w.Wait()
}

func sendChannel(c *chan int, count int) {
	for i := 0; i < count; i++ {
		*c <- i
		time.Sleep(time.Millisecond * 100)
	}
	close(*c)
}

func recvChannel(c *chan int) {
	for i := range(*c) {
		fmt.Println(i)
	}
}


func exampleBlockingChannelCode(buffer_size int) {
	c := make(chan string, buffer_size) // till channel sends buffer_size items into the channel, it won't be blocked
	c <- "foo"
	// c <- "bar" since buffer_size == 1; if this is sent in the channel, it will become deadlock
	msg := <- c
	fmt.Println(msg)
}


func exampleStringChannel() {
	c := make(chan string)
	// Since this doesn't have close channel func, this func will but the 
	// msg will be waiting the sender which creates a deadlock
	// go runCodeChannelWithoutClose("foo", 5, c)  	
	// So use use the function with close channel once the we ensured 
	// there is nothing to send through the channel
	go runCodeChannelWithClose("foo", 5, c)

	/* for {
		msg, open := <- c
		if !open {
			break
		} 
		fmt.Println(msg)  
	}
	*/
	// more direct way for above method
	for msg := range c {  // blocking operation
		fmt.Println(msg)
	}

}

func exampleWaitGroupCode() {
	// When wg.Done() is executed wg counter will decrease by 1 and the wg.wait group
	// will be waiting till the wg counter becomes zero which finishes the exampleWaitGroupCode()
	var wg sync.WaitGroup
	wg.Add(2) // Mentions that we will span 1 go coroutine
	var fun = func(str string) {
		runCodeFinite(str, 5)
		wg.Done()
	} // inline function that defines have context of exampleWaitGroupCode() variables.  
	go fun("foo")
	go fun("bar")

	wg.Wait() 
}

func exampleCompleteGoCoroutineCode() {
	// Since both the function were running in go coroutine this function has no blocking
	// So main thread finishes leaving no room to for finish runCode()
	go runCode("foo")
	go runCode("bar")
}


func exampleGoCoroutineCode() {
	// Here the runCode() with foo parameter will run on a go coroutine, 
	// so the runCode() with bar parameter will on main thread.
	go runCode("foo")
	runCode("bar")
}

func exampleSyncCode() {
	runCode("foo")
	runCode("bar") // this never prints because the above function is on infinite loop
} 

func runCodeChannelWithClose(str string, limit int, c chan string) {
	for i := 0; i < limit; i++ {
		c <- str + " " + strconv.Itoa(i)  
		time.Sleep(time.Millisecond * 100)
	}
	close(c) 
} 

func runCodeChannelWithoutClose(str string, limit int, c chan string) {
	for i := 0; i < limit; i++ {
		c <- str + " " + strconv.Itoa(i)  // send & receive through channel is blocking mechanism
		time.Sleep(time.Millisecond * 100)
	}
}

func runCodeFinite(str string, limit int) {
	for i := 0; i < limit; i++ {
		fmt.Println(i, str)
		time.Sleep(time.Millisecond * 100)
	}
}

func runCode(str string) {
	for i := 0; true; i++ {
		fmt.Println(i, str)
		time.Sleep(time.Millisecond * 100)
	}
}