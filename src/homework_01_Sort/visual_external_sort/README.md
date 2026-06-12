# External Sort Visual Explainer

Open `index.html` in a browser to view the interactive explanation.

This page explains the most important part of `external_sort.py`:

- how `chunk_size` limits memory usage;
- how `split_and_sort_chunks()` divides the binary file;
- how `multiprocessing.Pool.map()` sorts chunks in parallel;
- how `sort_chunk_by_index()` reads, sorts, and writes one temporary chunk;
- how `merge_sorted_chunks()` uses a heap for k-way merge;
- why the heap only stores the current candidate value from each sorted chunk;
- how `sorted_input.bin` is produced step by step.

The visualization uses a small example array, but the flow is the same as the
real program.
