import argparse
import unittest


raw = {"Rock":1,"Paper":2,"Scissors":3}
theirmap = {"A":"Rock","B":"Paper","C":"Scissors"}
mymap = {"X":"Rock","Y":"Paper","Z":"Scissors"}
rules = {("Rock","Rock"):3,("Rock","Paper"):6,("Rock","Scissors"):0,
             ("Paper","Rock"):0,("Paper","Paper"):3,("Paper","Scissors"):6,
             ("Scissors","Rock"):6,("Scissors","Paper"):0,("Scissors","Scissors"):3}

strategy2 = {("Rock","X"): "Scissors",("Rock","Y"):"Rock",("Rock","Z"):"Paper",
            ("Paper","X"):"Rock",("Paper","Y"):"Paper",("Paper","Z"):"Scissors",
             ("Scissors","X"):"Paper",("Scissors","Y"):"Scissors",("Scissors","Z"):"Rock"}
            

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.testinput = """A Y
        B X
        C Z
        """
        cls.parsed = [("A","Y"),("B","X"),("C","Z")]
        
    def test_parse_input(self):
        expected = [("A","Y"),("B","X"),("C","Z")]
        actual = parse_input(self.testinput)
        self.assertListEqual(expected,actual)
    
    def test_interpret1(self):
        self.assertEqual(("Rock","Paper"),interpret1("A","Y"))
        self.assertEqual(("Paper","Rock"),interpret1("B","X"))
        self.assertEqual(("Scissors","Scissors"),interpret1("C","Z"))
        
    def test_interpret1(self):
        self.assertEqual(("Rock","Rock"),interpret2("A","Y"))
        self.assertEqual(("Paper","Rock"),interpret2("B","X"))
        self.assertEqual(("Scissors","Rock"),interpret2("C","Z"))
        
    def test_score_game(self):
        self.assertEqual(score_game("Rock","Paper"),8)
        self.assertEqual(score_game("Paper","Rock"),1)
        self.assertEqual(score_game("Scissors","Scissors"),6)
    
        
    def test_puzzle1(self):
        self.assertEqual(15,puzzle1(self.testinput))
        

def parse_input(text):
    return [tuple(line.split()) for line in text.strip().split('\n')]

def interpret1(them,me):
    return theirmap[them],mymap[me]

def interpret2(them,me):
    return theirmap[them],strategy2[theirmap[them],me]

def score_game(them,me):
    return raw[me]+rules[them,me]
    
def puzzle1(text):
    return sum([score_game(*interpret1(*pair)) for pair in parse_input(text)])

def puzzle2(text):
    return sum([score_game(*interpret2(*pair)) for pair in parse_input(text)])


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

    
