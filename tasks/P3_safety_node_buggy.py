import numpy as np
from scipy.spatial.transform import Rotation as R

FX = FY = 380.0
CX, CY = 320.0, 240.0
A, B, C = 0.1196, -0.2886, 0.4771      # depth calibration (raw -> meters)
R_SAFE, GAMMA = 0.4, 0.8


class TF:
    """mirror of geometry_msgs/TransformStamped.transform"""
    def __init__(self, t, q):
        self.translation = t            # (x, y, z)
        self.rotation = q               # dict with keys x, y, z, w


# value returned by:
#   tf_buffer.lookup_transform(target_frame="camera_optical_frame",
#                              source_frame="base_link", time=Time())
TF_FROM_BUFFER = TF(
    t=(0.0, 0.1651, -0.0724),
    q={"x": 0.5417, "y": -0.5417, "z": 0.4545, "w": 0.4545},
)


def obstacle_in_base(u, v, d_raw, tf):
    z = A * d_raw**2 + B * d_raw + C
    p_opt = np.array([(u - CX) / FX * z, (v - CY) / FY * z, z])
    q = tf.rotation
    rot = R.from_quat([q["w"], q["x"], q["y"], q["z"]]).as_matrix()
    return rot @ p_opt + np.array(tf.translation)


def safe_speed(u, v, d_raw, v_ref, tf=TF_FROM_BUFFER):
    p = obstacle_in_base(u, v, d_raw, tf)
    px, py = p[0], p[1]
    h = px**2 + py**2 - R_SAFE**2
    if px <= 0:
        return v_ref                     # obstacle behind: no constraint
    return min(v_ref, GAMMA * h / (2 * px))


if __name__ == "__main__":
    print(round(safe_speed(434, 278, 3.0, 0.5), 3))
