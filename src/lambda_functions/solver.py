class NumberPlaceSolver():
    def __init__(self, input_data):
        self.num = 9
        self.sub_num = 3
        self.fields = self.__parse(input_data)
        self.constraints = [-1 if value != 0 else 0 for value in self.fields]
        self.iteration = 0


    def get_fields(self):
        return self.fields

    
    def get_fields_output(self):
        return "".join(map(str, self.fields))


    def get_iteration(self):
        return self.iteration


    def solve(self, next_index):
        self.iteration += 1
        if next_index == self.num * self.num:
            return True

        x = next_index % self.num
        y = next_index // self.num

        for i in range(self.num):
            value = i + 1   # 1-9

            if self.fields[next_index] != 0:
                next_index += 1
                if self.solve(next_index) == True:
                    return True
                else:
                    next_index -= 1
                    if self.constraints[next_index] == -1:
                        return False
                    else:
                        self.fields[next_index] = 0
            else:
                placable = self.__is_placable(x, y, value)

                if placable == True:
                    self.fields[next_index] = value
                    next_index += 1
                    if self.solve(next_index) == True:
                        return True
                    else:
                        next_index -= 1
                        self.fields[next_index] = 0
                else:
                    pass

        return False


    def __get_index(self, x, y):
        if x >= 0 and x < self.num and y >= 0 and y < self.num:
            return y * self.num + x
        else:
            return -1


    def __get_area(self, x, y):
        result_x = -1
        result_y = -1

        for i in range(self.sub_num):
            if x < (i + 1) * self.sub_num:
                result_x = i
                break

        for i in range(self.sub_num):
            if y < (i + 1) * self.sub_num:
                result_y = i
                break

        if result_x != -1 and result_y != -1:
            return result_y * self.sub_num + result_x
        else:
            return -1


    def __get_value(self, x, y):
        result = self.__get_index(x, y)
        if result != -1:
            return self.fields[result]
        else:
            return -1


    def __is_placable(self, x, y, value):
        area = self.__get_area(x, y)
        if area == -1:
            return False

        if self.__get_value(x, y) != 0:
            return False

        for i in range(self.num):
            if value == self.__get_value(x, i) and value > 0 and value <= self.num:
                return False

        for i in range(self.num):
            if value == self.__get_value(i, y) and value > 0 and value <= self.num:
                return False

        for i in range(self.num):
            for j in range(self.num):
                if area == self.__get_area(i, j) and value == self.__get_value(i, j):
                    return False

        return True


    def __parse(self, input_str):
        return [int(value) for value in list(input_str)]
