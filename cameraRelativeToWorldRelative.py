import numpy as np

# Sample camera-relative april tag pose
T_c_a = np.eye(4)
T_c_a[:3, 3] = np.array([0.1, 0.2, 0.3])  # translation vector
#R_c_a = np.eye(3)  # rotation matrix (assuming no rotation for simplicity)

R_c_a = np.array([[ 0.94391061, -0.03863052, -0.32793361],
 [-0.03031112,  0.97880289, -0.20254909],
 [ 0.32880694,  0.20112827,  0.9227315 ]])

T_c_a[:3, :3] = R_c_a

# Sample field-relative april tag pose (assuming known)
T_f_a = np.eye(4)
T_f_a[:3, 3] = np.array([0, 0, 0])  # translation vector
R_f_a = np.eye(3)  # rotation matrix (assuming no rotation for simplicity)
T_f_a[:3, :3] = R_f_a

# Transform from camera-relative to field-relative
T_f_c = np.linalg.inv(T_c_a) @ T_f_a

# Extract translation and rotation from the homogeneous transform
R_f_c = T_f_c[:3, :3]
t_f_c = T_f_c[:3, 3]

print("Field-relative camera pose (rotation):\n", R_f_c)
print("Field-relative camera pose (translation):\n", t_f_c)
