#!/usr/bin/env python
# coding: utf-8

"""Fix the .pdf_tex files produced by inkscape that try to include too many pages.

For a desciption of the bug that makes this necessary, follow this link:
http://tex.stackexchange.com/questions/243499/sharelatex-pdf-inclusion-required-page-does-not-exist-5/268880#268880

Inkscape needs to be in the system path and the Python package PyPDF2 must be installed.

This module exports the folloing functions:
    fix_file    Fix a .pdf_tex file.
    fix_dir     Fix all the .pdf_tex files in a directory.

When executed as a script, the containing directory is fixed.
"""

import argparse
import re
import os
import PyPDF2
import glob
import shutil
import sys


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # # Positional mandatory arguments
    # parser.add_argument("folder", help="PATH/TO/FOLDER/WITH/SVG", type=str)

    # Optional arguments
    parser.add_argument("-oF", "--outputFolder", help="name of folder where files will be stored", type=str,
                        default='LaTeX')
    parser.add_argument("-rF", "--RAWFolder", help="name of folder where SVGs are", type=str,
                        default='RawSVG')
    parser.add_argument("-d", "--duplicate", help="checks in ech `RAWFolder` if SVGs needs to be duplicated with duplicateSVGs.py", type=bool,
                        default=True)

    # Print version
    parser.add_argument("--version", action="version",
                        version='%(prog)s - Version 1.0')

    # Parse arguments
    args = parser.parse_args()

    return args


def fix_dir(dir, check_svg=True):
    countSVG = len(glob.glob(os.path.join(dir, '*.svg')))
    counter = 1
    """Fix all the .pdf_tex files in the directory.
    If check_svg is True, old and missing .pdf and .pdf_tex files will be newly exported.
    """
    print('exporting and fixing the directory', dir[-20:])
    dir_content = os.listdir(dir)
    if check_svg:
        for name in dir_content:
            if name.endswith('.svg'):
                basename = name[:-4]

                if (not (basename + '.pdf' in dir_content and basename + '.pdf_tex' in dir_content)
                        or os.path.getmtime(os.path.join(dir, basename + '.svg')) > os.path.getmtime(os.path.join(dir, basename + '.pdf'))):
                    _export_svg_to_pdf_latex(os.path.join(dir, name))
                    print("working on file number %02d of %02d " %
                          (counter, countSVG))
                    print("---------------------------------------------------------")
                    print("---------------------------------------------------------")
                    sys.stdout.flush()
                counter = counter + 1
        dir_content = os.listdir(dir)
    for name in dir_content:
        if name.endswith('.pdf_tex') and name[:-4] in dir_content:
            # fixes the import of the PDF pages if to many are listed
            fix_file(os.path.join(dir, name))


def fix_file(file, numpages=None):
    """Fix the .pdf_tex file.

    If numpages is not given, it is determined automatically.
    """
    if not file.endswith('.pdf_tex'):
        file += '.pdf_tex'
    if not numpages:
        numpages = _get_pdf_file_num_pages(file[:-4])
    tempfile = file + '.tmp'
    pageincln = re.compile(
        r'\s*\\put\(.*\)\{\\includegraphics\[.*,page=(\d+)\]\{.*\}\}%')
    changed = False
    with open(file, 'r') as rf:
        with open(tempfile, 'w') as wf:
            for line in rf:
                critline = pageincln.match(line)
                if critline and int(critline.groups()[0]) > numpages:
                    changed = True
                    continue
                wf.write(line)
    if changed:
        os.remove(file)
        os.rename(tempfile, file)
        print('fixed', file)
    else:
        os.remove(tempfile)


def _get_pdf_file_num_pages(f):
    pdf = PyPDF2.PdfFileReader(f)
    return pdf.numPages


def _export_svg_to_pdf_latex(f):
    if f.endswith('.svg'):
        f = f[:-4]

    if sys.platform == 'darwin' or sys.platform == 'Darwin':
        command = ('inkscape {0}.svg -z -C --batch-process --export-latex '
                   '--export-type=pdf').format(f)
    else:
        command = 'inkscape -z -C -f{0}.svg -A{0}.pdf --export-latex'.format(f)
    os.system(command)
    print('exported .pdf and .pdf_tex from', f[-20:] + '.svg')
    sys.stdout.flush()


def getFoldersWithRaw(homeDir, rawFolder):
    directory_list = list()
    for root, dirs, files in os.walk(homeDir, topdown=True):
        if rawFolder in dirs:
            directory_list.append(root)
    return directory_list


def main():
    # Parse the arguments
    args = parseArguments()

    #########################################
    homeDir = os.path.dirname(os.path.realpath(__file__))
    print('get folders where *.svg files are')
    sys.stdout.flush()
    workingFolders = getFoldersWithRaw(homeDir, args.RAWFolder)
    ########################
    for dir in workingFolders:
        source_dir = os.path.join(homeDir, dir, args.RAWFolder)
        dst_dir = os.path.join(homeDir, dir, args.outputFolder)

        if args.duplicate and os.path.isfile(os.path.join(homeDir, 'duplicateSVGs.py')):
            command = 'python3 duplicateSVGs.py -f ' + source_dir + \
                ' -o ' + source_dir + ' -a step -s Step'
            os.system(command)

        # check if destination folder already exist
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        # moves existing exports to RAWfolder
        files = glob.glob(os.path.join(dst_dir, "*"))
        for f in files:
            shutil.move(f, source_dir)

        fix_dir(source_dir)

        files_src = glob.glob(os.path.join(source_dir, '*.pdf*'))
        for name in files_src:
            if os.path.isfile(name):
                shutil.move(name, dst_dir)
        files = glob.glob(os.path.join(source_dir, "*"))
        for f in files:
            if not f.endswith('.svg') and not f.endswith('.py'):
                os.remove(f)


if __name__ == '__main__':
    main()
