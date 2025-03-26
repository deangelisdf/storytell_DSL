
class IfStatement:
    __slots__ = "parent", "condition", "block", "block_else"
    def __init__(self, condition:list, block:list, block_else, parent):
        self.parent = parent
        self.condition = condition
        self.block = block
        self.block_else = block_else
    def __str__(self):
        """Get string version"""
        r = f"if {str(self.condition[0])} then {[str(b)+';' for b in self.block[0]]}"
        for cond, block in zip(self.condition[1:], self.block[1:]):
            r += f" else if {cond} then {[str(b)+';' for b in block]}"
        if self.block_else:
            r += f" else {[str(b)+';' for b in self.block_else]}"
        return r

class CodeBlock:
    __slots__ = "block", "parent"
    def __init__(self, block:list, parent):
        self.parent = parent
        self.block  = block
    def __getitem__(self, key):
        return self.block[key]
    def __str__(self):
        """Get string version"""
        return f"{[str(b) for b in self.block]}"

class BinaryExpParent:
    __slots__ = "left", "op", "right", "parent"
    def __init__(self, left, op:list, right:list, parent):
        self.parent = parent
        self.left = left
        self.op = op
        self.right = right
    def __str__(self):
        """Get string version"""
        r = f"{str(self.left)}"
        for op, right in zip(self.op, self.right):
            r += f" {op} {str(right)}"
        return r
class BoolExpr(BinaryExpParent):
    pass
class BinaryExpression(BinaryExpParent):
    pass
class Term(BinaryExpParent):
    pass
class AssignExpression(BinaryExpParent):
    pass

class Factor:
    __slots__ = "sign", "op", "parent"
    def __init__(self, sign:str, op, parent):
        self.parent = parent
        self.sign   = sign
        self.op     = op
    def __str__(self):
        """Get string version"""
        r = str(self.op)
        if self.sign:
            r = f"{self.sign}{r}"
        return r

class Operand:
    __slots__ = "op_num", "op_id", "op_expr", "parent"
    def __init__(self, op_num:int, op_id:str, op_expr, parent):
        self.parent = parent
        self.op_num = op_num
        self.op_id  = op_id
        self.op_expr = op_expr
    def __str__(self):
        """Get string version"""
        if self.op_id:
            return str(self.op_id)
        if self.op_expr:
            return str(self.op_expr)
        return str(self.op_num)

NODE_CLASSES = [IfStatement, BoolExpr, CodeBlock, BinaryExpression, Term,
                Factor, Operand, AssignExpression]
