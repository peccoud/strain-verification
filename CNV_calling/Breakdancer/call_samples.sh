#!/bin/bash

bash Breakdancer/configure_breakdancer.sh > Breakdancer/breakdancer.conf
breakdancer-max Breakdancer/breakdancer.conf > Breakdancer/Results/Breakdancer_call_results.tsv
