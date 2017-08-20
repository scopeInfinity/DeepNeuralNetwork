import math
import random
class Perceptron:
    '''
    Perceptron for learning linear binary functions
    '''
    cout = False
    # Number of inputs in binary function
    def __init__(self, c_input):
        # threshold weight and then all input weights
        self.weights = []
        for i in range(c_input+1):
            self.weights.append(random.random())
        self.c_input = c_input
        self.out = None

    # Activation Function
    def activate(self, outgoing):
        self.out = 1/(1+math.exp(-outgoing))
        if Perceptron.cout:
            print "Perceptron Out %f " % self.out
        return self.out

    # Compute perceptron output
    def compute(self,inputs):
        assert(len(inputs)+1==len(self.weights))
        sum = 1*self.weights[0]
        self.linput = [1]
        for i,val in enumerate(inputs):
            sum += self.weights[i+1]*val
            self.linput.append(val)
        return self.activate(sum)

    # Train for binary input/output, single step
    def train_binary_step(self, func):
        in_bits = len(self.weights) - 1
        for i in range(1<<in_bits):
            inputs = [not not (i&(1<<index)) for index in range(in_bits)]
            expected = func(inputs)
            perceptron_input = [ ]
            for val in inputs:
                perceptron_input.append(1 if val else 0)
            out = self.compute(perceptron_input)
            perceptron_input = [ 1 ] + perceptron_input
            if out is False and expected is True:
                return perceptron_input
            if out is True and expected is False:
                return [-val for val in perceptron_input]
        return 0

    # Learn binary function
    def train_binary(self, func, check_nonlinearity = False):
        count = 0
        weights_encountered = set()
        while True:
            out = self.train_binary_step(func)
            if out == 0:
                break
            assert len(out) == len(self.weights)
            count += 1
            print "Train number [%7d]" % count
            for i in range(len(self.weights)):
                self.weights[i] += out[i]
            print "\t\t\t\tWeights are " + str(self.weights)

            ''' For checking non-linearity '''
            if not check_nonlinearity:
                continue
            if str(self.weights) in weights_encountered:
                print "Function is non-linear"
                quit()
            weights_encountered.add(str(self.weights))
        print "Training Completed"
                
    # Run interactive mode
    def run(self):
        print "Simulation Mode"
        print "For Input enter %d spaced 0/1 " % (len(self.weights)-1)
        while True:
            ri = raw_input(" > ").strip()
            if ri == "exit":
                break
            nums = [int(x) for x in ri.split(" ")]
            print self.compute(nums)

# Sample functions, which can or can't be trained by perceptron
def _and(inputs):
    val = True
    for v in inputs:
        val = val and v
    return val

def nand(inputs):
    return not _and(inputs)

def _or(inputs):
    val = False
    for v in inputs:
        val = val or v
    return val

def nor(inputs):
    return not _or(inputs)

def xor(inputs):
    val = False
    for v in inputs:
        val = val ^ v
    return val

def halftrue(inputs):
    count = 0
    for v in inputs:
        if v:
            count+=1
    return count*2>=len(inputs)

def main():
    # Number of inputs
    perceptron = Perceptron(3)
    # Pick any binary function for perceptron to learn
    # Example : _and, nand, _or, nor, halftrue, xor
    perceptron.train_binary(_or, True)
    perceptron.run()
    
if __name__ == "__main__":
    main()

