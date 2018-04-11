"""
Process a scattered latex file into one thing.
"""
import os
import subprocess
import shutil


def process(fname, oname=None, folder=None):
    if oname is None:
        oname = folder + '/' + fname.split('.tex')[0] + '_processed.tex'

    try:
        os.mkdir(folder)
    except OSError:
        pass

    # Export the bib file to a subset
    cmd = 'bibexport -o {}/refs.bib {}.aux'.format(folder, fname.split('.tex')[0])
    subprocess.call(cmd, shell=True)

    f = open(fname, 'r')
    out = open(oname, 'w')

    recurse(f, out, folder)

    f.close()
    out.close()


def process_dependency(out, line, folder):
    f = line.replace('% include --> ', '').strip()
    shutil.copy(f, folder + '/' + f)
    out.write(line)


def process_figure(out, line, folder):
    figf = line.split('{')[1].split('}')[0]
    base = figf.split('/')[-1]
    print('Processing figure:  ' + figf)
    shutil.copy(figf, folder + '/' + base)
    out.write(line.replace(figf, base))


def recurse(f, out, folder):
    for line in f:
        if line.startswith('\\bibliography{'):
            out.write('\\bibliography{refs.bib}')
            continue
        if line.startswith('\includegraphics'):
            process_figure(out, line, folder)
            continue
        if line.startswith('% include --> '):
            process_dependency(out, line, folder)
            continue
        if not line.startswith('\\input{'):
            out.write(line)
            continue

        # deal with inputs

        subf = line.split('{')[1].split('}')[0]

        print(subf)

        with open(subf+'.tex', 'r') as sf:
            out.write('{}  {}  {}\n'.format('%'*10, line[:-1], '%'*10))
            recurse(sf, out, folder)
            out.write('{}  {}  {}\n'.format('%'*10, line[:-1], '%'*10))


if __name__ == '__main__':
    # process('richardseqn_cockett2017.tex', folder='iop_processed')
    process('richardseqn_cockett2017-els.tex', folder='candg_processed')
