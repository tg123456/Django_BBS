import random
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO


#隨機驗證碼
def random_verificate_code(length):
    """
    隨機驗證碼
    :param length: 驗證碼的長度
    :return: 字符串驗證碼、驗證碼字符組成的列表
    """
    v_code_list = []
    v_code_str = ""
    for i in range(length):
        num_str = str(random.randint(0,9))
        uppercase = chr(random.randint(65,90))
        lowercase = chr(random.randint(97,122))
        v_code_list.append(random.choice([num_str,lowercase,uppercase]))

    v_code_str = "".join(v_code_list)
    return v_code_str,v_code_list

#獲取隨機顔色
def get_random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))


#隨機生成驗證碼圖片
def random_verificate_code_img():

    im_path = "static/imgs/v_code_bj_1.png"
    image_obj = Image.open(im_path)
    # cropedIm = im.crop((700, 100, 1200, 1000))
    # cropedIm.save(r'C:\Users\Administrator\Desktop\cropped.png')

    # image_obj = Image.new(
    #     "RGB",  # 格式
    #     (250,35),  # 大小
    #     # (255,255,255)  # 顔色
    #     get_random_color()
    # )

    draw_obj = ImageDraw.Draw(image_obj)  # 在哪裏寫
    font_obj = ImageFont.truetype("static/fonts/AjiwaiPro.TTF",28)  # 用什麽寫
    v_code_str, v_code_list = random_verificate_code(5)
    for i in range(len(v_code_list)):
        draw_obj.text((i * 20 + 15, 2), v_code_list[i], fill=get_random_color(), font=font_obj)

    width = 125
    height = 35
    # for i in range(5):
    #     x1 = random.randint(0,width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw_obj.line((x1,y1,x2,y2),fill=get_random_color())
    #
    # for i in range(40):
    #     draw_obj.point([random.randint(0,width),random.randint(0,height)],fill=get_random_color())
    #     x = random.randint(0,width)
    #     y = random.randint(0, height)
    #     draw_obj.arc((x,y,x+4,y+4),0,90,fill=get_random_color())

    #直接將生成的圖片保存到内存中
    f = BytesIO()
    image_obj.save(f,'png')
    v_code_img = f.getvalue()

    return v_code_img,v_code_str








