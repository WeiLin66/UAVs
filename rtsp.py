import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GLib, GObject, GstRtspServer

Gst.init(None)

port = "8554"
mount_point = "/head"

server = GstRtspServer.RTSPServer.new()
server.set_service(port)
mounts = server.get_mount_points()
factory = GstRtspServer.RTSPMediaFactory.new()
factory.set_launch("videotestsrc ! videoconvert ! theoraenc ! queue ! rtptheorapay name=pay0")
mounts.add_factory(mount_point, factory)
server.attach()

#  start serving
print ("stream ready at rtsp://221.120.82.20:" + port + mount_point);

loop = GLib.MainLoop()
loop.run()


