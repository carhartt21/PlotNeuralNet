
import sys
sys.path.append('.')
from pycore.tikz import *
from pycore.blocks  import *
from pycore.execute import *

arch = [
    head('.'),
    def_colors(),
    env_begin(),

    input_image('./examples/fcn8s/cats.jpg'),
    conv_relu(name='ccr_b1', z_label=500, n_filter=(64, 64, 64, 64, 64), offset="(0, 0, 0)", to="(0, 0, 0)", width=(2, 2, 2, 2, 2), height=40, depth=40),
    pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),

    *conv_pool(name='b2', bottom='pool_b1', top='pool_b2', z_label=256, n_filter=128, offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5),
    *conv_pool(name='b3', bottom='pool_b2', top='pool_b3', z_label=128, n_filter=256, offset="(1,0,0)", size=(25, 25, 4.5), opacity=0.5),
    *conv_pool(name='b4', bottom='pool_b3', top='pool_b4', z_label=64,  n_filter=512, offset="(1,0,0)", size=(16, 16, 5.5), opacity=0.5),
    *sum(name='add', prev='pool_b4', offset='(1,0,0)'),
    *mult(name='mult', prev='add'),
    *conc(name='conc', prev='mult'),
    to_long_connection(of='ccr_b1', to='add'),
    to_long_connection(of='ccr_b2', to='add'),
    to_long_connection(of='ccr_b3', to='add'),
    env_end()
    ]

def main():
    try:
        namefile = str(sys.argv[0]).split('.')[0]

        content = build_architecture(arch)
        write_tex(content, namefile + ".tex")
        tex_to_pdf(namefile + ".tex")

        openPDF("SumatraPDF", namefile + ".pdf")
    except:
        print("Unexpected error:", sys.exc_info()[0])

if __name__ == '__main__':
    main()
