import argparse
import logging
import sys
import pyexamples
import os
import pycore.execute as execute

log = logging.getLogger(__name__)

def get_arch(arch):
    return ('pyexamples.' + arch + '.create_architecture()')


if __name__ == '__main__':

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    parser_ = argparse.ArgumentParser(description='Parameters')

    parser_.add_argument('--arch', type=str, default='HRNet',
                         help='The architecture to build.')
    parser_.add_argument('--pdf', type=bool, default=False,
                         help='Build and open pdf file')
    parser_.add_argument('--out', type=str, default='output',
                         help='Output directory')
    args = parser_.parse_args()
    creator = get_arch(args.arch)
    log.info(creator)
    arch = eval(creator)
    log.info('created architecture')
    content = execute.build_architecture(arch)
    if not os.path.isdir(args.out):
        os.makedirs(args.out)
    file_name = args.out
    execute.write_tex(content, os.path.join(args.out, args.arch + '.tex'))
    log.info('tex data written to {}'.format(os.path.join(args.out, args.arch + '.tex')))
    if args.pdf:
        log.info('creating pdf data')
        execute.tex_to_pdf(file=args.arch + '.tex', folder=args.out)
        log.info('opening pdf file {}'.format(os.path.join(args.out, args.arch + '.pdf')))
        if sys.platform.startswith('linux'):
            execute.open_pdf('xdg-open', os.path.join(args.out, args.arch + '.pdf'))
        elif sys.platform.startswith('win32'):
            os.startfile(os.path.join(args.out, args.arch + '.pdf'))
        elif sys.platform.startswith('macos'):
            execute.open_pdf('open', os.path.join(args.out, args.arch + '.pdf'))
