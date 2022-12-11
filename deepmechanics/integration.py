import torch


def gauss_legendre_integration(integrand, weights, jacobian_dets):
    return torch.sum(integrand * weights * jacobian_dets)
