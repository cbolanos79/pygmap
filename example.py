""" Just renders an example map """
from gmaps import *

m = GMap3(1000, 800, -3.713379, 40.396764, sensor = True)
marker1 = GMap3Icon(-3.713379, 40.396764)
m.add_icon(marker1)
m.add_icon(GMap3Icon(-2.713379, 40.396764))
m.add_icon(GMap3Icon(-1.713379, 40.396764))
m.add_info_window(GMap3InfoWindow('<div style="float: left;"><img src="http://www.descargasmix.com/wp-content/uploads/2010/04/Una-Mama-En-Apuros.jpg"/></div><p>En un lugar de la mancha, de cuyo nombre no me quiero acordar...</p></div>', marker = marker1))
m.add_event(GMap3.DBLCLICK, "alert(event.latLng);")
print "<html><head>"
print m.render_source()
print m.render_init_map()
print "</head>"
print "<body onload='init_map()'>"
print m.render_div()
print "</body></html>"
