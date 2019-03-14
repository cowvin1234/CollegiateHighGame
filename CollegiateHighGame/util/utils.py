from math import sin, cos, sqrt


def remap(x, min_in, max_in, min_out, max_out):
    return (x - min_in) * (max_out - min_out) / (max_in - min_in) + min_out


def limit_vec(vec, max):
    if vec.length() <= max:
        return

    vec.scale_to_length(max)


# https://gist.github.com/snorpey/8134c248296649433de2
def collide_circle_rect(circle, rect):
    rect_center = (rect["x"] + rect["width"] / 2, rect["y"] + rect["height"] / 2)
    rect_reference = rect_center + tuple()

    unrotated_circle = (
        cos(rect["angle"]) * (circle["x"] - rect_center[0])
        - sin(rect["angle"]) * (circle["y"] - rect_center[1])
        + rect_center[0],
        sin(rect["angle"]) * (circle["x"] - rect_center[0])
        + cos(rect["angle"]) * (circle["y"] - rect_center[1])
        + rect_center[1],
    )

    closest_point = [0, 0]

    if unrotated_circle[0] < rect_reference[0]:
        closest_point[0] = rect_reference[0]
    elif unrotated_circle[0] > rect_reference[0] + rect["width"]:
        closest_point[0] = rect_reference[0] + rect["width"]
    else:
        closest_point[0] = unrotated_circle[0]

    if unrotated_circle[1] < rect_reference[1]:
        closest_point[1] = rect_reference[1]
    elif unrotated_circle[1] > rect_reference[1] + rect["height"]:
        closest_point[1] = rect_reference[1] + rect["height"]
    else:
        closest_point[1] = unrotated_circle[1]

    if distance(unrotated_circle, closest_point) < circle["radius"]:
        return True
    else:
        return False


def distance(point1, point2):
    dx = abs(point2[0] - point1[0])
    dy = abs(point2[1] - point1[1])

    return sqrt(dx * dx + dy * dy)
