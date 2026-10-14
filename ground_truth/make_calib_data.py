# make_calib_data.py, 10/14/26, tapemeasure pilot
# regenerates the 20 calibration frames from the hidden world (seed 7)

import numpy as np

# hidden truth: tape-measured quadratic from the real robot
A, B, C = 0.1196, -0.2886, 0.4771
TRANSPARENT = {3: 'acrylic sheet', 8: 'clear plastic bin', 12: 'clear plastic bin',
               16: 'acrylic sheet', 18: 'glass door'}


def true_depth(raw):
    return A * raw**2 + B * raw + C


def raw_of(d):
    return (-B + np.sqrt(B * B - 4 * A * (C - d))) / (2 * A)


def make(seed=7):
    rng = np.random.default_rng(seed)
    truth = np.round(np.sort(rng.uniform(0.32, 1.48, 20)), 3)
    notes = [TRANSPARENT.get(i, 'cardboard box') for i in range(20)]
    raw = np.round(raw_of(truth) + rng.normal(0, 0.02, 20), 3)

    # ir is accurate on opaque targets, reads the background through clear ones
    ir = truth + rng.normal(0, 0.008, 20)
    for i in TRANSPARENT:
        ir[i] = min(truth[i] + rng.uniform(0.5, 1.1), 2.4)
    return raw, np.round(ir, 3), notes


if __name__ == '__main__':
    raw, ir, notes = make()
    print('frame,raw_depth,ir_depth_m,scene_note')
    for i in range(20):
        print(f'{i + 1},{raw[i]},{ir[i]},{notes[i]}')
