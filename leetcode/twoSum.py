# nums list[int]
# target int
nums = [49,51]
target = 100
for i in nums:
    first=nums.index(i)
    differ = target-i
    nums[first]=None
    try:

        y = nums.index(differ)
        if y>0:
            print([first,y])
            break
    except:
        continue
    
    # return [i,y]