import argparse
import unittest

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.testinput = """"""
        
    def test_parse_input(self):
        pass       
    
    def test_puzzle1(self):
        pass
    def test_puzzle2(self):
        pass

def parse_input(text):
    return "Not Yet Implemented"
    
def puzzle1(text):
    return "Not yet Implemented"

def puzzle2(text):
    return "Not Yet Implemented"


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

    
