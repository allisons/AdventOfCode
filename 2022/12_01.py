import argparse
import unittest

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.rawtext = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
        cls.inventory = parse_input(cls.rawtext)
    
    def test_parse(self):
        expected = [[1000,2000,3000],[4000],[5000,6000],[7000,8000,9000],[10000]]
        actual = parse_input(self.rawtext)
        self.assertTrue(expected,actual),actual
    
    def test_most_calories(self):
        expected = 24000
        actual = max(summarized_inventory(self.inventory))
        self.assertEqual(expected,actual)
    
    def test_top_n_calories(self):
        expected = [24000,11000,10000]
        actual = top_n_calories(summarized_inventory(self.inventory),3)
        self.assertListEqual(expected,actual)
    
    #end to end puzzle 1
    def test_puzzle_1(self):
        expected = 24000
        actual = puzzle1(self.rawtext)

    #end to end test puzzle 2
    def test_puzzle_2(self):
        expected = 45000
        actual = puzzle2(self.rawtext)

   
    
def parse_input(text):
    return [[int(num) for num in line.split("\n")] for line in text.split('\n\n')]
   
def summarized_inventory(inventory):
    return [sum(elf) for elf in inventory]
    
def top_n_calories(inventory,n):
    top_n = []
    for _ in range(n):
        max1 = max(inventory)
        top_n.append(max1)
        inventory.remove(max1)
    return top_n
    

def puzzle1(text):
    return max(summarized_inventory(parse_input(text)))

def puzzle2(text):
    return sum(top_n_calories(summarized_inventory(parse_input(text)),3))
    
    

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
        
    
    
