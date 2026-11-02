
int lengthOfLongestSubstring(char* s)
{
    // Store the last seen index of each possible byte value
    int lastSeen[256];

    // Initialize all entries to -1
    for (int i = 0; i < 256; i++)
    {
        lastSeen[i] = -1;
    }

    int left = 0;
    int maxLength = 0;

    // Traverse the string
    for (int right = 0; s[right] != '\0'; right++)
    {
        unsigned char ch = (unsigned char)s[right];

        // Check whether character was previously seen
        if (lastSeen[ch] >= left)
        {
            left = lastSeen[ch] + 1;
        }

        // Update the latest occurrence
        lastSeen[ch] = right;

        // Calculate current window length
        int currentLength = right - left + 1;

        // Update maximum length
        if (currentLength > maxLength)
        {
            maxLength = currentLength;
        }
    }

    return maxLength;
}
