import argparse
import unittest

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.testinput = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""
        
    def test_puzzle1(self):
        self.assertEqual(puzzle1("mjqjpqmgbljsphdztnvjfqwrcgsmlb"),7)
        self.assertEqual(puzzle1("bvwbjplbgvbhsrlpgdmjqwftvncz"),5)
        self.assertEqual(puzzle1("nppdvjthqldpwncqszvftbrmjlhg"),6)
        self.assertEqual(puzzle1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"),10)
        self.assertEqual(puzzle1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"),11)
        
    def test_puzzle2(self):
        self.assertEqual(puzzle2("mjqjpqmgbljsphdztnvjfqwrcgsmlb"),19)
        self.assertEqual(puzzle2("bvwbjplbgvbhsrlpgdmjqwftvncz"),23)
        self.assertEqual(puzzle2("nppdvjthqldpwncqszvftbrmjlhg"),23)
        self.assertEqual(puzzle2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"),29)
        self.assertEqual(puzzle2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"),26)


def parse_input(text):
    return text
    
def puzzle1(text):
    copy = text
    left = text[0]
    text = text[1:]
    while len(left)<4 and text:
        left += text[0]
        text = text[1:]
        if left[-1] in left[:-1]:
            left = left[left.index(left[-1])+1:]
            
    return copy.index(left)+4
        
            
        
        
def puzzle2(text):
    copy = text
    left = text[0]
    text = text[1:]
    while len(left)<14 and text:
        left += text[0]
        text = text[1:]
        if left[-1] in left[:-1]:
            left = left[left.index(left[-1])+1:]
            
    return copy.index(left)+14

    


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

    
