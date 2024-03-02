#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>
#include <malloc.h>

#define NAME_SIZE 0x20
#define MAX_CHILDREN 0x10
#define MAX_WISHES 0x10
#define INPUT_SIZE 0x20

// Structures
typedef struct {
    char *name;
    char *wishes[MAX_WISHES];
    unsigned long wish_sizes[MAX_WISHES];
    char *letter;
    unsigned long letter_size;
} child;

// Prototypes
void init();
void ascii_art();
void meet_santa();
void* calloc_check(size_t, size_t);
unsigned long get_int();
void print_santa_options();
void ask_santa(child*);
void add_wish(child*);
void remove_wish(child*);
void edit_wish(child*);
void print_wishes(child*);
void prepare_letter(child*);
void write_letter(child*);
void delete_letter(child*);

// Global variables
child *children[MAX_CHILDREN] = {0};
unsigned int children_count = 0;

// Functions
int main(int argc, char const *argv[])
{
    init();
    ascii_art();
    meet_santa();
    return 0;
}

void init()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    alarm(60);
}

void ascii_art()
{
    FILE *file;
    unsigned int length;
    const char filename[] = "./santa_ascii.txt";
    char *buffer;

    file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Error while opening the file santa_ascii.txt. Check if the file is in the current directory\n");
        exit(EXIT_FAILURE);
    }
    fseek(file, 0, SEEK_END);
    length = ftell(file);
    buffer = calloc(1, length + 1);
    if (!buffer)
    {
        fclose(file);
        fprintf(stderr, "Malloc failed\n");
        exit(EXIT_FAILURE);        
    }
    fseek(file, 0, SEEK_SET);
    fread(buffer, 1, length, file);
    fclose(file);
    puts(buffer);
    free(buffer);
}

void* calloc_check(size_t nitems, size_t size)
{
    void* ptr;

    ptr = calloc(nitems, size);
    if (!ptr)
    {
        fprintf(stderr, "Calloc failed\n");
        exit(EXIT_FAILURE);               
    }
    return ptr;
}

void meet_santa()
{
    char name[NAME_SIZE];
    unsigned int len, i;
    bool new_child;

    while (1)
    {
        if (children_count >= MAX_CHILDREN)
            break;
        puts("Ho ho ho! Welcome! What's your name, little one?"
            " Come, sit on my lap and tell me, what would you like for Christmas this year?");
        len = 0;
        while (len <= 3)
        {
            memset(name, 0, NAME_SIZE);
            printf("Name: ");
            len = read(STDIN_FILENO, name, NAME_SIZE-1);
            if (len <= 3)
                puts("Oh, it's okay, little one. "
                    "I have ears like an elf sometimes; "
                    "they're not as sharp as they used to be! "
                    "Could you please tell me your name again, a little louder? "
                    "I want to make sure I get it right for my nice list!");
        }
        if (name[len-1] == '\n')
            name[len-1] = '\0';
        new_child = true;
        for (i = 0; i < children_count; i++)
        {
            if (strcmp(name, children[i]->name) == 0)
            {
                puts("Oooh! I know you, little one! Did you forget to ask Santa a present?");
                ask_santa(children[i]);
                new_child = false;
            }
        }
        if (new_child)
        {
            children[i] = calloc_check(1, sizeof(child));
            children[children_count]->name = strdup(name);
            printf("Nice to meet you %s! Do you want to write me a letter for Christmas?\n", children[children_count]->name);
            ask_santa(children[children_count]);
            children_count++;
        }
    }
    puts("Thank you, little ones, for such a magical time!"
        " Remember to always be kind, share joy, and believe in the magic of Christmas!");
}

unsigned long get_int()
{
    char buffer[INPUT_SIZE] = {0};

    read(STDIN_FILENO, buffer, INPUT_SIZE-1);
    return strtoul(buffer, NULL, 10);
}

void print_santa_options()
{
    puts("What can I do for you, little one?");
    puts("1) Add wish");
    puts("2) Remove wish");
    puts("3) Change wish");
    puts("4) Wishes list");
    puts("5) Prepare letter");
    puts("6) Write letter");
    puts("7) Trash letter");
    puts("8) Leave");
}

void ask_santa(child* cur_child)
{
    unsigned long choice;

    while (1)
    {
        print_santa_options();
        printf("> ");
        choice = get_int();
        switch (choice)
        {
            case 1: add_wish(cur_child);
                    break;
            case 2: remove_wish(cur_child);
                    break;
            case 3: edit_wish(cur_child);
                    break;
            case 4: print_wishes(cur_child);
                    break;
            case 5: prepare_letter(cur_child);
                    break;
            case 6: write_letter(cur_child);
                    break;
            case 7: delete_letter(cur_child);
                    break;
            case 8: return;
                        break;
            default:    puts("Invalid option!");
                        break;
        }


    }
}

void add_wish(child* cur_child)
{
    unsigned int i;
    unsigned long size;

    for (i = 0; i < MAX_WISHES; i++)
        if (!cur_child->wishes[i])
            break;
    if (i == MAX_WISHES)
    {
        puts("No more wishes for you little one!"
            "You got enough!");
        return;
    }
    puts("How much details do you wanna give me about your wish?");
    printf("Size: ");
    size = get_int();
    if (size < 0x10)
    {
        puts("I need more details so I won't be wrong with your present!");
        return;
    }
    if (size > 0x250)
    {
        puts("Too many details in your wish!");
        return;
    }
    cur_child->wishes[i] = calloc_check(1, size);
    cur_child->wish_sizes[i] = size;
    puts("Tell me your wish");
    printf("Wish: ");
    read(STDIN_FILENO, cur_child->wishes[i], cur_child->wish_sizes[i]-1);
    printf("Great wish, my dear! I will remember it as wish #%u\n", i);
}

void remove_wish(child* cur_child)
{
    unsigned int i;

    puts("Which wish do you want to remove?");
    printf("Index: ");
    i = get_int();
    if (i >= MAX_WISHES)
    {
        puts("I don't think I have such a wish!");
        return;
    }
    free(cur_child->wishes[i]);
    cur_child->wishes[i] = NULL;
    cur_child->wish_sizes[i] = 0;
    puts("Wish removed.");
}

void edit_wish(child* cur_child)
{
    unsigned int i;

    puts("Which wish do you want to change?");
    printf("Index: ");
    i = get_int();
    if (i >= MAX_WISHES)
    {
        puts("I don't think I have such a wish!");
        return;
    }
    if (!cur_child->wishes[i])
    {
        puts("Are you sure is the right wish?");
        return;
    }
    puts("Tell me your new wish");
    printf("New wish: ");
    read(STDIN_FILENO, cur_child->wishes[i], cur_child->wish_sizes[i]-1);
    puts("Wish changed!");
}

void print_wishes(child* cur_child)
{
    unsigned int i;

    puts("Your wishes:");
    for (i = 0; i < MAX_WISHES; i++)
        if (cur_child->wishes[i])
            printf("%02u) %s\n", i, cur_child->wishes[i]);
}

void prepare_letter(child* cur_child)
{
    unsigned long size; 

    if (cur_child->letter)
    {
        puts("We have already prepared the paper little one :D");
        return;
    }
    puts("How much paper do you need?");
    printf("Size: ");
    size = get_int();
    if (size < 0x650)
    {
        printf("Santa doesn't like short letters. At least %u characters!", 0x650);
        return;
    }
    if (size > 0x1000)
    {
        puts("I don't have so much paper my dear :(");
        return;
    }
    cur_child->letter = calloc_check(1, size);
    cur_child->letter_size = size;
    puts("Paper ready!");
}


void write_letter(child* cur_child)
{
    unsigned int i, length;


    if(!cur_child->letter)
    {
        puts("You have to prepare your letter first!");
        return;
    }
    puts("Ok little one, I'm helping you writing the letter. "
        "However, we can put only one wish in the letter. "
        "Which one would you like it to be?");
    printf("Index: ");
    i = get_int();
    if (i >= MAX_WISHES)
    {
        puts("I don't think I have such a wish!");
        return;
    }
    if (!cur_child->wishes[i])
    {
        puts("Are you sure is the right wish?");
        return;
    }
    length = snprintf(cur_child->letter, cur_child->letter_size-1, "Dear Santa Claus,\n\n"
        "My name is %s, and I am writing to you from Milan. "
        "I hope you, Mrs. Claus, the elves, and all the reindeers are doing well at the North Pole.\n\n"
        "As Christmas is approaching, I have been trying my best to be kind and dedicated to my studies. "
        "This year, I obtained good results in my university career and I did all the challenges in the Offensive and Defensive Cybersecurity course.\n\n"
        "There is something special I have been wishing for this Christmas. My biggest wish this year is: %s. \n\n"
        "I understand that Christmas is a time of giving and sharing, and I promise to share my joy and whatever I receive with others. "
        "I also want to wish a Merry Christmas to everyone, especially those who might need some extra cheer this year. "
        "Thank you, Santa, for bringing magic and joy to children all around the world. "
        "I will make sure to leave some cookies and milk for you on Christmas Eve, and some carrots and sugar sticks for the reindeers too!\n\n"
        "Merry Christmas, Santa!\n\n"
        "With love, \n\n%s.",  cur_child->name, cur_child->wishes[i], cur_child->name);
    cur_child->letter[length-1] = '\0';
    printf("Here's your beautiful letter:\n%s\n", cur_child->letter);
}

void delete_letter(child* cur_child)
{
    free(cur_child->letter);
    cur_child->letter = NULL;
    cur_child->letter_size = 0;
    puts("Letter thrashed");
}