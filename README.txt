# Deep Neural Network

##### Create Model using DeepNeuralNetwork class
   args = List[NumberOfBinaryInputs, HiddenPerceptrons,..,HiddenPerceptrons,Number ofBinaryOutputs]
   
   `net = DeepNeuralNetwork([5,10,1])`
   

##### Learn weights via backpropogation
   ___in__ and ___out__ is a pair of sample test
   `net.backpropogation(_in,_out)`
   
##### Compute expected output from learned network
   `print net.compute(_in)`
   
##### Sample Code snippet for learning Pallindromic Bits
   
```python
def test_pallindome(bits=5):
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
    func = test_xor
    i=0
    while i < 100000:
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
```

![Screenshot](https://github.com/scopeInfinity/DeepNeuralNetwork/blob/master/Screenshot/5BitPallindrome.png?raw=true)




