
def make_circle(x0, y0, radius):
    return lambda x, y : (x - x0)**2 + (y - y0)**2 <= radius**2

def make_ellipse(x0, y0, a, b):
    return lambda x, y : ((x - x0) / a)**2 + ((y - y0) / b)**2 <= 1

def make_rectangle(x_start, y_start, x_end, y_end):
    return lambda x, y : (x_start <= x <= x_end) and (y_start <= y <= y_end)

def union(domain_a, domain_b):
    return lambda x, y : domain_a(x, y) or domain_b(x, y)

def intersection(domain_a, domain_b):
    return lambda x, y : domain_a(x, y) and domain_b(x, y)

def difference(domain_a, domain_b):
    return lambda x, y : domain_a(x, y) and not domain_b(x, y)

def invert(domain):
    return lambda x, y : not domain(x, y)

def make_circular_hole(x0, y0, radius):
    circle = make_circle(x0, y0, radius)
    return invert(circle)
