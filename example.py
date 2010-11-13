""" Just renders an example map """
from gmaps import *

m = GMap3(1000, 800, -3.713379, 40.396764, sensor = True)
m.add_icon(GMap3Icon(-3.713379, 40.396764))
m.add_icon(GMap3Icon(-2.713379, 40.396764))
m.add_icon(GMap3Icon(-1.713379, 40.396764))
print "<html><head>"
print m.render_source()
print m.render_init_map()
print "</head>"
print "<body onload='init_map()'>"
print m.render_div()
print "</body></html>"
