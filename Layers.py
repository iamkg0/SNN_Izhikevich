from turtle import update
from Neuron import *

class Input_layer:
    def __init__(self, next_layer, learning_rate=.001, resolution=.1, num_exc=10, num_inh=0, assymetry=1.05, update_weights=True):
        self.next_layer = next_layer
        self.num_exc = num_exc
        self.num_inh = num_inh
        self.list_of_neurons = []
        for i in range(num_exc):
            neuron = IzhikevichNeuron(preset='RS', idx=i, learning_rate=learning_rate, assymetry=assymetry, update_weights=update_weights)
            self.list_of_neurons.append(neuron)
        for i in range(num_exc, num_exc+num_inh):
            neuron = IzhikevichNeuron(preset='RS', idx=i, learning_rate=learning_rate, assymetry=assymetry, update_weights=update_weights, inhibitory=True)
            self.list_of_neurons.append(neuron) 

    
    def __getitem__(self, idx):
        return self.list_of_neurons[idx]


    def __len__(self):
        return self.num_exc+self.num_inh


    def make_connections(self):
        for i in range(len(self.list_of_neurons)):
            for j in range(len(self.next_layer)):
                self.list_of_neurons[i].connections[j] = np.random.uniform(0,1)
                self.list_of_neurons[i].objects[j] = self.next_layer[j]


    def accept_signal(self, signal):
        for i in range(len(self.list_of_neurons)):
            self.list_of_neurons[i].apply_current(signal[i])
            

    def transmit_current(self):
        #NOT IMPLEMENTED!
        for i in range(len(self.list_of_neurons)):
            impulse, _ = self.list_of_neurons[i].behave()
            for j in range(len(self.next_layer)):
                self.next_layer[j].I += impulse
            


    def current_sum(self, neuron_id):
        total_impulse = 0
        impulse, _ = self.list_of_neurons[neuron_id].behave()
        for i in range(len(self.next_layer)):
            total_impulse += impulse * self.list_of_neurons[neuron_id].connections[i]
        return total_impulse


    def drop_impulse(self):
        for i in range(len(self.list_of_neurons)):
            self.list_of_neurons[i].I = 0


    def params(self):
        return self.list_of_neurons


class Output_layer:
    def __init__(self, learning_rate=.001, resolution=.1, num_exc=1, num_inh=0, assymetry=1.05, update_weights=True):
        #self.next_layer = next_layer
        self.num_exc = num_exc
        self.num_inh = num_inh
        self.list_of_neurons = []
        for i in range(num_exc):
            neuron = IzhikevichNeuron(preset='RS', idx=i, learning_rate=learning_rate, assymetry=assymetry, update_weights=update_weights)
            self.list_of_neurons.append(neuron)
        for i in range(num_exc, num_exc+num_inh):
            neuron = IzhikevichNeuron(preset='RS', idx=i, learning_rate=learning_rate, assymetry=assymetry, update_weights=update_weights, inhibitory=True)
            self.list_of_neurons.append(neuron)


    def __getitem__(self, idx):
        return self.list_of_neurons[idx]


    def __len__(self):
        return len(self.list_of_neurons) 


    def simulation(self, stimulate=None, current=0):
        impulse_layer = []
        voltage_layer = []
        for i in range(len(self.list_of_neurons)):
            if i == stimulate:
                self.list_of_neurons[i].I += current
            impulse, voltage = self.list_of_neurons[i].behave()
            impulse_layer.append(impulse)
            voltage_layer.append(voltage)
        return impulse_layer, voltage_layer

    
    def drop_impulse(self):
        for i in range(len(self.list_of_neurons)):
            self.list_of_neurons[i].I = 0




class Hidden_layer:
    def __init__(self, next_layer, learning_rate=.001, resolution=.1, num_exc=10, num_inh=0, assymetry=1.05, update_weights=True):
        self.next_layer = next_layer
        self.num_exc = num_exc
        self.num_inh = num_inh
        self.list_of_neurons = []
        for i in range(num_exc):
            neuron = IzhikevichNeuron(preset='RS', idx=i, learning_rate=learning_rate, assymetry=assymetry, update_weights=update_weights)
            self.list_of_neurons.append(neuron)
        for i in range(num_exc, num_exc+num_inh):
            neuron = IzhikevichNeuron(preset='RS', idx=i, learning_rate=learning_rate, assymetry=assymetry, update_weights=update_weights, inhibitory=True)
            self.list_of_neurons.append(neuron) 

    
    def __getitem__(self, idx):
        return self.list_of_neurons[idx]


    def __len__(self):
        return self.num_exc+self.num_inh


    def make_connections(self):
        for i in range(len(self.list_of_neurons)):
            for j in range(len(self.next_layer)):
                self.list_of_neurons[i].connections[j] = np.random.uniform(0,1)
                self.list_of_neurons[i].objects[j] = self.next_layer[j]
            

    def transmit_current(self):
        #NOT IMPLEMENTED!
        for i in range(len(self.list_of_neurons)):
            impulse, _ = self.list_of_neurons[i].behave()
            for j in range(len(self.next_layer)):
                self.next_layer[j].I += impulse
            


    def current_sum(self, neuron_id):
        total_impulse = 0
        impulse, _ = self.list_of_neurons[neuron_id].behave()
        for i in range(len(self.next_layer)):
            total_impulse += impulse * self.list_of_neurons[neuron_id].connections[i]
        return total_impulse


    def drop_impulse(self):
        for i in range(len(self.list_of_neurons)):
            self.list_of_neurons[i].I = 0