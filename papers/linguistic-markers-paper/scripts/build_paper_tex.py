#!/usr/bin/env python3
"""Compatibility entry point for the corrected Markdown-to-PDF build.

The pre-correction converter is preserved with the legacy artifact snapshot.
Bibliography URLs now come from the manuscript rather than a separate map.
"""

from build_corrected_paper import main


if __name__ == "__main__":
    main()
