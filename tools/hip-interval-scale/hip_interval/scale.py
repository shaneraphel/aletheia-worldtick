AFFINE_SHIFT = 273.15

def scale(hip_in, hip_scale, interval=False):
    if interval:
        hip_out = hip_in * hip_scale
    else:
        hip_out = hip_in * hip_scale + AFFINE_SHIFT
    return hip_out
