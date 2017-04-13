#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class LCSAnalyser:
    """
    A utility class able to find the LCS between three strings / arrays
    """

    def __init__(self,
                 comparator=lambda a, b: a == b,
                 concatenate=lambda a, b: a + b,
                 boxing=lambda x: [x]):
        self.comparator = comparator
        self.concatenate = concatenate
        self.boxing = boxing

    def lcs(self, b, l, r):
        """
        Returns the longuest-common-subsequence between three strings/arrays
        """
        size = max(len(b), len(l), len(r))
        self.__reset_lcs_cache(size)
        subs = self.__lcs(b, len(b) - 1, l, len(l) - 1, r, len(r) - 1, size)
        self.__reset_lcs_cache(size)
        return self.__concatenate_subsequences(subs)

    def __lcs(self, b, pos_b, l, pos_l, r, pos_r, size):
        i = pos_b
        j = pos_l
        k = pos_r

        if (i >= 0) and (j >= 0) and (k >= 0):
            if (self.comparator(b[i], l[j]) and self.comparator(l[j], r[k])):
                return self.__cached_lcs(b, i - 1, l, j - 1, r, k - 1,
                                         size) + [Subsequence(self.boxing(b[i]), i, j, k)]
            else:
                tmp_b = self.__cached_lcs(b, i - 1, l, j, r, k, size)
                tmp_l = self.__cached_lcs(b, i, l, j - 1, r, k, size)
                tmp_r = self.__cached_lcs(b, i, l, j, r, k - 1, size)

                if (len(tmp_b) >= len(tmp_l)) and (len(tmp_b) >= len(tmp_r)):
                    return tmp_b
                elif (len(tmp_l) >= len(tmp_b)) and (len(tmp_l) >= len(tmp_r)):
                    return tmp_l
                elif (len(tmp_r) >= len(tmp_b)) and (len(tmp_r) >= len(tmp_l)):
                    return tmp_r
                else:
                    raise RuntimeException("Oops")
        else:
            return []

    def __concatenate_subsequences(self, subs):
        result = []
        curr = None
        last_b = last_l = last_r = -1

        for sub in subs:
            if (curr == None):
                curr = sub
                last_b = sub.pos_b
                last_l = sub.pos_l
                last_r = sub.pos_r
            elif (sub.pos_b == last_b + 1) and (sub.pos_l == last_l + 1) and (
                    sub.pos_r == last_r + 1):
                curr = Subsequence(
                    self.concatenate(curr.content, sub.content), curr.pos_b, curr.pos_l, curr.pos_r)
                last_b = sub.pos_b
                last_l = sub.pos_l
                last_r = sub.pos_r
            else:
                result += [curr]
                curr = sub
                last_b = sub.pos_b
                last_l = sub.pos_l
                last_r = sub.pos_r
        if curr != None:
            result += [curr]

        return result

    def __reset_lcs_cache(self, size):
        self.__lcs_cache = {}

    def __cached_lcs(self, b, pos_b, l, pos_l, r, pos_r, size):
        key = (((pos_b * size) + pos_l) * size) + pos_r
        if key in self.__lcs_cache:
            return self.__lcs_cache[key]
        else:
            res = self.__lcs(b, pos_b, l, pos_l, r, pos_r, size)
            self.__lcs_cache[key] = res
            return res


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
        return repr(self.content) + " @ b" + str(self.pos_b) + " l" + str(self.pos_l) + " r" + str(
            self.pos_r)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


if __name__ == '__main__':
    print("This is just a utility module, not to be launched directly.")
    sys.exit(1)
