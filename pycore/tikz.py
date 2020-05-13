import os
import warnings


def list_to_string(list):
    s = ','.join(str(e) for e in list)
    return s

def start(path='../'):
    header = head(path)
    header += def_colors()
    header += env_begin()
    return header

def head(projectpath):
    pathlayers = os.path.join(projectpath, 'layers/').replace('\\', '/')
    return r'''
\documentclass[border=8pt, multi, tikz]{standalone}
\usepackage{import}
\usepackage{graphicx}
\subimport{''' + pathlayers + r'''}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} %for including external image
'''


# Color definitions
def def_colors():
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
\def\ShortcutColor{rgb: blue, 3; green, 1; white, 5}
\def\MultColor{rgb: magenta, 1}
\def\ConcColor{rgb:red, 5}
\def\input_image{../examples/stop_sign.jpg}
'''


def env_begin():
    return r'''
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++ (0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
'''


# Input Image Layer
def input_image(name, file, to='(-3,0,0)', size=[8, 8]):
    return r'''
\node[canvas is zy plane at x=0] (''' + name + ''') at ''' + to + ''' {\\includegraphics[size[0]=''' + str(size[0]) + '''cm ,height=''' + str(size[1]) + '''cm ]{''' + file + '''}};
'''


# image
def image(name, file, to, size=[8, 8]):
    return r'''
\node[canvas is zy plane at x=0] (''' + name + ''') at (''' + to + r''') {\includegraphics[width=''' + str(size[0]) + '''cm ,height=''' + str(size[1]) + '''cm ]{''' + file + '''}};
'''

def grid(name, to, size=[4, 4], steps=1):
    return r'''
\node[canvas is zy plane at x=0] (''' + name + ''') at (''' + to + r''') {\drawgrid{''' + str(size[0]) + '''}{''' + str(size[1]) + '''}{''' + str(size[1] / steps) + '''}};
'''

# \node[canvas is zy plane at x=0] (image_1) at (conv_82-east) {\includegraphics[width=0.25cm,height=0.25cm]{../examples/fcn8s/cats.jpg}};
# \node[canvas is zy plane at x=2] (image_1_2) at (conv_82-east) {\includegraphics[width=3cm,height=3cm]{../examples/fcn8s/cats.jpg}};
# \node[canvas is zy plane at x=0] (grid) at (image_1_2) {\drawgrid{3}{3}{0.33}};


# Conv
def conv(name, s_filter='', n_filter=(64, 64), offset='(0,0,0)', to='0,0,0', width=(2), size=[40, 40], caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            raise Exception("Size of n_filters does not match size of width")
        xlabel_string = list_to_string(n_filter)
        width_string = list_to_string(width)
    else:
        xlabel_string = str(n_filter)
        width_string = str(width)
    return r'''
\pic[shift={''' + offset + '''}] at (''' + to + ''')
    {Box={
        name=''' + name + ''',
        caption=''' + caption + ''',
        xlabel={(''' + xlabel_string + ''',)},
        zlabel=''' + str(s_filter) + ''',
        fill=\\ConvColor,
        height=''' + str(size[0]) + ''',
        depth=''' + str(size[1]) + ''',
        width={''' + width_string + '''}
        }
    };
'''


# Conv,relu
def conv_relu(name, s_filter='', n_filter='', offset=(0, 0, 0), to='0,0,0', width=(2), size=(40, 40), caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            raise Exception("Size of n_filters does not match size of width")
        xlabel_string = list_to_string(n_filter)
        width_string = list_to_string(width)
    else:
        xlabel_string = str(n_filter)
        width_string = str(width)
    return r'''
\pic[shift={''' + str(offset) + '''}] at (''' + to + ''')
    {RightBandedBox={
        name=''' + name + ''',
        caption=''' + caption + ''',
        xlabel={(''' + xlabel_string + ''',)},
        zlabel=''' + str(s_filter) + ''',
        fill=\\ConvColor,
        bandfill=\\ConvReluColor,
        height=''' + str(size[0]) + ''',
        depth=''' + str(size[1]) + ''',
        width={''' + width_string + '''}
        }
    };
'''

# Conv,relu
def upsample(name, s_filter='', n_filter=(), offset=(0,0,0), to='0,0,0', width=(2),
             size_1=(40, 40), size_2=(80, 80), caption=' '):
    return r'''
\pic[shift={''' + str(offset) + '''}] at (''' + to + ''')
    {Box={
        name=''' + name + '''_0,
        fill=\\UpsampleColor,
        height=''' + str(size_1[0]) + ''',
        depth=''' + str(size_1[1]) + r''',
        width={1}
        }
    };
\pic[shift={''' + str(offset) + '''}] at (''' + name + '''_0-east)
    {Box={
        name=''' + name + ''',
        fill=\\UpsampleColor,
        height=''' + str(size_2[0]) + ''',
        depth=''' + str(size_2[1]) + r''',
        width={1}
        }
    };
\draw[densely dashed]
    (''' + name + '''_0-nearnortheast) coordinate(a) -- (''' + name + '''-nearnorthwest)
    (''' + name + '''_0-nearsoutheast) coordinate(b) -- (''' + name + '''-nearsouthwest)
    (''' + name + '''_0-farsoutheast) coordinate(c) -- (''' + name + '''-farsouthwest)
    (''' + name + '''_0-farnortheast) coordinate(d) -- (''' + name + '''-farnorthwest)

    (a)--(b)--(c)--(d)
    ;
'''


# Pool
def pool(name, offset='(0,0,0)', to='(0,0,0)', width=1, height=32, depth=32, opacity=0.5, caption=' '):
    return r'''
\pic[shift={''' + offset + '''}] at (''' + to + ''')
    {Box={
        name=''' + name + ''',
        caption=''' + caption + r''',
        fill=\PoolColor,
        opacity=''' + str(opacity) + ''',
        height=''' + str(height) + ''',
        width=''' + str(width) + ''',
        depth=''' + str(depth) + '''
        }
    };
'''

# Detect
def detect(name, s_filter='', n_filter=(64, 64), offset='(0,0,0)', to='0,0,0', width=(2), size=(40, 40), caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            warnings.warn('Size of n_filters does not match size of width')
        width_string = list_to_string(width)
    else:
        width_string = str(width)
    return r'''
\pic[shift={''' + offset + '''}] at (''' + to + ''')
    {Box={
        name=''' + name + ''',
        caption=''' + caption + ''',
        zlabel=''' + str(s_filter) + ''',
        fill=\\DetectColor,
        height=''' + str(size[0]) + ''',
        depth=''' + str(size[1]) + ''',
        width={''' + width_string + '''}
        }
    };
'''


# Unpool4,
def unpool(name, offset='(0,0,0)', to='(0,0,0)', width=1, height=32, depth=32, opacity=0.5, caption=' '):
    return r'''
\pic[shift={ ''' + offset + ''' }] at ''' + to + '''
    {Box={
        name=''' + name + ''',
        caption=''' + caption + r''',
        fill=\UnpoolColor,
        opacity=''' + str(opacity) + ''',
        height=''' + str(height) + ''',
        width=''' + str(width) + ''',
        depth=''' + str(depth) + '''
        }
    };
'''


# Convolution, resize
def conv_res(name, s_filter=256, n_filter=64, offset='(0,0,0)', to='(0,0,0)', width=6, height=40, depth=40, opacity=0.2, caption=' '):
    return r'''
\pic[shift={ ''' + offset + ''' }] at ''' + to + '''
    {RightBandedBox={
        name=''' + name + ''',
        caption=''' + caption + ''',
        xlabel={{''' + str(n_filter) + '''}},
        zlabel=''' + str(s_filter) + r''',
        fill={rgb:white,1;black,3},
        bandfill={rgb:white,1;black,2},
        opacity=''' + str(opacity) + ''',
        height=''' + str(height) + ''',
        width=''' + str(width) + ''',
        depth=''' + str(depth) + '''
        }
    };
'''


# ConvSoftMax
def conv_soft_max(name, s_filter=40, offset='(0,0,0)', to='(0,0,0)', width=1, height=40, depth=40, caption=' '):
    return r'''
\pic[shift={''' + offset + '''}] at ''' + to + '''
    {Box={
        name=''' + name + ''',
        caption=''' + caption + ''',
        zlabel=''' + str(s_filter) + ''',
        fill=\\SoftmaxColor,
        height=''' + str(height) + ''',
        width=''' + str(width) + ''',
        depth=''' + str(depth) + '''
        }
    };
'''

# SoftMax
def soft_max(name, s_filter=10, offset='(0,0,0)', to='(0,0,0)', width=1.5, height=3, depth=25, opacity=0.8, caption=' '):
    return r'''
\\pic[shift={''' + offset + '''}] at ''' + to + '''
    {Box={
        name=''' + name + ''',
        caption=''' + caption + ''',
        xlabel={{' ','dummy'}},
        zlabel=''' + str(s_filter) + ''',
        fill=\\SoftmaxColor,
        opacity=''' + str(opacity) + ''',
        height=''' + str(height) + ''',
        width=''' + str(width) + ''',
        depth=''' + str(depth) + '''
        }
    };
'''


# shortcut
def shortcut(name, s_filter='', n_filter=(64, 64), offset='(0,0,0)', to='0,0,0', width=(1), size=[40, 40], caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            warnings.warn('Size of n_filters does not match size of width')
        width_string = list_to_string(width)
    else:
        width_string = str(width)
    return r'''
\pic[shift={''' + offset + '''}] at (''' + to + ''')
    {Box={
        name=''' + name + ''',
        caption=''' + caption + ''',
        zlabel=''' + str(s_filter) + ''',
        fill=\\ShortcutColor,
        height=''' + str(size[0]) + ''',
        depth=''' + str(size[1]) + ''',
        width={''' + width_string + '''}
        }
    };
'''


# Short straight connection
def short_connection(of, to, anchor_of='-east', anchor_to='-west'):
    return r'''
\draw [connection] (''' + of + anchor_of + ''') -- node {\\midarrow} (''' + to + anchor_to + ''');
'''


# Long connection
def long_connection(of, to, pos=1.25, anchor_of_1='-south', anchor_of_2='-north', anchor_to='-north'):
    return r'''
\path (''' + of + anchor_of_1 + ''') -- (''' + of + anchor_of_2 + ''') coordinate[pos=''' + str(pos) + '''] (''' + of + r'''-dummy) ;
\path (''' + of + '''-dummy |- ''' + to + anchor_to + ''') coordinate (''' + to + r'''-dummy)  ;

\draw [connection] (''' + of + anchor_of_2 + ''')
-- node {}(''' + of + anchor_of_2 + ''' |- ''' + of + '''-dummy)
-- node {\\midarrow}(''' + of + '''-dummy -| ''' + to + anchor_to + ''')
-- node {}(''' + to + anchor_to + ''');
'''


# Skip connection
def skip(of, to, pos=1.25):
    return r'''
\path (''' + of + '''-southeast) -- (''' + of + '''-northeast) coordinate[pos=''' + str(pos) + '''] (''' + of + r'''-top) ;
\path (''' + to + '''-south)  -- (''' + to + '''-north)  coordinate[pos=''' + str(pos) + '''] (''' + to + r'''-top) ;
\draw [copyconnection]  (''' + of + '''-northeast)
-- node {\\copymidarrow}(''' + of + '''-top)
-- node {\\copymidarrow}(''' + to + '''-top)
-- node {\\copymidarrow} (''' + to + '''-north);
'''


# Add ball
def add(name, to, offset='(1,0,0)', opacity=0.4, caption=''):
    return r'''
\pic[shift={''' + offset + '''}] at (''' + to + '''-east)
    {Ball={
        name=''' + name + ''',
        caption=''' + caption + ''',
        fill=\\SumColor,
        opacity=''' + str(opacity) + ''',
        radius=2.5,
        logo=$+$
        }
    };
'''


# Multiply ball
def multiply(name, to, offset='(1,0,0)', opacity=0.6, caption='', ):
    return r'''
\pic[shift={''' + offset + '''}] at (''' + to + '''-east)
    {Ball={
        name=''' + name + ''',
        caption=''' + caption + ''',
        fill=\\MultColor,
        opacity=''' + str(opacity) + ''',
        radius=2.5,
        logo=$\\times$
        }
    };
'''


# Concatenate ball
def concatenate(name, to, offset='(1,0,0)', opacity=0.6, caption=''):
    return r'''
\pic[shift={''' + offset + '''}] at (''' + to + '''-east)
    {Ball={
        name=''' + name + ''',
        caption=''' + caption + ''',
        fill=\\ConcColor,
        opacity=''' + str(opacity) + ''',
        radius=2,
        logo=$\\oplus$
        }
    };
'''


def resample(of, to):
    return r'''
\draw[densely dashed]
    (''' + of + '''-nearnortheast) coordinate(a) -- (''' + to + '''-nearnorthwest)
    (''' + of + '''-nearsoutheast) coordinate(b) -- (''' + to + '''-nearsouthwest)
    (''' + of + '''-farsoutheast) coordinate(c) -- (''' + to + '''-farsouthwest)
    (''' + of + '''-farnortheast) coordinate(d) -- (''' + to + '''-farnorthwest)
    ;
'''


def ellipsis(of, to, offset='(0.5,0,0)'):
    return r'''
\draw [connection] (''' + of + r'''-east) -- node [fill=white,inner sep=1pt, opacity=1] {\ldots} (''' + to + '''-west);
'''


# End document
def env_end():
    return r'''
\end{tikzpicture}
\end{document}
'''

def legend():
    return r'''
\pic[shift={(0, -3, 0)}] at (image_0.south)
    {RightBandedBox={
        name=legend_1,
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height=5.0,
        depth=5.0,
        width={1.0}
    }
};
\node [shift={(1,0,0)}, anchor=west] at (legend_1-east) {\LARGE{Convolution layer}};

\pic[shift={(0, -1, 0)}] at (legend_1-southwest)
{Box={
        name=legend_2,
        fill=\ShortcutColor,
        height=5.0,
        depth=5.0,
        width={1}
    }
};
\node [shift={(1,0,0)}, anchor=west] at (legend_2-east) {\LARGE{Shortcut layer}};

\pic[shift={(0, -1, 0)}] at (legend_2-southwest)
{Box={
        name=legend_3,
        fill=\DetectColor,
        height=5.0,
        depth=5.0,
        width={1}
    }
};
\node [shift={(1,0,0)}, anchor=west] at (legend_3-east) {\LARGE{Detection layer}};

\pic[shift={(0, -1, 0)}] at (legend_3-southwest)
{Box={
        name=legend_4,
        fill=\UpsampleColor,
        height=5.0,
        depth=5.0,
        width={1}
    }
};
\node [shift={(1,0,0)}, anchor=west] at (legend_4-east) {\LARGE{Upsample layer}};

\pic[shift={(0,-1,0)}] at (legend_4-south)
{Ball={
        name=legend_5,
        caption=,
        fill=\ConcColor,
        opacity=0.6,
        radius=2,
        logo=$\oplus$
    }
};
\node [shift={(0.75,0,0)}, anchor=west] at (legend_5-east) {\LARGE{Concatenation}};

\node[draw=black,ultra thick,inner sep=2ex,circle] (circle) at (yolo_83-anchor) {};
\node[shift={(2.5,-5,0)}](image_yolo) at (circle) {\scalebox{-1}[1]{\includegraphics[width=5cm,height=5cm]{\input_image}}};
\node(grid_yolo_1) at (image_yolo) {\drawgrid{5}{5}{0.384615385}};
\node[canvas is zy plane at x=0] (grid_yolo_1) at (image_yolo_83) {\drawgrid{0.25}{0.25}{1.0}};
\node[draw=black,ultra thick,inner sep=2.5cm,rectangle] (rectangle) at (image_yolo) {};
\node[anchor=north] at (rectangle.south) {$13\times13$ grid};
\draw[ultra thick] (circle.south east) -- (rectangle.north);
'''
