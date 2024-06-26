num_of_boxes = int(input("Enter the number of boxes that you want : "))

horizontal = num_of_boxes
spaces = num_of_boxes - 2

print(f'{"#" * horizontal}')
for i in range(num_of_boxes - 2):
    print(f'#{" " * spaces}#')
if num_of_boxes != 1:   
    print(f'{"#" * horizontal}')