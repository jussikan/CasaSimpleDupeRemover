# CasaSimpleDupeRemover

CasaSimpleDupeRemover is a duplicate files finder and deletion application for macOS.

Implemented mostly in Python to produce the application quickly with ease, and to have accessibility to all possible bells & whistles under the hood.

Functional tests are currently being written, and a better application for a larger problem scope is being designed.


## Modus operandi
1. Acquire and store checksums of all files under a directory dropped into its graphical user interface,
1. Add macOS Finder tags on duplicate candidate files,
1. Move all tagged files to trash.
