# SHA-256 Collisions

This repository contains step-reduced SHA-256 SFS collision data, specifically
the SAT solver log files and notes.

## SFS Collisions

In the `sfs` directory, the `encodings` directory contains the SAT encodings for
the verions of step-reduced SHA-256 ranging from 20 to 38 steps.

Each log file is named in the format: `{steps}-{seed}-sfs-{solver}`.
