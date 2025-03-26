import os
import dsl.Nodes
import textx
import textx.export
import textx.metamodel
from textx import metamodel_from_file

DSL_MODEL = "dsl.tx"

def get_metamodel(debug: bool = True) -> textx.metamodel.TextXMetaModel:
    """
    Get metamodel from the textX described in dsl.tx
    Return:
        (TextXMetaModel) metamodel
    """
    this_folder = os.path.dirname(os.path.abspath(__file__))
    path_metamodel = os.path.join(this_folder, DSL_MODEL)
    meta_model = metamodel_from_file(path_metamodel, classes=dsl.Nodes.NODE_CLASSES)
    if debug:
        textx.export.metamodel_export(meta_model, os.path.join(this_folder, 'dsl.dot'))
    return meta_model

def storytell_dsl(code_path: str, debug: bool = False):
    """
    Get parsed Semantic tree
    Args:
        (str) code_path
        (bool) debug: to enable debug mode (False by default)
    """
    assert os.path.exists(code_path)
    meta_model: textx.metamodel.TextXMetaModel = get_metamodel(debug=debug)
    model = meta_model.model_from_file(code_path)
    return model
