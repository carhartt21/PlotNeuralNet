
import sys
sys.path.append('.')
from pycore.tikzeng import *
from pycore.blocks  import *
from pycore.execute import *

arch = [
    to_head('.'),
    to_color(),
    to_begin(),

    to_input('./examples/fcn8s/cats.jpg'),
    to_ConvRelu(name='ccr_b1', s_filter=500, n_filter=(64, 64, 64, 64, 64), offset="(0, 0, 0)", to="(0, 0, 0)", width=(2, 2, 2, 2, 2), height=40, depth=40),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),

    *block_2ConvPool(name='b2', bottom='pool_b1', top='pool_b2', s_filter=256, n_filter=128, offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5),
    *block_2ConvPool(name='b3', bottom='pool_b2', top='pool_b3', s_filter=128, n_filter=256, offset="(1,0,0)", size=(25, 25, 4.5), opacity=0.5),
    *block_2ConvPool(name='b4', bottom='pool_b3', top='pool_b4', s_filter=64,  n_filter=512, offset="(1,0,0)", size=(16, 16, 5.5), opacity=0.5),
    *sum(name='add', prev='pool_b4', offset='(1,0,0)'),
    *mult(name='mult', prev='add'),
    *conc(name='conc', prev='mult'),
    to_long_connection(of='ccr_b1', to='add'),
    to_long_connection(of='ccr_b2', to='add'),
    to_long_connection(of='ccr_b3', to='add'),
    to_end()
    ]

def main():
    try:
        namefile = str(sys.argv[0]).split('.')[0]

        content = buildArchitecture(arch)
        writeTex(content, namefile + ".tex")
        texToPDF(namefile + ".tex")

        openPDF("SumatraPDF", namefile + ".pdf")
    except:
        print("Unexpected error:", sys.exc_info()[0])

if __name__ == '__main__':
    main()
