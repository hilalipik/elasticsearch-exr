from db_handler import DBHandle

def main():
    handle = DBHandle("sentence-db")
    print(f'Current sentences: \n{handle.get_all()}')
    print('Adding three more...')
    handle.write("this is my program")
    handle.write("my program is great!")
    handle.write("elasticsearch is great")

    print(f'Current sentences: \n{handle.get_all()}')
    print(f' only sentences containing the word "program": \n{handle.get_containing("program")}')
    print(f' only sentences containing the word "great": \n{handle.get_containing("great")}')


if __name__ == "__main__":
    main()