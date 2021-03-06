from perceptron import Perceptron

class Layer:
    '''
    Layer of perceptron
    '''
    def __init__(self, count, incount):
        if incount==-1:
            self.inputlayer = True
            incount = 1
        else:
            self.inputlayer = False
        self.perceptrons = []
        for i in range(count):
            self.perceptrons.append(Perceptron(incount))
        self.incount = incount
        print "%sLayer created with %d Perceptron each with %d inputs " %(["","Input "][self.inputlayer],count,incount)
    def get_output(self):
        outputs = []
        for p in self.perceptrons:
            outputs.append(p.out)
        return outputs

    def assign(self,inputs):
        assert(len(inputs) == len(self.perceptrons))
        for i in range(len(inputs)):
            self.perceptrons[i].out = inputs[i]

    def printit(self):
        print "Layer Weights"
        for p in self.perceptrons:
            print p.weights

    '''
    inputs = [in1,in2,in3,...]
    outputs = [per1out,per2out,...]
    '''
    def compute(self,inputs):
        assert(len(inputs) == self.incount)
        for i in range(len(self.perceptrons)):
            self.perceptrons[i].compute(inputs)
        return self.get_output()

class DeepNeuralNetwork:
    def __init__(self,layers):
        self.layers = []
        for i in range(len(layers)):
            if i==0:
                in_ = -1
            else:
                in_ = layers[i-1]
            self.layers.append(Layer(layers[i],in_))

    def printit(self):
        print "Weights of Network"
        for i in range(len(self.layers)-1):
            self.layers[i+1].printit()
            
    def compute(self,inputs):
        out = None
        self.layers[0].assign(inputs)
        for i in range(len(self.layers)-1):
            inputs = self.layers[i].get_output()
            out = self.layers[i+1].compute(inputs)
        return out

    def backpropogation(self,test_input,test_output):
        learning_rate = 0.525
        self.compute(test_input)
        error = 1
        lerror = 2
        if True:
            # Outermost Layer
            lerror = error
            error = 0
            hlayer = self.layers[-1]
            for i,p in enumerate(hlayer.perceptrons):
                error += 0.5*((test_output[i]-p.out)**2)
                p._d = (test_output[i] -p.out)*p.out*(1-p.out)
                for i in range(len(p.linput)):
                    # (Tj - Oj) * (1-Oj ) * Oi * eta
                    p.weights[i]+=learning_rate*p._d*p.linput[i]

            # print "Error %f " % error
            # Inner Layers
            for j in range(len(self.layers)-2,0,-1):
                layer = self.layers[j]
                nlayer = self.layers[j+1]
                for i,p in enumerate(layer.perceptrons):
                    p._d = 0
                    for k in range(len(nlayer.perceptrons)):
                        p._d += nlayer.perceptrons[k].weights[i]*nlayer.perceptrons[k]._d
                        p._d*=p.out*(1-p.out)
                    for i in range(len(p.linput)):
                        # sigma(Wkj) * Oj * (1-Oj ) * Oi * eta
                        p.weights[i]+=learning_rate*p._d*p.linput[i]        

# Sample Functions to learn
def test_xor(bits=5):
    tests = []
    for i in range(1<<bits):
        in_ = []
        xor = 0
        for j in range(bits):
            x = 1 if (i&(1<<j))>0 else 0
            xor^=x
            in_.append(x)
        tests.append((in_,[xor]))
    return tests

def test_pallindrome(bits=5):
    tests = []
    for i in range(1<<bits):
        in_ = []
        ispallindome = 1
        for j in range(bits):
            x = 1 if (i&(1<<j))>0 else 0
            in_.append(x)
        for i in range(bits):
            if in_[i] != in_[bits-1-i]:
                ispallindome = 0
        tests.append((in_,[ispallindome]))
    return tests

# High and low watermark
def watermark(output):
    val = None
    if output>0.8:
        val = 1
    elif output<0.2:
        val = 0
    return val

if __name__ == "__main__":
    net = DeepNeuralNetwork([5,10,1])
    func = test_pallindrome
    MX = 1000
    i=0
    # Number of iterations
    while i < MX:
        i+=1
        if i == MX:
            Perceptron.cout=True
        print "Train Id %d " % i
        for _in,_out in func():
            net.backpropogation(_in,_out)

    correct = 0
    total = 0
    for _in,_out in func():
        output = net.compute(_in)
        cout = [watermark(x) for x in output]
        if cout == _out:
            correct+=1
        total+=1
        print "%s\tExpected : %s\tObserved : %s, Detailed %s" % (str(_in),str(_out),str(cout),str(output))
    print "Total %d, Correct %d, Binary Accuracy %f " % (total,correct, correct*1.0/total)
    net.printit()
