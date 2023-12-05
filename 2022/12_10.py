import argparse
import unittest
from collections import defaultdict
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.testinput = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
        
    def test_little_input(self):
        testinput = parse_input("""noop
addx 3
addx -5""")
        cycles = [1,1,1,4,4,-1]
        actual = run_program(testinput,1)
        self.assertEqual(actual,cycles,actual)

    def test_run(self):
        cycles = run_program(parse_input(self.testinput),1)
        self.assertEqual(cycles[19],21)
        self.assertEqual(cycles[59],19)
        self.assertEqual(cycles[139],21)
        self.assertEqual(cycles[179],16)
        self.assertEqual(cycles[219],18)

    def test_puzzle1(self):
        actual = puzzle1(self.testinput)
        self.assertEqual(actual,13140)
        
    def test_crt(self):
        print (np2str(draw_crt(parse_input(self.testinput),1)))
    def test_puzzle2(self):
        pass

def run_program(instructions,X):
    i = 0
    values = [X]
    for line in instructions:
        if line == 'noop':
            values.append(X)
        else:
            values.append(X)
            X+=line[1]
            values.append(X)
    return values

def np2str(crt):
    string = ""
    for i in range(6):
        for j in range(40):
            string+=crt[i,j]
        string+="\n"
    return string

    
def draw_crt(instructions,X):
    instructions = run_program(instructions,1)
    crt = np.zeros((6,40),dtype=str)
    crt.fill(".")
    for i in range(6):
        for j in range(40):
            sprite_center = instructions[i*40+j]
            sprite = [sprite_center-1,sprite_center,sprite_center+1]
            if j in sprite:
                crt[i,j]="#"
    return crt
            
    
    
    
    
    
def parse_input(text):
    lines = text.split("\n")
    for i in range(len(lines)):
        if len(lines[i].split()) > 1:
            instruction, value = lines[i].split()
            lines[i] = (instruction,int(value))
        else:
            continue
    return lines
    
def puzzle1(text):
    cycles = run_program(parse_input(text),1)
    return sum([cycles[c-1] * c for c in [20,60,100,140,180,220]])
        

def puzzle2(text):
    print (np2str(draw_crt(parse_input(text),1)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="mode")
    
    run = subparser.add_parser('run')
    run.add_argument("--input",required=True,type=str)
    run.add_argument("--puzzle",required=True,type=int)
    
    
    args = parser.parse_args()
    if args.mode =='run':
        with open(args.input) as f:
            text = f.read().strip()
        if args.puzzle == 1:
            print (puzzle1(text))
            
        elif args.puzzle==2:
            print (puzzle2(text))
    else:
        unittest.main()

    
