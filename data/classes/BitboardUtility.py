import numpy as np

RANKS = np.array(
            [np.uint64(0x00000000000000FF) << np.uint8(8*i) for i in range(8)],
            dtype=np.uint64)
FILES = np.array(
            [np.uint64(0x0101010101010101) << np.uint8(i) for i in range(8)],
            dtype=np.uint64)

RANK_MASKS = np.fromiter(
        (RANKS[i//8] for i in range(64)),
        dtype=np.uint64,
        count=64)

FILE_MASKS = np.fromiter(
        (FILES[i%8] for i in range(64)),
        dtype=np.uint64,
        count=64)