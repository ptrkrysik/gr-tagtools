#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import pmt
#from mpmath import mp,mpf

class gapfiller(gr.sync_block):
    """
    docstring for block gapfiller
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="gapfiller",
            in_sig=[numpy.complex64],
            out_sig=[numpy.complex64])
            
        self.got_fist_tag = False
        self.rx_rate = None
        self.offset_prev = None
        self.rx_time_prev_secs = None
        self.rx_time_prev_frac = None
#        mp.dps = 20

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        if self.got_fist_tag is not True:
            rx_rate_tags = self.get_tags_in_window(0, 0, len(in0), pmt.string_to_symbol("rx_rate"))
            rx_time_tags = self.get_tags_in_window(0, 0, len(in0), pmt.string_to_symbol("rx_time"))
            if len(rx_time_tags) > 0:
                self.got_fist_tag = True
#                self.rx_rate      = mpf(pmt.to_double(rx_rate_tags[0].value))
                self.rx_rate      = pmt.to_double(rx_rate_tags[0].value)
                self.offset_prev  = rx_time_tags[0].offset
#                self.rx_time_prev_secs = mpf(pmt.to_uint64(pmt.tuple_ref(rx_time_tags[0].value, 0)))
#                self.rx_time_prev_frac = mpf(pmt.to_double(pmt.tuple_ref(rx_time_tags[0].value, 1)))
                self.rx_time_prev_secs = pmt.to_uint64(pmt.tuple_ref(rx_time_tags[0].value, 0))
                self.rx_time_prev_frac = pmt.to_double(pmt.tuple_ref(rx_time_tags[0].value, 1))
                if len(rx_time_tags) > 1:
                    print "Usupported situation - more than one tag in a single work(..) call"
        else:
            rx_time_tags = self.get_tags_in_window(0, 0, len(in0), pmt.string_to_symbol("rx_time"))
            if len(rx_time_tags) > 0:
                tt = rx_time_tags[0]
#                print "Offset:",tt.offset," Offset_prev:",self.offset_prev," wartosc:",tt.value
                #compute number of zeros to add
#                self.rx_time_secs = mpf(pmt.to_uint64(pmt.tuple_ref(tt.value, 0)))
#                self.rx_time_frac = mpf(pmt.to_double(pmt.tuple_ref(tt.value, 1)))
                self.rx_time_secs = pmt.to_uint64(pmt.tuple_ref(tt.value, 0))
                self.rx_time_frac = pmt.to_double(pmt.tuple_ref(tt.value, 1))
                self.offset       = tt.offset

                diff_offset       = self.offset - self.offset_prev
                diff_offset_real  = ((self.rx_time_secs-self.rx_time_prev_secs)+(self.rx_time_frac-self.rx_time_prev_frac))*self.rx_rate
#                print "self.rx_time_secs:",self.rx_time_secs,"self.rx_time_prev_frac:",self.rx_time_prev_frac
                zeros = diff_offset_real - diff_offset
#                print "diff_offset_real:",diff_offset_real,"diff_offset:",diff_offset
                print "Found a gap in the data at offset:",self.offset," with length:", zeros, " [samps]"
                #save previous value
                self.offset_prev = self.offset
                self.rx_time_prev_secs = self.rx_time_secs
                self.rx_time_prev_frac = self.rx_time_frac      
            
            if len(rx_time_tags) > 1:
                print "Usupported situation - more than one tag in a single work(..) call"


        out[:] = in0

        return len(output_items[0])


