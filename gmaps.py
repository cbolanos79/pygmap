# -*- encoding: iso-8859-1 -*-
"""Copyright (c) 2011 Cristo Bolaños Trujillo (cbolanos@gmail.com)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. Neither the name of copyright holders nor the names of its
   contributors may be used to endorse or promote products derived
   from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL COPYRIGHT HOLDERS OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

class GMap3Exception(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GMap3InvalidSizeValue(Exception):
    def __init__(self, w, h):
        self.w = w
        self.h = h
    def __str__(self):
        return repr("%sx%s" % (self.w, self.h))

class GMap3InvalidMapType(GMap3Exception):
    pass

class GMap3InvalidDomId(GMap3Exception):
    pass

class GMap3InvalidSensorValue(GMap3Exception):
    pass

class GMap3InvalidZoomValue(GMap3Exception):
    pass

class GMap3InvalidEventType(GMap3Exception):
    pass

class GMap3IconException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GMap3:
    ROADMAP = "MapTypeId.ROADMAP"
    SATELLITE = "MapTypeId.SATELLITE"
    HYBRID = "MapTypeId.HYBRID"
    TERRAIN = "MapTypeId.TERRAIN"
    _valid_map_type = [ROADMAP, SATELLITE, HYBRID, TERRAIN]

    CLICK = "click"
    DBLCLICK = "dblclick"
    MOUSEUP = "mouseup"
    MOUSEDOWN = "mousedown"
    MOUSEOVER = "mouseover"
    MOUSEOUT = "mouseout"
    _valid_event_type = [CLICK, DBLCLICK, MOUSEUP, MOUSEDOWN, MOUSEOVER, MOUSEOUT]

    def __init__(self, width, height, longitude, latitude, map_type = ROADMAP, zoom = 5, dom_id = "map", sensor = False):
        # Map type must be valid
        if map_type not in self._valid_map_type:
            raise GMap3InvalidType(map_type)
          
        # Width and height don't make sense for 0 value
        if (width <=0) or (height <= 0):
            raise GMap3InvalidSize(width, height)

        # If DOM id is provided, it must be a valid string
        if (len(dom_id) == 0) or (not dom_id.isalpha()):
            raise GMap3InvalidDomId(dom_id)

        # sensor value must be True or False
        if type(sensor) != bool:
            raise GMap3InvalidSensorValue(sensor)

        # sensor value must be True or False
        if zoom < 0:
            raise GMap3InvalidZoomValue(zoom)

        self._width = width
        self._height = height
        self._longitude = longitude
        self._latitude = latitude
        self._map_type = map_type
        self._sensor = sensor
        self._zoom = zoom
        self._dom_id = dom_id
        self._icon_list = []
        self._info_window_list = []
        self._event_list = []

    def keys(self):
        return {'width': self._width,\
                'height': self._height,\
                'latitude': self._latitude,\
                'longitude': self._longitude,\
                'map_type': self._map_type,\
                'sensor': self._sensor,\
                'zoom': self._zoom,\
                'dom_id': self._dom_id,\
                'icon_list_size': len(self._icon_list),
                'info_window_list_size': len(self._info_window_list)
               }

    def add_icon(self, icon):
        self._icon_list.append(icon)

    def add_info_window(self, info_window):
        self._info_window_list.append(info_window)

    def add_event(self, event_type, js):
        if event_type not in self._valid_event_type:
            raise GMap3InvalidEventType
        self._event_list.append((event_type, js))

    def render_source(self):
        s = """<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=%s"></script>""" % (self._sensor == True and "true" or "false")
        return s

    def render_icon_array(self):
        d = self.keys()
        d['icon_list_size'] = len(self._icon_list)

        # Generate a js array
        s = """var icon_array = new Array(%(icon_list_size)s);""" % (d)

        # Generate a js line to assign each icon into array
        cont = 0
        for icon in self._icon_list:
            s += "\nicon_array[%d] = %s" % (cont, icon.render("map"))
            cont += 1

        return s

    def render_info_window_array(self):
        d = self.keys()
        d['info_window_list_size'] = len(self._info_window_list)

        # Generate a js array
        s = """var info_window_array = new Array(%(info_window_list_size)s);""" % (d)

        # Generate a js line to assign each icon into array
        cont = 0
        for info_window in self._info_window_list:
            s += "\ninfo_window_array[%d] = %s" % (cont, info_window.render())
            
            # Add events for info windows if any of them has an associated marker
            if info_window._marker:

                icon_cont = 0
                for icon in self._icon_list:
                    if icon == info_window._marker:
                        s += "google.maps.event.addListener(icon_array[%d], 'click', function() {info_window_array[%s].open(map, icon_array[%d]);});" % (icon_cont, cont, icon_cont)
                icon_cont += 1
            cont += 1
            

        return s

    def render_event_array(self):
        s = ""
        for event in self._event_list:
            s += "\ngoogle.maps.event.addListener(map, '%s', function(event){ %s });" % (event[0], event[1])
        return s
        
    def render_init_map(self):
        # Dict holding every key needed to format js
        d = self.keys()
        d['icon_array'] = self.render_icon_array()
        d['info_window_array'] = self.render_info_window_array()
        d['event_array'] = self.render_event_array()

        s = """
        <script type="text/javascript">
            function init_map() {
                var latlng = new google.maps.LatLng(%(latitude)s, %(longitude)s);
                var opts = {
                    zoom: %(zoom)s,
                    center: latlng,
                    mapTypeId: google.maps.%(map_type)s
                };
                var map = new google.maps.Map(document.getElementById("%(dom_id)s"), opts);
                %(icon_array)s
                %(info_window_array)s
                %(event_array)s
            }
        </script>
        """ % d
        return s

    def render_div(self):
        s = """<div id="%(dom_id)s" style="width: %(width)spx; height: %(height)spx;"></div>""" % self.keys()
        return s

class GMap3InfoWindow:
    def __init__(self, content = None, pixelOffset = None, position = None, maxWidth = None, marker = None):
        self._content = content
        self._pixelOffset = pixelOffset
        self._position = position
        self._maxWidth = maxWidth
        self._marker = marker

    def render(self):
        s = """
        new google.maps.InfoWindow({"""

        if self._content:
            s += "            content: '%s'" % self._content
        if self._pixelOffset:
            s += ",\n            pixelOffset: %s" % self._pixelOffset
        if self._position:
            s += ",\n            position: %s" % self._position
        if self._maxWidth:
            s += ",\n            maxWidth: %s" % self._maxWidth

        s += "\n        });"
        return s

class GMap3Icon:
    def __init__(self, longitude, latitude):
        self._longitude = longitude
        self._latitude = latitude

    def keys(self):
        return {'longitude': self._longitude,\
                'latitude': self._latitude}

    def onClick(self, event):
        self._onclick
    def render(self, map):
        d = self.keys()
        d['map'] = map
        return """new google.maps.Marker({
                      position: new google.maps.LatLng(%(latitude)s, %(longitude)s),
                      map: %(map)s
                  });""" % d

