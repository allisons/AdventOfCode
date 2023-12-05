import argparse
import unittest
import re
from collections import defaultdict

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.testinput = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
        # cls.start_pos,cls.instructions = parse_input(cls.testinput)
        
    def setUp(self):
        self.start_pos,self.instructions = parse_input(self.testinput)
    
    def test_parse_input(self):
        expected_positions = {1:['Z','N'],2:['M',"C",'D'],3:["P"]}
        expected_instructions = [[1,2,1],[3,1,3],[2,2,1],[1,1,2]]
        actual_positions,actual_instructions = parse_input(self.testinput)
        self.assertListEqual(expected_instructions,actual_instructions)
        self.assertDictEqual(expected_positions,actual_positions)
    
    def test_move_one(self):
        new_state = move_one(self.instructions[0],self.start_pos)
        expected_positions = {1:['Z','N','D'],2:['M',"C"],3:["P"]}
        self.assertDictEqual(expected_positions,new_state)
        
        new_state = move_one(self.instructions[1],new_state)
        expected_positions = {1:[],2:['M',"C"],3:["P","D","N","Z"]} 
        self.assertDictEqual(expected_positions,new_state)
        
        new_state = move_one(self.instructions[2],new_state)
        expected_positions = {2:[],1:["C","M"],3:["P","D","N","Z"]}
        self.assertDictEqual(expected_positions,new_state)
        
        new_state = move_one(self.instructions[3],new_state)
        expected_positions = {2:["M"],1:["C"],3:["P","D","N","Z"]}
        self.assertDictEqual(expected_positions,new_state)
    
    def test_move_multi(self):
        new_state = move_multi(self.instructions[0],self.start_pos)
        expected_positions = {1:['Z','N','D'],2:['M',"C"],3:["P"]}
        self.assertDictEqual(expected_positions,new_state)
        
        new_state = move_multi(self.instructions[1],new_state)
        expected_positions = {1:[],2:['M',"C"],3:["P","Z","N","D"]} 
        self.assertDictEqual(expected_positions,new_state)
        
        new_state = move_multi(self.instructions[2],new_state)
        expected_positions = {2:[],1:['M',"C"],3:["P","Z","N","D"]} 
        self.assertDictEqual(expected_positions,new_state)
        
        new_state = move_multi(self.instructions[3],new_state)
        expected_positions = {2:["C"],1:['M'],3:["P","Z","N","D"]} 
        self.assertDictEqual(expected_positions,new_state)

        
    
    
    def test_puzzle1(self):
        self.assertEqual("CMZ",puzzle1(self.testinput))
    def test_puzzle2(self):
        self.assertEqual("MCD",puzzle2(self.testinput))

def parse_input(text):
    stacks = defaultdict(list)
    initial_pos,move_instructions = text.split("\n\n")
    lines = initial_pos.split("\n")
    depth = len(lines)-2
    while (depth >=0):
        pointer = 1
        stack = 1
        while pointer < len(lines[depth]):
            if lines[depth][pointer].isalpha():
                stacks[stack].append(lines[depth][pointer])
            pointer +=4
            stack+=1
        depth-=1
    
    lines = move_instructions.split("\n")
    move_instructions= [[int(v) for v in (re.findall(r"\d{1,3}",line))] for line in lines]
    return (stacks,move_instructions)
        
def move_one(instruction,state):
    state = state.copy()
    for _ in range(instruction[0]):
        moving = state[instruction[1]][-1]
        state[instruction[2]].append(moving)
        state[instruction[1]] = state[instruction[1]][:-1]
    return state

def move_multi(instruction,state):
    state = state.copy()
    moving = state[instruction[1]][-instruction[0]:]
    state[instruction[2]]+=moving
    state[instruction[1]] = state[instruction[1]][:-instruction[0]]
    return state

    
def puzzle1(text):
    state,instructions = parse_input(text)
    for instruction in instructions:
        state = move_one(instruction,state)
    return "".join([v[-1] for v in state.values()])
        

def puzzle2(text):
    state,instructions = parse_input(text)
    for instruction in instructions:
        state = move_multi(instruction,state)
    return "".join([v[-1] for v in state.values()])


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

    
