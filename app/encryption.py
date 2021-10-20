#Encryption logic from lab 2
#Set D to -1 to de-encrypt, with same N, from original encryption
#We should hard-code N in our app for simplicity

def encrypt(inputText, N, D):
  # flip string
  reversedText = inputText[::-1]
  # make N negative if direction is left
  N = int(N)
  D = int(D)
  shift = D*N
  encrypted = ''
  # 'rotate' ASCII
  for char in reversedText:
    oldASCII = ord(char)
    if oldASCII < 34:
      encrypted += char
      continue
    incASCII = oldASCII + shift
    newASCII = incASCII if (incASCII <= 126) else ((incASCII % 127) + 34)
    newChar = chr(newASCII)
    encrypted += newChar
  return encrypted

def testEncrypt():
  try:
    userInput = input("Enter UserID as text : ")
    if ' ' in userInput or '!' in userInput:
      raise ValueError
  except ValueError:
    print("'!' and ' ' not allowed.")
    userInput = input("Re-enter UserID: ")

  try: 
    passInput = input("Enter password as text : ")
    if ' ' in passInput or '!' in passInput:
      raise ValueError
  except ValueError:
    print("'!' and ' ' not allowed.")
    passInput = input("Re-enter password: ")

  try:
    nInput = input("Enter value of n : ")
    nInt = int(nInput)
  except ValueError:
    print("Invalid type entered.")
    nInput = input("Re-enter value for n : ")

  try:
    dInput = input("Enter value of d : ")
    dInt = int(dInput)
    if not (dInt == -1 or dInt == 1):
      raise TypeError
  except ValueError:
    print("Invalid type entered.")
    dInput = input("Re-enter value for d : ")
  except TypeError:
    print("Value must be 1 or -1.")
    dInput = input("Re-enter value for d : ")

  print('')
  encryptedUser = encrypt(userInput, nInput, dInput)
  encryptedPass = encrypt(passInput, nInput, dInput)

  print("encrypted userid: " + encryptedUser)
  print("encrypted password: " + encryptedPass)
  print("Original userid: " + userInput)
  print("Original password: " + passInput)
