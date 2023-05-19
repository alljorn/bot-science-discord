def levenshtein_distance(input_string, compared_string):
    if input_string == compared_string:
        return 0
    if len(input_string) > len(compared_string):
        input_string, compared_string = compared_string, input_string
    input_length = len(input_string)
    compared_length = len(compared_string)
    if input_length == 0:
        return compared_length
    if compared_length == 0:
        return input_length

    array_1 = [0] * (compared_length+1)
    array_2 = [0] * (compared_length+1)

    for i in range(input_length + 1):
        array_1[i] = i

    for i in range(input_length):
        array_2[0] = i + 1
        for j in range(compared_length):
            cost = 1
            if input_string[i] == compared_string[j]:
                cost = 0
            array_2[j+1] = min(array_2[j] + 1, array_1[j+1] + 1, array_1[j] + cost)
        array_1, array_2 = array_2, array_1

    return array_1[input_length]
