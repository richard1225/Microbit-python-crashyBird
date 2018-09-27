from microbit import *
import random
import time
OBS_ARRAY = [[ '0' for i in range(5)] for j in range(5)]
SCORE = 0
BIRD_POINT = 2 # 小鸟初始化在2点
GAME_OVER = False
WILL_GEN_NEW = 1 # 当前轮次是否产生新障碍
SPEED = 1000 # 障碍移动速度，1秒
obs_last_count = 0
bird_last_count = 0

def is_crashed(bird_point, obstate_array):
    """
        判断小鸟是否撞毁，如果撞毁，返回True
    """
    return True if obstate_array[BIRD_POINT][0] != '0' else False

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
    global WILL_GEN_NEW
    global OBS_ARRAY
    global GAME_OVER
    global SCORE
    new_obs = 0

    # 障碍总体向左移动
    for line in OBS_ARRAY:
        for i in range(0,4): # 从 0 到 4-1
            line[i] = line[i+1]

    if WILL_GEN_NEW == 1:
        new_obs = random.randint(0,4) # 从 0 到 4
        
        obs_line = [ '9' for i in range(5) ]
        obs_line[new_obs] = '0'
    else:
        obs_line = [ '0' for i in range(5) ]

    for i in range(0,5): # 从 0 到 5-1
        OBS_ARRAY[i][4] = obs_line[i]

    if is_crashed(BIRD_POINT, OBS_ARRAY):
        GAME_OVER = True
    else:
        SCORE += 1
    WILL_GEN_NEW ^= 1 # 隔次生成障碍

def deepcopy(array):
    return [i[:] for i in array]

def bird_move(step):
    """
        验证小鸟是否合法
    """
    global BIRD_POINT
    global GAME_OVER
    if BIRD_POINT + step >= 0 and BIRD_POINT + step <= 4:
        if is_crashed(BIRD_POINT + step, OBS_ARRAY):
            GAME_OVER = True
            BIRD_POINT += step
            pass
        else:
            BIRD_POINT += step

initial_array = deepcopy(OBS_ARRAY)

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
            if running_time() - obs_last_count > SPEED:
                obs_move()
                obs_last_count = running_time()

            tmp = deepcopy(OBS_ARRAY)
            tmp[BIRD_POINT][0] = '9'
            display.show(array_to_image(tmp))
            if button_a.is_pressed():
                bird_move(1)
                time.sleep(0.1) 
            elif button_b.is_pressed():
                bird_move(-1)
                time.sleep(0.1)  
        else:
            display.scroll('Score: '+str(SCORE-5))
            break

display.clear()

