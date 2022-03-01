from __future__ import annotations

from typing import Mapping, overload,MutableMapping,Generic, TypeVar, Iterator
from json import dumps
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_T = TypeVar("_T")

def hashable(data):
    if isinstance(data, list):
        data = tuple(data)
    elif isinstance(data, dict):
        data = dumps(data)
    return hash(data)

def str2re(a):
    if isinstance(a, str):
        return f'"{a}"'
    else:
        return f'{a}'

class HessianDict(MutableMapping[_KT,_VT], Generic[_KT,_VT]):
    def __init__(self, **kargs):
        self.data = {}
        self.key = {}
        for k,v in kargs:
            t = hashable(k)
            self.data[t] = v
            self.key[t] = k
        
    def keys(self):
        return self.key.values()
    
    def values(self):
        return self.data.values()

    def items(self):
        return [(k,v) for k,v in zip(self.key.values(), self.data.values())]
    
    def get(self, __key: _KT, __default: _VT | _T=...)-> _VT | _T:
        key = hashable(__key)
        if key not in self.data:
            if isinstance(__default,type(...)):
                raise ValueError(f'{__key} not in dict!!')
            return __default
        else:
            return self.data[key]

    def pop(self, __key: _KT, __default: _VT | _T=...)-> _VT | _T:
        key = hashable(__key)
        if key not in self.data:
            if isinstance(__default,type(...)):
                raise ValueError(f'{__key} not in dict!!')
            return __default
        else:
            self.key.pop(key)
            return self.data.pop(key)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, __k):
        key = hashable(__k)
        if key not in self.data:
            raise ValueError(f'{__k} not in dict!!')
        else:
            return self.data[key]
    
    def __setitem__(self, __k, __v):
        k = hashable(__k)
        self.data[k] = __v
        self.key[k] = __k
    
    def __delitem__(self, __k):
        key = hashable(__k)
        if key not in self.data:
            raise ValueError(f'{__k} not in dict!!')
        else:
            self.data.pop(key)
            self.key.pop(key)

    def __iter__(self) -> Iterator[_KT]: ...

    def update(self, other=(), /, **kwds):
        if isinstance(other, Mapping):
            for key in other:
                k = hashable(key)
                self.data[k] = other[key]
                self.key[k] = key
        elif hasattr(other, "keys"):
            for key in other.keys():
                k = hashable(key)
                self.data[k] = other[key]
                self.key[k] = key
        else:
            for key, value in other.items():
                k = hashable(key)
                self.data[k] = value
                self.key[k] = key
        for key, value in kwds.items():
            k = hashable(key)
            self.data[k] = value
            self.key[k] = key
    def __repr__(self):
        re = []
        k,v = self.key.values(), self.data.values()
        for a,b in zip(k,v):
            if id(b)==id(self):
                re.append(f'{str2re(a)}:...')
            else:
                re.append(f'{str2re(a)}:{str2re(b)}')
        return '{'+','.join(re)+'}'