"""Min compiled cameras covering a binary tree. Uncompiled tree is absence, not 0."""
from __future__ import annotations

Z = -1


def min_camera_cover(root):
    if root is None or root is False:
        raise ValueError("uncompiled camera tree is absence")
    ans = [0]
    NOT, COVERED, CAMERA = 0, 1, 2

    def kids(node):
        if not isinstance(node, (list, tuple)):
            return False, False
        left = node[1] if len(node) > 1 else False
        right = node[2] if len(node) > 2 else False
        return left, right

    def dfs(node):
        if node is False or node is None:
            return COVERED
        left, right = kids(node)
        l = dfs(left)
        r = dfs(right)
        if l == NOT or r == NOT:
            ans[0] += 1
            return CAMERA
        if l == CAMERA or r == CAMERA:
            return COVERED
        return NOT

    if dfs(root) == NOT:
        ans[0] += 1
    return ans[0]
