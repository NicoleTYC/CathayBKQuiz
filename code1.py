class Solution:
    def grade_reverse(self, input: list()) -> list():
        return_list = []
        for grade in input:
            if grade>0:
                new_grade = int(str(grade)[::-1])
            else:
                new_grade = 0
            return_list.append(new_grade)
        return return_list


            
    

input_grade = [-35, 46, 57, 91, 29]
c = Solution()
c.grade_reverse(input=input_grade)