import os
import shutil
from textnode import TextNode

def main():
    text_node = TextNode("Hello", "Greeting", "https://www.example.com")
    print(text_node)

def copyFiles(source, target):
    shutil.rmtree(target, ignore_errors=True)

    def helper(src, dst):
        entries = os.listdir(src)

        for entry in entries:
            source_path = os.path.join(src, entry)
            target_path = os.path.join(dst, entry)

            if os.path.isdir(source_path):
                os.makedirs(target_path, exist_ok=True)
                helper(source_path, target_path)
            else:
                shutil.copy(source_path, target_path)

    helper(source, target)

if __name__ == "__main__":
    # main()
    copyFiles("static", "public")
