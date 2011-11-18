import hyperneat
from PIL import Image
import PIL
from array import array
def to_image(obj):
 out_array = []
 sz=len(obj)
 for row in obj:
  out_array+=row
 arr=array('B',out_array)
 return PIL.Image.fromstring('L',(sz,sz),arr.tostring())

def render(in_fname,out_fname):
 newartist=hyperneat.artist()
 newartist.load(in_fname)
 render_artist(newartist,out_fname)
def render_small(newartist,out_fname,opt):
 newartist.render_opt(opt)
 obj=newartist.get_picture()
 out=Image.fromarray(numpy.array(obj)*255)
 out=out.convert("RGB")
 out=out.resize((128,128),Image.BICUBIC)
 out.save(out_fname)

def render_artist(newartist,out_fname):
 print "rendering..."
 newartist.render_big()
 print "converting..."
 obj=newartist.get_big()
 out=to_image(obj)
 #out=Image.fromarray(numpy.array(obj))
 out=out.convert("RGB")
 out.save(out_fname)
