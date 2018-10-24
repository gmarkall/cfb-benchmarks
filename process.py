#!/usr/bin/env python3

import numpy as np
import os
import subprocess

from compile_args import compile_args

def run(cmd, **kwargs):
    print(" ".join(cmd))
    cp = subprocess.run(cmd, **kwargs)
    cp.check_returncode()

def clean():
    print("Cleaning")
    cmd = [ 'rm -rf output' ]
    run(cmd, shell=True)
    os.mkdir('output')

def prepare(balance):
    print("Preparing. Balance: %s" % balance)
    for i in range(1, 13):
        clang = [ 'clang', '-S', '-emit-llvm',
            './functions/f%d.c' % i, '-o', 'output/f%d.ll' % i ]
        run(clang)

        balance_arg = 1 if balance else 0
        llvm = [ 'llc', 'output/f%d.ll' % i, '-riscv-cfg-balance=%d' % balance_arg,
            '-o', 'output/f%d.s' % i ]
        run(llvm)

def make_all_tests():
    print("Building")
    gcc = 'riscv32-unknown-elf-gcc'
    for ((test, instance, variant), args) in compile_args:
        src = './test-cases/main%d-%d.c' % (test, instance)
        asm = 'output/f%d.s' % test
        exe = 'output/test%d-%d-%d' % (test, instance, variant)
        args = [ '-DARG%d=%d' % (i+1, arg) for i, arg in enumerate(args) ]
        cmd = [ gcc, src, asm, '-g', '-o', exe ]
        cmd += args
        run(cmd)

gdb_commands = '''\
set logging file output/gdb_output.txt
set logging on
target remote :51000
stepi
stepi
load
break main
break exit
jump *_start
monitor cyclecount
cont
monitor cyclecount
disconnect
quit'''

def execute(test, instance, variant):
    run(['rm', '-f', 'output/gdb_output.txt'])
    run(['rm', '-f', 'output/gdb_commands.txt'])
    gdb_lines = 'file output/test%d-%d-%d\n' % (test, instance, variant)
    gdb_lines += gdb_commands
    with open('output/gdb_commands.txt', 'w') as f:
        f.write(gdb_lines)
    cmd = [ 'riscv32-unknown-elf-gdb', '-x', 'output/gdb_commands.txt' ]
    run(cmd)

def is_cycle_count(line):
    try:
        int(line)
        return True
    except ValueError:
        return False

def parse_test(output_file):
    found_start = False
    with open(output_file) as f:
        for line in f:
            if is_cycle_count(line):
                if found_start:
                    end = int(line)
                    return end - start
                else:
                    start = int(line)
                    found_start = True



def run_all_tests():
    print("Running")
    counts = {}
    for ((test, instance, variant), _) in compile_args:
        print("-", test, instance, variant)
        execute(test, instance, variant)
        cycles = parse_test('output/gdb_output.txt')
        counts[test, instance, variant] = cycles

    return counts

def compute_stats(counts):
    tests = set([ v[0][0] for v in compile_args ])
    stats = []
    for test in tests:
        #input_variant = 0 # temp for now - will do all sets later
        keys = [ k for k in counts if k[0] == test ]
        variants = set([ k[2] for k in keys])
        for v in variants:
            values = []
            subkeys = [ k for k in keys if k[2] == v ]
            for k in subkeys:
                values.append(counts[k])
            sd = np.std(values)
            mean = np.mean(values)
            rsd = (sd / mean) * 100
            stats.append((test, v, sd, mean, rsd))
    return stats

def main():
    clean()
    prepare(True)
    make_all_tests()
    balanced_counts = run_all_tests()

    clean()
    prepare(False)
    make_all_tests()
    unbalanced_counts = run_all_tests()

    # Sanity check - boths dicts should have the same keys:
    if sorted(balanced_counts) != sorted(unbalanced_counts):
        raise RuntimeError('Balanced and unbalanced counts have different keys')

    #from IPython import embed
    #embed()

    print(compute_stats(balanced_counts))
    print(compute_stats(unbalanced_counts))


if __name__ == '__main__':
    main()
