import sentenceDBlib as dbHandle

print(f'Current sentences: \n{dbHandle.get_all()}')
print('Adding three more...')
dbHandle.write("this is my program")
dbHandle.write("my program is great!")
dbHandle.write("elasticsearch is great")

print(f'Current sentences: \n{dbHandle.get_all()}')
print(f' only sentences containing the word "program": \n{dbHandle.get_containing("program")}')
print(f' only sentences containing the word "great": \n{dbHandle.get_containing("great")}')