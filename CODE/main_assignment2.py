#!/usr/bin/env python3
"""
SAT Assignment Part 2 - Non-consecutive Sudoku Solver (puzzle -> SAT/UNSAT)

Do NOT modify this file - instead, implement your function in encoder.py

Usage:
  python main.py --in <puzzle.txt>

Behavior:
  - Reads a Sudoku puzzle in plain text format (N x N grid, 0 = empty).
  - Encodes it to CNF, runs the solver, and decides satisfiability.
  - Prints exactly one line to stdout:
        SAT
     or
        UNSAT
"""

import argparse
from typing import Tuple, Iterable
from encoder import to_cnf
from solver import solve_cnf
import json
import time

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True)
    p.add_argument("--sat", dest="sat", action='store_true')
    return p.parse_args()

def main():

  times = []
  for i in range(100):
    clauses, num_vars = parse_dimacs(f"/Users/rjkbo/Ariel/knowledge_representation/CODE/UF250_106_100/uf250-0{i+1}.cnf")
    start = time.time()
    status, model = solve_cnf(clauses, num_vars)
    end_time = time.time() - start
    times.append(end_time)
    print(status)

    # model_negatives = set()
    # model_positives = set()

    # for literal in model:
    #     if literal < 0:
    #         model_negatives.add(-literal)
    #     else:
    #         model_positives.add(literal)

    string_model = ""

    # for literal in sorted(model_negatives):
    #     string_model += str(-literal) + " "

    # for literal in sorted(model_positives):
    #     string_model += str(literal) + " "

    if model is not None:
      for literal in model:
          string_model += str(literal) + " "

    # print(string_model.strip())
  with open("data2.json", "w") as file:
    json.dump(times, file)


def parse_dimacs(input_path: str) -> Tuple[Iterable[Iterable[int]], int]:
    close = False
    if isinstance(input_path, str):
        file = open(input_path, "r")
        close = True
    else:
        file = input_path


    for _ in range(8):
      line = file.readline()

    components = line.strip().split(" ")
    components = [com for com in components if com != ""]
       
    if len(components)!= 4 or components[0]!="p" or components[1]!="cnf":
      print("Wrong file format! Expected first line to be 'p cnf NUM_VARS NUM_CLAUSES")
      exit(1)

    num_vars=int(components[2])
    num_clauses=int(components[3])

    clauses=[]

    line=file.readline()
    while(line):
       if line.strip().split(" ")[0] == '%':
          break
       numbers = []
       for x in line.strip().split(" "):
          if x == "":
             pass
          else:
             numbers.append(int(x))
       if(numbers[-1]!=0):
          print("Wrong format! Clause lines must be terminated with a 0")

       clauses.append(numbers[:-1])

       line=file.readline()


    return clauses, num_vars

if __name__ == "__main__":
    main()
