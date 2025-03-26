import argparse
import dsl

def print_storytell(model):
    """A pretty print for the model"""
    print("scene:", model.name)
    print("actor names:")
    for act in model.actors:
        print(act.name)
    for diag in model.dialogue[0].lines:
        print(diag.actor.name, ":", diag.entry)

def main():
    """main function"""
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file_path", type=str,
                           help="The path to the textual file.")
    args = argparser.parse_args()
    storytell_model = dsl.storytell_dsl(args.file_path)
    print_storytell(storytell_model)

if __name__ == "__main__":
    main()
