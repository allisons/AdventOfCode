import argparse
import unittest
import numpy as np
from collections import defaultdict
import pandas as pd

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.testinput = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
    def test_puzzle2(self):
        # expected_snake = np.array([(3,3),(3,2),(3,3),(3,4),(3,3),(2,2)]+[(1,1)]*4)
        # print (puzzle2(self.testinput))
        self.assertEqual(puzzle2(self.testinput),1)

    def test_tail_movement(self):
        oldrope = np.array([(1,5),(1,4),(1,3),(1,2)]+[(1,1)]*6)
        expected = np.array([(5,5),(4,5),(3,5),(3,4),(3,3),(2,2)]+[(1,1)]*4)
        for step in range(1,5):
            newrope = np.zeros_like(oldrope)
            newrope[0] = move(*oldrope[0],'U')
            for i in range(1,len(newrope)):
                newrope[i] = follow(*newrope[i-1],*oldrope[i])
            oldrope = newrope
        self.assertTrue(np.all(oldrope==expected))
        
        
            
            
            
        
        
        
    def test_parse_input(self):
        expected = [("R",4),("U",4),("L",3),("D",1),("R",4),("D",1),("L",5),("R",2)]
        self.assertListEqual(expected, parse_input(self.testinput))
    
    def test_follow(self):
        #Initial
        self.assertEqual(follow(1,1,1,1),(1,1))
        #R 4
        self.assertEqual(follow(1,2,1,1),(1,1))
        self.assertEqual(follow(1,3,1,1),(1,2))
        self.assertEqual(follow(1,4,1,2),(1,3))
        self.assertEqual(follow(1,5,1,3),(1,4))
        
        #U 4
        self.assertEqual(follow(2,5,1,4),(1,4))
        self.assertEqual(follow(3,5,1,4),(2,5))
        self.assertEqual(follow(4,5,2,5),(3,5))
        self.assertEqual(follow(5,5,3,5),(4,5))

        #L 3
        self.assertEqual(follow(5,4,4,5),(4,5))
        self.assertEqual(follow(5,3,4,5),(5,4))
        self.assertEqual(follow(5,2,5,4),(5,3))

        #D 1
        self.assertEqual(follow(4,2,5,3),(5,3))
        
        #R 4
        self.assertEqual(follow(4,3,5,3),(5,3))
        self.assertEqual(follow(4,4,5,3),(5,3))
        self.assertEqual(follow(4,5,5,3),(4,4))
        self.assertEqual(follow(4,6,4,4),(4,5))

        #D 1
        self.assertEqual(follow(3,6,4,5),(4,5))

        #L 5
        self.assertEqual(follow(3,5,4,5),(4,5))
        self.assertEqual(follow(3,4,4,5),(4,5))
        self.assertEqual(follow(3,3,4,5),(3,4))
        self.assertEqual(follow(3,2,3,4),(3,3))
        self.assertEqual(follow(3,1,3,3),(3,2))
        
        #R 2
        self.assertEqual(follow(3,2,3,2),(3,2))
        self.assertEqual(follow(3,3,3,2),(3,2))
        
    def test_movement(self):
        head_row,head_col = (1,1)
        tail_row,tail_col = (1,1)
        for _ in range(4):
            head_row,head_col = move(head_row,head_col,"R")
            tail_row,tail_col = follow(head_row,head_col,tail_row,tail_col)
        self.assertEqual((head_row,head_col,tail_row,tail_col),(1,5,1,4))
    def test_puzzle1(self):
        self.assertEqual(puzzle1(self.testinput),13)

def parse_input(text):
    return [(line.split()[0],int(line.split()[1])) for line in text.split("\n")]

def follow (hr,hc,tr,tc):
    dist = ((hr-tr)**2+(hc-tc)**2)**(1/2)
    if dist < 2:
        return (int(tr),int(tc))
    elif dist == 2 or np.round(dist)==3:
        return int(tr+(hr-tr)/2),int((tc+(hc-tc)/2))
    elif np.round(dist)==2:
        if abs(hr-tr)==2:
            return (int(tr+(hr-tr)/2),int(hc))
        elif abs(hc-tc)==2:
            return (int(hr),int(tc+(hc-tc)/2))
        else:
            print (hr,hc,tr,tc)
            return "A diagonal case you didn't expect"
        
        
def move(hr,hc,direction):
    if direction == "U":
        return hr+1,hc
    elif direction == "D":
        return hr-1,hc
    elif  direction == "L":
        return hr,hc-1
    elif direction == "R":
        return hr,hc+1
    
    
def puzzle1(text):
    visited = defaultdict(int)
    instructions = parse_input(text)
    head_row,head_col = (1,1)
    tail_row,tail_col = (1,1)
    for direction,number in instructions:
        for _ in range(number):
            head_row,head_col = move(head_row,head_col,direction)
            tail_row,tail_col = follow(head_row,head_col,tail_row,tail_col)
            visited[(tail_row,tail_col)]+=1
    return len(visited)

def puzzle2(text):
    instructions = parse_input(text)
    oldrope = np.array([(1,1)]*10)
    tailvisits = defaultdict(int)
    for direction,number in instructions:
        for _ in range(number):
            newrope = np.zeros_like(oldrope)
            newrope[0] = move(*oldrope[0],direction)
            newrope[1] = follow(*newrope[0],*oldrope[1])
            for i in range(2,len(newrope)):
                newrope[i] = follow(*newrope[i-1],*oldrope[i])
        
            oldrope = newrope
            tailvisits[f"{oldrope[-1]}"]+=1
    return len(tailvisits)


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

    
