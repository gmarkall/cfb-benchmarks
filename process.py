#!/usr/bin/env python3

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

def main():
    clean()
    prepare(False)
    make_all_tests()

if __name__ == '__main__':
    main()
