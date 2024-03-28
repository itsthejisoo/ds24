#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct ListNode
{
    // 처음부터 int형으로 해서 atoi 사용하여 파일 데이터들을 int형으로 가져와도 됨
    char *item;
    struct ListNode *next;
} ListNode;

typedef struct LinkedList
{
    ListNode *head;
    ListNode *tail;
    int numItems;
} LinkedList;

ListNode *newListNode(char *newItem, ListNode *nextNode)
{
    ListNode *node = (ListNode *)malloc(sizeof(ListNode));
    node->item = strdup(newItem); // 복사된 string 주소 포인터
    node->next = nextNode;
    return node;
}

LinkedList *newLinkedList()
{
    LinkedList *list = (LinkedList *)malloc(sizeof(LinkedList));
    list->head = newListNode("dummy", NULL);
    list->tail = NULL;
    list->numItems = 0;
    return list;
}

ListNode *getNode(LinkedList *list, int i)
{
    ListNode *curr = list->head;
    for (int index = 0; index <= i; index++)
        curr = curr->next;
    return curr;
}

void append(LinkedList *list, char *newItem)
{
    ListNode *newNode = newListNode(newItem, NULL);
    if (list->head->next == NULL)
        list->head->next = newNode;
    else
        list->tail->next = newNode;
    list->tail = newNode;
    list->numItems++;
}

// i번째 노드 삭제
void removeNode(LinkedList *list, int i)
{
    if (i >= 0 && i < list->numItems)
    {
        ListNode *prev = getNode(list, i - 1);
        ListNode *curr = prev->next;
        prev->next = curr->next;

        if (i == list->numItems - 1)
            list->tail = prev;

        list->numItems--;
    }
    else
    {
        printf("%d\n", list->numItems);
        printf("Index %d out of bounds\n", i);
    }
}

int isEmpty(LinkedList *list)
{
    return list->numItems == 0 ? 1 : 0;
}

int findindex(LinkedList *list, char *x)
{
    ListNode *curr = list->head->next;
    int cnt = 0;
    while (curr != NULL)
    {
        cnt++;
        if (strcmp(curr->item, x) == 0) // strcmp: curr->item과 x가 같으면 0
            return cnt - 1;
        curr = curr->next;
    }
}

int inNode(LinkedList *list, char *x)
{
    ListNode *curr = list->head->next;
    while (curr != NULL)
    {
        if (strcmp(curr->item, x) == 0)
            return 1;
        curr = curr->next;
    }
    return 0;
}

typedef struct CacheSimulator
{
    int cache_slots;
    int cache_hit;
    int tot_cnt;
    LinkedList *lists;
} CacheSimulator;

CacheSimulator *newCacheSim(int cache_slots)
{
    CacheSimulator *cacheSim = (CacheSimulator *)malloc(sizeof(CacheSimulator));
    cacheSim->cache_slots = cache_slots;
    cacheSim->cache_hit = 0;
    cacheSim->tot_cnt = 1;
    cacheSim->lists = newLinkedList();

    return cacheSim;
}

void doSim(CacheSimulator *cacheSim, char *page)
{
    if (isEmpty(cacheSim->lists))
    {
        append(cacheSim->lists, page);
    }
    else
    {
        if (cacheSim->lists->numItems >= cacheSim->cache_slots)
        {
            if (inNode(cacheSim->lists, page))
            {
                removeNode(cacheSim->lists, findindex(cacheSim->lists, page));
                cacheSim->cache_hit++;
            }
            else
            {
                removeNode(cacheSim->lists, 0);
            }
            append(cacheSim->lists, page);
            cacheSim->tot_cnt++;
        }
        else
        {
            if (inNode(cacheSim->lists, page))
            {
                removeNode(cacheSim->lists, findindex(cacheSim->lists, page));
                cacheSim->cache_hit++;
            }
            append(cacheSim->lists, page);
            cacheSim->tot_cnt++;
        }
    }
}

void printStats(CacheSimulator *cacheSim)
{
    printf("cache_slot = %d, cache_hit = %d, hit ratio = %f\n", cacheSim->cache_slots, cacheSim->cache_hit, (float)cacheSim->cache_hit / cacheSim->tot_cnt);
}

int main()
{
    FILE *data_file = fopen("linkbench.trc", "r");
    char line[1000];
    LinkedList *lines = newLinkedList();

    while (fgets(line, sizeof(line), data_file))
    {
        char *ptr = strtok(line, "\n"); // "\n"을 기준으로 split해서 ptr에 저장해준다
        append(lines, ptr);
    }
    fclose(data_file);

    for (int cache_slots = 100; cache_slots <= 1000; cache_slots += 100)
    {
        CacheSimulator *cacheSim = newCacheSim(cache_slots);
        ListNode *page = lines->head->next;

        while (page != NULL)
        {
            doSim(cacheSim, page->item);
            page = page->next;
        }
        printStats(cacheSim);
    }

    return 0;
}
