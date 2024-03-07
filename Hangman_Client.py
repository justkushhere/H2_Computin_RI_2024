import socket


game_socket = socket.socket()
game_socket.connect(('127.0.0.1', 12345))

def get_input():
    while True:
        #Print menu
        print("Menu")
        print("1) Guess a letter")
        print("2) Guess a word")
        print("3) Quit")
        choice = input("Enter choice: ")
        if choice == "1": #letter
            while True:
                letter = input("Enter a letter: ")
                if letter.isalpha() and len(letter) == 1:
                    return [letter,1]
                    break
        elif choice == "2": #word
            while True:
                word = input("Enter a word: ")
                if word.isalpha():
                    return [word,2]
                    break
        elif choice == "3":
            return[0,3]
            break
        else:
            print("Invalid Choice \n")

while True:
    data = game_socket.recv(1024).decode()
    print("DataPrint: ",data)
    if "START" in data:
        lenOfWord = int(data[6:].strip())
        curr = list("?" * lenOfWord)
        print("Current Word Guessed", str(curr), "\n")
        response = get_input()
        if response[1] == 1:
            msg = str(response[0]) + "\n GUESS"
            game_socket.sendall(msg.encode())
        elif response[1] == 2:
            msg = str(response[0]) + "\n HWORD"
            game_socket.sendall(msg.encode())
        elif response[1] == 3:
            print("Thank you for playing")
            game_socket.sendall("QUIT\n".encode())
        elif "QUIT" in data:
            break
        
    elif "GUESS" in data:
        positions = []
        for char in data:
            if char.isnumeric():
                positions.append(int(char))
        for position in positions:
            print("guessed char =", data[-2])
            curr[int(position)] = data[-2]
        print("Current Word Guessed", str(curr), "\n")
        response = get_input()
        if response[1] == 1:
            msg = str(response[0]) + "\n GUESS"
            print('MSG',msg)
            game_socket.sendall(msg.encode())
        elif response[1] == 2:
            msg = str(response[0]) + "\n HWORD"
            game_socket.sendall(msg.encode())
        else:
            print("Thank you for playing")
            game_socket.sendall("QUIT\n".encode())
    elif "WIN" in data:
        print("Player won!")
        break
    elif "LOSE" in data:
        print("Player loses.")
        break
    elif "QUIT" in data:
        break
    
        
        

game_socket.close()
