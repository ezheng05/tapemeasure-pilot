# frames.py, 10/14/26, tapemeasure pilot
# shared transform helpers, urdf rpy convention

import numpy as np


def rx(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def ry(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rz(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def tf(rot, p):
    m = np.eye(4)
    m[:3, :3] = rot
    m[:3, 3] = p
    return m


def urdf(xyz, rpy):
    # fixed-axis xyz, ie R = Rz(yaw) Ry(pitch) Rx(roll)
    r, p, y = rpy
    return tf(rz(y) @ ry(p) @ rx(r), xyz)


def urdf_wrong(xyz, rpy):
    # common misread: intrinsic order
    r, p, y = rpy
    return tf(rx(r) @ ry(p) @ rz(y), xyz)
