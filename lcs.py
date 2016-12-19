#!/usr/bin/python3
# -*- coding: utf-8 -*-


class LCS:
    """
    A representation of the longuest-common-subsequence between parts of a conflict
    """

    def __init__(self):
        self.subsequences = []

    def __str__(self):
        result = ""
        for subsequence in self.subsequence:
            result += str(subsequence)


class Subsequence:
    """
    Represents a subsequence in an LCS result
    """

    def __init__(self, content, pos_b, pos_l, pos_r):
        self.content = content
        self.pos_b = pos_b
        self.pos_l = pos_l
        self.pos_r = pos_r

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return repr(self.content) + " @ b" + str(self.pos_b) + " l" + str(self.pos_l) + " r" + str(self.pos_r)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


def lcs(conflict):
    """
    Returns the longuest-common-subsequence between each parts of a conflict
    """
    b = conflict.base
    l = conflict.local
    r = conflict.remote
    return lcs(b,l,r)


def lcs(b, l, r):
    """
    Returns the longuest-common-subsequence between three strings/arrays
    """
    size = max(len(b), len(l), len(r))
    _reset_lcs_cache(size)
    subs = _lcs(b, 0, l, 0, r, 0, size)

    result = []
    curr = None
    last_b = last_l = last_r = -1

    for sub in subs:
        if (curr == None) :
            curr = sub
            last_b = sub.pos_b
            last_l = sub.pos_l
            last_r = sub.pos_r
        elif (sub.pos_b == last_b + 1) and (sub.pos_l == last_l + 1) and (sub.pos_r == last_r + 1):
            curr = Subsequence(curr.content + sub.content, curr.pos_b, curr.pos_l, curr.pos_r)
            last_b = sub.pos_b
            last_l = sub.pos_l
            last_r = sub.pos_r
        else :
            result += [curr]
            curr = sub
            last_b = sub.pos_b
            last_l = sub.pos_l
            last_r = sub.pos_r
    if curr != None:
        result += [curr]

    _reset_lcs_cache(size)
    return result


def _lcs(b, pos_b, l,pos_l, r, pos_r, size):
    """
    Returns the longuest-common-subsequence between three strings
    """
    i = pos_b
    j = pos_l
    k = pos_r

    if (i < len(b)) and (j < len(l)) and (k < len(r)):
        if (b[i] == l[j]) and (l[j] == r[k]) :
            return [Subsequence(b[i], i, j, k)] + _cached_lcs(b, i + 1, l, j + 1, r, k + 1, size)
        else :
            tmp_b = _cached_lcs(b, i + 1, l, j, r, k, size)
            tmp_l = _cached_lcs(b, i, l, j + 1, r, k, size)
            tmp_r = _cached_lcs(b, i, l, j, r, k + 1, size)
            if (len(tmp_b) >= len(tmp_l)) and (len(tmp_b) >= len(tmp_r)):
                return tmp_b
            elif (len(tmp_l) >= len(tmp_b)) and (len(tmp_l) >= len(tmp_r)):
                return tmp_l
            elif (len(tmp_r) >= len(tmp_b)) and (len(tmp_r) >= len(tmp_l)):
                return tmp_r
            else:
                raise RuntimeException("Oops")
    else :
        return []

lcs_cache = {}

def _reset_lcs_cache(size):
    global lcs_cache
    lcs_cache = {}

def _cached_lcs(b, pos_b, l, pos_l, r, pos_r, size):
    global lcs_cache
    key = (((pos_b * size) + pos_l) * size) + pos_r
    if key in lcs_cache :
        return lcs_cache[key]
    else:
        res = _lcs(b, pos_b, l, pos_l, r, pos_r, size)
        lcs_cache[key] = res
        return res


if __name__ == '__main__':
    print("This is just a utility module, not to be launched directly.")
    sys.exit(1)
