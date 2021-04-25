from PIL import Image
from PIL import ImageChops

nums = [Image.open("../CODE/number/%d.png"%i) for i in range(10)]

# 识别整个验证码
def classify_code(pic):
    pic = to_black_and_white(pic)
    code = ""
    for im in split_pic(pic):
        code += str(classify_num(im))
    return code


# 识别单个数字
def classify_num(pic):
    for i in range(10):
        if ImageChops.difference(pic, nums[i]).getbbox() is None:
            return i
    return -1


# 切分图片
def split_pic(pic):
    ims = []
    for i in range(0,88,22):
        ims.append(pic.crop((i,19,i+21,39)))
    return ims


# 二值化
def to_black_and_white(pic):
    return pic.convert('1')
