import sys
import subprocess

#Read the input arguments
if len(sys.argv) != 4:
    print("python sendmoney.py -c/j/p <parity> <message filename>")
    sys.exit(1)
codetype = sys.argv[1][1]
paritybits = sys.argv[2]
fname = sys.argv[3]
try:
    f = open(fname, "r")
    message = f.readline()
    f.close()
except:
    print("python sendmoney.py -c/j/p <parity> <message filename>")
    sys.exit(1)

#Parse out the sender, money, and recipient from the message
#There is a bug in this code block
message = message.strip()
m = message.split(" ")
if len(m) > 6:
    print("Cannot parse message. Money transfer aborted.")
    sys.exit(1)
if m[1] != "sends" or m[3] != "to" or m[2][0] != "$":
    print("Cannot parse message. Money transfer aborted.")
    sys.exit(1)
sender = m[0]
recipient = m[4]
try:
    moneyamt = int(m[2][1:])
except:
    print("Cannot parse message. Money transfer aborted.")
    sys.exit(1)

#Define the command to run in order to check the code
#This means that you need to compile the code yourself and use a correct filename
if codetype == "c":
    checkcmd = ["./a3a", message]
if codetype == "p":
    checkcmd = ["python", "a3a.py", message]
if codetype == "j":
    checkcmd = ["java", "a3a", message]

#Check the code and send money or abort
a = subprocess.check_output(checkcmd).strip()
print("a: ", a)
print("type of a: ", type(a))
if a == paritybits:
    print("{} successfully sends ${} to {}!".format(sender, moneyamt, recipient))
else:
    print("Hamming code check failed. Money transfer aborted.")
