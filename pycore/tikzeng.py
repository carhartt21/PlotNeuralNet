import os, warnings


def listToString(list):
    s = ','.join(str(e) for e in list)
    return s

def to_Start(path='../'):
    header = to_Head(path)
    header += to_Color()
    header += to_Begin()
    return header

def to_Head(projectpath):
    pathlayers = os.path.join(projectpath, 'layers/').replace('\\', '/')
    return r'''
\documentclass[border=8pt, multi, tikz]{standalone}
\usepackage{import}
\subimport{'''+ pathlayers + r'''}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} %for including external image
'''


# Color definitions
def to_Color():
    return r'''
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UpsampleColor{rgb:green,5; white,2}
\def\DetectColor{rgb:red,5; white,2}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:magenta,5;black,7}
\def\SumColor{rgb:green, 1}
\def\MultColor{rgb: magenta, 1}
\def\ConcColor{rgb:red, 5}
'''


def to_Begin():
    return r'''
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
'''


# Layer definition
def to_Input(pathfile, to='(-3,0,0)', width=8, height=8, name='temp'):
    return r'''
\node[canvas is zy plane at x=0] (''' + name + ''') at '''+ to +''' {\includegraphics[width='''+ str(width)+'cm'+''',height='''+ str(height)+'cm'+''']{'''+ pathfile +'''}};
'''


# Conv
def to_Conv(name, s_filter='', n_filter=(64, 64), offset='(0,0,0)', to='0,0,0', width=(2), size=(40,40), caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            warnings.warn('Size of n_filters does not match size of width');
        xlabel_string = listToString(n_filter)
        width_string = listToString(width)
    else:
        xlabel_string = str(n_filter)
        width_string = str(width)
    return r'''
\pic[shift={'''+ offset +'''}] at ('''+ to +''')
    {Box={
        name=''' + name +''',
        caption='''+ caption +r''',
        xlabel={('''+ xlabel_string +''',)},
        zlabel='''+ str(s_filter) +''',
        fill=\\ConvColor,
        height='''+ str(size[0]) +''',
        depth='''+ str(size[1]) +''',
        width={'''+ width_string +'''}
        }
    };
'''


# Conv,relu
def to_ConvRelu(name, s_filter='', n_filter=(), offset='(0,0,0)', to='0,0,0', width=(2), size=(40,40), caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            warnings.warn('Size of n_filters does not match size of width');
        xlabel_string = listToString(n_filter)
        width_string = listToString(width)
    else:
        xlabel_string = str(n_filter)
        width_string = str(width)
    return r'''
\pic[shift={'''+ offset +'''}] at ('''+ to +''')
    {RightBandedBox={
        name=''' + name +''',
        caption='''+ caption +r''',
        xlabel={('''+ xlabel_string +''',)},
        zlabel='''+ str(s_filter) +''',
        fill=\\ConvColor,
        bandfill=\\ConvReluColor,
        height='''+ str(size[0]) +''',
        depth='''+ str(size[1]) +''',
        width={'''+ width_string +'''}
        }
    };
'''

# Conv,relu
def to_Upsample(name, s_filter='', n_filter=(), offset='(0,0,0)', to='0,0,0', width=(2), size=(40,40), caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            warnings.warn('Size of n_filters does not match size of width');
        xlabel_string = listToString(n_filter)
        width_string = listToString(width)
    else:
        xlabel_string = str(n_filter)
        width_string = str(width)
    return r'''
\pic[shift={'''+ offset +'''}] at ('''+ to +''')
    {Box={
        name=''' + name +''',
        caption='''+ caption +r''',
        xlabel={('''+ xlabel_string +''',)},
        zlabel='''+ str(s_filter) +''',
        fill=\\UpsampleColor,
        height='''+ str(size[0]) +''',
        depth='''+ str(size[1]) +''',
        width={'''+ width_string +'''}
        }
    };
'''


# Pool
def to_Pool(name, offset='(0,0,0)', to='(0,0,0)', width=1, height=32, depth=32, opacity=0.5, caption=' '):
    return r'''
\pic[shift={'''+ offset +'''}] at ('''+ to +''')
    {Box={
        name='''+name+''',
        caption='''+ caption +r''',
        fill=\PoolColor,
        opacity='''+ str(opacity) +''',
        height='''+ str(height) +''',
        width='''+ str(width) +''',
        depth='''+ str(depth) +'''
        }
    };
'''

# Detect
def to_Detect(name, s_filter='', n_filter=(64, 64), offset='(0,0,0)', to='0,0,0', width=(2), size=(40,40), caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            warnings.warn('Size of n_filters does not match size of width');
        xlabel_string = listToString(n_filter)
        width_string = listToString(width)
    else:
        xlabel_string = str(n_filter)
        width_string = str(width)
    return r'''
\pic[shift={'''+ offset +'''}] at ('''+ to +''')
    {Box={
        name=''' + name +''',
        caption='''+ caption +r''',
        xlabel={('''+ xlabel_string +''',)},
        zlabel='''+ str(s_filter) +''',
        fill=\\DetectColor,
        height='''+ str(size[0]) +''',
        depth='''+ str(size[1]) +''',
        width={'''+ width_string +'''}
        }
    };
'''


# Unpool4,
def to_UnPool(name, offset='(0,0,0)', to='(0,0,0)', width=1, height=32, depth=32, opacity=0.5, caption=' '):
    return r'''
\pic[shift={ '''+ offset +''' }] at '''+ to +'''
    {Box={
        name='''+ name +r''',
        caption='''+ caption +r''',
        fill=\UnpoolColor,
        opacity='''+ str(opacity) +''',
        height='''+ str(height) +''',
        width='''+ str(width) +''',
        depth='''+ str(depth) +'''
        }
    };
'''


# Conv, resize
def to_ConvRes(name, s_filter=256, n_filter=64, offset='(0,0,0)', to='(0,0,0)', width=6, height=40, depth=40, opacity=0.2, caption=' '):
    return r'''
\pic[shift={ '''+ offset +''' }] at '''+ to +'''
    {RightBandedBox={
        name='''+ name + ''',
        caption='''+ caption + ''',
        xlabel={{'''+ str(n_filter) + '''}},
        zlabel='''+ str(s_filter) +r''',
        fill={rgb:white,1;black,3},
        bandfill={rgb:white,1;black,2},
        opacity='''+ str(opacity) +''',
        height='''+ str(height) +''',
        width='''+ str(width) +''',
        depth='''+ str(depth) +'''
        }
    };
'''


# ConvSoftMax
def to_ConvSoftMax(name, s_filter=40, offset='(0,0,0)', to='(0,0,0)', width=1, height=40, depth=40, caption=' '):
    return r'''
\pic[shift={'''+ offset +'''}] at '''+ to +'''
    {Box={
        name=''' + name +''',
        caption='''+ caption +''',
        zlabel='''+ str(s_filter) +''',
        fill=\\SoftmaxColor,
        height='''+ str(height) +''',
        width='''+ str(width) +''',
        depth='''+ str(depth) +'''
        }
    };
'''

# SoftMax
def to_SoftMax(name, s_filter=10, offset='(0,0,0)', to='(0,0,0)', width=1.5, height=3, depth=25, opacity=0.8, caption=' '):
    return r'''
\pic[shift={'''+ offset +'''}] at '''+ to +'''
    {Box={
        name=''' + name +''',
        caption='''+ caption +''',
        xlabel={{' ','dummy'}},
        zlabel='''+ str(s_filter) +''',
        fill=\\SoftmaxColor,
        opacity='''+ str(opacity) +''',
        height='''+ str(height) +''',
        width='''+ str(width) +''',
        depth='''+ str(depth) +'''
        }
    };
'''


# Short straight connection
def to_ShortConnection(of, to, anchor_of='-east', anchor_to='-west'):
    return r'''
\draw [connection]  ('''+of+anchor_of+''') -- node {\\midarrow} ('''+to+anchor_to+''');
'''


# Long connection going around
def to_LongConnection(of, to):
    return r'''
\path ('''+ of +'''-southeast) -- ('''+ of +'''-northeast) coordinate[pos=1.25] ('''+ of +'''-top) ;
\path ('''+ of +'''-top |- '''+ to +'''-north) coordinate ('''+ to +'''-top)  ;

\draw [connection]  ('''+ of +'''-northeast)
-- node {\midline}('''+ of +'''-northeast |- '''+ of +'''-top)
-- node {\midarrow}('''+ of +'''-top -| '''+ to +'''-north)
-- node {\midline}('''+ to +'''-north);
'''


# Skip connection
def to_Skip(of, to, pos=1.25):
    return r'''
\path ('''+ of +'''-southeast) -- ('''+ of +'''-northeast) coordinate[pos='''+ str(pos) +'''] ('''+ of +'''-top) ;
\path ('''+ to +'''-south)  -- ('''+ to +'''-north)  coordinate[pos='''+ str(pos) +'''] ('''+ to +'''-top) ;
\draw [copyconnection]  ('''+of+'''-northeast)
-- node {\copymidarrow}('''+of+'''-top)
-- node {\copymidarrow}('''+to+'''-top)
-- node {\copymidarrow} ('''+to+'''-north);
'''


# Add ball
def to_Add(name, to, offset='(1,0,0)', opacity=0.4, caption=''):
    return r'''
\pic[shift={''' + offset + '''}] at (''' + to + '''-east)
    {Ball={
        name=''' + name +''',
        caption=''' + caption + ''',
        fill=\\SumColor,
        opacity=''' + str(opacity) + ''',
        radius=2.5,
        logo=$+$
        }
    };
'''


# Multiply ball
def to_Multiply(name, to, offset='(1,0,0)', opacity=0.5, caption=''):
    return r'''
\pic[shift={'''+ offset +'''}] at ('''+ to +'''-east)
    {Ball={
        name=''' + name + ''',
        caption='''+ caption + ''',
        fill=\\MultColor,
        opacity=''' + str(opacity) + ''',
        radius=2.5,
        logo=$\\times$
        }
    };
'''


# Concatenate ball
def to_Concatenate(name, to, offset='(1,0,0)', opacity=0.5, caption=''):
    return r'''
\pic[shift={'''+ offset +'''}] at ('''+ to +'''-east)
    {Ball={
        name=''' + name + ''',
        caption=''' + caption + ''',
        fill=\\ConcColor,
        opacity=''' + str(opacity) + ''',
        radius=2.5,
        logo=$\\oplus$
        }
    };
'''


def to_Resample(of, to):
    return r'''
    \draw[densely dashed]
    ('''+of+'''-nearnortheast) coordinate(a) -- ('''+to+'''-nearnorthwest)
    ('''+of+'''-nearsoutheast) coordinate(b) -- ('''+to+'''-nearsouthwest)
    ('''+of+'''-farsoutheast) coordinate(c) -- ('''+to+'''-farsouthwest)
    ('''+of+'''-farnortheast) coordinate(d) -- ('''+to+'''-farnorthwest)

    (a)--(b)--(c)--(d)
    ;
'''


def to_Ellipsis(of, name, offset='(0.5,0,0)'):
    return r'''
\node [shift={'''+offset+'''}] at ('''+of+'''-east) ('''+name+''') {\\ldots};
'''


# End document
def to_End():
    return r'''
\end{tikzpicture}
\end{document}
'''


def to_Generate(arch, pathname='file.tex'):
    with open(pathname, 'w') as f:
        for c in arch:
            # print(c)
            f.write(str(c))
