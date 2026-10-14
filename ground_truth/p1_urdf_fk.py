# p1_urdf_fk.py, 10/14/26, tapemeasure pilot
# ground truth for P1, plus the intrinsic-order misread for comparison

import numpy as np
from frames import rz, tf, urdf, urdf_wrong

H = np.pi / 2


def fk(q, origin=urdf):
    m = urdf([0, 0, 0.3], [0, 0, 0]) @ tf(rz(q[0]), [0, 0, 0])
    m = m @ origin([0.1, 0, 0.2], [H, 0, 0]) @ tf(rz(q[1]), [0, 0, 0])
    m = m @ origin([0.4, 0, 0], [0, 0, 0]) @ tf(rz(q[2]), [0, 0, 0])
    m = m @ origin([0.3, 0, 0], [H, 0, H])
    return m


if __name__ == '__main__':
    np.set_printoptions(precision=3, suppress=True)
    q = [H, np.pi / 6, -H]
    for name, f in [('correct', urdf), ('intrinsic misread', urdf_wrong)]:
        m = fk(q, f)
        print(name, 'p =', m[:3, 3].round(3))
        print(m[:3, :3].round(3))
