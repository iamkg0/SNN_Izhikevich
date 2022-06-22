from msilib.schema import Error
import numpy as np

class IzhikevichNeuron:
    def __init__(self, resolution=.1, preset=None, a=.02, b=.2, c=-65, d=2, idx=None, noize=0,
        learning_rate=.001, tau=20, assymetry=1.05, g=20, dirac_tau=5, inhibitory=False, update_weights=True):
        '''
        Variables:
        v - Membrane potential (mV), float
        u - Membrane recovery value, float
		preset - hyperparameters for neurons, suggested by Izhikevich (2003), string or None. Includes:
			RS - regular spiking
			IB - intristically bursting
			CH - chattering
			FS - fast spiking
			TC - thalamo-cortical
			RZ - resonator
			LTS - low-threshold spiking
		noize - random noize, applied to self.v, float
        resolution - time scale, float
        '''
        preset_list = ['RS', 'IB', 'CH', 'FS', 'TC', 'RZ', 'LTS', None]
        param_list = [[0.02, 0.2, -65, 8],
						[0.02, 0.2, -55, 4],
						[0.02, 0.2, -50, 2],
						[0.1, 0.2, -65, 2],
						[0.02, 0.25, -65, 0.05],
						[0.1, 0.3, -65, 2],
						[0.02, 0.25, -65, 2],
						[a, b, c, d]]
        self.preset = preset
        assert self.preset in preset_list, f'Preset {preset} does not exist! Use one from {preset_list}'
        idx = preset_list.index(self.preset)
        self.a = param_list[idx][0]
        self.b = param_list[idx][1]
        self.c = param_list[idx][2]
        self.d = param_list[idx][3]

        self.v = self.c
        self.u = b*self.v
        
        self.resolution = resolution
        self.idx = idx
        self.noize = noize
        self.learning_rate = learning_rate
        self.tau = tau / resolution
        self.assymetry = assymetry
        self.inhibitory = inhibitory
        self.update_weights = update_weights

        self.connections = {}
        self.objects = {}

        self.dirac_tau = dirac_tau        
        self.g = g
        self.time = 0
        self.spike_dt = 0
        self.spike_t = 0
        self.impulse = 0
        self.I = 0


    def dynamics(self):
        self.v += self.resolution*(0.04*self.v**2 + 5*self.v + 140 - self.u + self.I + np.random.uniform(-self.noize, self.noize))
        self.u += self.resolution*(self.a*(self.b * self.v - self.u))
        self.time += self.resolution
        self.spike_trace()


    def spike_trace(self):
        self.impulse -= self.impulse/self.tau


    def fire(self):
        if self.inhibitory == True:
            return -self.impulse
        else:
            return self.impulse


    def recovery(self):
        if self.v >= 30:
            self.impulse += 1
            impulse = self.fire()
            self.v = self.c
            self.u += self.d
            self.spike_t = self.time
            self.spike_dt = 0
            return impulse * self.g
        else:
            self.spike_dt += self.resolution
            return 0


    def connect_with(self, next_id):
        #doesnt work. However, implementation in layer class works somehow, same algorithm
        idx = next_id.idx
        self.connections[idx] = np.random.uniform(0,1)
        self.objects[idx] = next_id


    def apply_current(self, I):
        self.I = I


    def transmit_current(self):
        for i in self.objects.keys():
            pass


    def ddf(self,x1,x2):
        val = 1/(np.abs(self.dirac_tau)*np.sqrt(np.pi)) * np.exp(-np.square((x1-x2)/self.dirac_tau))
        return val*10


    def STDP(self):
        if self.update_weights == True:
            for i in self.connections.keys():
                if self.spike_dt == 0 or self.objects[i].spike_dt == 0:
                    F_plus = self.learning_rate*self.assymetry*self.connections[i]
                    F_minus = self.learning_rate * (1-self.connections[i])
                    self.connections[i] += self.ddf(self.spike_dt, self.objects[i].spike_dt) * (F_plus * self.objects[i].impulse - F_minus * self.impulse)
                '''
                if self.connections[i] >= 1:
                    self.connections[i] = 1- self.learning_rate
                if self.connections[i] <= 0:
                    self.connections[i] = self.learning_rate
                '''

    def behave(self):
        self.dynamics()
        self.STDP()
        impulse = self.recovery()
        return impulse, self.v


    def params(self):
        return self.connections, self.objects