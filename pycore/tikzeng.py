
import os

def to_head(projectpath):
    pathlayers = os.path.join(projectpath, 'layers/').replace('\\', '/')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone}
\usepackage{import}
\subimport{"""+ pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} %for including external image
"""

def to_cor():
    return r"""
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:magenta,5;black,7}
\def\SumColor{rgb:green, 1}
\def\MultColor{rgb: magenta, 1}
\def\ConcColor{rgb:red, 5}
"""

def to_begin():
    return r"""
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
"""

# layers definition

def to_input(pathfile, to='(-3,0,0)', width=8, height=8, name="temp"):
    return r"""
\node[canvas is zy plane at x=0] (""" + name + """) at """+ to +""" {\includegraphics[width="""+ str(width)+"cm"+""",height="""+ str(height)+"cm"+"""]{"""+ pathfile +"""}};
"""

# Conv
def to_Conv(name, s_filter=256, n_filter=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +"""
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filter) +""", }},
        zlabel="""+ str(s_filter) +""",
        fill=\ConvColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# Conv,Conv,relu
# Bottleneck
def to_ConvConvRelu(name, s_filter=256, n_filter=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +"""
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(n_filter[0]) +""", """+ str(n_filter[1]) +""" }},
        zlabel="""+ str(s_filter) +""",
        fill=\\ConvColor,
        bandfill=\\ConvReluColor,
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""



# Pool
def to_Pool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +"""
    {Box={
        name="""+name+""",
        caption="""+ caption +r""",
        fill=\PoolColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# unpool4,
def to_UnPool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +"""
    {Box={
        name="""+ name +r""",
        caption="""+ caption +r""",
        fill=\UnpoolColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""



def to_ConvRes(name, s_filter=256, n_filter=64, offset="(0,0,0)", to="(0,0,0)", width=6, height=40, depth=40, opacity=0.2, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +"""
    {RightBandedBox={
        name="""+ name + """,
        caption="""+ caption + """,
        xlabel={{ """+ str(n_filter) + """, }},
        zlabel="""+ str(s_filter) +r""",
        fill={rgb:white,1;black,3},
        bandfill={rgb:white,1;black,2},
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""


# ConvSoftMax
def to_ConvSoftMax(name, s_filter=40, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +"""
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        zlabel="""+ str(s_filter) +""",
        fill=\\SoftmaxColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# SoftMax
def to_SoftMax(name, s_filter=10, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=3, depth=25, opacity=0.8, caption=" "):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +"""
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        xlabel={{" ","dummy"}},
        zlabel="""+ str(s_filter) +""",
        fill=\\SoftmaxColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""


def to_short_connection(of, to):
    return r"""
\draw [connection]  ("""+of+"""-east) -- node {\\midarrow} ("""+to+"""-west);
"""


def to_long_connection(of, to):
    return r"""
\path ("""+ of +"""-southeast) -- ("""+ of +"""-northeast) coordinate[pos=1.25] ("""+ of +"""-top) ;
\path ("""+ of +"""-top |- """+ to +"""-north) coordinate ("""+ to +"""-top)  ;

\draw [connection]  ("""+ of +"""-northeast)
-- node {\midline}("""+ of +"""-northeast |- """+ of +"""-top)
-- node {\midarrow}("""+ of +"""-top -| """+ to +"""-north)
-- node {\midline}("""+ to +"""-north);
"""


def to_skip(of, to, pos=1.25):
    return r"""
\path ("""+ of +"""-southeast) -- ("""+ of +"""-northeast) coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-top) ;
\path ("""+ to +"""-south)  -- ("""+ to +"""-north)  coordinate[pos="""+ str(pos) +"""] ("""+ to +"""-top) ;
\draw [copyconnection]  ("""+of+"""-northeast)
-- node {\copymidarrow}("""+of+"""-top)
-- node {\copymidarrow}("""+to+"""-top)
-- node {\copymidarrow} ("""+to+"""-north);
"""

def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""


def to_add(name, to, offset="(1,0,0)", opacity=0.4, caption=''):
    return r"""
\pic[shift={""" + offset + """}] at (""" + to + """-east)
    {Ball={
        name=""" + name +""",
        caption=""" + caption + """,
        fill=\\SumColor,
        opacity=""" + str(opacity) + """,
        radius=2.5,
        logo=$+$
        }
    };
"""


def to_multiply(name, to, offset="(1,0,0)", opacity=0.5, caption=''):
    return r"""
\pic[shift={"""+ offset +"""}] at ("""+ to +"""-east)
    {Ball={
        name=""" + name + """,
        caption="""+ caption + """,
        fill=\\MultColor,
        opacity=""" + str(opacity) + """,
        radius=2.5,
        logo=$\\times$
        }
    };
"""

def to_concatenate(name, to, offset="(1,0,0)", opacity=0.5, caption=''):
    return r"""
\pic[shift={"""+ offset +"""}] at ("""+ to +"""-east)
    {Ball={
        name=""" + name + """,
        caption=""" + caption + """,
        fill=\\ConcColor,
        opacity=""" + str(opacity) + """,
        radius=2.5,
        logo=$\\oplus$
        }
    };
"""


def to_generate(arch, pathname="file.tex"):
    with open(pathname, "w") as f:
        for c in arch:
            print(c)
            f.write(str(c))
