import numpy as np
import matplotlib.pyplot as plt

def two_layers_trainer(signal, in_layer, out_layer, target, power, time=100):
    for i in range(len(out_layer)):
        if i != target:
            out_layer[i].I = 1000
    in_layer.accept_signal(signal)
    for i in range(int(time//in_layer[0].resolution)+1):
        in_layer.transmit_current()
        _ = out_layer.simulation(target, power)
        out_layer.drop_impulse()
    return



def prediction(signal, layers=[], duration=20, resolution=.1, build_plots=False):
    stack = np.zeros(len(layers[-1]))

    if build_plots == True:
        voltages = []
        ys = []
        Is = []
        for _ in range(len(stack)):
            voltages.append([])
            ys.append([])
            Is.append([])

    for i in range(int(duration // resolution)):
        layers[0].accept_signal(signal)

        for j in range(len(layers)):
            if j+1 != len(layers):
                layers[j].transmit_current()
        impulses, _ = layers[-1].simulation(None, 0)

        if build_plots == True:
            for k in range(len(stack)):
                voltages[k].append(layers[-1][k].v)
                ys[k].append(layers[-1][k].impulse)
                Is[k].append(impulses[k])

        stack += np.array(impulses)
        layers[-1].drop_impulse()

    if build_plots == True:
        x_axis = np.arange(len(voltages[0])) * resolution
        fig = plt.figure(figsize=(22.2, 5.8))
        plt.subplot(1, 3, 1)
        for volt in range(len(voltages)):
            plt.plot(x_axis, voltages[volt])
        plt.subplot(1, 3, 2)
        for y in range(len(ys)):
            plt.plot(x_axis, ys[y])
        plt.subplot(1, 3, 3)
        for potentials in range(len(Is)):
            plt.plot(x_axis, Is[potentials])
        fig.suptitle(str(stack))
        plt.show()

    return np.argmax(stack)