class Solution:  
    def __init__(self, input_string) -> None:
        
        self.input_string = input_string.upper().replace(' ','')
        self.key_list = list(set(self.input_string))

    def custom_sort(self):
        def sort_key(item):
            if item.isdigit() :
                return (0, item)
            elif isinstance(item, str) and len(item) == 1 and item.isalpha():
                return (1, ord(item))
            else:
                return (2, item)
        self.key_list = sorted(self.key_list, key=sort_key)
        
    def count_char(self):
        for key in self.key_list:            
            print(f'{key} {self.input_string.count(key)}')




input = 'Hello welcome to Cathay 60th year anniversary'

c = Solution(input)
c.custom_sort()
c.count_char()
        
