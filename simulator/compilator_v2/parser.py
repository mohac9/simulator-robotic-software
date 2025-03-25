import re

class ArduinoParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.functions = []
        self.variables = []
        self.setup_block = None
        self.loop_block = None

    def parse(self):
        with open(self.file_path, 'r') as file:
            code = file.read()

        # Extract functions
        self.functions = re.findall(r'(\w+\s+\w+\s*\([^)]*\)\s*{)', code)

        # Extract global variables
        self.variables = re.findall(r'(int|float|char|bool|long|double)\s+\w+\s*;', code)

        # Extract setup block
        setup_match = re.search(r'void\s+setup\s*\(\)\s*{([^}]*)}', code, re.DOTALL)
        if setup_match:
            self.setup_block = setup_match.group(1).strip()

        # Extract loop block
        loop_match = re.search(r'void\s+loop\s*\(\)\s*{([^}]*)}', code, re.DOTALL)
        if loop_match:
            self.loop_block = loop_match.group(1).strip()

    def get_summary(self):
        return {
            "functions": self.functions,
            "variables": self.variables,
            "setup_block": self.setup_block,
            "loop_block": self.loop_block
        }


# Example usage
if __name__ == "__main__":
    parser = ArduinoParser("example.ino")
    parser.parse()
    summary = parser.get_summary()
    print("Functions:", summary["functions"])
    print("Variables:", summary["variables"])
    print("Setup Block:", summary["setup_block"])
    print("Loop Block:", summary["loop_block"])