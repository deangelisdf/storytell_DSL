"""Unit test actions
author: domenico francesco de angelis"""
import sys
import os
import unittest

src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, src_path)

import dsl.Nodes # noqa: E402

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

#TESTs
class actions_testing(unittest.TestCase):
    def test_Operand(self):
        """Test Case 0
        - Operand shall print properly: int, ID or expression
        """
        op = dsl.Nodes.Operand(0, "ID", None, None)
        self.assertEqual(str(op), "ID")
        op = dsl.Nodes.Operand(15, "", None, None)
        self.assertEqual(str(op), "15")
        op = dsl.Nodes.Operand(0, "", dsl.Nodes.Factor('+',
                                                       dsl.Nodes.Operand(1, "", None, None), None),
                                      None)
        self.assertEqual(str(op), "+1")
    def test_Factor(self):
        """Test Case 1
        - Operand shall print properly: int, string or expression,
          with a possible sign ('+' or '-')
        """
        op = dsl.Nodes.Operand(0, "ID", None, None)
        factor = dsl.Nodes.Factor('+', op, None)
        self.assertEqual(str(factor), "+ID")
        factor = dsl.Nodes.Factor('-', op, None)
        self.assertEqual(str(factor), "-ID")
        factor = dsl.Nodes.Factor('', op, None)
        self.assertEqual(str(factor), "ID")
        op = dsl.Nodes.Operand(0, "15", None, None)
        factor = dsl.Nodes.Factor('+', op, None)
        self.assertEqual(str(factor), "+15")
        factor = dsl.Nodes.Factor('-', op, None)
        self.assertEqual(str(factor), "-15")
        factor = dsl.Nodes.Factor('', op, None)
        self.assertEqual(str(factor), "15")
    def test_BinaryExpParent(self):
        """Test Case 2
        - Shall generate a string as proper abstraction of all kind of binary expression
        """
        node = dsl.Nodes.BinaryExpParent(left='1', op=['+'], right=['2'], parent=None)
        self.assertEqual(str(node), "1 + 2")
        op1 = dsl.Nodes.Operand(0, "a", None, None)
        factor1 = dsl.Nodes.Factor('+', op1, None)
        op2 = dsl.Nodes.Operand(0, "b", None, None)
        factor2 = dsl.Nodes.Factor('-', op2, None)
        node = dsl.Nodes.BinaryExpParent(left=factor1, op=['=='], right=[factor2], parent=None)
        self.assertEqual(str(node), "+a == -b")
    def test_CodeBlock(self):
        """Test Case 3
        - Shall handle multiple expressions and convert it correctly in a string
        """
        code_block = dsl.Nodes.CodeBlock([], None)
        self.assertEqual(str(code_block), "[]")
        op1 = dsl.Nodes.Operand(1, "", None, None)
        op2 = dsl.Nodes.Operand(2, "", None, None)
        code_block = dsl.Nodes.CodeBlock(block=[op1, op2],
                                         parent=None)
        self.assertEqual(str(code_block), "['1', '2']")
    def test_IfStatement(self):
        """Test Case 4
        - Shall handle if statement
        """
        a_op = dsl.Nodes.Operand(0, 'a', None, None)
        cond = dsl.Nodes.BoolExpr(a_op, ['=='],
                                  [dsl.Nodes.Operand(1, '', None, None)], None)
        assign = dsl.Nodes.AssignExpression(a_op, ['='],
                                            [dsl.Nodes.Operand(0, '', None, None)], None)
        code_block = dsl.Nodes.CodeBlock(block=[assign],
                                         parent=None)
        ifstatement =dsl.Nodes.IfStatement(condition=[cond],
                                           block=[code_block],
                                           block_else=[],
                                           parent=None)
        self.assertEqual(str(ifstatement), "if a == 1 then ['a = 0;']")
        code_block = dsl.Nodes.CodeBlock(block=[assign],
                                         parent=None)
        ifstatement.block_else = code_block
        self.assertEqual(str(ifstatement), "if a == 1 then ['a = 0;'] else ['a = 0;']")
        cond = dsl.Nodes.BoolExpr(a_op, ['=='],
                                  [dsl.Nodes.Operand(2, '', None, None)], None)
        assign.right[0].op_num = 2
        code_block = dsl.Nodes.CodeBlock(block=[assign],
                                         parent=None)
        ifstatement.block.append(code_block)
        ifstatement.condition.append(cond)
        self.assertEqual(str(ifstatement), "if a == 1 then ['a = 2;'] else if a == 2 then ['a = 2;'] else ['a = 2;']")

if __name__ == "__main__":
    unittest.main()
