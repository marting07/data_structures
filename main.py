# This is a sample Python script.
from lisp_like.lisp_element import create_atom, create_list
from skip_list.skip_list import SkipList


def lisp_example():
    elem1 = create_atom(1)
    elem2 = create_atom(2)
    elem3 = create_atom(3)
    list_2_3 = create_list([elem2, elem3])
    list_1_2_3_nested = create_list([elem1, create_list([elem2, create_list([elem3])])])
    main_list = create_list([elem1, list_2_3, list_1_2_3_nested, elem2])
    print(main_list)


def skip_list_example():
    # Create a new Skip List with a maximum level of 5 and probability of 0.5
    skip_list = SkipList(max_level=5, p=0.5)
    # Insert elements into the Skip List
    elements = [3, 7, 15, 22, 27, 35, 43]
    for element in elements:
        skip_list.insert(element)
    # Print the contents of the Skip List after insertion
    print("Skip List after insertion:")
    print(skip_list)
    # Search for specific elements in the Skip List
    search_values = [7, 33, 43]
    for value in search_values:
        node = skip_list.search(value)
        if node:
            print(f"Element {value} found in the Skip List")
        else:
            print(f"Element {value} not found in the Skip List")
    # Delete elements from the Skip List
    delete_values = [3, 27, 50]
    for value in delete_values:
        if skip_list.delete(value):
            print(f"Element {value} deleted from the Skip List")
        else:
            print(f"Element {value} not found in the Skip List")
    # Print the contents of the Skip List after deletion
    print("Skip List after deletion:")
    print(skip_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #lisp_example()
    skip_list_example()
