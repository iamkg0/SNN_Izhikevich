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