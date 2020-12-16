from turtle import Turtle, Screen
import random
import time

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
abc = [a+a.lower() for a in alphabet]

nums = [i for i in range(21) if i > 0]

print(abc)
print(nums)

s = Screen()
width = height = 700
height = 500
s.setup(width=width,height=height)

t = Turtle()
t.hideturtle()
t.penup()
font_size = 256
t.setx(-font_size/2)
t.sety(-font_size/2)
font = ("Times", font_size, "bold")


# TODO make these function calls

correct = 0
for a in abc:
    t.write(a, font=font)
    guess = input("Which letter this this? ")
    if guess.lower() == a[0].lower():
        print("Yes!")
        correct += 1
    else:
        print("Sorry =[")
    s.clear()

print(f"Score: {correct}")
print(round(correct * 100 / len(abc)), "%")

correct = 0
for n in nums:
    t.write(i, font=font)
    guess = input("What number is this?")
    if guess == str(n):
        print("Yes!")
        correct += 1
    else:
        print("Sorry =[")
    s.clear()

print(f"Score: {correct}")
print(round(correct * 100 / i), "%")

