import os
import textx
import textx.export
import textx.metamodel
from textx import metamodel_from_file

DSL_MODEL = "dsl.tx"

class IfStatement:
    __fields__ = "parent", "condition", "block", "block_else"
    def __init__(self, condition, block, block_else, parent):
        self.parent = parent
        self.condition = condition
        self.block = block
        self.block_else = block_else
    def __str__(self):
        r = f"if {str(self.condition[0])} then {[str(b)+';' for b in self.block[0]]}"
        for cond, block in zip(self.condition[1:], self.block[1:]):
            r += f" else if {cond} then {[str(b)+';' for b in block]}"
        if self.block_else:
            r += f" else {[str(b)+';' for b in self.block_else]}"
        return r
class CodeBlock:
    __fields__ = "block", "parent"
    def __init__(self, block, parent):
        self.parent = parent
        self.block  = block
    def __getitem__(self, key):
        return self.block[key]
    def __str__(self):
        return f"{[str(b) for b in self.block]}"
class BinaryExpParent:
    __fields__ = "left", "op", "right", "parent"
    def __init__(self, left, op, right, parent):
        self.parent = parent
        self.left = left
        self.op = op
        self.right = right
    def __str__(self):
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
class Factor:
    __fields__ = "sign", "op", "parent"
    def __init__(self, sign, op, parent):
        self.parent = parent
        self.sign   = sign
        self.op     = op
    def __str__(self):
        r = str(self.op)
        if self.sign:
            r = f"{self.sign}{r}"
        return r
class Operand:
    __fields__ = "op_num", "op_id", "op_expr", "parent"
    def __init__(self, op_num, op_id, op_expr, parent):
        self.parent = parent
        self.op_num = op_num
        self.op_id  = op_id
        self.op_expr = op_expr
    def __str__(self):
        if self.op_id:
            return str(self.op_id)
        if self.op_expr:
            return str(self.op_expr)
        return str(self.op_num)
class AssignExpression(BinaryExpParent):
    pass

def get_metamodel(debug: bool = True) -> textx.metamodel.TextXMetaModel:
    """
    Get metamodel from the textX described in dsl.tx
    Return:
        (TextXMetaModel) metamodel
    """
    this_folder = os.path.dirname(os.path.abspath(__file__))
    path_metamodel = os.path.join(this_folder, DSL_MODEL)
    meta_model = metamodel_from_file(path_metamodel, classes=[IfStatement, BoolExpr, CodeBlock,
                                                              BinaryExpression, Term,
                                                              Factor, Operand, AssignExpression])
    if debug:
        textx.export.metamodel_export(meta_model, os.path.join(this_folder, 'dsl.dot'))
    return meta_model

def storytell_dsl(code_path: str):
    meta_model: textx.metamodel.TextXMetaModel = get_metamodel(debug=True)
    model = meta_model.model_from_file(code_path)
    return model