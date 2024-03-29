""" Homework 7 - Thinning
Yi-Fan Wu (R08921104)
"""

import cv2
import numpy as np


# a1, a2, a3, a4, 
# and their corresponding neighbors' directions
NEIGHBORS = {
    (0, 1): [(-1, 0), (-1, 1)],     # a1 
    (-1, 0): [(-1, -1), (0, -1)],   # a2
    (0, -1): [(1, -1), (1, 0)],     # a3
    (1, 0): [(1, 1), (0, 1)]        # a4
}


def binarize_image(img):
    height, width = img.shape[:2]
    for h in range(height):
        for w in range(width):
            if img[h, w] < 128:
                img[h, w] = 0
            else:
                img[h, w] = 255

    # cv2.imwrite('binary_lena.bmp', img)
    return img


# From 512x512 to 64x64
def downsample(img):
    height, width = img.shape[:2]
    down_img = np.zeros((64, 64), dtype=int)
    for h in range(0, height, 8):
        for w in range(0, width, 8):
            down_img[int(h/8), int(w/8)] = img[h, w]

    cv2.imwrite('downsample.bmp', down_img)
    return down_img


def thinning(img):
    height, width = img.shape[:2]
    
    change = True
    # Repeat checking while stop updating the image
    while change:
        change = False
        indices_p = [] # Indices for pixels which are indicated 'p'

        # Get the Yokoi matrix
        matrix_yokoi = count_connectivity(img)
        
        # Pair relationship operating
        for h in range(height):
            for w in range(width):
                if matrix_yokoi[h, w] == 1:
                    flag = False # flag = True if one of the neighbors has Yokoi value = 1
                    for n in NEIGHBORS:
                        if 0 <= h + n[0] < height and 0 <= w + n[1] < width:
                            if matrix_yokoi[h + n[0], w + n[1]] == 1:
                                flag = True
                                break
                    if flag:
                        indices_p.append((h, w))

        # Check marked pixels and do the thin operation
        for (h, w) in indices_p:
            count = 0
            for n, d in NEIGHBORS.items():
                if 0 <= h + n[0] < height and 0 <= w + n[1] < width:
                    neighbor = img[h + n[0], w + n[1]]
                    if neighbor:
                        h1, w1 = h + d[0][0], w + d[0][1]
                        h2, w2 = h + d[1][0], w + d[1][1]
                        # two case for counting:
                        if h1 < 0 or h1 == height or w1 < 0 or w1 == width or \
                            h2 < 0 or h2 == height or w2 < 0 or w2 == width:
                            # 1. out of bound
                            count += 1
                        elif img[h1, w1] != neighbor or img[h2, w2] != neighbor:
                            # 2. one of pixel not equal
                            count += 1

            # exactly one neighbor has yokoi number = 1
            if count == 1 and img[h, w] != 0:
                change = True
                img[h, w] = 0

    return img


def count_connectivity(img):
    height, width = img.shape[:2]
    # The result will be a 64x64 matrix
    result = np.zeros(img.shape, dtype=int)
    
    for h in range(height):
        row_arr = []
        for w in range(width):
            count = 0
            if img[h, w]:
                # 4 neighbors need to be checked
                count_r = 0
                for n, d in NEIGHBORS.items():
                    if 0 <= h + n[0] < height and 0 <= w + n[1] < width:
                        neighbor = img[h + n[0], w + n[1]]
                        if neighbor:
                            h1, w1 = h + d[0][0], w + d[0][1]
                            h2, w2 = h + d[1][0], w + d[1][1]
                            # two case for counting:
                            if h1 < 0 or h1 == height or w1 < 0 or w1 == width or \
                                h2 < 0 or h2 == height or w2 < 0 or w2 == width:
                                # 1. out of bound
                                count += 1
                            elif img[h1, w1] != neighbor or img[h2, w2] != neighbor:
                                # 2. one of pixel not equal
                                count += 1 
                            elif img[h1, w1] == neighbor and img[h2, w2] == neighbor:
                                count_r += 1
                if count_r == 4:
                    count = 5
            result[h, w] = count

    return result




def main():
    print('1. Reading the image and binarizing...')
    img = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
    binary_img = binarize_image(img)

    print('2. Downsampling...')
    down_img = downsample(binary_img)

    print('3. Thinning...')
    thin_img = thinning(down_img)
    cv2.imwrite('thinning.bmp', thin_img)
    


if __name__ == '__main__':
    main()