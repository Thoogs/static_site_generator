from static_site_gen.file_handler import copy_files_recursive


def main():
    copy_files_recursive("./static", "./public")


if __name__ == "__main__":
    main()
