import subprocess
import tempfile
import os
import re
import shutil

template = r"""\documentclass{article}
\usepackage[paperwidth=\maxdimen,paperheight=\maxdimen]{geometry}
\pagestyle{empty}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{bytefield}
\begin{document}
\begin{samepage}
\begin{bytefield}{%s}
%s
\end{bytefield}
\end{samepage}
\end{document}
"""
    
def create_tex(message):
    field_text = " & ".join([r'\bitbox{%d}{%s}' % (field.width, field.name) for field in message.fields]) + r' \\'
    tex_data = template % (message.width, field_text)
    print "Created: ", tex_data
    return tex_data

def process(message, image_name):
    tmpdir = tempfile.mkdtemp()
    diagram_tex = os.path.join(tmpdir, "diagram.tex")
    diagram_dvi = os.path.join(tmpdir, "diagram.dvi")

    open(diagram_tex, "w").write(create_tex(message))
    
    os.chdir(os.path.dirname(__file__))
    subprocess.call('latex -halt-on-error -output-directory="%s" "%s"' % (tmpdir, diagram_tex), shell=True)
    subprocess.call('dvipng -q -x "1400" -p "1" --height --depth -T tight --png -z 9 -o "%s" "%s"' % (image_name, 
                                                                                                      diagram_dvi), shell=True)
    shutil.rmtree(tmpdir)


        