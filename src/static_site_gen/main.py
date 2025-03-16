import shutil
import os

from static_site_gen.file_handler import (
    copy_files_recursive,
    generate_page,
)


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    copy_files_recursive("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")


if __name__ == "__main__":
    main()
