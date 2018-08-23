#!/usr/bin/env python3

import pandas as pd

instances = [ 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 8, 16 ]

def is_cycle_count(line):
    try:
        int(line)
        return True
    except ValueError:
        return False

def parse_test(test, instance):
    counts = []
    found_start = False
    with open('gdb_output/gdb_output_test%d-%d.txt' % (test, instance)) as f:
        for line in f:
            if is_cycle_count(line):
                if found_start:
                    end = int(line)
                    found_start = False
                    counts.append(end - start)
                else:
                    start = int(line)
                    found_start = True
    return counts

def parse_results_to_df():
    results = pd.DataFrame()

    for test in range(12):
        for instance in range(1, instances[test] + 1):
            test_num = test + 1
            cycles = parse_test(test_num, instance)
            results[(test_num, instance)] = cycles

    return results

def main():
    results = parse_results_to_df()

    print(results.T)

if __name__ == '__main__':
    main()
