def initialize():
 global global_v
 global_v = {}

def set(arg,value):
 global_v[arg] = value

def get(arg):
 return global_v[arg]

