import argparse
import unittest

valuemap = {l:v for l,v in zip("abcdefghijklmnopqrstuvwxyz",range(1,27))}
valuemap = {l:v for l,v in zip("abcdefghijklmnopqrstuvwxyz".upper(),range(27,53))}|valuemap
class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.testinput = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
        
    def test_parse_input1(self):
        expected = [("vJrwpWtwJgWr","hcsFMMfFFhFp"),
                   ("jqHRNqRjqzjGDLGL","rsFMfFZSrLrFZsSL"),
                   ("PmmdzqPrV","vPwwTWBwg"),
                    ("wMqvLMZHhHMvwLH","jbvcjnnSBnvTQFn"),
                   ("ttgJtRGJ","QctTZtZT"),
                    ("CrZsJsPPZsGz","wwsLwLmpwMDw")]
        self.assertListEqual(expected,parse_input1(self.testinput))
    
    def test_in_common(self):
        self.assertEqual(in_common1(*parse_input1(self.testinput)[0]),"p")
        self.assertEqual(in_common1(*parse_input1(self.testinput)[1]),"L")
        self.assertEqual(in_common1(*parse_input1(self.testinput)[2]),"P")
        self.assertEqual(in_common1(*parse_input1(self.testinput)[3]),"v")
        self.assertEqual(in_common1(*parse_input1(self.testinput)[4]),"t")
        self.assertEqual(in_common1(*parse_input1(self.testinput)[5]),"s")    
    def test_value_map(self):
        self.assertEqual(valuemap["p"],16)
        self.assertEqual(valuemap["L"],38)
        self.assertEqual(valuemap["P"],42)
        self.assertEqual(valuemap["v"],22)
        self.assertEqual(valuemap["t"],20)
        self.assertEqual(valuemap["s"],19)
    
    def test_puzzle1(self):
        self.assertEqual(157,puzzle1(self.testinput))
        
    def test_parse_input2(self):
        self.assertListEqual([["vJrwpWtwJgWrhcsFMMfFFhFp",
                                "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                                "PmmdzqPrVvPwwTWBwg"],
                              ["wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
                               "ttgJtRGJQctTZtZT","CrZsJsPPZsGzwwsLwLmpwMDw"]],parse_input2(self.testinput))
                     
    def test_in_common2(self):
        sets = parse_input2(self.testinput)
        self.assertEqual(in_common2(*sets[0]),"r")
        self.assertEqual(in_common2(*sets[1]),"Z")
        
    def test_puzzle2(self):
        self.assertEqual(puzzle2(self.testinput),70)

def parse_input1(text):
    return [(line[:len(line)//2],line[len(line)//2:]) for line in text.split("\n")]

def parse_input2(text):
    
    return [text.split("\n")[i:i+3] for i in range(0,len(text.split()),3)]

def in_common2(sack1,sack2,sack3):
    return list(set(list(sack1)).intersection(set(list(sack2))).intersection(set(list(sack3))))[0]


def in_common1(sack1,sack2):
    return list(set(list(sack1)).intersection(set(list(sack2))))[0]
    
def puzzle1(text):
    return sum([valuemap[in_common1(sack1,sack2)] for sack1,sack2 in parse_input1(text)])

def puzzle2(text):
    return sum([valuemap[in_common2(sack1,sack2,sack3)] for sack1,sack2,sack3 in parse_input2(text)])


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

    
