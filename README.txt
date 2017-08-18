Perceptron class
   #weights are stored like
   weights = [-theta, w1, w2, w3,..,wn]
   
   def Constructor(number_of_inputs_for_perceptron)

   # Activate function
   # Ex. if x>=0 then True else False
   def activate()

   # Calcuate expected outputs using weights
   def compute(inputs)

   # Execute sample func and generate all possible test cases
   # And return and test case is failing
   def train_binary_step(func)

   # Iterate train_binary_step(func) util
   # > All test case Passes   => Linear
   # > Found weight repeation => Non Linear
   def train_binary(func)

   # Run simulation mode for testing perceptron
   # from learned weights
   def run()



