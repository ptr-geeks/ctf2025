package main

import (
	"encoding/binary"
	"fmt"
	"math/rand"
	"net"
	"os"
	"time"
)

func main() {
	listener, err := net.Listen("tcp", ":1337")
	if err != nil {
		fmt.Println("Error starting server:", err)
		return
	}
	defer listener.Close()

	fmt.Println("Server is listening on port 1337...")

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}

		go handleConnection(conn)
	}
}

func genBarrier() (int, int) {
	for {
		from := rand.Intn(20)
		to := rand.Intn(20)
		if to < from {
			from, to = to, from
		}

		if to-from >= 3 && to-from <= 10 {
			return from, to
		}
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	fmt.Println("Client connected:", conn.RemoteAddr())
	conn.SetDeadline(time.Now().Add(60 * time.Second))

	player := 10
	iterations := 50
	forward := 5
	barriers := make([][2]int, iterations+forward)
	for i := 0; i < iterations+forward; i++ {
		from, to := genBarrier()
		barriers[i] = [2]int{from, to}
	}

	for i := range forward {
		from, to := barriers[i][0], barriers[i][1]
		if err := sendBarrier(conn, from, to); err != nil {
			fmt.Println("Error sending barrier:", err)
			return
		}
	}

	for i := range iterations {
		moves, err := recvMoves(conn)
		if err != nil {
			fmt.Println("Error receiving moves:", err)
			return
		}

		for _, move := range moves {
			if move == 'L' || move == 'l' {
				player--
			} else if move == 'R' || move == 'r' {
				player++
			}
			if player < 0 {
				player = 0
			}
			if player >= 20 {
				player = 19
			}
		}

		from, to := barriers[i][0], barriers[i][1]
		fmt.Println("Iteration:", i, "Player position:", player, "Barrier:", from, to)
		if player >= from && player <= to {
			fmt.Println("Player is within the barrier:", from, to)
			return
		}

		from, to = barriers[i+forward][0], barriers[i+forward][1]
		if err := sendBarrier(conn, from, to); err != nil {
			fmt.Println("Error sending barrier:", err)
			return
		}
	}

	fmt.Println("Game completed successfully.")
	flagfile := "flag.txt"
	data, err := os.ReadFile(flagfile)
	if err != nil {
		fmt.Println("Error reading flag file:", err)
		return
	}

	_, err = conn.Write(data)
	if err != nil {
		fmt.Println("Error sending flag:", err)
		return
	}
}

func sendBarrier(conn net.Conn, from, to int) error {
	bs := make([]byte, 8)
	binary.LittleEndian.PutUint32(bs[0:4], uint32(from))
	binary.LittleEndian.PutUint32(bs[4:8], uint32(to))
	_, err := conn.Write(bs)
	return err
}

func recvMoves(conn net.Conn) ([]rune, error) {
	buf := make([]byte, 5)
	_, err := conn.Read(buf)
	if err != nil {
		return nil, err
	}

	moves := make([]rune, 0, 5)
	for _, b := range buf {
		r := rune(b)
		if r != 'L' && r != 'R' && r != 'l' && r != 'r' && r != 'X' && r != 'x' {
			return nil, fmt.Errorf("invalid move: %c", r)
		}
		moves = append(moves, r)
	}

	return moves, nil
}
