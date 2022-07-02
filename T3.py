from scipy.io import arff
import pandas as pd
import numpy as np
import sympy as sp
import streamlit
import random
import FlajoletMartin


class BloomFilter(object):
    """
        Class for Bloom filter
    """

    def __init__(self, n, S, hash_number=10, hash_values=None):
        """

        :param n: length of bit array
        :param S: set of key values
        :param hash_values: values of hash function

        Initializes instance and fills bitmap according to key values given
        """
        if hash_values is None:
            hash_values = \
                [(sp.randprime(1, 1000), sp.randprime(1, 1000), sp.randprime(1, 1000)) for f in range(0, hash_number)]
        self.bitmap = np.zeros(n)
        self.hash_values = hash_values
        for key in S:
            self.add(key)

    def hashing(self, item, values):
        """

        :param item: item to be hashed
        :param values: integers to be used in hash functions
        :return: hashed position of item
        """
        return (values[0] * item + values[1]) % values[2]

    def add(self, item):
        """

        :param item: new key Value
        :return: hashes new item as key value in S
        """
        for value in self.hash_values:
            self.bitmap[self.hashing(item, value)] = 1

    def check(self, item):
        """

        :param item: stream data to be filtered
        :return: boolean whether data is part of S or not
        """
        for value in self.hash_values:
            if not (self.bitmap[self.hashing(item, value)]):
                return False
        return True

    # def Flajolet_Martin(self, stream):
    #     """
    #     :param stream: incoming data
    #     :return: distinct elements expected from stream
    #     """
    #     tail = 0
    #     for entry in stream:
    #         number = bin(self.hashing(entry, self.hash_values[0]))[2:]
    #         new_tail = len(number) - len(number.rstrip('0'))
    #         tail = max(tail, new_tail)
    #
    #     return 2 ** tail

    def Flajolet_Martin(self, stream):
        """
        :param stream: incoming data
        :return: distinct elements expected from stream
        """
        return FlajoletMartin.cardinality(stream)


data = arff.loadarff('EEG Eye State.arff')
df = pd.DataFrame(data[0])
AF3 = df["AF3"].to_numpy().astype(int)
F7 = df["F7"].to_numpy().astype(int)
F8 = df["F8"].to_numpy().astype(int)
S1 = [random.choice(AF3)for i in range(0, 100)]
S2 = [random.choice(F7)for i in range(0, 100)]
S3 = [random.choice(F8) for i in range(0, 100)]
BloomAF3 = BloomFilter(len(AF3), S1)
BloomF7 = BloomFilter(len(F7), S2)
BloomF8 = BloomFilter(len(F8), S3)