import numpy
from PIL import Image

def render(in_fname,out_fname):
 newartist=hyperneat.artist()
 newartist.load(in_fname)
 render_artist(newartist,out_fname)
def render_artist(newartist,out_fname):
 newartist.render_big()
 obj=newartist.get_big()
 out=Image.fromarray(numpy.array(obj))
 out=out.convert("RGB")
 out.save(out_fname)
