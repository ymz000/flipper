from ctypes import *

types = dict(
	void = 2,

	int = 4,
	ptr = 6,

	u8 = 0,
	u16 = 1,
	u32 = 3,
	u64 = 7,
	s8 = 8,
	s16 = 9,
	s32 = 11,
	s64 = 15,

	_default_ = -1,
)

class lf_type:
	type = None
	value = None
	def __init__(self, type, value):
		self.type = type
		self.value = value
		return

def u8(a):
	return lf_type(types['u8'], a)

libflipper = CDLL('libflipper.so')
#libflipper.lf_set_debug_level(3)

class flipper:
	ref = None
	def __init__(self, name = None):
		if (name == None):
			device = current_device()
		self.ref = device
		return

class module:
	ref = None
	def __init__(self, name, device = None, ref = None):
		if (device == None):
			device = flipper()
		if (ref):
			self.ref = ref
		else:
			libflipper.lf_module_create.restype = c_void_p
			self.ref = libflipper.lf_module_create(c_char_p(name), device.ref)
			bind(self, device)

def attach():
	libflipper.flipper_attach.restype = c_void_p
	return libflipper.flipper_attach()

def attach_network(hostname):
	libflipper.carbon_attach_hostname.restype = c_void_p
	return libflipper.carbon_attach_hostname(c_char_p(hostname))

def bind(module, device):
	libflipper.lf_bind(c_void_p(module.ref), c_void_p(device.ref))

def current_device():
	libflipper.lf_get_current_device.restype = c_void_p
	return libflipper.lf_get_current_device()

def lf_ll_from_list(l):
	ll = c_void_p(0)
	for i in l:
		libflipper.lf_arg_create.restype = c_void_p
		arg = libflipper.lf_arg_create(c_byte(i.type), c_ulonglong(i.value))
		libflipper.lf_ll_append(byref(ll), c_void_p(arg), libflipper.lf_arg_release)
	return ll

def getModule(name):
	_module = c_void_p.in_dll(libflipper, '_' + name)
	return module(name, None, byref(_module))

def invoke(module, function, ret, arguments):
	libflipper.lf_invoke(module.ref, c_byte(function), c_byte(ret), lf_ll_from_list(arguments))
	return
