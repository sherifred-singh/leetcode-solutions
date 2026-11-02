
#include <stdlib.h>

int compare(const void *a, const void *b)
{
    int x = *(const int *)a;
    int y = *(const int *)b;

    // Avoid subtraction because it can overflow
    if (x < y) return -1;
    if (x > y) return 1;

    return 0;
}

int minMoves2(int* nums, int numsSize)
{
    // Step 1: Sort the array
    qsort(nums, numsSize, sizeof(int), compare);

    // Step 2: Find the median
    int median = nums[numsSize / 2];

    // Step 3: Calculate total moves
    long long moves = 0;

    for (int i = 0; i < numsSize; i++)
    {
        long long diff = (long long)nums[i] - median;

        if (diff < 0)
        {
            diff = -diff;
        }

        moves += diff;
    }

    return (int)moves;
}
