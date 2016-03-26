#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Debug
# Generated: Sat Mar 26 18:23:02 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import gr, blocks
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import gapfiller as tagtools
#import tagtools 


class debug(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Debug")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.tagtools_gapfiller_0 = tagtools.gapfiller()
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_file_meta_source_0 = blocks.file_meta_source("tmp_detached", False, True, "tmp_detached.hdr")

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_meta_source_0, 0), (self.tagtools_gapfiller_0, 0))    
        self.connect((self.tagtools_gapfiller_0, 0), (self.blocks_null_sink_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def main(top_block_cls=debug, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
