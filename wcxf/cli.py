import argparse
import wcxf
import sys
import logging
import os
import yaml


def convert():
    from wcxf.converters.yamljson import convert_json, convert_yaml
    parser = argparse.ArgumentParser(description="""Command line script to convert WCxf files between YAML and JSON.""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("FORMAT", help="Output format (should be yaml or json)", type=str)
    parser.add_argument("FILE", nargs='?', help="Input file. If \"-\", read from standard input",
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument("--output", nargs='?', help="Output file. If absent, print to standard output",
                        type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    if args.FORMAT.lower() == 'json':
        convert_json(args.FILE, args.output)
    if args.FORMAT.lower() == 'yaml':
        convert_yaml(args.FILE, args.output)

def translate():
    parser = argparse.ArgumentParser(description="""Command line script for basis translation of WCxf files.""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("BASIS", help="Output basis", type=str)
    parser.add_argument("FILE", nargs='?', help="Input file. If \"-\", read from standard input",
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument("--output", nargs='?', help="Output file. If absent, print to standard output",
                        type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument("--format", help="Output format (default: json)", type=str, default="json")
    args = parser.parse_args()
    wc_in = wcxf.WC.load(args.FILE)
    wc_out = wc_in.translate(args.BASIS)
    wc_out.dump(stream=args.output, fmt=args.format)

def match():
    parser = argparse.ArgumentParser(description="""Command line script for matching of WCxf files.""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("EFT", help="Output EFT", type=str)
    parser.add_argument("BASIS", help="Output basis", type=str)
    parser.add_argument("FILE", nargs='?', help="Input file. If \"-\", read from standard input",
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument("--output", nargs='?', help="Output file. If absent, print to standard output",
                        type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument("--format", help="Output format (default: json)", type=str, default="json")
    args = parser.parse_args()
    wc_in = wcxf.WC.load(args.FILE)
    wc_out = wc_in.match(args.EFT, args.BASIS)
    wc_out.dump(stream=args.output, fmt=args.format)

def validate():
    parser = argparse.ArgumentParser(description="""Command line script for validation of WCxf files.""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("TYPE", help="Type of file to validate: should be 'eft', 'basis', or 'wc'", type=str)
    parser.add_argument("FILE", nargs='?', help="Input file. If \"-\", read from standard input",
                        type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()
    if args.TYPE == 'eft':
        eft = wcxf.EFT.load(args.FILE)
    elif args.TYPE == 'basis':
        basis = wcxf.Basis.load(args.FILE)
        basis.validate()
    elif args.TYPE == 'wc':
        wc = wcxf.WC.load(args.FILE)
        wc.validate()
    else:
        logging.error("TYPE should be 'eft', 'basis', or 'wc'")
        return 1
    print("Validation successful.")
    return 0

def eos():
    from wcxf.converters.eos import wcxf2eos, get_sm_wcs
    parser = argparse.ArgumentParser(description="""Command line script to convert a WCxf file to an EOS Wilson coefficient parameter file.""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("FILE", nargs='?', help="Input file. If \"-\", read from standard input",
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument("--eosprefix", help="Installation prefix for the EOS installation. Defaults to /usr",
                        default='/usr')
    parser.add_argument("--output", nargs='?', help="Output file. If absent, print to standard output",
                        type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument("--eoshome", help="EOS home directory. If specified, values will be written to EOSHOME/parameters/wcxf.yaml. Cannot be used simultaneously with output",
                        default=None)
    args = parser.parse_args()
    # check sanity of inputs
    if args.output != sys.stdout and args.eoshome is not None:
        logging.error("Cannot use --output and --eoshome arguments simultaneously")
        return 1
    elif args.output == sys.stdout and args.eoshome is not None:
        output_dir = os.path.join(args.eoshome, 'parameters')
        if not os.path.isdir(output_dir):
            logging.error("Output directory {} does not exist".format(output_dir))
            return 1
        f = open(os.path.join(output_dir, 'wcxf.yaml'), 'w')
    else:
        f = args.output
    # read in & validate WCxf file
    wc = wcxf.WC.load(args.FILE)
    wc.validate()
    # read EOS SM contributions
    sm_wc_dict = get_sm_wcs(os.path.join(args.eosprefix, 'share/eos', 'parameters'))
    # convert to EOS parameters
    eos_dict = wcxf2eos(wc, sm_wc_dict)
    yaml.dump(eos_dict, f, default_flow_style=False)
    f.close()
    return 0
