import argparse
import os
import shutil
import subprocess
import sys
import tempfile

def take_snapshot(url, screenshot=None, pdf=None, width=1920, height=1200, sandbox=True):
    if screenshot and pdf:
        raise ValueError('Pass either screenshot or PDF; Chrome headless can\'t deal with both at present')
    command = list(filter(None, [
        'google-chrome',
        ('--no-sandbox' if not sandbox else None),
        '--headless',
        '--disable-gpu',
        '--disable-audio',
        '--window-size=%dx%d' % (width, height),
        ('--screenshot=/out/screenshot.png' if screenshot else None),
        ('--print-to-pdf=/out/pdf.pdf' if pdf else None),
        url,
    ]))
    vol_path = tempfile.mkdtemp(dir='/tmp')
    try:
        subprocess.check_call(['docker', 'run', '-it', '-v', '%s:/out' % vol_path, 'chrome-dev'] + command)
        if screenshot:
            shutil.copyfile('%s/screenshot.png' % vol_path, screenshot)
            print('Wrote %s' % screenshot)
        if pdf:
            shutil.copyfile('%s/pdf.pdf' % vol_path, pdf)
            print('Wrote %s' % pdf)
    finally:
        shutil.rmtree(vol_path)


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('--help', action='help')
    ap.add_argument('-w', '--width', default=1920)
    ap.add_argument('-h', '--height', default=1200)
    ap.add_argument('-s', '--screenshot', default=None)
    ap.add_argument('-p', '--pdf', default=None)
    ap.add_argument('--sandbox', dest='sandbox', action='store_true', default=None)
    ap.add_argument('--no-sandbox', dest='sandbox', action='store_false')
    ap.add_argument('url')
    args = ap.parse_args()
    if args.sandbox is None:  # No --sandbox/--no-sandbox set?
        # Docker for Mac's kernel doesn't have userns enabled, so Chrome can't enable its sandbox.
        # Related issue: https://github.com/jessfraz/dockerfiles/issues/65
        # (Let's assume all Mac users are using Docker for Mac.)
        args.sandbox = (sys.platform != 'darwin')
    take_snapshot(**vars(args))


if __name__ == '__main__':
    main()
