from custom_parser import Parser
import sys

parser = Parser()
parser.build()

if len(sys.argv) < 2:
    print("Usage: python compiler.py <input_forth_file>")
    sys.exit(1)

input_file_name = sys.argv[1]

if not input_file_name.endswith(".forth"):
    print("Error: Input file must have a .forth extension")
    sys.exit(1)

try:
    with open(input_file_name, "r") as file:
        input_text = file.read()
        print("\n\nINPUT CODE:")
        print(input_text)
        output_text = parser.parser.parse(input_text)

    if output_text:
        output_file_name = input_file_name[:-6] + ".ewvm"
        with open(output_file_name, "w") as file:
            print("\n\nOUTPUT CODE:")
            print(output_text)
            file.write(output_text)
    else:
        print("Compile error: No output generated")
except FileNotFoundError:
    print(f"Error: File {input_file_name} not found")
except Exception as e:
    print(f"Error: {e}")