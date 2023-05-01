class LispElement:
    def __init__(self, atom=None, lst=None):
        if atom is not None and lst is not None:
            raise ValueError("LispElement cannot be both atom and list.")
        self.atom = atom
        self.lst = lst

    def is_atom(self):
        return self.atom is not None

    def is_list(self):
        return self.lst is not None

    def __repr__(self):
        if self.is_atom():
            return str(self.atom)
        elif self.is_list():
            return f"({', '.join(map(str, self.lst))})"
        return "()"


def create_atom(value):
    return LispElement(atom=value)


def create_list(elements):
    if not elements:
        return LispElement()
    return LispElement(lst=elements)
