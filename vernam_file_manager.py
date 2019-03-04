import os
import sys


def main():
    print("--- VERNAM FILE MANAGER ---")
    mainMenu()



def encodeMessage(key, plaintext):
    while len(key) < len(plaintext):
        key += key
    if len(key) > len(plaintext):
        key = key[:len(plaintext) - len(key)]

   ciphertext = ""
    for i in range(len(plaintext)):
        plainChar = plaintext[i]
        keyChar = key[i]
        ciphertext += chr(ord(plainChar) ^ ord(keyChar))

    return(ciphertext)



def decodeMessage(key, ciphertext):
    while len(key) < len(ciphertext):
        key += key
    if len(key) > len(ciphertext):
        key = key[:len(ciphertext) - len(key)]

    plaintext = ""
    for i in range(len(ciphertext)):
        cipherChar = ciphertext[i]
        keyChar = key[i]
        plaintext += chr(ord(cipherChar) ^ ord(keyChar))

    return(plaintext)



def mainMenu():
    while True:
        print("\n---Main Menu---")
        filename = FILE_PATH + input("Please enter either:\n"
                                    + "- A filename to access that file.\n"
                                    + "- \"new\" to create new file.\n"
                                    # + "- \"del\" to delete a file.\n"
                                    + "- \"look\" to see avalible files.\n"
                                    + "- \"exit\" to close program.\n\n")
        
        if filename.lower() == FILE_PATH + "exit":
            sys.exit()
            
        elif filename.lower() == FILE_PATH + "new":
            newFileScreen()
            
        elif filename.lower() == FILE_PATH + "look":
            print("\n---Avalible Files---")
            for file in os.listdir(FILE_PATH):
                print("-", file)
                
        elif filename.lower() == FILE_PATH + "/del":
            print("\n---Delete File---")
            while True:
                filename = input("Please enter filename to delete:\n")
                if validFilename(filename):
                    break
                else:
                    print("Invalid!\n")
                print("deleting")
                ## TODO create code to delete file

        elif validFilename(filename):
            fileMenu(filename)
                    
        else:
            print("Invalid!") 
        


def validFilename(filename):
    if os.path.isfile(filename):
        return True
    else:
        return False



def newFileScreen():
    print("\n---New File---")
    filename = FILE_PATH + input("Enter new file name:\n")

    if filename[-4:] != ".txt":
        filename = filename + ".txt"

    try:
        write(filename, "w", "null")
    except:
        print("Invalid!\n")
        newFileScreen()

    fileMenu(filename)

    

def fileMenu(filename):
    while True:
        print("\n---" + filename + "---")
        print("1. Read")
        print("2. Write")
        print("3. Edit Line")
        print("4. Delete Line")
        print("0. Back")

        while True:
            choice = input("\nPlease type selection: ")
            if validMenuSelection(choice, 4):
                        break
            print("Invalid!\n")

        if choice == "0": break
        elif choice == "1": readScreen(filename)
        elif choice == "2": writeScreen(filename)
        elif choice == "3": editScreen(filename)
        elif choice == "4": deleteScreen(filename)
    


def readScreen(filename):
    print("\n---Read File---")
    key = input("Key: ").lower()
    print("\n---" + filename.upper() + "---")

    encodedLines = readLines(filename)       
    i = 0
    for line in encodedLines:
       print(str(i) + ": " + decodeMessage(key, line))
       i += 1



def writeScreen(filename):
    print("\n---Write File---")
    key = input("Key: ").lower()
    while True:
        line = input("\nPlaintext to append or \"end\" to finish:\n").upper()
        if line == "END":
            break
        ciphertext = encodeMessage(key, line)
        write(filename, "a", ciphertext)



def editScreen(filename):
    print("\n---Edit Line---")
    lines = readLines(filename)
    while True:
        lineNum = input("Line to edit: ")
        if validMenuSelection(lineNum, len(lines) -1):
            print()
            break
        print("Invalid!\n")
    key = input("Key: ").lower()
    line = input("\nPlaintext to edit to:\n").upper()
    ciphertext = encodeMessage(key, line)
    editLine(filename, lineNum, key, ciphertext)



def deleteScreen(filename):
    print("\n---Delete Line---")
    lines = readLines(filename)

    while True:
        lineNum = input("Line to delete: ")
        if validMenuSelection(lineNum, len(lines) -1):
            break
        print("Invalid!\n")
    deleteLine(filename, lineNum)



def readLines(filename):
    with open(filename) as f:
        lines = f.readlines()
    out = []
    for line in lines:
        out.append(line.rstrip("\n"))
    return out



def write(filename, mode, line):
    if line == "null":
        with open(filename, mode) as f:
            f.write("")
    else:
        with open(filename, mode) as f:
            f.write(line + "\n")



def editLine(filename, lineNum, key, editTo):
    lineNum = int(lineNum)    
    lines = readLines(filename)
    newLines = lines[:lineNum]
    newLines.append(editTo)
    newLines.extend(lines[lineNum + 1:])

    write(filename, "w", newLines[0])
    for line in newLines[1:]:
        write(filename, "a", line)



def deleteLine(filename, lineNum):
    lineNum = int(lineNum)
    lines = readLines(filename)
    newLines = lines[:lineNum]
    newLines.extend(lines[lineNum + 1:])

    write(filename, "w", newLines[0])
    for line in newLines[1:]:
        write(filename, "a", line)
    


def validMenuSelection(selection, numChoices):
    if not selection.isnumeric(): return False
    selection = int(selection)
    if selection < 0: return False
    if selection > numChoices: return False
    return True


FILE_PATH = "vernam-encrypted-files/"
main()
