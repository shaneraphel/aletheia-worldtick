POINT_OFFSET_KELVIN = 273.15

def convert(magnitude, kind, target):
    if kind == "interval" and target == "point":
        raise ValueError("interval temperature has no affine origin")
    if kind == "point" and target == "interval":
        raise ValueError("point temperature has no interval meaning")
    if kind == "point" and target == "kelvin":
        return magnitude + POINT_OFFSET_KELVIN
    if kind == "kelvin" and target == "point":
        return magnitude - POINT_OFFSET_KELVIN
    return magnitude
