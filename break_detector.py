#!/usr/bin/env python

''' break_detector.py - runs a Monte Carlo simulation of ALT of parts '''

import argparse
import multiprocessing
from components import sensornetwork

def build_part_configs():
    '''Builds a five sensor network based on resistances that produce useful results.
    Feel free to experiment; five or six parts per network seems to be about the most
    this system can differentiate.'''
    resistances = [1e3, 2e3, 3e3, 4e3, 5e3]
    mean_time_to_failure = 15.
    part_configs = []
    for partnum in resistances:
        part_config = {"mttf":mean_time_to_failure,
            "resistance":partnum}
        part_configs.append(part_config)
    return part_configs

def main():
    '''Main entry point of the program'''
    parser = argparse.ArgumentParser(description='Monte Carlo ALT simulation')
    parser.add_argument('-n', action="store", type=int, default=1000,
        dest="num_sims", help="Specify number of simulations to run (default 1000)")
    parser.add_argument('-m', action="store_true", default=False,
        dest='multicore', help='Use multiprocess mode (defaults to single process)')
    parser.add_argument('-o', action="store", type=str, default="results.csv",
        dest='output_file', help="Store output in specified file")
    args = parser.parse_args()
    part_configurations = build_part_configs()
    number_of_cycles = 3*part_configurations[0].get('mttf')
    if not args.multicore:
        print("Running single process:  {0} simulations, output saved to '{1}'\n".format(
            args.num_sims, args.output_file))
        sensornetwork.run_simulation(num_simulations=args.num_sims, num_cycles=number_of_cycles,
            part_configurations=part_configurations, start_time=0, fname=args.output_file)
    else:
        print("Running multiple processes:  {0} simulations, output saved to '{1}'\n".format(
            args.num_sims, args.output_file))
        sensornetwork.multirun_simulation(num_simulations=args.num_sims, num_cycles=number_of_cycles,
            part_configurations=part_configurations, start_time=0, fname=args.output_file)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    import datetime
    tstart = datetime.datetime.utcnow()
    main()
    tfinish = datetime.datetime.utcnow()
    print("Elapsed time: {0}\n".format(tfinish-tstart))