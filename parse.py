import json
import argparse
from io import TextIOWrapper

DEFAULT_MINIMUM_DEPTH = 1
OUTPUT_SEPARATOR = "_"


def build_output(data: dict, out: dict, depth_min: int,
                 depth: int = 0, key_in_progress="", payload_in_progress: dict = None):
    payload = {} if payload_in_progress is None else payload_in_progress.copy()

    data_to_process = []
    updated_key = key_in_progress

    # no data means we've hit one possible end scenario for an inheritance chain
    if len(data) == 0:
        out[updated_key] = payload
    else:
        for key, value in data.items():
            # defer recursion until afterwards to ensure we get all payload information
            if type(value) is dict:
                data_to_process.append((key, value))
            else:
                if key == 'include' and key in payload:
                    payload[key] = "{0},{1}".format(payload[key], value)
                else:
                    payload[key] = value

        # no more dict objects means we've hit the other possible end scenario for an inheritance chain
        if len(data_to_process) is 0:
            if depth >= depth_min:
                out[updated_key] = payload
        if len(data_to_process) > 0:
            for item in data_to_process:
                new_key = item[0] if len(updated_key) is 0 else (key_in_progress + OUTPUT_SEPARATOR + item[0])
                build_output(item[1], out, depth_min, depth + 1, new_key, payload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSON file leveraging inheritance.")
    parser.add_argument("infile", action="store", type=argparse.FileType("r"),
                        metavar="input_file", help="JSON file to parse.")
    parser.add_argument("outfile", action="store", type=argparse.FileType("w"),
                        metavar="output_file", help="Path to output JSON file results.")
    parser.add_argument("-md", "--min-depth", action="store", default=DEFAULT_MINIMUM_DEPTH, type=int, dest="min_depth",
                        metavar="min_depth", help="Minimum depth required to concatenate parsed entities.")

    args = parser.parse_args()

    infile: TextIOWrapper = args.infile
    outfile: TextIOWrapper = args.outfile
    min_depth: int = args.min_depth

    file_as_json: dict = json.loads("\n".join(infile.readlines()))
    output = {}
    build_output(file_as_json, output, min_depth)

    output_as_json = json.dumps(output, indent=2, sort_keys=True)
    outfile.write(output_as_json)

    print("Parsing complete: " + infile.name)

    infile.close()
    outfile.close()
