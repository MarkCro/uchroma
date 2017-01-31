import struct
from enum import Enum

import numpy as np
from grapefruit import Color


class ByteArgs(object):
    """
    Helper class for assembling byte arrays from
    argument lists of varying types
    """
    def __init__(self, max_size, size=0, data=None):
        self._size = size
        self._data_ptr = 0

        if data is None:
            self._data = np.zeros(shape=(max_size,), dtype=np.uint8)
        else:
            self._data = np.frombuffer(data, dtype=np.uint8)


    @property
    def data(self):
        """
        The byte array assembled from supplied arguments
        """
        return self._data


    @property
    def size(self):
        """
        Size of the byte array
        """
        if self._size is None:
            return len(self._data)
        return self._size


    def _ensure_space(self, size):
        if self._size is None:
            return
        assert (len(self._data) + size) <= self._size, \
                ('Additional argument (len=%d) would exceed size limit %d (cur=%d)'
                 % (size, self._size, len(self._data)))


    def clear(self):
        """
        Empty the contents of the array

        :return: The empty ByteArgs
        :rtype: ByteArgs
        """
        self._data.fill(0)
        self._data_ptr = 0
        return self


    def put(self, arg, packing='=B'):
        """
        Add an argument to this array

        :param arg: The argument to append
        :type arg: varies

        :param packing: The representation passed to struct.pack
        :type packing: str

        :return: This ByteArgs instance
        :rtype: ByteArgs
        """
        data = None
        if isinstance(arg, Color):
            for component in arg.intTuple:
                data = struct.pack(packing, component)
        elif isinstance(arg, Enum):
            if hasattr(arg, "opcode"):
                data = arg.opcode
            else:
                data = arg.value
        elif isinstance(arg, np.ndarray):
            data = arg.flatten()
        elif isinstance(arg, bytes) or isinstance(arg, bytearray):
            data = arg
        else:
            data = struct.pack(packing, arg)

        if isinstance(data, int):
            self._ensure_space(1)
            self._data[self._data_ptr] = data
            self._data_ptr += 1
        else:
            datalen = len(data)
            if datalen > 0:
                self._ensure_space(datalen)
                if not isinstance(data, np.ndarray):
                    data = np.frombuffer(data, dtype=np.uint8)
                self._data[self._data_ptr:self._data_ptr+datalen] = data
                self._data_ptr += datalen

        return self


    def put_all(self, args, packing='=B'):
        for arg in args:
            self.put(arg, packing=packing)
        return self


    def put_short(self, arg):
        """
        Convenience method to add an argument as a short to
        the array

        :param arg: The argument to append
        :type arg: varies

        :return: This ByteArgs instance
        :rtype: ByteArgs
        """
        return self.put(arg, '=H')


    def put_int(self, arg):
        """
        Convenience method to add an argument as an integer to
        the array

        :param arg: The argument to append
        :type arg: varies

        :return: This ByteArgs instance
        :rtype: ByteArgs
        """
        return self.put(arg, '=I')
