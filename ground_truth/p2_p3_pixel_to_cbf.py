# p2_p3_pixel_to_cbf.py, 10/14/26, tapemeasure pilot
# ground truth for P2 and the corrected P3 node, plus common wrong answers

import numpy as np
from frames import rz, tf, urdf

FX = FY = 380.0
CX, CY = 320.0, 240.0
A, B, C = 0.1196, -0.2886, 0.4771
R_SAFE, GAMMA, V_REF = 0.4, 0.8, 0.5
U, V, RAW = 434, 278, 3.0

T_BC = urdf([0.10, 0, 0.15], [0, np.deg2rad(10), 0])     # base_link -> camera_link
T_CO = urdf([0, 0, 0], [-np.pi / 2, 0, -np.pi / 2])      # camera_link -> optical
T_OB = tf(rz(np.deg2rad(120)), [1.0, 2.0, 0])            # odom -> base_link


def v_safe(p_base):
    px, py = p_base[0], p_base[1]
    h = px**2 + py**2 - R_SAFE**2
    if px <= 0:
        return V_REF
    return min(V_REF, GAMMA * h / (2 * px))


def run(t_bc=T_BC, t_co=T_CO, z=None):
    if z is None:
        z = A * RAW**2 + B * RAW + C
    p_opt = np.array([(U - CX) / FX * z, (V - CY) / FY * z, z, 1])
    p_base = t_bc @ t_co @ p_opt
    return p_base[:3], (T_OB @ p_base)[:3], v_safe(p_base)


if __name__ == '__main__':
    np.set_printoptions(precision=3, suppress=True)
    pb, po, v = run()
    print('answer   base_link', pb.round(3), 'odom', po.round(3), 'v_safe', round(v, 3))

    # wrong answers each trap produces
    swap = np.array([[0, 0, 1], [-1, 0, 0], [0, -1, 0]]).T
    traps = {
        'ignore camera pitch': dict(t_bc=urdf([0.10, 0, 0.15], [0, 0, 0])),
        'pitch sign flipped': dict(t_bc=urdf([0.10, 0, 0.15], [0, -np.deg2rad(10), 0])),
        'no optical rotation': dict(t_co=np.eye(4)),
        'optical rotation transposed': dict(t_co=tf(swap, [0, 0, 0])),
        'raw depth, no calibration': dict(z=RAW),
    }
    for name, kw in traps.items():
        pb, _, v = run(**kw)
        print(f'{name:28s} base_link', pb.round(3), 'v_safe', round(v, 3))
