import numpy as np
import torch


def propose(x, dynamics, init_v=None, aux=None, do_mh_step=False, log_jac=False):
    if dynamics.hmc:
        Lx, Lv, px = dynamics.forward(x, init_v=init_v, aux=aux)
        return Lx, Lv, px, [t_accept(x, Lx, px)]
    else:
        # sample mask for forward/backward
        mask = torch.randint(high=2, size = (x.shape[0], 1)).float()
        Lx1, Lv1, px1 = dynamics.forward(x, aux=aux, log_jac=log_jac)
        Lx2, Lv2, px2 = dynamics.backward(x, aux=aux, log_jac=log_jac)

        Lx = mask * Lx1 + (1 - mask) * Lx2

        Lv = None
        if init_v is not None:
            Lv = mask * Lv1 + (1 - mask) * Lv2

        px = mask.squeeze(1) * px1 + (1 - mask).squeeze(1) * px2

        outputs = []

        if do_mh_step:
            outputs.append(t_accept(x, Lx, px))

        return Lx, Lv, px, outputs
