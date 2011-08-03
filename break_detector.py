#!/usr/bin/env python

''' break_detector.py - runs a Monte Carlo simulation of ALT of parts '''

import argparse
import multiprocessing
from components import sensornetwork
import analysis

def build_part_configs():
    '''Builds a five sensor network based on resistances that produce useful results.
    Feel free to experiment; five or six parts per network seems to be about the most
    this system can differentiate.'''
    resistances = [2e6, 3e6, 4e6, 5e6] # Should work in most scenarios
    # If you'd prefer testing something known to not work:
    # resistances = [1e3, 2e3, 3e3, 4e3, 5e3]
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
    parser.add_argument('-c', action="store_true", default=False,
        dest='check_results', help='Analyze the results and report if the network appears valid')
    parser.add_argument('-t', action='store', type=float, default=0.1,
        dest='collision_threshold', help='Specifies tolerance for calling a collision (defaults to 0.1)')
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
    if args.check_results:
        print("Analyzing results")
        analyzer = analysis.Analysis(args.output_file, threshold=args.collision_threshold)
        obvious_collisions = analyzer.check_obvious_collisions()
        num_collisions = len(obvious_collisions)
        if num_collisions == 0:
            print("No obvious collisions found.")
        else:
            print("{0} obvious collisions found.".format(num_collisions))

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()