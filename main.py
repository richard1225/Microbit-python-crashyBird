from microbit import *

M_ARRAY = [[ '0' for i in range(5)] for j in range(5)]
SCORE = 0
BIRD_POINT = 2 # 小鸟初始化在2点
GAME_OVER = False
obs_last_count = 0
bird_last_count = 0

def is_crashed(bird_point, obstate_array):
    """
        判断小鸟是否撞毁，如果撞毁，返回True
    """
    return True if obstate_array[BIRD_POINT][0] == '0' else False

def array_to_image(m_array):
    """
        把二维字符串输转转成Image对象
    """
    res_str = ''
    for line in m_array:
        res_str += ''.join(line)
        res_str += ':'

    res_str = res_str[:-1]
    return Image(res_str)

def obs_move():
    pass

def bird_move(step):
    """
        验证小鸟是否合法
    """
    global BIRD_POINT
    global GAME_OVER
    if BIRD_POINT + step >= 0 and BIRD_POINT + step <= 4:
        if is_crashed(BIRD_POINT + step, M_ARRAY):
            GAME_OVER = True
        else:
            BIRD_POINT += step

initial_array = M_ARRAY[:]

while True:
    if obs_last_count == 0:
        initial_array[BIRD_POINT][0] = '9'
        display.show(array_to_image(initial_array))
        if button_a.is_pressed():
            obs_last_count = running_time()
            bird_last_count = running_time()
            # display.show(running_time())

    # start game
    else:
        if not GAME_OVER:
            tmp = M_ARRAY[:]
            tmp[BIRD_POINT][0] = '9'
            display.show(array_to_image(M_ARRAY))
            if button_a.is_pressed():
                bird_move(1)
            elif button_b.is_pressed():
                bird_move(-1)
        else:
            display.scroll('Score: '+str(SCORE))
            break

display.clear()

