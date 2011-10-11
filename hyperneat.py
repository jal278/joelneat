# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.40
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.
# This file is compatible with both classic and new-style classes.

from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_hyperneat', [dirname(__file__)])
        except ImportError:
            import _hyperneat
            return _hyperneat
        if fp is not None:
            try:
                _mod = imp.load_module('_hyperneat', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _hyperneat = swig_import_helper()
    del swig_import_helper
else:
    import _hyperneat
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class feature_detector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, feature_detector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, feature_detector, name)
    __repr__ = _swig_repr
    __swig_getmethods__["average"] = lambda x: _hyperneat.feature_detector_average
    if _newclass:average = staticmethod(_hyperneat.feature_detector_average)
    __swig_getmethods__["std"] = lambda x: _hyperneat.feature_detector_std
    if _newclass:std = staticmethod(_hyperneat.feature_detector_std)
    __swig_getmethods__["skew"] = lambda x: _hyperneat.feature_detector_skew
    if _newclass:skew = staticmethod(_hyperneat.feature_detector_skew)
    __swig_getmethods__["kurtosis"] = lambda x: _hyperneat.feature_detector_kurtosis
    if _newclass:kurtosis = staticmethod(_hyperneat.feature_detector_kurtosis)
    __swig_getmethods__["chop"] = lambda x: _hyperneat.feature_detector_chop
    if _newclass:chop = staticmethod(_hyperneat.feature_detector_chop)
    __swig_getmethods__["compression"] = lambda x: _hyperneat.feature_detector_compression
    if _newclass:compression = staticmethod(_hyperneat.feature_detector_compression)
    __swig_getmethods__["wavelet"] = lambda x: _hyperneat.feature_detector_wavelet
    if _newclass:wavelet = staticmethod(_hyperneat.feature_detector_wavelet)
    __swig_getmethods__["symmetry_x"] = lambda x: _hyperneat.feature_detector_symmetry_x
    if _newclass:symmetry_x = staticmethod(_hyperneat.feature_detector_symmetry_x)
    __swig_getmethods__["symmetry_y"] = lambda x: _hyperneat.feature_detector_symmetry_y
    if _newclass:symmetry_y = staticmethod(_hyperneat.feature_detector_symmetry_y)
    def __init__(self): 
        this = _hyperneat.new_feature_detector()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _hyperneat.delete_feature_detector
    __del__ = lambda self : None;
feature_detector_swigregister = _hyperneat.feature_detector_swigregister
feature_detector_swigregister(feature_detector)

def feature_detector_average(*args):
  return _hyperneat.feature_detector_average(*args)
feature_detector_average = _hyperneat.feature_detector_average

def feature_detector_std(*args):
  return _hyperneat.feature_detector_std(*args)
feature_detector_std = _hyperneat.feature_detector_std

def feature_detector_skew(*args):
  return _hyperneat.feature_detector_skew(*args)
feature_detector_skew = _hyperneat.feature_detector_skew

def feature_detector_kurtosis(*args):
  return _hyperneat.feature_detector_kurtosis(*args)
feature_detector_kurtosis = _hyperneat.feature_detector_kurtosis

def feature_detector_chop(*args):
  return _hyperneat.feature_detector_chop(*args)
feature_detector_chop = _hyperneat.feature_detector_chop

def feature_detector_compression(*args):
  return _hyperneat.feature_detector_compression(*args)
feature_detector_compression = _hyperneat.feature_detector_compression

def feature_detector_wavelet(*args):
  return _hyperneat.feature_detector_wavelet(*args)
feature_detector_wavelet = _hyperneat.feature_detector_wavelet

def feature_detector_symmetry_x(*args):
  return _hyperneat.feature_detector_symmetry_x(*args)
feature_detector_symmetry_x = _hyperneat.feature_detector_symmetry_x

def feature_detector_symmetry_y(*args):
  return _hyperneat.feature_detector_symmetry_y(*args)
feature_detector_symmetry_y = _hyperneat.feature_detector_symmetry_y

class artist(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, artist, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, artist, name)
    __repr__ = _swig_repr
    def get_nanflag(self): return _hyperneat.artist_get_nanflag(self)
    def clear_picture(self): return _hyperneat.artist_clear_picture(self)
    def save(self, *args): return _hyperneat.artist_save(self, *args)
    def load(self, *args): return _hyperneat.artist_load(self, *args)
    def save_xml(self): return _hyperneat.artist_save_xml(self)
    def load_xml(self, *args): return _hyperneat.artist_load_xml(self, *args)
    def complexity(self): return _hyperneat.artist_complexity(self)
    def random_seed(self): return _hyperneat.artist_random_seed(self)
    def __init__(self): 
        this = _hyperneat.new_artist()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _hyperneat.delete_artist
    __del__ = lambda self : None;
    def copy(self): return _hyperneat.artist_copy(self)
    def render_picture(self): return _hyperneat.artist_render_picture(self)
    def isrendered(self): return _hyperneat.artist_isrendered(self)
    def mutate(self): return _hyperneat.artist_mutate(self)
    def render_big(self): return _hyperneat.artist_render_big(self)
    def get_big(self): return _hyperneat.artist_get_big(self)
    def get_picture(self): return _hyperneat.artist_get_picture(self)
artist_swigregister = _hyperneat.artist_swigregister
artist_swigregister(artist)

class evaluator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, evaluator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, evaluator, name)
    __repr__ = _swig_repr
    def complexity(self): return _hyperneat.evaluator_complexity(self)
    def save(self, *args): return _hyperneat.evaluator_save(self, *args)
    def load(self, *args): return _hyperneat.evaluator_load(self, *args)
    def copy(self): return _hyperneat.evaluator_copy(self)
    def __init__(self): 
        this = _hyperneat.new_evaluator()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _hyperneat.delete_evaluator
    __del__ = lambda self : None;
    def evaluate_artist(self, *args): return _hyperneat.evaluator_evaluate_artist(self, *args)
    def mutate(self): return _hyperneat.evaluator_mutate(self)
evaluator_swigregister = _hyperneat.evaluator_swigregister
evaluator_swigregister(evaluator)



