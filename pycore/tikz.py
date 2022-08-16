import os
import warnings
from math import log



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
\usetikzlibrary{decorations,shapes}
\usetikzlibrary{decorations.shapes}
\usetikzlibrary{decorations.markings}
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
\def\input_image{../examples/input_image.jpg}
\def\output_image{../examples/output_image.png}
\def\skyseg{../examples/sky_segmentation.png}
'''


def env_begin():
    return r'''
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++ (0.3,0);}

\begin{document}
    \begin{tikzpicture}
        \tikzstyle{fillwhite} = [fill=white,inner sep=0pt, opacity=1]
        \tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
        \tikzstyle{fuseconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw=orange, decorate,decoration={markings,
            mark connection node=my node,
            mark=at position .8 with
            {\node [draw, fill=orange, rectangle, minimum height = 4mm, minimum width=1mm,
            transform shape, inner sep=0pt] (my node) {};}}], opacity=0.7]

        %\tikzstyle{fuseconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw=orange, decorate,decoration={shape backgrounds,shape=signal, shape size=.2mm, shape sep={2mm, between borders}}, signal from=west, signal pointer angle = 5]
        %\tikzstyle{fuseconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw=orange]
        \tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
'''


# Input Image Layer
def input_image(name, file, to='(-3,0,0)', size=[8, 8], x_shift=1):
    return r'''
        \node[canvas is zy plane at x=''' + x_shift + '''](''' + name + ''') at ''' + to + ''' {\\includegraphics[size[0] = ''' + str(size[0]) + '''cm, height = ''' + str(size[1]) + '''cm]{''' + file + '''}};
'''


# image
def image(name, file, to, size=[8, 8], x_shift=1):
    return r'''
        \node[canvas is zy plane at x=''' + str(x_shift) + '''] (''' + name + ''') at (''' + to + r''') {\includegraphics[width=''' + str(size[0]) + '''cm ,height=''' + str(size[1]) + '''cm ]{''' + file + '''}};
'''

def grid(name, to, size=[4, 4], steps=1):
    return r'''
        \node[canvas is zy plane at x=0] (''' + name + ''') at (''' + to + r''') {\drawgrid{''' + str(size[0]) + '''}{''' + str(size[1]) + '''}{''' + str(size[1] / steps) + '''}};
'''

# \node[canvas is zy plane at x=0] (image_1) at (conv_82-east) {\includegraphics[width=0.25cm,height=0.25cm]{../examples/fcn8s/cats.jpg}};
# \node[canvas is zy plane at x=2] (image_1_2) at (conv_82-east) {\includegraphics[width=3cm,height=3cm]{../examples/fcn8s/cats.jpg}};
# \node[canvas is zy plane at x=0] (grid) at (image_1_2) {\drawgrid{3}{3}{0.33}};


# Conv
def conv(name, z_label='', n_filter=(64, 64), offset=(0, 0, 0), to='0,0,0', width=(2), size=[40, 40], caption=' '):
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
            {Box={
                name=''' + name + ''',
                caption=''' + caption + ''',
                xlabel={(''' + xlabel_string + ''',)},
                zlabel=''' + str(z_label) + ''',
                fill=\\ConvColor,
                height=''' + str(size[0]) + ''',
                depth=''' + str(size[1]) + ''',
                width={''' + width_string + '''}
                }
            };
'''

# fully_connected_convolution block
def full_con(name, z_label='', n_filter=(64, 64), offset=(0, 0, 0), to='0,0,0', width=(2), size=[40, 40], caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            raise Exception("Size of n_filters does not match size of width")
        xlabel_string = list_to_string(n_filter)
        width_string = list_to_string(width)
    else:
        width = log(n_filter)
        xlabel_string = str(n_filter)
        width_string = str(width)
    return r'''
        \pic[shift={''' + str(offset) + '''}] at (''' + to + ''')
            {Box={
                name=''' + name + ''',
                caption=''' + caption + ''',
                xlabel={(''' + xlabel_string + ''',)},
                zlabel=''' + str(z_label) + ''',
                fill=\\UpsampleColor,
                height=''' + str(size[0]) + ''',
                width=''' + width_string + ''',
                depth={''' + str(size[1]) + '''}
                }
            };
'''




# Conv,relu
def conv_relu(name, z_label='', n_filter='', offset=(0, 0, 0), to='0,0,0', width=(2), size=(40, 40), caption=' ', label = True, options=''):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            raise Exception("Size of n_filters does not match size of width")
        xlabel_string = list_to_string(n_filter)
        width_string = list_to_string(width)
    else:
        xlabel_string = str(n_filter)
        width_string = str(width)
    if not label:
        xlabel_string = ''
    return r'''
        \pic[shift={''' + str(offset) + '''}, ''' + options + '''] at (''' + to + ''')
            {RightBandedBox={
                name=''' + name + ''',
                caption=''' + caption + ''',
                xlabel={(''' + xlabel_string + ''',)},
                zlabel=''' + str(z_label) + ''',
                fill=\\ConvColor,
                bandfill=\\ConvReluColor,
                height=''' + str(size[0]) + ''',
                depth=''' + str(size[1]) + ''',
                width={''' + width_string + '''}
                }
            };
'''


def rtl_conv_relu(name, z_label='', n_filter='', offset=(0, 0, 0), to='0,0,0', width=(2), size=(40, 40), caption=' ', options=''):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            raise Exception("Size of n_filters does not match size of width")
        xlabel_string = list_to_string(n_filter)
        width_string = list_to_string(width)
    else:
        xlabel_string = str(n_filter)
        width_string = str(width)
    return r'''
        \pic[shift={''' + str(offset) + '''}, '''+ options +'''] at (''' + to + ''')
            {LeftBandedBox={
                name=''' + name + ''',
                caption=''' + caption + ''',
                xlabel={(''' + xlabel_string + ''',)},
                zlabel=''' + str(z_label) + ''',
                fill=\\ConvColor,
                bandfill=\\ConvReluColor,
                height=''' + str(size[0]) + ''',
                depth=''' + str(size[1]) + ''',
                width={''' + width_string + '''}
                }
            };
'''


def z_conv_relu(name, z_label='', n_filter='', offset=(0, 0, 0), to='0,0,0', width=2, size=(40, 40), caption=' ', options=''):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            raise Exception("Size of n_filters does not match size of width")
        xlabel_string = list_to_string(n_filter)
        width_string = list_to_string(width)
    else:
        xlabel_string = str(n_filter)
        width_string = str(log(n_filter, 4))
    return r'''
        \pic[shift={''' + str(offset) + '''}, ''' + options + '''] at (''' + to + ''')
            {BandedBox={
                name=''' + name + ''',
                caption=''' + caption + ''',
                xlabel={(''' + xlabel_string + ''',)},
                zlabel=''' + str(z_label) + ''',
                fill=\\ConvColor,
                bandfill=\\ConvReluColor,
                height=''' + str(size[0]) + ''',
                depth=''' + width_string + ''',
                width={''' + str(size[1]) + '''}
                }
            };
'''

# Conv,relu
def upsample(name, z_label='', n_filter=(), offset=(0, 0, 0), to='0,0,0', width=(2),
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
def pool(name, offset=(0, 0, 0), to='(0,0,0)', width=1, size=(40, 40), opacity=0.5, caption=' ', grid=False, gridsize=1, anchor= '-east'):
    return r'''
        \pic[shift={''' + str(offset) + '''}] at (''' + to + anchor + ''')
            {Box={
                name=''' + name + ''',
                caption=''' + caption + r''',
                fill=\PoolColor,
                opacity=''' + str(opacity) + ''',
                height=''' + str(size[0]) + ''',
                depth=''' + str(size[1]) + ''',
                width=''' + str(width) + ''',
                }
            };
'''

def grid(name, at, color='black', size=(2,2), steps=1):
    dist=size[0]/steps
    return r'''
	\node[canvas is zy plane at x=0]('''+ name +''') at ('''+ at +'''-east) {\drawcoloredgrid{'''+ str(size[0]) +'''}{'''+ str(size[1]) +'''}{''' + str(dist) +'''}{'''+ color +'''}};
'''


# Detect
def detect(name, z_label='', n_filter=(64, 64), offset=(0, 0, 0), to='0,0,0', width=(2), size=(40, 40), caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            warnings.warn('Size of n_filters does not match size of width')
        width_string = list_to_string(width)
    else:
        width_string = str(width)
    return r'''
        \pic[shift={''' + str(offset) + '''}] at (''' + to + ''')
            {Box={
                name=''' + name + ''',
                caption=''' + caption + ''',
                zlabel=''' + str(z_label) + ''',
                fill=\\DetectColor,
                height=''' + str(size[0]) + ''',
                depth=''' + str(size[1]) + ''',
                width={''' + width_string + '''}
                }
            };
'''


# Unpool4,
def unpool(name, offset=(0, 0, 0), to='(0,0,0)', width=1, height=32, depth=32, opacity=0.5, caption=' '):
    return r'''
        \pic[shift={ ''' + str(offset) + ''' }] at ''' + to + '''
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
def conv_res(name, z_label='', n_filter=64, offset=(0, 0, 0), to='(0,0,0)', width=6, height=40, depth=40, opacity=0.2, caption=' '):
    return r'''
        \pic[shift={ ''' + str(offset) + ''' }] at ''' + to + '''
            {RightBandedBox={
                name=''' + name + ''',
                caption=''' + caption + ''',
                xlabel={{''' + str(n_filter) + '''}},
                zlabel=''' + str(z_label) + r''',
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
def conv_soft_max(name, z_label=40, offset=(0, 0, 0), to='(0,0,0)', width=1, height=40, depth=40, caption=' '):
    return r'''
        \pic[shift={''' + str(offset) + '''}] at ''' + to + '''
            {Box={
                name=''' + name + ''',
                caption=''' + caption + ''',
                fill=\\SoftmaxColor,
                height=''' + str(height) + ''',
                width=''' + str(width) + ''',
                depth=''' + str(depth) + '''
                }
            };
'''

# relu
def relu(name, z_label='', n_filter=(64, 64), offset=(0, 0, 0), to='0,0,0', width=(1), size=[40, 40], caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            warnings.warn('Size of n_filters does not match size of width')
        width_string = list_to_string(width)
    else:
        width_string = str(width)
    return r'''
        \pic[shift={''' + str(offset) + '''}] at (''' + to + ''')
            {Box={
                name=''' + name + ''',
                caption=''' + caption + ''',
                zlabel=''' + str(z_label) + r''',
                fill=\ConvReluColor,
                height=''' + str(size[0]) + ''',
                depth=''' + str(size[1]) + ''',
                width={''' + width_string + '''}
                }
            };
'''



# SoftMax
def soft_max(name, z_label='', n_filter=32, offset=(0, 0, 0), to='(0,0,0)', width=1.5,
             size=[40, 40], opacity=0.8, caption=' ', anchor_to='-west'):
    return r'''
        \pic[shift={''' + str(offset) + '''}] at (''' + to + anchor_to +''')
            {Box={
                name=''' + name + ''',
                caption=''' + caption + ''',
                zlabel=''' + str(z_label) + ''',
                fill=\\SoftmaxColor,
                opacity=''' + str(opacity) + ''',
                height=''' + str(size[0]) + ''',
                depth=''' + str(size[1]) + ''',
                width=''' + str(width) + '''
                }
            };
'''


# shortcut
def shortcut(name, z_label='', n_filter=(64, 64), offset=(0, 0, 0), to='0,0,0', width=(1), size=[40, 40], caption=' '):
    if isinstance(width, list):
        if(len(n_filter) != len(width)):
            warnings.warn('Size of n_filters does not match size of width')
        width_string = list_to_string(width)
    else:
        width_string = str(width)
    return r'''
        \pic[shift={''' + str(offset) + '''}] at (''' + to + ''')
            {Box={
                name=''' + name + ''',
                caption=''' + caption + ''',
                zlabel=''' + str(z_label) + r''',
                fill=\ShortcutColor,
                height=''' + str(size[0]) + ''',
                depth=''' + str(size[1]) + ''',
                width={''' + width_string + '''}
                }
            };
    '''


# Short straight connection
def short_connection(of, to, anchor_of='-east', anchor_to='-west', fill='[fillwhite]', name='', options=''):
    return r'''
        \draw [connection, '''+ options +'''] (''' + of + anchor_of + r''') -- node ''' + fill + name + r''' {\midarrow}(''' + to + anchor_to + ''');
'''


# Long connection
def long_connection(of, to, pos=1.25, anchor_of_1='-south', anchor_of_2='-north', anchor_to='-north'):
    return r'''
        \path (''' + of + anchor_of_1 + ''') -- (''' + of + anchor_of_2 + ''') coordinate[pos=''' + str(pos) + '''] (''' + of + r'''-dummy) ;
        \path (''' + of + '''-dummy |- ''' + to + anchor_to + ''') coordinate (''' + to + r'''-dummy)  ;

        \draw [connection] 
            (''' + of + anchor_of_2 + ''')
            -- node {}(''' + of + anchor_of_2 + ''' |- ''' + of + r'''-dummy)
            -- node {\midarrow}(''' + of + '''-dummy -| ''' + to + anchor_to + ''')
            -- node {}(''' + to + anchor_to + ''');
    '''

# Long connection right to left
def long_connection_reversed(of, to, pos=1.25, anchor_of_1='-south', anchor_of_2='-north', anchor_to='-north'):
    return r'''
        \path (''' + of + anchor_of_1 + ''') -- (''' + of + anchor_of_2 + ''') coordinate[pos=''' + str(pos) + '''] (''' + of + r'''-dummy) ;
        \path (''' + of + '''-dummy |- ''' + to + anchor_to + ''') coordinate (''' + to + r'''-dummy)  ;

        \draw [connection] 
            (''' + to + anchor_to + ''')
            -- node {}(''' + to + anchor_to + ''' |- ''' + of + r'''-dummy)
            -- node {\midarrow}(''' + of + '''-dummy -| ''' + of + anchor_of_1 + ''')
            -- node {}(''' + of + anchor_of_2 + ''')
;
    '''


# connection along z-axis with right angle
def z_connection(of, to, z_shift=0, anchor_of='-near', anchor_to='-west', shift=(1,0,0)):
    if z_shift:
        shift=(0,0,z_shift)
    return r'''
        \draw [connection]  (''' + of + anchor_of + ''')    -- node {} ++''' + str(shift) + r''' -- node {\midarrow} (''' + to + anchor_to + ''');
    '''


def double_connection(of, over, to, anchor_of='-east', anchor_to='-west', fill='[fillwhite]', name='', options=''):
    return r'''
        \draw [connection, ''' + options + '''] (''' + of + anchor_of + r''') -- node {} ('''+ over +''') -- node ''' + fill + name + r''' {\midarrow}(''' + to + anchor_to + ''');
'''

def coordinate(name, of, offset):
    return r'''
    	\coordinate [shift={'''+ str(offset) +'''}] ('''+ name +''') at ('''+ of +''');
    '''

def fuseconnection(of, to, anchor_of='-east', anchor_to='-south', x_shift=0.5, y_shift=1):
    if 'north' in anchor_to:
        y_shift = -1
    return r'''
        \draw[fuseconnection](''' + of + anchor_of + ''')++(''' + str(x_shift) + ''',0) -| +(0,''' + str(y_shift) + ''') -- (''' + to + anchor_to + ''');
    '''

# Skip connection
def skip(of, to, pos=1.25):
    return r'''
        \path (''' + of + '''-southeast) -- (''' + of + '''-northeast) coordinate[pos=''' + str(pos) + '''] (''' + of + r'''-top) ;
        \path (''' + to + '''-south)  -- (''' + to + '''-north)  coordinate[pos=''' + str(pos) + '''] (''' + to + r'''-top) ;
        \draw [copyconnection]  
            (''' + of + r'''-northeast)
            -- node {\copymidarrow}(''' + of + r'''-top)
            -- node {\copymidarrow}(''' + to + r'''-top)
            -- node {\copymidarrow} (''' + to + '''-north);
    '''


# Add ball
def add(name, to, offset=(1, 0, 0), opacity=0.4, caption=''):
    return r'''
        \pic[shift={''' + str(offset) + '''}] at (''' + to + '''-east)
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
def multiply(name, to, offset=(1, 0, 0), opacity=0.6, caption='', ):
    return r'''
        \pic[shift={''' + str(offset) + '''}] at (''' + to + '''-east)
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
def concatenate(name, to, offset=(1, 0, 0), opacity=0.6, caption=''):
    return r'''
        \pic[shift={''' + str(offset) + '''}] at (''' + to + '''-east)
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


def resample(of, to):
    return r'''
        \draw[densely dashed]
            (''' + of + '''-nearnortheast) coordinate(a) -- (''' + to + '''-nearnorthwest)
            (''' + of + '''-nearsoutheast) coordinate(b) -- (''' + to + '''-nearsouthwest)
            (''' + of + '''-farsoutheast) coordinate(c) -- (''' + to + '''-farsouthwest)
            (''' + of + '''-farnortheast) coordinate(d) -- (''' + to + '''-farnorthwest)
            ;
    '''


def full_connection(of, to):
    return r'''
        \draw[densely dashed]
            (''' + of + '''-nearnortheast) -- (''' + to + '''-farnorthwest)
            (''' + of + '''-nearnortheast) -- (''' + to + '''-nearnorthwest)
            (''' + of + '''-farnortheast) -- (''' + to + '''-nearnorthwest)
            (''' + of + '''-farnortheast) -- (''' + to + '''-farnorthwest)
            (''' + of + '''-farnortheast) -- (''' + to + '''-nearsouthwest)
            (''' + of + '''-nearsoutheast) -- (''' + to + '''-farsouthwest)
            (''' + of + '''-nearsoutheast) -- (''' + to + '''-nearsouthwest)
            (''' + of + '''-nearsoutheast) -- (''' + to + '''-farnorthwest)
            (''' + of + '''-farsoutheast) --(''' + to + '''-nearsouthwest)
            (''' + of + '''-farsoutheast) --(''' + to + '''-farsouthwest);
'''


def ellipsis(of, to, offset='(0.5,0,0)', name=''):
    return r'''
        \draw [connection] (''' + of + r'''-east) -- node [fill=white,inner sep=1pt, opacity=1]''' + name + '''{\ldots} (''' + to + '''-west);
    '''


# End document
def env_end():
    return r'''
        \end{tikzpicture}
        \end{document}
    '''

def results_upsampling():
    return r'''
    \pic[shift={(2, 0, 0)}] at (soft_max-west)
		{Box={
            name=image_1,
            caption= ,
            zlabel=,
            fill=white,
            opacity=0.8,
            height=5.0,
            depth=5.0,
            width=0.5
        }
    };

    \pic[shift={(4, 0, 0)}] at (image_1-west)
    {Box={
        name=image_2,
        caption= ,
        zlabel=,
        fill=white,
        opacity=0.8,
        height=40.0,
        depth=40.0,
        width=0.5
        }
    };

    \node[canvas is zy plane at x=0] (img_1) at (image_1-east) {\includegraphics[width=2cm,height=2cm]{\skyseg}};

    \draw [connection] (soft_max-east) -- node [fillwhite] {\midarrow}(image_1-west);

    \node[canvas is zy plane at x=0] (img_2) at (image_2-east) {\includegraphics[width=9cm ,height=9cm ]{\skyseg}};

    \draw[densely dashed]
    (image_1-nearnortheast) coordinate(a) -- (image_2-nearnorthwest)
    (image_1-nearsoutheast) coordinate(b) -- (image_2-nearsouthwest)
    (image_1-farsoutheast) coordinate(c) -- (image_2-farsouthwest)
    (image_1-farnortheast) coordinate(d) -- (image_2-farnorthwest);

    \draw [connection, ] (conv_68-west) -- node [fillwhite] {\midarrow}(soft_max-east);
    '''

def spatial_mask():
    return r'''
    \pic[shift={(5, 0, 0)}] at (image_0.south east)
	{Box={
			name=spatial_mask,
			caption= ,
			zlabel=,
			fill=white,
			opacity=0.8,
			height=15.0,
			depth=15.0,
			width=0.5
		}
	};

    \draw [connection, pos=0.8]  (image_0.south)   -- node {} ++(-0.45, -0.45, 4) -- node {\midarrow} (spatial_mask-west);

	\node[canvas is zy plane at x=0](grid_3) at (spatial_mask-east) {\drawcoloredgrid{3}{3}{1.0}{black}};
	
	\coordinate [shift={(-2, 2, 0)}] (dummy_mask) at (conv_68-far);

    \draw [connection, pos=0.8] (grid_3) -- node {} ++(7,0,0) -- node [fillwhite] {\midarrow} (dummy_mask) -- node {} ++(4, 0, 0) -- node {}(conv_68-far);
'''

def text(shift=(0,0,0), of='', text=''):
    return r'''
        	\node [shift={'''+shift+''')}] at ('''+of+''') {\LARGE{'''+text+'''}};
            '''

def legend():
    return r'''
        \pic[shift={(0, -15, 0)}] at (0,0,0)
            {RightBandedBox={
                name=legend_1,
                fill=\ConvColor,
                bandfill=\ConvReluColor,
                height=5.0,
                depth=5.0,
                width={1.0}
            }
        };
        \node [shift={(0, -1.3, 0)}] at (legend_1-anchor) {\LARGE{Convolution layer}};

        \pic[shift={(5, 0, 0)}] at (legend_1-west)
        {Box={
                name=legend_2,
                fill=\PoolColor,
                height=5.0,
                depth=5.0,
                width={1}
            }
        };
        \node [shift={(0, -1.3, 0)}] at (legend_2-anchor) {\LARGE{Pooling layer}};

        \pic[shift={(5, 0, 0)}] at (legend_2-west)
        {Box={
                name=legend_3,
                fill=\UpsampleColor,
                height=5.0,
                depth=5.0,
                width={1}
            }
        };
        \node [shift={(0, -1.3, 0)}] at (legend_3-anchor) {\LARGE{Upsample layer}};

        \pic[shift={(5, 0, 0)}] at (legend_3-west)
        {Box={
                name=legend_4,
                fill=\SoftmaxColor,
                height=5.0,
                depth=5.0,
                width={1}
            }
        };
        \node [shift={(0, -1.3, 0)}] at (legend_4-anchor) {\LARGE{Softmax layer}};


        \pic[shift={(5, 0, 0)}] at (legend_4-west)
        {Ball={
                name=legend_6,
                caption=,
                fill=\ConcColor,
                opacity=0.6,
                radius=2,
                logo=$\oplus$
            }
        };
        \node [shift={(0,-1.3,0)}] at (legend_6-anchor) {\LARGE{Concatenation}};

        \pic[shift={(5, 0, 0)}] at (legend_6-west)
        {Ball={
                name=legend_7,
                caption=,
                fill=\SumColor,
                opacity=0.6,
                radius=2,
                logo=$+$
            }
        };
        \node [shift={(0,-1.3,0)}] at (legend_7-anchor) {\LARGE{Summation}};     

        
        
   
    '''
