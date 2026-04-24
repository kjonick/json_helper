import argparse

from .operations import create_file, copy_file, merge_files, delete_file

class TopLevelFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        if heading == "positional arguments":
            heading = "Commands"
        elif heading in ("options", "optionals"):
            heading = "Options"
        super().start_section(heading)

class SubcommandFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        if heading == "positional arguments":
            heading = "Arguments"
        elif heading in ("options", "optionals"):
            heading = "Options"
        super().start_section(heading)

class CustomParser(argparse.ArgumentParser):
    def format_help(self):
        parts = []

        # 1. Description
        if self.description:
            parts.append(self.description + "\n\n")

        # 2. Custom usage
        parts.append("Usage: json-helper [command] [-h]  ...\n\n")

        # 3. Get argparse's help
        formatted = super().format_help()

        # Remove argparse's description
        if self.description:
            formatted = formatted.replace(self.description, "")
        
        # Remove argparse's default usage block
        if formatted.startswith("usage:"):
            formatted = formatted.split("\n", 1)[1]

        # Strip leading/trailing blank lines
        formatted = formatted.strip("\n")

        # Ensure exactly one blank line before Options
        parts.append(formatted + "\n")

        return "".join(parts)


def build_parser():

    def add_sub(parser, name, help):
        return parser.add_parser(
            name,
            help=help,
            formatter_class=SubcommandFormatter,
        )

    parser = CustomParser(
        prog="json-helper",
        description="Welcome to JSON Helper tool!",
        formatter_class=TopLevelFormatter,
        add_help=False,
    )

    # Options
    options = parser.add_argument_group("Options")
    options.add_argument("-h", "--help", action="help", help="show this help message and exit")

    # Commands
    subparsers = parser.add_subparsers(
        title="Commands",
        dest="command",
        metavar="",
    )

    # new
    new_parser = add_sub(subparsers, "new", help="Create a new empty JSON file")
    new_parser.add_argument("file", help="Path to the JSON file to create")

    # copy
    copy_parser = add_sub(subparsers, "copy", help="Copy a JSON file to a new location")
    copy_parser.add_argument("source", help="Source JSON file")
    copy_parser.add_argument("dest", help="Destination path")

    # merge
    merge_parser = add_sub(subparsers, "merge", help="Merge two JSON files into a third")
    merge_parser.add_argument("file1", help="First JSON file")
    merge_parser.add_argument("file2", help="Second JSON file")
    merge_parser.add_argument("output", help="Output JSON file")

    # delete
    delete_parser = add_sub(subparsers, "delete", help="Delete a JSON file")
    delete_parser.add_argument("file", help="Path to the JSON file to delete")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "new":
            create_file(args.file)
        elif args.command == "copy":
            copy_file(args.source, args.dest)
        elif args.command == "merge":
            merge_files(args.file1, args.file2, args.output)
        elif args.command == "delete":
            delete_file(args.file)
        else:
            parser.print_help()
    except (FileNotFoundError, FileExistsError, OSError) as e:
        print(f"Error: {e}")
        raise SystemExit(1)
