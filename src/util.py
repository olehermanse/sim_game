
def native(method):
    method.is_native = True
    return method

def is_native(method):
    return hasattr(method, "is_native")

@native
def chain_print(self):
    if is_native(self.chain_print):
        print("Native")
    else:
        print("Inherited")
    return "GraphicsObject"
