
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */

struct ListNode* addTwoNumbers(struct ListNode* l1,
                               struct ListNode* l2)
{
    int carry = 0;

    // Dummy node simplifies linked-list construction
    struct ListNode dummy;
    dummy.next = NULL;

    struct ListNode* tail = &dummy;

    // Continue until both lists and carry are exhausted
    while (l1 != NULL || l2 != NULL || carry != 0)
    {
        int sum = carry;

        // Read digit from first linked list
        if (l1 != NULL)
        {
            sum += l1->val;
            l1 = l1->next;
        }

        // Read digit from second linked list
        if (l2 != NULL)
        {
            sum += l2->val;
            l2 = l2->next;
        }

        // Calculate digit and carry
        carry = sum / 10;
        int digit = sum % 10;

        // Allocate a new node
        struct ListNode* newNode =
            (struct ListNode*)malloc(sizeof(struct ListNode));

        newNode->val = digit;
        newNode->next = NULL;

        // Attach node to result list
        tail->next = newNode;
        tail = newNode;
    }

    return dummy.next;
}
