#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import TypeVar, Generic, List, Any

S = TypeVar('S')  # Generic Sequence
I = TypeVar('I')  # Generic Item


class SubSeq(Generic[S]):
    """
    Represents a SubSequence
    """

    def __init__(self):
        pass


class CommonSubSeq(Generic[S], SubSeq[S]):
    """
    Represents a sub-sequence in an LCS result, where all three versions are the same
    """

    def __init__(self, content: S, pos_b: int, pos_l: int, pos_r: int):
        super().__init__()
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


class DiffSubSeq(Generic[S], SubSeq[S]):
    """
    Represents a sub-sequence in an LCS result, where at least one version is different
    """

    def __init__(self, content_b: S, content_l: S, content_r: S, pos_b: int, pos_l: int, pos_r: int):
        super().__init__()
        self.content_b = content_b
        self.content_l = content_l
        self.content_r = content_r
        self.pos_b = pos_b
        self.pos_l = pos_l
        self.pos_r = pos_r

    def __repr__(self):
        return repr(self.content_b) + " @ b" + str(self.pos_b) + " / " + repr(self.content_l) + " l" + str(
            self.pos_l) + " / " + repr(self.content_r) + " r" + str(self.pos_r)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


def len_common_ss(l: List[SubSeq]):
    length = 0
    for ss in l:
        if ss is CommonSubSeq:
            length += 1
    return length


class Sequencer(Generic[S, I]):
    """
    An object used by the LCSAnalyser to decompose the given objects in sequences
    """

    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def concat(self, a: S, b: S) -> S:
        """
        :param a: a sequence
        :param b: another sequence
        :return: a sequence containing the items from both params
        """
        return a + b

    # noinspection PyMethodMayBeStatic
    def get_item(self, seq: S, pos: int) -> I:
        """
        :param seq: the sequence
        :param pos: an index in the sequence
        :return: the item at the given position in the sequence
        """
        return seq[pos]

    # noinspection PyMethodMayBeStatic
    def sub_sequence(self, seq: S, start: int, end: int) -> S:
        return seq[start:end]

    # noinspection PyMethodMayBeStatic
    def are_items_equal(self, a: I, b: I) -> bool:
        """
        :param a: an item from an analysed sequence
        :param b: another item from an analysed sequence
        :return: whether the two items can be considered equal
        """
        return a == b

    # noinspection PyMethodMayBeStatic
    def box(self, item: I) -> S:
        """
        :param item: an item
        :return: a sequence only containing the given item
        """
        pass


class StringSequencer(Sequencer[str, str]):
    def box(self, item: str):
        return str(item)

    def concat(self, a: str, b: str) -> str:
        return a + b


class ListSequencer(Generic[I], Sequencer[List[I], I]):
    def box(self, item: I) -> List[I]:
        return [item]

    def concat(self, a: List[I], b: List[I]) -> List[I]:
        return a + b


class LCSAnalyser(Generic[S, I]):
    """
    A utility class able to find the LCS between three strings / arrays
    """

    def __init__(self, sequencer: Sequencer[S, I]):
        self.sequencer = sequencer

    def lcs_with_diff(self, base: S, left: S, right: S) -> List[SubSeq[S]]:
        """
        Returns the longest common sub-sequence between three strings/arrays
        :param base:
        :param left:
        :param right:
        :return:
        """
        self.__reset_lcs_cache()

        size = max(len(base), len(left), len(right))
        subs = self.__lcs(base, len(base) - 1, left, len(left) - 1, right, len(right) - 1, size)

        return self.__compute_diff(self.__concatenate_sub_sequences(subs), base, left, right)

    def lcs(self, base: S, left: S, right: S) -> List[CommonSubSeq[S]]:
        """
        Returns the longest common sub-sequence between three strings/arrays
        """
        self.__reset_lcs_cache()

        size = max(len(base), len(left), len(right))
        subs = self.__lcs(base, len(base) - 1, left, len(left) - 1, right, len(right) - 1, size)

        return self.__concatenate_sub_sequences(subs)

    def __lcs(self, b: S, pos_b: int, l: S, pos_l: int, r: S, pos_r: int, size: int) -> List[CommonSubSeq[S]]:
        i = pos_b
        j = pos_l
        k = pos_r

        if (i >= 0) and (j >= 0) and (k >= 0):
            item_b = self.sequencer.get_item(b, i)
            item_l = self.sequencer.get_item(l, j)
            item_r = self.sequencer.get_item(r, k)

            if self.sequencer.are_items_equal(item_b, item_l) and self.sequencer.are_items_equal(item_b, item_r):
                return self.__cached_lcs(b, i - 1, l, j - 1, r, k - 1, size) + [
                    CommonSubSeq(self.sequencer.box(item_b), i, j, k)]
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
                    raise RuntimeError("Oops")
        else:
            return []

    def __concatenate_sub_sequences(self, subs: List[CommonSubSeq[S]]) -> List[CommonSubSeq[S]]:
        result = []
        curr = None
        last_b = last_l = last_r = -1

        for sub in subs:
            if curr is None:
                curr = sub
                last_b = sub.pos_b
                last_l = sub.pos_l
                last_r = sub.pos_r
            elif (sub.pos_b == last_b + 1) and (sub.pos_l == last_l + 1) and (sub.pos_r == last_r + 1):
                curr = CommonSubSeq(self.sequencer.concat(curr.content, sub.content), curr.pos_b, curr.pos_l,
                                    curr.pos_r)
                last_b = sub.pos_b
                last_l = sub.pos_l
                last_r = sub.pos_r
            else:
                result += [curr]
                curr = sub
                last_b = sub.pos_b
                last_l = sub.pos_l
                last_r = sub.pos_r
        if curr is not None:
            result += [curr]

        return result

    def __compute_diff(self, subs: List[CommonSubSeq[S]], b: S, l: S, r: S) -> List[SubSeq[S]]:
        result = []
        prev = CommonSubSeq([], 0, 0, 0)

        for css in subs:
            if css.pos_b > 0 or css.pos_l > 0 or css.pos_r > 0:
                lpc = len(prev.content)
                tmp_b = self.sequencer.sub_sequence(b, prev.pos_b + lpc, css.pos_b)
                tmp_l = self.sequencer.sub_sequence(l, prev.pos_l + lpc, css.pos_l)
                tmp_r = self.sequencer.sub_sequence(r, prev.pos_r + lpc, css.pos_r)
                result += [DiffSubSeq(tmp_b, tmp_l, tmp_r, prev.pos_b + lpc, prev.pos_l + lpc, prev.pos_r + lpc)]
            result += [css]
            prev = css

        lpc = len(prev.content)
        if prev.pos_b + lpc < len(b) or prev.pos_l + lpc < len(l) or prev.pos_r + lpc < len(r):
            tmp_b = self.sequencer.sub_sequence(b, prev.pos_b + lpc, len(b))
            tmp_l = self.sequencer.sub_sequence(l, prev.pos_l + lpc, len(l))
            tmp_r = self.sequencer.sub_sequence(r, prev.pos_r + lpc, len(r))
            result += [DiffSubSeq(tmp_b, tmp_l, tmp_r, prev.pos_b + lpc, prev.pos_l + lpc, prev.pos_r + lpc)]

        return result

    def __reset_lcs_cache(self):
        self.__lcs_cache = {}

    def __cached_lcs(self, b, pos_b, l, pos_l, r, pos_r, size):
        key = (((pos_b * size) + pos_l) * size) + pos_r
        if key in self.__lcs_cache:
            return self.__lcs_cache[key]
        else:
            res = self.__lcs(b, pos_b, l, pos_l, r, pos_r, size)
            self.__lcs_cache[key] = res
            return res


if __name__ == '__main__':
    print("This is just a utility module, not to be launched directly.")
    sys.exit(1)
