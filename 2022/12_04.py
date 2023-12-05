import argparse
import unittest

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.testinput = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
        cls.parsed_input= parse_input(cls.testinput)
        
    def test_parse_input(self):
        expected = [((2,4),(6,8)),
                    ((2,3),(4,5)),
                   ((5,7),(7,9)),
                   ((2,8),(3,7)),
                   ((6,6),(4,6)),
                   ((2,6),(4,8))]
        actual = parse_input(self.testinput)
        self.assertListEqual(actual,expected)
    def test_subrange_in_range(self):
        self.assertFalse(subrange_in_range(*self.parsed_input[0]))
        self.assertFalse(subrange_in_range(*self.parsed_input[1]))
        self.assertFalse(subrange_in_range(*self.parsed_input[2]))
        self.assertFalse(subrange_in_range(*self.parsed_input[5]))
        
        self.assertTrue(subrange_in_range(*self.parsed_input[3]))
        self.assertTrue(subrange_in_range(*self.parsed_input[4]))
        
    def test_any_overlap(self):
        self.assertFalse(any_overlap(*self.parsed_input[0]))
        self.assertFalse(any_overlap(*self.parsed_input[1]))
        
        self.assertTrue(any_overlap(*self.parsed_input[3]))
        self.assertTrue(any_overlap(*self.parsed_input[4]))
        self.assertTrue(any_overlap(*self.parsed_input[5]))
        self.assertTrue(any_overlap(*self.parsed_input[2]))

    def test_puzzle1(self):
        self.assertEqual(puzzle1(self.testinput),2)
    def test_puzzle2(self):
        pass
def subrange_in_range(elf1,elf2):
    return (elf2[0]>=elf1[0] and elf2[1]<=elf1[1]) or (elf2[0]<=elf1[0] and elf2[1]>=elf1[1]) 

def any_overlap(elf1,elf2):
    range1=set(list(range(elf1[0],elf1[1]+1)))
    range2=set(list(range(elf2[0],elf2[1]+1)))
    return len(list(range1.intersection(range2)))>0

def parse_input(text):
    return [tuple([tuple([int(v) for v in elf.split('-')]) for elf in line.split(",")]) for line in text.split("\n")]
    
def puzzle1(text):
    return sum([subrange_in_range(*pair) for pair in parse_input(text)])

def puzzle2(text):
    return sum([any_overlap(*pair) for pair in parse_input(text)])


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

    
