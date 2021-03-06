import math, re

# 网线长度 1m=100cm 1cm=10mm
# CABLE_LENGTH = [3000, 5000, 6000, 8000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000] #mm


# 挂纤轮本身直径
WHEEL = 103
WHEEL_D = 62 #小直径

# 13个挂纤轮底部圆弧到底部的距离，每个间距228
WHEEL_DISTANCE = [3047, 2819, 2591, 2363, 2135, 1907, 1679, 1451, 1223, 995, 767, 539, 311]
# WHEEL_DISTANCE = {
#     '1': 3150,
#     '2': 2922,
#     '3': 2694,
#     '4': 2466,
#     '5': 2238,
#     '6': 2010,
#     '7': 1782,
#     '8': 1554,
#     '9': 1326,
#     '10': 1098,
#     '11': 870,
#     '12': 642,
#     '13': 414
# }

# 大线环1、2本身直径
LINE = 56

# 正面大线环1底边框到底部的距离（每块slot的border-bottom到底部距离）,每个间距340
BIGLINE_DISTANCE = {
    '1': 2886,
    '2': 2546,
    '3': 2206,
    '4': 1866,
    '5': 1526,
    '6': 1186,
    '7': 846,
    '8': 506,
    '9': 166
}

#大线环2底边框到底部距离，（每个大线环2之间340mm），（大线环1和大线环2之间83mm），（大线环2本身高度67mm）
BIGLINE2_DISTANCE = {
    '1': 2803,
    '2': 2463,
    '3': 2123,
    '4': 1783,
    '5': 1443,
    '6': 1103,
    '7': 763,
    '8': 423,
    '9': 83
}


# 组合线环底边框到底部距离，每个组合线环之间169mm，每4个之间相距527mm
COMBINATION_RING = {
    '1': 3035,
    '2': 2866,
    '3': 2697,
    '4': 2528,
    '5': 2001,
    '6': 1832,
    '7': 1663,
    '8': 1494,
    '9': 967,
    '10': 798,
    '11': 629,
    '12': 460
}

# 72芯配线单元ABCD EFGH IJKL
PEIXIAN_DANYUAN = {
    '1': '12',
    '2': '11',
    '3': '10',
    '4': '9',
    '5': '8',
    '6': '7',
    '7': '6',
    '8': '5',
    '9': '4',
    '10': '3',
    '11': '2',
    '12': '1'
}


# 组合线环对应的大线环2所在的设备区域H
COMBINATION_VS_BIGLINE2 = {
    '1': '1',
    '2': '1',
    '3': '2',
    '4': '2',
    '5': '3',
    '6': '4',
    '7': '5',
    '8': '5',
    '9': '7',
    '10': '7',
    '11': '8',
    '12': '8'
}


# 从96芯出来后分别对应左挂纤轮
FRONT_LEFT_WHEEL = {
    '1': '3',
    '2': '4',
    '3': '6',
    '4': '7',
    '5': '9',
    '6': '10',
    '7': '12',
    '8': '13',
    '9': '13'
}


# 从72芯出来后分别对应右挂纤轮
BACK_RIGHT_WHEEL = {
    '1': '3',
    '2': '3',
    '3': '4',
    '4': '4',
    '5': '6',
    '6': '7',
    '7': '8',
    '8': '9',
    '9': '11',
    '10': '12',
    '11': '12',
    '12': '13'
}


def format_radio_96(row, col):
    return str(1+24*(int(row)-1)+(int(col)-1))


# 计算每块slot的端口数，用户template模板渲染
def calculate_slot(rows,cols,list):
    cols = range(1,cols+1)
    rows = range(1,rows+1)
    for r in rows:
        for c in cols:
            list.append((r,c))
    return list


def distance_sqrt(row, col):
    row = int(row)
    col = int(col)
    result = math.sqrt(row*row + col*col)
    return result

# 计算同一设备、同side、正面，跳纤方式
def calculate_one_front_front(jiechushebei_radio,jierushebei_radio, \
                              jiechushebei_slot_rows,jiechushebei_slot_cols, \
                              jierushebei_slot_rows,jierushebei_slot_cols, \
                              jiechushebei,jierushebei,CABLE_LENGTH):
    # json0 = ['相同机架的96芯设备单元与96芯设备单元跳纤']
    from_point = jiechushebei_radio
    to_point = jierushebei_radio
    from_slot_rows = jiechushebei_slot_rows
    from_slot_cols = jiechushebei_slot_cols
    to_slot_rows = jierushebei_slot_rows
    to_slot_cols = jierushebei_slot_cols
    from_name = jiechushebei
    to_name = jierushebei
    print('from_point'+str(from_point))
    print('to_point'+str(to_point))
    # 1. 先往下走到小线环
    distance_step_1 = (len(from_slot_rows) - int(from_point[1]) + 1) * 35
    # distance_step_1 = (len(from_slot_rows) - int(from_point[1]) + 1) * 35 + 900
    print('1. 先从'+from_name+'的'+from_point[0]+'('+from_point[1]+','+from_point[2]+')'+'端口出来往下经过下方最近的8位小线环:' + str(distance_step_1))

    log1 = '先从'+from_name+'的96芯设备单元H'+from_point[0]+'端口('+format_radio_96(from_point[1],from_point[2])+')'+'出来往下经过下方邻近的8位小线环。'
    pic_step1 = (230+(int(from_point[2])-1)*18, 315+(int(from_point[0])-1)*320+(int(from_point[1])-1)*35)
    pic_step2 = (pic_step1[0], pic_step1[1]+35*(5-int(from_point[1])))

    json1 = from_point[0]+'('+from_point[1]+','+from_point[2]+')'

    # 2. 往右穿过中线环，最后一个端口到slot边框/中线环是26mm，（到大线环1左边框是99mm，）,从中线环顶边到大线环2底边是190mm
    if int(from_point[2]) < 12 :
        distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 12 + 26 + 140
    else:
        distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 26 + 140
    print('2. 再经过中线环到大线环1:' + str(distance_step_2))

    log2 = '往右穿过中线环再到设备单元H'+from_point[0]+'的大线环1。'
    pic_step3 = (pic_step2[0]+distance_step_2-140,pic_step2[1])
    pic_step4 = (pic_step3[0]+80,pic_step3[1]+30)

    json2 = from_point[0]+'-大线环1'

    # 3. 往上走先到高于from_pront的挂纤轮，再往下走直到侧面最下面那个挂纤轮调头向上走
    # 大线环1到高于其的挂纤轮
    wheel_above = []
    wheel_bottom = []
    # if from_point[0] < to_point[0]:
    #     above_point = from_point[0]
    # else:
    #     above_point = to_point[0]
    for wheel_d in WHEEL_DISTANCE:
        if wheel_d + WHEEL_D > (WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]])-1-1]):
            wheel_above.append(wheel_d)
    wheel_above.sort()
    # from_point大线环1到from_ponit下面左挂纤轮+左挂纤轮到wheel_above
    distance_step_3_1 = distance_sqrt(450, BIGLINE_DISTANCE[from_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]])-1])
    distance_step_3_1 = distance_step_3_1 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]])-1]))
    # distance_step_3_1_0 = wheel_above[0]+WHEEL - (BIGLINE_DISTANCE[from_point[0]]+LINE)
    # print('dddddd', distance_step_3_1_0)

    # 高挂纤轮wheel_above到最下面的挂纤轮
    distance_step_3_2 = wheel_above[0]+WHEEL - WHEEL_DISTANCE[-1]

    # 调头向上到高于to_point的挂纤轮
    if int(to_point[0]) == 9:
        wheel_bottom.append(WHEEL_DISTANCE[-2])
    else:
        for wheel_d in WHEEL_DISTANCE:
            if wheel_d + WHEEL_D > (WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]])-1-1]):
                wheel_bottom.append(wheel_d)
        wheel_bottom.sort()
    distance_step_3_3 = wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[-1]

    distance_step_3 = distance_step_3_1 + distance_step_3_2 + distance_step_3_3

    # log[2]
    log3 = '穿过设备单元H'+from_point[0]+'大线环1后，经过'+from_name+'左挂纤轮'+str(13-int(FRONT_LEFT_WHEEL[from_point[0]])+1)+'，至中挂纤轮'+str(12-WHEEL_DISTANCE.index(wheel_above[0])+1)+\
           '。再到最下面的中挂纤轮1'+'，再至中挂纤轮'+str(12-WHEEL_DISTANCE.index(wheel_bottom[0])+1)+'，至左挂纤轮'+str(13-int(FRONT_LEFT_WHEEL[to_point[0]])+1)
    if int(to_point[0]) == 9 and int(from_point[0]) == 9:
        log3 = '穿过设备单元H' + from_point[0] + '大线环1后，经过' + from_name + '中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
               '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
    elif int(to_point[0]) == 9:
        log3 = '穿过设备单元H' + from_point[0] + '大线环1后，经过' + from_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
               '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
    elif int(from_point[0]) == 9:
        log3 = '穿过设备单元H' + from_point[0] + '大线环1后，经过' + from_name + '中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
               '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[to_point[0]]) + 1)
    pic_step5 = (255, 470+(int(from_point[0])-1)*320)  # 侧-大线环1
    pic_step5_1 = (405, 360+(int(FRONT_LEFT_WHEEL[from_point[0]])-1)*220)  # from_point对应左挂纤轮
    if int(from_point[0]) == 9:
        pic_step5_1 = (0,0)
    pic_step6 = (590, 230+(WHEEL_DISTANCE.index(wheel_above[0])+1-1)*215)  # wheel_above
    pic_step7 = (590, 230+(WHEEL_DISTANCE.index(wheel_bottom[0])+1-1)*215)  # wheel_bottom
    pic_step7_1 = (405, 360+(int(FRONT_LEFT_WHEEL[to_point[0]])-1)*220)  # to_point对应做挂纤轮
    if int(to_point[0]) == 9:
        pic_step7_1 = (0,0)

    json3 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0])+1)
    json4 = '挂纤轮-13'
    json5 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0])+1)

    # 4. wheel_bottom到to_point下面左挂纤轮+to_point下面做挂纤轮到to_point大线环1
    distance_step_4 = distance_sqrt(450, BIGLINE_DISTANCE[to_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]])-1])
    distance_step_4 = distance_step_4 + distance_sqrt(200, (wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]])-1]))
    # distance_step_4_0 = wheel_bottom[0] + WHEEL - (BIGLINE_DISTANCE[to_point[0]] + LINE)
    # print(distance_step_4_0)

    log4 = '进入'+to_name+'的96芯设备单元H'+to_point[0]+'的大线环1。'
    pic_step8 = (255,490+(int(to_point[0])-1)*320)  # to_point 大线环1

    # 6. 往左进入slot的中线环，进入该端口邻近的8位小线环
    if int(to_point[2]) < 12 :
        distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 12 + 26 + 140
    else:
        distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 26 + 140
    print('6. 往左进入slot的中线环，进入该端口邻近的8位小线环:' + str(distance_step_6))

    log5 = '从'+to_name+'的96芯设备单元H'+to_point[0]+'的大线环1出来后，往左进入'+to_name+'设备单元'+to_point[0]+'的中线环，并将线嵌入邻近的8位小线环中。'
    pic_step9 = (230+(int(to_point[2])-1)*18, 315+(int(to_point[0])-1)*320+(int(to_point[1])-1)*35)
    pic_step10 = (pic_step9[0] , pic_step9[1]+35*(5-int(to_point[1])))
    pic_step11 = (pic_step10[0]+distance_step_6-140,pic_step10[1])
    pic_step12 = (pic_step11[0]+80,pic_step11[1]+30)

    json6 = to_point[0] + '-大线环1'
    json7 = to_point[0] + '(' + to_point[1] + ',' + to_point[2] + ')'

    # 7. 往上插入端口
    distance_step_7 = (len(to_slot_rows) - int(to_point[1]) + 1) * 35
    print('往上插入端口:' + str(distance_step_7))

    log6 = '最后往上将线插入'+to_name+'96芯设备单元H'+to_point[0]+'端口('+format_radio_96(to_point[1],to_point[2])+')中。'

    used_distance = distance_step_1+distance_step_2+distance_step_3+distance_step_4+distance_step_6+distance_step_7+200
    print('总共需要线长：' + str(used_distance))
    cable_list = []
    for cable in CABLE_LENGTH:
        if cable > used_distance:
            cable_list.append(cable)
    cable_list.sort()
    shengyu_xianchang = cable_list[0]-used_distance
    print('剩余线长：'+ str(shengyu_xianchang))


    # # 调整上下挂纤轮

    log0 = '此次跳纤计算的长度为' + str(round(used_distance / 1000, 1)) + '米，请选择一根长度为' + \
           str(int(cable_list[0] / 1000)) + '米的光纤跳线。'
    # json3 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
    # json5 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0]) + 1)

    log_list = [log0, log1, log2, log3, log4, log5, log6]
    step_list = [pic_step1, pic_step2, pic_step3, pic_step4, pic_step5, pic_step6, pic_step7, pic_step8, \
                 pic_step9, pic_step10, pic_step11, pic_step12, pic_step5_1, pic_step7_1]
    json_list = [1, log_list, json1, json2, json3, json4, json5, json6, json7]

    print(step_list)
    print(log_list)
    print('used_distance:', used_distance)
    return step_list, log_list, json_list, int(cable_list[0] / 1000)


# 计算同一设备、同side、背面，跳纤方式
def calculate_one_back_back(jiechushebei_radio,jierushebei_radio, \
                              jiechushebei,jierushebei,CABLE_LENGTH):
    # json0 = ['相同机架的72芯配线单元与72芯配线单元跳纤']
    from_point = jiechushebei_radio
    to_point = jierushebei_radio
    from_name = jiechushebei
    to_name = jierushebei
    print('from_point'+str(from_point))
    print('to_point'+str(to_point))
    # 1. 先从第几排托盘往左出来
    distance_step_1 = 84 + 20.5 * (int(from_point[2]) - 1)
    # log[1] 一
    log1 = '先从' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[from_point[0]] + '端口(' + str(from_point[1]) + ',' + str(from_point[2]) + ')出来。'
    if int(from_point[0]) <= 4:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25)
    elif int(from_point[0]) > 4 and int(from_point[0]) <= 8:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25 + 335)
    elif int(from_point[0]) > 8 and int(from_point[0]) <= 12:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25 + 335 * 2)
    pic_step2 = (250, pic_step1[1])

    json1 = PEIXIAN_DANYUAN[from_point[0]] + '(' + from_point[1] + ',' + from_point[2] + ')'

    # 2. 进入组合线环#XX中的小孔
    distance_step_2 = 34 + 26 * (6 - int(from_point[1]))
    print('2. 进入组合线环' + str(from_point[0]) + '中的小孔:' + str(distance_step_2))
    # log[2] 一
    log2 = '进入' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[from_point[0]] + '组合线环的小孔。'
    if int(from_point[0]) <= 4:
        pic_step3 = (250, 360 + 160 * (int(from_point[0]) - 1))
    elif int(from_point[0]) > 4 and int(from_point[0]) <= 8:
        pic_step3 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340)
    elif int(from_point[0]) > 8 and int(from_point[0]) <= 12:
        pic_step3 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340 * 2)

    json2 = PEIXIAN_DANYUAN[from_point[0]] + '-小孔'

    # 3. 进入组合线环#XX+1的大孔
    if int(from_point[0]) < 12:
        if from_point[0] == '4' or from_point[0] == '8':
            distance_step_3 = 527  # 每四个之间相距527mm
        else:
            distance_step_3 = 169  # 组合线环之间相距169mm
        log3 = '进入' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]) + 1)] + '组合线环的大孔。'
        if int(from_point[0]) + 1 <= 4:
            pic_step4 = (250, 360 + 160 * int(from_point[0]))  # 背-大孔
            pic_step5 = (1080, 340 + 160 * int(from_point[0]))  # 侧-大孔
        elif int(from_point[0]) + 1 > 4 and int(from_point[0]) + 1 <= 8:
            pic_step4 = (250, 360 + 160 * int(from_point[0]) + 340)
            pic_step5 = (1080, 340 + 160 * int(from_point[0]) + 340)
        elif int(from_point[0]) + 1 > 8 and int(from_point[0]) + 1 <= 12:
            pic_step4 = (250, 360 + 160 * int(from_point[0]) + 340 * 2)
            pic_step5 = (1080, 340 + 160 * int(from_point[0]) + 340 * 2)
        pic_step5_1 = (785, 360 + (int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) - 1) * 220)  # from_point对应右挂纤轮
        json3 = PEIXIAN_DANYUAN[str(int(from_point[0]) + 1)] + '-大孔'

    elif int(from_point[0]) == 12:
        distance_step_3 = 0
        # log3 = '进入' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]))] + '组合线环的大孔。'
        log3 = '从组合线环穿出至侧面挂纤轮。'
        if int(from_point[0]) <= 4:
            pic_step4 = (250, 360 + 160 * (int(from_point[0])-1))  # 背-大孔
            pic_step5 = (1080, 340 + 160 * (int(from_point[0])-1)) # 侧-大孔
        elif int(from_point[0]) + 1 > 4 and int(from_point[0]) <= 8:
            pic_step4 = (250, 360 + 160 * (int(from_point[0])-1) + 340)
            pic_step5 = (1080, 340 + 160 * (int(from_point[0])-1) + 340)
        elif int(from_point[0]) + 1 > 8 and int(from_point[0]) <= 12:
            pic_step4 = (250, 360 + 160 * (int(from_point[0])-1) + 340 * 2)
            pic_step5 = (1080, 340 + 160 * (int(from_point[0])-1) + 340 * 2)
        pic_step5_1 = (785, 360 + (int(BACK_RIGHT_WHEEL[from_point[0]]) - 1) * 220)  # from_point对应右挂纤轮
        json3 = PEIXIAN_DANYUAN[str(int(from_point[0]))] + '-大孔'

    # 4. 往上至高于from_point的挂纤轮，再往下走直到侧面最下面那个挂纤轮调头向上走
    wheel_above = []
    wheel_bottom = []
    if int(from_point[0]) < 12:
        compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) - 1 - 1]
    elif int(from_point[0]) == 12:
        compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1 - 1]
    for wheel_d in WHEEL_DISTANCE:
        if (wheel_d + WHEEL_D) > compare_num:
            wheel_above.append(wheel_d)
    wheel_above.sort()

    if int(from_point[0]) < 12:
        distance_step_4 = distance_sqrt(430, COMBINATION_RING[str(int(from_point[0])+1)] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0])+1)])-1])
        distance_step_4 = distance_step_4 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0])+1)])-1])
    elif int(from_point[0]) == 12:
        distance_step_4 = distance_sqrt(430, COMBINATION_RING[str(int(from_point[0]))] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1])
        distance_step_4 = distance_step_4 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1])

    # if int(from_point[0]) < 12:
    #     distance_step_4 = wheel_above[0]+WHEEL - COMBINATION_RING[str(int(from_point[0])+1)]
    # elif int(from_point[0]) == 12:
    #     distance_step_4 = wheel_above[0] + WHEEL - COMBINATION_RING[str(int(from_point[0]))]
    # 高挂纤轮到最下面的挂纤轮
    distance_step_5_1 = wheel_above[0]+WHEEL - WHEEL_DISTANCE[-1]
    # 调头向上到高于to_point的挂纤轮
    if int(to_point[0]) < 12:
        compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0]) + 1)]) - 1 - 1]
    elif int(to_point[0]) == 12:
        compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1 - 1]
    for wheel_d in WHEEL_DISTANCE:
        if (wheel_d + WHEEL_D) > compare_num:
            wheel_bottom.append(wheel_d)
    wheel_bottom.sort()
    distance_step_5_2 = wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[-1]
    distance_step_5 = distance_step_5_1 + distance_step_5_2

    pic_step6 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0])+1-1) * 215)  # wheel_above
    pic_step7 = (590, 230 + (WHEEL_DISTANCE.index(wheel_bottom[0])+1-1) * 215)  # wheel_bottom

    json4 = '挂纤轮-'+str(WHEEL_DISTANCE.index(wheel_above[0])+1)
    json5 = '挂纤轮-13'
    json6 = '挂纤轮-'+str(WHEEL_DISTANCE.index(wheel_bottom[0])+1)


    # wheel_bottom到to_point下面右挂纤轮，右挂纤轮至to_point大孔
    # 5. 往下进入to_point组合线环#XX+1的大孔
    if int(to_point[0]) < 12:
        log4_1 = '，再至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[str(int(to_point[0]) + 1)]) + 1)
    elif int(to_point[0]) == 12:
        log4_1 = '，再至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[to_point[0]]) + 1)
    if int(from_point[0]) < 12:
        log4 = '从72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]) + 1)] + '的大孔穿出后，至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) + 1) + \
               '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + '，再至最下面中挂纤轮1，然后至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + \
               log4_1
    elif int(from_point[0]) == 12:
        log4 = '从72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]))] + '的小孔穿出后，至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[from_point[0]]) + 1) + \
               '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + '，再至最下面中挂纤轮1，然后至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + \
               log4_1

    if int(to_point[0]) < 12:
        distance_step_6 = distance_sqrt(200, wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)]) - 1])
        distance_step_6 = distance_step_6 +        distance_sqrt(430, COMBINATION_RING[str(int(to_point[0])+1)] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)])-1])
        # distance_step_6 = wheel_bottom[0]+WHEEL - COMBINATION_RING[str(int(to_point[0])+1)]
        # log[5]
        log5 = '进入'+to_name+'72芯配线单元L'+PEIXIAN_DANYUAN[str(int(to_point[0])+1)]+'组合线环的大孔。'
        json7 = PEIXIAN_DANYUAN[str(int(to_point[0])+1)] + '-大孔'
        if int(to_point[0])+1 <= 4:
            pic_step8 = (1080, 340 + 160 * int(to_point[0]))  # 侧-组合线环大孔
        elif int(to_point[0])+1 > 4 and int(to_point[0])+1 <= 8:
            pic_step8 = (1080, 340 + 160 * int(to_point[0]) + 340)
        elif int(to_point[0])+1 > 8 and int(to_point[0])+1 <= 12:
            pic_step8 = (1080, 340 + 160 * int(to_point[0]) + 340 * 2)
    elif int(to_point[0]) == 12:
        distance_step_6 = distance_sqrt(200, wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1])
        distance_step_6 = distance_step_6 +        distance_sqrt(430, COMBINATION_RING[to_point[0]] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1])
        # distance_step_6 = wheel_bottom[0]+WHEEL - COMBINATION_RING[str(int(to_point[0]))]
        # log[5]
        # log5 = '进入'+to_name+'72芯配线单元L'+PEIXIAN_DANYUAN[str(int(to_point[0]))]+'组合线环的大孔。'
        log5 = '进入'+to_name+'72芯配线单元L'+PEIXIAN_DANYUAN[str(int(to_point[0]))]+'组合线环'
        json7 = PEIXIAN_DANYUAN[str(int(to_point[0]))] + '-大孔'
        if int(to_point[0]) <= 4:
            pic_step8= (1080, 340 + 160 * (int(to_point[0])-1))
        elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
            pic_step8 = (1080, 340 + 160 * (int(to_point[0])-1) + 340)
        elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
            pic_step8 = (1080, 340 + 160 * (int(to_point[0])-1) + 340 * 2)


    # 6. 再向上进入to_point组合线环#XX的小孔
    if int(to_point[0]) < 12 :
        distance_step_7 = COMBINATION_RING[to_point[0]] - COMBINATION_RING[str(int(to_point[0])+1)]
        if int(to_point[0]) <= 4:
            pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1))  # 侧-组合线环小孔
        elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
            pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340)
        elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
            pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340 * 2)
    elif int(to_point[0]) == 12:
        distance_step_7 = 0
        pic_step9 = (pic_step8[0], pic_step8[1])

    log6 = '再进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]))] + '组合线环的小孔。'

    json8 = PEIXIAN_DANYUAN[str(int(to_point[0]))]+'-小孔'

    # 7. 往右进入指定托盘
    distance_step_8 = 34 + 26 * (6 - int(to_point[1])) + 84 + 20.5 * (int(to_point[2])-1)
    print('1. 往右进入'+to_name+'的'+str(to_point[0])+'号72芯配线单元的('+str(to_point[1])+','+str(to_point[2])+')托盘:'+str(distance_step_8))

    log7 = '从'+to_name+'72芯配线单元L'+PEIXIAN_DANYUAN[to_point[0]]+'组合线环的小孔穿出。'
    log8 = '往右进入'+to_name+'72芯配线单元L'+PEIXIAN_DANYUAN[str(to_point[0])]+'端口('+str(to_point[1])+','+str(to_point[2])+')中。'

    if int(to_point[0]) <= 4:
        pic_step10 = (250, 360 + 160 * (int(to_point[0])-1))
        pic_step12 = (325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25)
    elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
        pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1) + 340)
        pic_step12 = (325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335)
    elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
        pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1) + 340 * 2)
        pic_step12 = (325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335 * 2)
    pic_step11 = (250, pic_step12[1])

    json9 = PEIXIAN_DANYUAN[to_point[0]]+'('+to_point[1]+','+to_point[2]+')'

    if int(from_point[0]) == 6 and int(to_point[0]) == 12:
        increase = 180
    else:
        increase = 0
    used_distance = distance_step_1 + distance_step_2 + distance_step_3 + distance_step_4 + \
                    distance_step_5 + distance_step_6 + distance_step_7 + distance_step_8 + increase + 200
    print('总共需要线长：' + str(used_distance))
    cable_list = []
    for cable in CABLE_LENGTH:
        if cable > used_distance:
            cable_list.append(cable)
    cable_list.sort()
    shengyu_xianchang = cable_list[0] - used_distance
    print('剩余线长：' + str(shengyu_xianchang))

    # # 调整上下挂纤轮

    log0 = '此次跳纤计算的长度为' + str(round(used_distance / 1000, 1)) + '米，请选择一根长度为' + \
           str(int(cable_list[0] / 1000)) + '米的光纤跳线。'

    json4 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
    json6 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0]) + 1)  # json[6]

    if int(to_point[0]) < 12:
        pic_step8_1 = (405, 360 + (int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)]) - 1) * 220)  # to_point对应左挂纤轮
    elif int(to_point[0]) == 12:
        pic_step8_1 = (405, 360 + (int(BACK_RIGHT_WHEEL[to_point[0]]) - 1) * 220)  # to_point对应左挂纤轮

    log_list = [log0, log1, log2, log3, log4, log5, log6, log7, log8]
    step_list = [pic_step1, pic_step2, pic_step3, pic_step4, pic_step5, pic_step6, pic_step7, pic_step8, \
                 pic_step9, pic_step10, pic_step11, pic_step12, pic_step5_1, pic_step8_1]
    json_list = [1, log_list, json1, json2, json3, json4, json5, json6, json7, json8, json9]

    print(step_list)
    print(log_list)
    print('used_distance:', used_distance)
    return step_list, log_list, json_list, int(cable_list[0] / 1000)


# 计算不同设备、同side、正面，跳纤方式
def calculate_two_front_front(jiechushebei_radio,jierushebei_radio, \
                              jiechushebei_slot_rows,jiechushebei_slot_cols, \
                              jierushebei_slot_rows,jierushebei_slot_cols, \
                              jiechushebei,jierushebei,\
                              shebei_count,CABLE_LENGTH):
    # json0 = ['不同机架的96芯设备单元与96芯设备单元跳纤']
    from_point = jiechushebei_radio
    to_point = jierushebei_radio
    from_slot_rows = jiechushebei_slot_rows
    from_slot_cols = jiechushebei_slot_cols
    to_slot_rows = jierushebei_slot_rows
    to_slot_cols = jierushebei_slot_cols
    from_name = jiechushebei
    to_name = jierushebei
    right_to_left = 0
    if re.findall('\d+', from_name)[0] < re.findall('\d+', to_name)[0]:
        right_to_left = 1
    print('from_point'+str(from_point))
    print('to_point'+str(to_point))
    # 1. 先往下走到小线环
    distance_step_1 = (len(from_slot_rows) - int(from_point[1]) + 1) * 35

    if not right_to_left:
        log1 = '先从'+from_name+'的96芯设备单元H'+from_point[0]+'端口('+format_radio_96(from_point[1],from_point[2])+')'+'出来往下经过下方邻近的8位小线环。'
        pic_step1 = (230+(int(from_point[2])-1)*18, 315+(int(from_point[0])-1)*320+(int(from_point[1])-1)*35)
        pic_step2 = (pic_step1[0], pic_step1[1]+35*(5-int(from_point[1])))

        json1 = from_point[0]+'('+from_point[1]+','+from_point[2]+')'

        # 2. 往右穿过中线环，最后一个端口到slot边框/中线环是26mm，（到大线环1左边框是99mm，）,从中线环顶边到大线环2底边是190mm
        if int(from_point[2]) < 12:
            distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 12 + 26 + 140
        else:
            distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 26 + 140

        log2 = '往右穿过中线环再到设备单元H' + from_point[0] + '的大线环1。'
        if not right_to_left:
            log2 = '往右穿过中线环沿着水平走线槽经过' + str(shebei_count - 1) + '个机架，到' + to_name + '96芯设备单元H' + from_point[0] + '的大线环2。'
        pic_step3 = (pic_step2[0] + distance_step_2 - 140, pic_step2[1])
        pic_step4 = (pic_step3[0] + 80, pic_step3[1] + 30)

        json2 = from_point[0] + '-大线环1'

        # 3. 往上走先到高于from_pront的挂纤轮，再往下走直到侧面最下面那个挂纤轮调头向上走
        # 大线环1到高于其的挂纤轮
        wheel_above = []
        wheel_bottom = []
        # if from_point[0] < to_point[0]:
        #     above_point = from_point[0]
        # else:
        #     above_point = to_point[0]
        for wheel_d in WHEEL_DISTANCE:
            if wheel_d + WHEEL_D > (WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]])-1-1]):
                wheel_above.append(wheel_d)
        wheel_above.sort()
        # from_point大线环1到from_ponit下面左挂纤轮+左挂纤轮到wheel_above
        distance_step_3_1 = distance_sqrt(430, BIGLINE_DISTANCE[from_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]]) - 1])
        distance_step_3_1 = distance_step_3_1 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]]) - 1]))
        # distance_step_3_1 = wheel_above[0] + WHEEL - (BIGLINE_DISTANCE[from_point[0]] + LINE)

        # 高挂纤轮wheel_above到最下面的挂纤轮
        distance_step_3_2 = wheel_above[0] + WHEEL - WHEEL_DISTANCE[-1]

        # 调头向上到高于to_point的挂纤轮
        if int(to_point[0]) == 9:
            wheel_bottom.append(WHEEL_DISTANCE[-2])
        else:
            for wheel_d in WHEEL_DISTANCE:
                if wheel_d + WHEEL_D > (WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]])-1-1]):
                    wheel_bottom.append(wheel_d)
            wheel_bottom.sort()
        distance_step_3_3 = wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[-1]

        distance_step_3 = distance_step_3_1 + distance_step_3_2 + distance_step_3_3

        # log[2]
        if right_to_left:
            log3 = '穿过设备单元H' + from_point[0] + '大线环1后，经过' + from_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                   '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[to_point[0]]) + 1)
            if int(to_point[0]) == 9 and int(from_point[0]) == 9:
                log3 = '穿过设备单元H' + from_point[0] + '大线环1后，经过' + from_name + '中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
            elif int(to_point[0]) == 9:
                log3 = '穿过设备单元H' + from_point[0] + '大线环1后，经过' + from_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
            elif int(from_point[0]) == 9:
                log3 = '穿过设备单元H' + from_point[0] + '大线环1后，经过' + from_name + '中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[to_point[0]]) + 1)
        elif not right_to_left:
            log3 = '从设备单元H' + from_point[0] + '大线环2穿出后，经过' + to_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                   '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[to_point[0]]) + 1)
            if int(to_point[0]) == 9 and int(from_point[0]) == 9:
                log3 = '从设备单元H' + from_point[0] + '大线环2穿出后，经过' + to_name + '中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
            elif int(to_point[0]) == 9:
                log3 = '从设备单元H' + from_point[0] + '大线环2穿出后，经过' + to_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
            elif int(from_point[0]) == 9:
                log3 = '从设备单元H' + from_point[0] + '大线环2穿出后，经过' + to_name + '中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[to_point[0]]) + 1)
        pic_step5 = (255, 470 + (int(from_point[0]) - 1) * 320)  # 侧-大线环1
        pic_step5_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[from_point[0]]) - 1) * 220)  # from_point对应左挂纤轮
        if int(from_point[0]) == 9:
            pic_step5_1 = (0, 0)
        pic_step6 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0]) + 1 - 1) * 215)  # wheel_above
        pic_step7 = (590, 230 + (WHEEL_DISTANCE.index(wheel_bottom[0]) + 1 - 1) * 215)  # wheel_bottom
        pic_step7_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[to_point[0]]) - 1) * 220)  # to_point对应做挂纤轮
        if int(to_point[0]) == 9:
            pic_step7_1 = (0, 0)

        json3 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
        json4 = '挂纤轮-13'
        json5 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0]) + 1)

        # 4. wheel_bottom到to_point下面左挂纤轮+to_point下面做挂纤轮到to_point大线环1
        distance_step_4_1 = distance_sqrt(430, BIGLINE2_DISTANCE[to_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1])
        distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, (wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1]))
        # distance_step_4_1 = wheel_bottom[0] + WHEEL - (BIGLINE2_DISTANCE[to_point[0]] + LINE)
        # 大线环2到水平走线槽边缘42mm，经过几个走线槽到to_point大线环1
        distance_step_4_2 = (shebei_count - 1) * 748 + 42
        if right_to_left:
            distance_step_4_2 = (shebei_count - 1) * 748 + 200  # 42
        distance_step_4 = distance_step_4_1 + distance_step_4_2

        log4 = '进入' + from_name + '96芯设备单元H' + to_point[0] + '的大线环2。'
        if not right_to_left:
            log4 = '进入' + to_name + '96芯设备单元H' + to_point[0] + '的大线环2。'
        log4_1 = '从' + from_name + '96芯设备单元H' + to_point[0] + '的大线环2出来后，沿水平走线槽经过' + str(shebei_count - 1) + '个机架。'
        log4_2 = '到' + to_name + '96芯设备单元H' + to_point[0] + '的中线环。'
        if not right_to_left:
            log4_1 = ''
            log4_2 = ''

        # pic_step6 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0]) + 1 - 1) * 215)  # wheel_above
        # # pic_step7 = (590, 230 + (WHEEL_DISTANCE.index(wheel_bottom[0])+1-1) * 215)  # wheel_bottom
        pic_step8_1 = (750, 535 + (int(to_point[0]) - 1) * 320)  # 2正-大线环2
        if right_to_left:
            pic_step8_1 = (750+930, 535 + (int(to_point[0]) - 1) * 320)  # 2正-大线环2
        # pic_step14 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0]) + 1 - 1) * 215)  #
        #
        pic_step8 = (235, 570+(int(to_point[0])-1)*320)  # 侧-大线环2

        # 6. 往左进入slot的中线环，进入该端口邻近的8位小线环
        if int(to_point[2]) < 12 :
            distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 12 + 26 + 140
        else:
            distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 26 + 140

        log5 = '从'+to_name+'的96芯设备单元H'+to_point[0]+'的中线环出来后，将线嵌入邻近的8位小线环中。'
        if not right_to_left:
            log5 = '从' + to_name + '的96芯设备单元H' + to_point[0] + '的大线环2出来后，进去中线环，再将线嵌入邻近的8位小线环中。'
        pic_step9 = (230+(int(to_point[2])-1)*18, 315+(int(to_point[0])-1)*320+(int(to_point[1])-1)*35)
        pic_step10 = (pic_step9[0], pic_step9[1]+35*(5-int(to_point[1])))
        pic_step11 = (pic_step10[0]+distance_step_6-140,pic_step10[1])
        pic_step12 = (pic_step11[0]+80, pic_step11[1]+30)

    elif right_to_left:
        log1 = '先从' + from_name + '的96芯设备单元H' + from_point[0] + '端口(' + format_radio_96(from_point[1], from_point[2]) + ')' + '出来往下经过下方邻近的8位小线环。'
        pic_step1 = (230 + (int(from_point[2]) - 1) * 18, 315 + (int(from_point[0]) - 1) * 320 + (int(from_point[1]) - 1) * 35)
        pic_step2 = (pic_step1[0], pic_step1[1] + 35 * (5 - int(from_point[1])))

        json1 = from_point[0] + '(' + from_point[1] + ',' + from_point[2] + ')'

        # 2. 往右穿过中线环，最后一个端口到slot边框/中线环是26mm，（到大线环1左边框是99mm，）,从中线环顶边到大线环2底边是190mm
        if int(from_point[2]) < 12:
            distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 12 + 26 + 140
        else:
            distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 26 + 140

        log2 = '往右穿过中线环再到设备单元H' + from_point[0] + '的大线环1。'
        if not right_to_left:
            log2 = '往右穿过中线环沿着水平走线槽经过' + str(shebei_count - 1) + '个机架，到' + to_name + '96芯设备单元H' + from_point[
                0] + '的大线环2。'
        pic_step3 = (pic_step2[0] + distance_step_2 - 140, pic_step2[1])
        pic_step4 = (pic_step3[0] + 80, pic_step3[1] + 30)

        json2 = from_point[0] + '-大线环1'

        # 3. 往上走先到高于from_pront的挂纤轮，再往下走直到侧面最下面那个挂纤轮调头向上走
        # 大线环1到高于其的挂纤轮
        wheel_above = []
        wheel_bottom = []
        # if from_point[0] < to_point[0]:
        #     above_point = from_point[0]
        # else:
        #     above_point = to_point[0]
        for wheel_d in WHEEL_DISTANCE:
            if wheel_d + WHEEL_D > (WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]]) - 1 - 1]):
                wheel_above.append(wheel_d)
        wheel_above.sort()
        # from_point大线环1到from_ponit下面左挂纤轮+左挂纤轮到wheel_above
        distance_step_3_1 = distance_sqrt(430, BIGLINE_DISTANCE[from_point[0]] + LINE - WHEEL_DISTANCE[
            int(FRONT_LEFT_WHEEL[from_point[0]]) - 1])
        distance_step_3_1 = distance_step_3_1 + distance_sqrt(200, (
        wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]]) - 1]))
        # distance_step_3_1 = wheel_above[0] + WHEEL - (BIGLINE_DISTANCE[from_point[0]] + LINE)

        # 高挂纤轮wheel_above到最下面的挂纤轮
        distance_step_3_2 = wheel_above[0] + WHEEL - WHEEL_DISTANCE[-1]

        # 调头向上到高于to_point的挂纤轮
        if int(to_point[0]) == 9:
            wheel_bottom.append(WHEEL_DISTANCE[-2])
        else:
            for wheel_d in WHEEL_DISTANCE:
                if wheel_d + WHEEL_D > (WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1 - 1]):
                    wheel_bottom.append(wheel_d)
            wheel_bottom.sort()
        distance_step_3_3 = wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[-1]

        distance_step_3 = distance_step_3_1 + distance_step_3_2 + distance_step_3_3

        # log[2]
        if right_to_left:
            log3 = '穿过设备单元H' + from_point[0] + '大线环1后，经过' + from_name + '左挂纤轮' + str(
                13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(
                12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                   '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(
                13 - int(FRONT_LEFT_WHEEL[to_point[0]]) + 1)
            if int(to_point[0]) == 9 and int(from_point[0]) == 9:
                log3 = '穿过设备单元H' + from_point[0] + '大线环1后，经过' + from_name + '中挂纤轮' + str(
                    12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
            elif int(to_point[0]) == 9:
                log3 = '穿过设备单元H' + from_point[0] + '大线环1后，经过' + from_name + '左挂纤轮' + str(
                    13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(
                    12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
            elif int(from_point[0]) == 9:
                log3 = '穿过设备单元H' + from_point[0] + '大线环1后，经过' + from_name + '中挂纤轮' + str(
                    12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(
                    12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(
                    13 - int(FRONT_LEFT_WHEEL[to_point[0]]) + 1)
        elif not right_to_left:
            log3 = '从设备单元H' + from_point[0] + '大线环2穿出后，经过' + to_name + '左挂纤轮' + str(
                13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(
                12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                   '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(
                13 - int(FRONT_LEFT_WHEEL[to_point[0]]) + 1)
            if int(to_point[0]) == 9 and int(from_point[0]) == 9:
                log3 = '从设备单元H' + from_point[0] + '大线环2穿出后，经过' + to_name + '中挂纤轮' + str(
                    12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
            elif int(to_point[0]) == 9:
                log3 = '从设备单元H' + from_point[0] + '大线环2穿出后，经过' + to_name + '左挂纤轮' + str(
                    13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(
                    12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
            elif int(from_point[0]) == 9:
                log3 = '从设备单元H' + from_point[0] + '大线环2穿出后，经过' + to_name + '中挂纤轮' + str(
                    12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                       '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(
                    12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(
                    13 - int(FRONT_LEFT_WHEEL[to_point[0]]) + 1)
        pic_step5 = (255, 470 + (int(from_point[0]) - 1) * 320)  # 侧-大线环1
        pic_step5_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[from_point[0]]) - 1) * 220)  # from_point对应左挂纤轮
        if int(from_point[0]) == 9:
            pic_step5_1 = (0, 0)
        pic_step6 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0]) + 1 - 1) * 215)  # wheel_above
        pic_step7 = (590, 230 + (WHEEL_DISTANCE.index(wheel_bottom[0]) + 1 - 1) * 215)  # wheel_bottom
        pic_step7_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[to_point[0]]) - 1) * 220)  # to_point对应做挂纤轮
        if int(to_point[0]) == 9:
            pic_step7_1 = (0, 0)

        json3 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
        json4 = '挂纤轮-13'
        json5 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0]) + 1)

        # 4. wheel_bottom到to_point下面左挂纤轮+to_point下面做挂纤轮到to_point大线环1
        distance_step_4_1 = distance_sqrt(430, BIGLINE2_DISTANCE[to_point[0]] + LINE - WHEEL_DISTANCE[
            int(FRONT_LEFT_WHEEL[to_point[0]]) - 1])
        distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, (
        wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1]))
        # distance_step_4_1 = wheel_bottom[0] + WHEEL - (BIGLINE2_DISTANCE[to_point[0]] + LINE)
        # 大线环2到水平走线槽边缘42mm，经过几个走线槽到to_point大线环1
        distance_step_4_2 = (shebei_count - 1) * 748 + 42
        if right_to_left:
            distance_step_4_2 = (shebei_count - 1) * 748 + 200  # 42
        distance_step_4 = distance_step_4_1 + distance_step_4_2

        log4 = '进入' + from_name + '96芯设备单元H' + to_point[0] + '的大线环2。'
        if not right_to_left:
            log4 = '进入' + to_name + '96芯设备单元H' + to_point[0] + '的大线环2。'
        log4_1 = '从' + from_name + '96芯设备单元H' + to_point[0] + '的大线环2出来后，沿水平走线槽经过' + str(shebei_count - 1) + '个机架。'
        log4_2 = '到' + to_name + '96芯设备单元H' + to_point[0] + '的中线环。'
        if not right_to_left:
            log4_1 = ''
            log4_2 = ''

        # pic_step6 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0]) + 1 - 1) * 215)  # wheel_above
        # # pic_step7 = (590, 230 + (WHEEL_DISTANCE.index(wheel_bottom[0])+1-1) * 215)  # wheel_bottom
        pic_step8_1 = (750, 535 + (int(to_point[0]) - 1) * 320)  # 2正-大线环2
        if right_to_left:
            pic_step8_1 = (750 + 930, 535 + (int(to_point[0]) - 1) * 320)  # 2正-大线环2
        # pic_step14 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0]) + 1 - 1) * 215)  #
        #
        pic_step8 = (235, 570 + (int(to_point[0]) - 1) * 320)  # 侧-大线环2

        # 6. 往左进入slot的中线环，进入该端口邻近的8位小线环
        if int(to_point[2]) < 12:
            distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 12 + 26 + 140
        else:
            distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 26 + 140

        log5 = '从' + to_name + '的96芯设备单元H' + to_point[0] + '的中线环出来后，将线嵌入邻近的8位小线环中。'
        if not right_to_left:
            log5 = '从' + to_name + '的96芯设备单元H' + to_point[0] + '的大线环2出来后，进去中线环，再将线嵌入邻近的8位小线环中。'
        pic_step9 = (
        230 + (int(to_point[2]) - 1) * 18, 315 + (int(to_point[0]) - 1) * 320 + (int(to_point[1]) - 1) * 35)
        pic_step10 = (pic_step9[0], pic_step9[1] + 35 * (5 - int(to_point[1])))
        pic_step11 = (pic_step10[0] + distance_step_6 - 140, pic_step10[1])
        pic_step12 = (pic_step11[0] + 80, pic_step11[1] + 30)

    json6 = to_point[0] + '-大线环1'
    json7 = to_point[0] + '(' + to_point[1] + ',' + to_point[2] + ')'

    # 7. 往上插入端口
    distance_step_7 = (len(to_slot_rows) - int(to_point[1]) + 1) * 35
    print('往上插入端口:' + str(distance_step_7))
    # log[5]
    log6 = '最后往上将线插入'+to_name+'96芯设备单元H'+to_point[0]+'端口('+format_radio_96(to_point[1],to_point[2])+')中。'

    if int(from_point[0]) > int(to_point[0]):
        increase = 450
    else:
        increase = 180
    used_distance = distance_step_1+distance_step_2+distance_step_3+distance_step_4+distance_step_6+distance_step_7+increase+200
    print('总共需要线长：' + str(used_distance))
    cable_list = []
    for cable in CABLE_LENGTH:
        if cable > used_distance:
            cable_list.append(cable)
    cable_list.sort()
    shengyu_xianchang = cable_list[0]-used_distance
    print('剩余线长：'+ str(shengyu_xianchang))

    # # 调整上下挂纤轮
    log0 = '此次跳纤计算的长度为' + str(round(used_distance / 1000, 1)) + '米，请选择一根长度为' + \
           str(int(cable_list[0] / 1000)) + '米的光纤跳线。'

    log_list = [log0, log1, log2, log3, log4, log4_1, log4_2, log5, log6]
    step_list = [pic_step1, pic_step2, pic_step3, pic_step4, pic_step5, pic_step6, pic_step7, pic_step8, \
                 pic_step9, pic_step10, pic_step11, pic_step12, pic_step8_1, pic_step5_1, pic_step7_1]
    json_list = [shebei_count, log_list, '1-'+json1, str(shebei_count)+'-'+json2, str(shebei_count)+'-'+json3, str(shebei_count)+'-'+json4, str(shebei_count)+'-'+json5, str(shebei_count)+'-'+json6, str(shebei_count)+'-'+json7]

    print(step_list)
    print(log_list)
    print('used_distance:', used_distance)
    return step_list, log_list, json_list, int(cable_list[0] / 1000), right_to_left


# 计算不同设备、同side、背面，跳纤方式
def calculate_two_back_back(jiechushebei_radio,jierushebei_radio, \
                              jiechushebei,jierushebei,\
                              shebei_count,CABLE_LENGTH):
    # json0 = ['不同机架的72芯配线单元与72芯配线单元跳纤']
    from_point = jiechushebei_radio
    to_point = jierushebei_radio
    from_name = jiechushebei
    to_name = jierushebei
    right_to_left = 0
    if re.findall('\d+', from_name)[0] < re.findall('\d+', to_name)[0]:
        right_to_left = 1
    print('from_point'+str(from_point))
    print('to_point'+str(to_point))
    # 1. 先从第几排托盘往左出来
    distance_step_1 = 84 + 20.5 * (int(from_point[2]) - 1)
    # log[1] 一
    log1 = '先从' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[from_point[0]] + '端口(' + str(from_point[1]) + ',' + str(from_point[2]) + ')出来。'
    if int(from_point[0]) <= 4:
        pic_step1 = (
        325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25)
    elif int(from_point[0]) > 4 and int(from_point[0]) <= 8:
        pic_step1 = (
        325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25 + 335)
    elif int(from_point[0]) > 8 and int(from_point[0]) <= 12:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20,
                     205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25 + 335 * 2)
    pic_step2 = (250, pic_step1[1])

    json1 = PEIXIAN_DANYUAN[from_point[0]] + '(' + from_point[1] + ',' + from_point[2] + ')'

    # 2. 进入组合线环#XX中的小孔
    distance_step_2 = 34 + 26 * (6 - int(from_point[1]))
    # log[2] 一
    log2 = '进入' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[from_point[0]] + '组合线环的小孔。'
    if int(from_point[0]) <= 4:
        pic_step3 = (250, 360 + 160 * (int(from_point[0]) - 1))
    elif int(from_point[0]) > 4 and int(from_point[0]) <= 8:
        pic_step3 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340)
    elif int(from_point[0]) > 8 and int(from_point[0]) <= 12:
        pic_step3 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340 * 2)

    json2 = PEIXIAN_DANYUAN[from_point[0]] + '-小孔'

    # 3. 进入组合线环#XX+1的大孔
    if int(from_point[0]) < 12:
        if from_point[0] == '4' or from_point[0] == '8':
            distance_step_3 = 527  # 每四个之间相距527mm
        else:
            distance_step_3 = 169  # 组合线环之间相距169mm
        # log[3] 一
        log3 = '进入' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]) + 1)] + '组合线环的大孔。'
        if int(from_point[0]) + 1 <= 4:
            pic_step4 = (250, 360 + 160 * int(from_point[0]))  # 背-大孔
            pic_step5 = (1080, 340 + 160 * int(from_point[0]))  # 侧-大孔
        elif int(from_point[0]) + 1 > 4 and int(from_point[0]) + 1 <= 8:
            pic_step4 = (250, 360 + 160 * int(from_point[0]) + 340)
            pic_step5 = (1080, 340 + 160 * int(from_point[0]) + 340)
        elif int(from_point[0]) + 1 > 8 and int(from_point[0]) + 1 <= 12:
            pic_step4 = (250, 360 + 160 * int(from_point[0]) + 340 * 2)
            pic_step5 = (1080, 340 + 160 * int(from_point[0]) + 340 * 2)
        pic_step5_1 = (785, 360 + (int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) - 1) * 220)  # from_point对应右挂纤轮
        json3 = PEIXIAN_DANYUAN[str(int(from_point[0]) + 1)] + '-大孔'

    elif int(from_point[0]) == 12:
        distance_step_3 = 0
        # log3 = '进入' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]))] + '组合线环的大孔。'
        log3 = '从组合线环穿出至侧面挂纤轮。'
        if int(from_point[0]) <= 4:
            pic_step4 = (250, 360 + 160 * (int(from_point[0]) - 1))  # 背-大孔
            pic_step5 = (1080, 340 + 160 * (int(from_point[0]) - 1))  # 侧-大孔
        elif int(from_point[0]) + 1 > 4 and int(from_point[0]) <= 8:
            pic_step4 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340)
            pic_step5 = (1080, 340 + 160 * (int(from_point[0]) - 1) + 340)
        elif int(from_point[0]) + 1 > 8 and int(from_point[0]) <= 12:
            pic_step4 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340 * 2)
            pic_step5 = (1080, 340 + 160 * (int(from_point[0]) - 1) + 340 * 2)
        pic_step5_1 = (785, 360 + (int(BACK_RIGHT_WHEEL[from_point[0]]) - 1) * 220)  # from_point对应右挂纤轮
        json3 = PEIXIAN_DANYUAN[str(int(from_point[0]))] + '-大孔'

    # 4. 往上至高于from_point的挂纤轮，水平走线槽，大线环2，wheel_above,wheel_bottom再调头向上走
    wheel_above = []
    wheel_bottom = []
    wheel_above2 = []
    if COMBINATION_RING[from_point[0]] > COMBINATION_RING[to_point[0]]:
        if int(from_point[0]) < 12:
            compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) - 1 - 1]
        elif int(from_point[0]) == 12:
            compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1 - 1]
    else:
        if int(to_point[0]) < 12:
            compare_num = WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0]) + 1)]]) - 1 - 1]
        elif int(to_point[0]) == 12:
            compare_num = WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) - 1 - 1]
    for wheel_d in WHEEL_DISTANCE:
        if (wheel_d + WHEEL_D) > (compare_num):
            wheel_above.append(wheel_d)
    wheel_above.sort()

    if int(to_point[0]) < 12:
        compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0]) + 1)]) - 1 - 1]
    elif int(to_point[0]) == 12:
        compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1 - 1]
    for wheel_d in WHEEL_DISTANCE:
        if (wheel_d + WHEEL_D) > compare_num:
            wheel_above2.append(wheel_d)
    wheel_above2.sort()

    # wheel_above到from_point对应的右挂纤轮
    if int(from_point[0]) < 12:
        distance_step_4_1 =        distance_sqrt(430, COMBINATION_RING[str(int(from_point[0])+1)] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0])+1)])-1])
        distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0])+1)])-1])
    elif int(from_point[0]) == 12:
        distance_step_4_1 =        distance_sqrt(430, COMBINATION_RING[str(int(from_point[0]))] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1])
        distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1])
    if int(to_point[0]) < 12:
        distance_step_4_2 =        distance_sqrt(430,BIGLINE2_DISTANCE[COMBINATION_VS_BIGLINE2[str(int(to_point[0]) + 1)]] + LINE -WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0]) + 1)]]) - 1])
        distance_step_4_2 = distance_step_4_2 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0]) + 1)]]) - 1]))
        distance_step_4_4 =        distance_sqrt(430,BIGLINE2_DISTANCE[COMBINATION_VS_BIGLINE2[str(int(to_point[0]) + 1)]] + LINE -WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0]) + 1)]]) - 1])
        distance_step_4_4 = distance_step_4_4 + distance_sqrt(200, (wheel_above2[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0]) + 1)]]) - 1]))
    elif int(to_point[0]) == 12:
        distance_step_4_2 =        distance_sqrt(430, BIGLINE2_DISTANCE[COMBINATION_VS_BIGLINE2[to_point[0]]] + LINE -WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) - 1])
        distance_step_4_2 = distance_step_4_2 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) - 1]))
        distance_step_4_4 =        distance_sqrt(430, BIGLINE2_DISTANCE[COMBINATION_VS_BIGLINE2[to_point[0]]] + LINE -WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) - 1])
        distance_step_4_4 = distance_step_4_4 + distance_sqrt(200, (wheel_above2[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) - 1]))
    # 大线环2到水平走线槽边缘42mm，经过几个走线槽到from_point大线环2
    distance_step_4_3 = (shebei_count - 1) * 748 + 42
    if right_to_left:
        distance_step_4_3 = (shebei_count - 1) * 748 + 200
    # 大线环2到to_point组合线环上方挂纤轮


    distance_step_4 = distance_step_4_1 + distance_step_4_2 + distance_step_4_3 + distance_step_4_4

    # # 高挂纤轮到最下面的挂纤轮
    distance_step_5 = 0

    # log[4] 二
    if int(to_point[0]) < 12:
        log4_1 = str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0]) + 1)]]) + 1)
    elif int(to_point[0]) == 12:
        log4_1 = str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) + 1)
    if int(from_point[0]) < 12:
        log4 = '从72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]) + 1)] + '的大孔穿出后，至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) + 1) + \
               '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + '，再至左挂纤轮' + log4_1
    elif int(from_point[0]) == 12:
        log4 = '从72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]))] + '的小孔穿出后，至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[from_point[0]]) + 1) + \
               '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + '，再至左挂纤轮' + log4_1


    if int(to_point[0]) < 12:
        log5 = '进入' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)] + '的大线环2。'
        log6 = '从' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)] + '的大线环2出来后，沿水平走线槽经过' + str(shebei_count - 1) + '个机架。'
        log7 = '到' + to_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)] + '的大线环2。'
        log8_1 = '，再至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[str(int(to_point[0]) + 1)]) + 1)
        log8 = '从' + to_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)] + '的大线环2穿出，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above2[0]) + 1) + \
               log8_1
    elif int(to_point[0]) == 12:
        log5 = '进入' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[to_point[0]] + '的大线环2。'
        log6 = '从' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[to_point[0]] + '的大线环2出来后，沿水平走线槽经过' + str(shebei_count - 1) + '个机架。'
        log7 = '到' + to_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[to_point[0]] + '的大线环2。'
        log8_1 = '，再至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[to_point[0]]) + 1)
        log8 = '从' + to_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[to_point[0]] + '的大线环2穿出，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above2[0]) + 1) + \
               log8_1
    pic_step6 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above2[0]) + 1 - 1) * 215)  # wheel_above2
    if int(to_point[0]) < 12:
        pic_step8_1 = (750, 535 + (int(COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]) - 1) * 320)  # 2正-大线环2
    elif int(to_point[0]) == 12:
        pic_step8_1 = (750, 535 + (int(COMBINATION_VS_BIGLINE2[to_point[0]]) - 1) * 320)  # 2正-大线环2
    pic_step14 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0]) + 1 - 1) * 215)  # wheel_above1

    json4 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
    json5 = COMBINATION_VS_BIGLINE2[to_point[0]] + '-大线环2'
    json6 = '水平走线槽'
    json7 = COMBINATION_VS_BIGLINE2[to_point[0]] + '-大线环2'
    json8 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
    json9 = '挂纤轮-13'
    # json10 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0]) + 1)


    # 5. 往下进入to_point组合线环#XX+1的大孔
    if int(to_point[0]) < 12:
        distance_step_6 = distance_sqrt(200, wheel_above2[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)]) - 1])
        distance_step_6 = distance_step_6 +        distance_sqrt(430, COMBINATION_RING[str(int(to_point[0])+1)] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)])-1])
        print('2. 往下进入'+to_name+'72芯配线单元'+PEIXIAN_DANYUAN[str(int(to_point[0])+1)]+'组合线环的大孔。')
        # log[9]
        log9 = '往下进入'+to_name+'72芯配线单元L'+PEIXIAN_DANYUAN[str(int(to_point[0])+1)]+'组合线环的大孔。'
        json11 = PEIXIAN_DANYUAN[str(int(to_point[0])+1)] + '-大孔'
        if int(to_point[0])+1 <= 4:
            pic_step8 = (1080, 340 + 160 * int(to_point[0]))  # 侧-组合线环大孔
        elif int(to_point[0])+1 > 4 and int(to_point[0])+1 <= 8:
            pic_step8 = (1080, 340 + 160 * int(to_point[0]) + 340)
        elif int(to_point[0])+1 > 8 and int(to_point[0])+1 <= 12:
            pic_step8 = (1080, 340 + 160 * int(to_point[0]) + 340 * 2)
    elif int(to_point[0]) == 12:
        distance_step_6 = distance_sqrt(200, wheel_above2[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1])
        distance_step_6 = distance_step_6 +        distance_sqrt(430, COMBINATION_RING[to_point[0]] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1])
        # log[9]
        # log9 = '往下进入'+to_name+'72芯配线单元L'+PEIXIAN_DANYUAN[str(int(to_point[0]))]+'组合线环的大孔。'
        log9 = '进入'+to_name+'72芯配线单元L'+PEIXIAN_DANYUAN[str(int(to_point[0]))]+'组合线环。'
        json11 = PEIXIAN_DANYUAN[str(int(to_point[0]))] + '-大孔'
        if int(to_point[0]) <= 4:
            pic_step8= (1080, 340 + 160 * (int(to_point[0])-1))
        elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
            pic_step8 = (1080, 340 + 160 * (int(to_point[0])-1) + 340)
        elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
            pic_step8 = (1080, 340 + 160 * (int(to_point[0])-1) + 340 * 2)


    # 6. 再向上进入to_point组合线环#XX的小孔
    if int(to_point[0]) < 12 :
        distance_step_7 = COMBINATION_RING[to_point[0]] - COMBINATION_RING[str(int(to_point[0])+1)]
        if int(to_point[0]) <= 4:
            pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1))  # 侧-组合线环小孔
        elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
            pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340)
        elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
            pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340 * 2)
    elif int(to_point[0]) == 12:
        distance_step_7 = 0
        pic_step9 = (pic_step8[0], pic_step8[1])

    # log[10]
    log10 = '再进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]))] + '组合线环的小孔。'
    # json[8]
    json12 = PEIXIAN_DANYUAN[str(int(to_point[0]))]+'-小孔'

    # 7. 往右进入指定托盘
    distance_step_8 = 34 + 26 * (6 - int(to_point[1])) + 84 + 20.5 * (int(to_point[2])-1)
    # log[11]
    log11 = '从'+to_name+'72芯配线单元L'+PEIXIAN_DANYUAN[to_point[0]]+'组合线环的小孔出穿出。'
    # log[12]
    log12 = '往右进入'+to_name+'72芯配线单元L'+PEIXIAN_DANYUAN[str(to_point[0])]+'端口('+str(to_point[1])+','+str(to_point[2])+')中。'

    if int(to_point[0]) <= 4:
        pic_step10 = (250, 360 + 160 * (int(to_point[0])-1))  # 背-组合线环小孔
        pic_step12 = (325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25)
    elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
        pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1) + 340)
        pic_step12 = (325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335)
    elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
        pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1) + 340 * 2)
        pic_step12 = (325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335 * 2)
    pic_step11 = (250, pic_step12[1])  # arc

    # json[9]
    json13 = PEIXIAN_DANYUAN[to_point[0]]+'('+to_point[1]+','+to_point[2]+')'

    used_distance = distance_step_1 + distance_step_2 + distance_step_3 + distance_step_4 + \
                    distance_step_5 + distance_step_6 + distance_step_7 + distance_step_8 + 200
    print('总共需要线长：' + str(used_distance))
    cable_list = []
    for cable in CABLE_LENGTH:
        if cable > used_distance:
            cable_list.append(cable)
    cable_list.sort()
    shengyu_xianchang = cable_list[0] - used_distance
    print('剩余线长：' + str(shengyu_xianchang))

    # # 调整上下挂纤轮

    pic_step7 = (590, 230)
    log0 = '此次跳纤计算的长度为' + str(round(used_distance / 1000, 1)) + '米，请选择一根长度为' + \
           str(int(cable_list[0] / 1000)) + '米的光纤跳线。'
    #
    # json8 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
    # # json10 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0]) + 1)  # json[6]
    json10 = ''

    if int(to_point[0]) < 12:
        pic_step13 = (235, 550 + (int(COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]) - 1) * 320)  # 侧-大线环2（第二步）
        pic_step13_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]]) - 1) * 220)  # to_point对应大线环2对应左挂纤轮
    elif int(to_point[0]) == 12:
        pic_step13 = (235, 550 + (int(COMBINATION_VS_BIGLINE2[to_point[0]]) - 1) * 320)  # 侧-大线环2（第二步）
        pic_step13_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) - 1) * 220)  # to_point对应大线环2对应左挂纤轮
    if int(COMBINATION_VS_BIGLINE2[to_point[0]]) == 9:
        pic_step13_1 = (0, 0)
    if int(to_point[0]) < 12:
        pic_step8_2 = (405, 360 + (int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)]) - 1) * 220)  # to_point对应左挂纤轮
    elif int(to_point[0]) == 12:
        pic_step8_2 = (405, 360 + (int(BACK_RIGHT_WHEEL[to_point[0]]) - 1) * 220)  # to_point对应左挂纤轮

    log_list = [log0, log1, log2, log3, log4, log5, log6, log7, log8, log9, log10, log11, log12]
    step_list = [pic_step1, pic_step2, pic_step3, pic_step4, pic_step5, pic_step6, pic_step7, pic_step8_1, pic_step8, \
                 pic_step9, pic_step10, pic_step11, pic_step12, pic_step13, pic_step14, pic_step5_1, pic_step13_1, pic_step8_2]
    json_list = [shebei_count, log_list, '1-'+json1, '1-'+json2, '1-'+json3, '1-'+json4, '1-'+json5, json6, str(shebei_count)+'-'+json7, str(shebei_count)+'-'+json8, str(shebei_count)+'-'+json9, str(shebei_count)+'-'+json10, str(shebei_count)+'-'+json11, str(shebei_count)+'-'+json12, str(shebei_count)+'-'+json13]

    print(step_list)
    print(log_list)
    print('used_distance:', used_distance)
    return step_list, log_list, json_list, int(cable_list[0] / 1000), right_to_left


# 计算同一设备、不同side、背面-正面，跳纤方式
def calculate_one_back_front(jiechushebei_radio,jierushebei_radio, \
                             jiechushebei_slot_rows,jiechushebei_slot_cols, \
                             jierushebei_slot_rows,jierushebei_slot_cols, \
                             jiechushebei,jierushebei,CABLE_LENGTH):
    # json0 = ['相同机架的72芯配线单元与796芯设备单元跳纤']
    from_point = jiechushebei_radio
    to_point = jierushebei_radio
    from_slot_rows = jiechushebei_slot_rows
    from_slot_cols = jiechushebei_slot_cols
    to_slot_rows = jierushebei_slot_rows
    to_slot_cols = jierushebei_slot_cols
    from_name = jiechushebei
    to_name = jierushebei
    print('from_point'+str(from_point))
    print('to_point'+str(to_point))
    # 1. 先从第几排托盘往左出来
    distance_step_1 = 84 + 20.5 * (int(from_point[2]) - 1)
    # log[1] 一
    log1 = '先从' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[from_point[0]] + '端口(' + str(from_point[1]) + ',' + str(from_point[2]) + ')出来。'
    if int(from_point[0]) <= 4:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25)
    elif int(from_point[0]) > 4 and int(from_point[0]) <= 8:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25 + 335)
    elif int(from_point[0]) > 8 and int(from_point[0]) <= 12:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25 + 335 * 2)
    pic_step2 = (250, pic_step1[1])

    json1 = PEIXIAN_DANYUAN[from_point[0]] + '(' + from_point[1] + ',' + from_point[2] + ')'

    # 2. 进入组合线环#XX中的小孔
    distance_step_2 = 34 + 26 * (6 - int(from_point[1]))
    print('2. 进入组合线环' + str(from_point[0]) + '中的小孔:' + str(distance_step_2))
    # log[2] 一
    log2 = '进入' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[from_point[0]] + '组合线环的小孔。'
    if int(from_point[0]) <= 4:
        pic_step3 = (250, 360 + 160 * (int(from_point[0]) - 1))
    elif int(from_point[0]) > 4 and int(from_point[0]) <= 8:
        pic_step3 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340)
    elif int(from_point[0]) > 8 and int(from_point[0]) <= 12:
        pic_step3 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340 * 2)

    json2 = PEIXIAN_DANYUAN[from_point[0]] + '-小孔'

    # 3. 进入组合线环#XX+1的大孔
    if int(from_point[0]) < 12:
        if from_point[0] == '4' or from_point[0] == '8':
            distance_step_3 = 527  # 每四个之间相距527mm
        else:
            distance_step_3 = 169  # 组合线环之间相距169mm
        log3 = '进入' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]) + 1)] + '组合线环的大孔。'
        if int(from_point[0]) + 1 <= 4:
            pic_step4 = (250, 360 + 160 * int(from_point[0]))  # 背-大孔
            pic_step5 = (1080, 340 + 160 * int(from_point[0]))  # 侧-大孔
        elif int(from_point[0]) + 1 > 4 and int(from_point[0]) + 1 <= 8:
            pic_step4 = (250, 360 + 160 * int(from_point[0]) + 340)
            pic_step5 = (1080, 340 + 160 * int(from_point[0]) + 340)
        elif int(from_point[0]) + 1 > 8 and int(from_point[0]) + 1 <= 12:
            pic_step4 = (250, 360 + 160 * int(from_point[0]) + 340 * 2)
            pic_step5 = (1080, 340 + 160 * int(from_point[0]) + 340 * 2)
        pic_step5_1 = (785, 360 + (int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)])-1)*220)  # from_point对应右挂纤轮
        json3 = PEIXIAN_DANYUAN[str(int(from_point[0]) + 1)] + '-大孔'

    elif int(from_point[0]) == 12:
        distance_step_3 = 0
        # log3 = '进入' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]))] + '组合线环的大孔。'
        log3 = '从组合线环穿出至侧面挂纤轮。'
        if int(from_point[0]) <= 4:
            pic_step4 = (250, 360 + 160 * (int(from_point[0]) - 1))  # 背-大孔
            pic_step5 = (1080, 340 + 160 * (int(from_point[0]) - 1))  # 侧-大孔
        elif int(from_point[0]) + 1 > 4 and int(from_point[0]) <= 8:
            pic_step4 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340)
            pic_step5 = (1080, 340 + 160 * (int(from_point[0]) - 1) + 340)
        elif int(from_point[0]) + 1 > 8 and int(from_point[0]) <= 12:
            pic_step4 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340 * 2)
            pic_step5 = (1080, 340 + 160 * (int(from_point[0]) - 1) + 340 * 2)
        pic_step5_1 = (785, 360 + (int(BACK_RIGHT_WHEEL[from_point[0]]) - 1) * 220)  # from_point对应右挂纤轮
        json3 = PEIXIAN_DANYUAN[str(int(from_point[0]))] + '-大孔'

    # 4. 往上至高于from_point的挂纤轮，再往下走直到侧面最下面那个挂纤轮调头向上走
    wheel_above = []
    # wheel_bottom = []
    if COMBINATION_RING[from_point[0]] > BIGLINE_DISTANCE[to_point[0]]:
        if int(from_point[0]) < 12:
            compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0])+1)])-1-1]
        elif int(from_point[0]) == 12:
            compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]])-1-1]
    else:
        compare_num = WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]])-1-1]
    for wheel_d in WHEEL_DISTANCE:
        if (wheel_d + WHEEL_D) > (compare_num):
            wheel_above.append(wheel_d)
    wheel_above.sort()
    if int(from_point[0]) < 12:
        distance_step_4_1 =        distance_sqrt(430, COMBINATION_RING[str(int(from_point[0])+1)] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0])+1)])-1])
        distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0])+1)])-1])
        distance_step_4_2 =        distance_sqrt(430, BIGLINE_DISTANCE[to_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1])
        distance_step_4_2 = distance_step_4_2 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1]))
        distance_step_4 = distance_step_4_1 + distance_step_4_2
        # distance_step_4_0 = wheel_above[0]+WHEEL - COMBINATION_RING[str(int(from_point[0])+1)]
        # print(distance_step_4_0)
        log4 = '从72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]) + 1)] + '的大孔穿出后，至右挂纤轮'+ str(13-int(BACK_RIGHT_WHEEL[str(int(from_point[0])+1)])+1)+\
               '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + '，再至左挂纤轮' + str(13-int(FRONT_LEFT_WHEEL[to_point[0]])+1)
    elif int(from_point[0]) == 12:
        distance_step_4_1 =        distance_sqrt(430, COMBINATION_RING[str(int(from_point[0]))] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1])
        distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1])
        distance_step_4_2 =        distance_sqrt(430, BIGLINE_DISTANCE[to_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1])
        distance_step_4_2 = distance_step_4_2 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1]))
        distance_step_4 = distance_step_4_1 + distance_step_4_2
        # distance_step_4 = wheel_above[0] + WHEEL - COMBINATION_RING[str(int(from_point[0]))]
        log4 = '从72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]))] + '的大孔穿出后，至右挂纤轮'+ str(13-int(BACK_RIGHT_WHEEL[from_point[0]])+1)+\
               '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + '，再至左挂纤轮' + str(13-int(FRONT_LEFT_WHEEL[to_point[0]])+1)



    pic_step6 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0])+1-1) * 215)  # wheel_above
    # pic_step7 = (590, 230 + (WHEEL_DISTANCE.index(wheel_bottom[0])+1-1) * 215)  # wheel_bottom

    json4 = '挂纤轮-'+str(WHEEL_DISTANCE.index(wheel_above[0])+1)
    # json_list.append('挂纤轮-13')  # json[5]
    # json_list.append('挂纤轮-'+str(WHEEL_DISTANCE.index(wheel_bottom[0])+1))  # json[6]


    # 5. 进入to_point大线环1
    # distance_step_5 = wheel_above[0] + WHEEL - (BIGLINE_DISTANCE[to_point[0]] + LINE)
    distance_step_5 = 0

    log5 = '进入' + to_name + '的96芯设备单元H' + to_point[0] + '的大线环1。'
    pic_step8 = (255, 470 + (int(to_point[0]) - 1) * 320)  # 侧-大线环1

    # 6. 往左进入slot的中线环，进入该端口邻近的8位小线环
    if int(to_point[2]) < 12:
        distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 12 + 26 + 140
    else:
        distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 26 + 140
    print('6. 往左进入slot的中线环，进入该端口邻近的8位小线环:' + str(distance_step_6))
    # log[6]
    log6 = '从' + to_name + '的96芯设备单元H' + to_point[0] + '的大线环1出来后，往左进入中线环，并将线嵌入邻近的8位小线环中。'
    pic_step9 = (230 + (int(to_point[2]) - 1) * 18, 315 + (int(to_point[0]) - 1) * 320 + (int(to_point[1]) - 1) * 35)
    pic_step10 = (pic_step9[0], pic_step9[1] + 35 * (5 - int(to_point[1])))
    pic_step11 = (pic_step10[0] + distance_step_6 - 140, pic_step10[1])
    pic_step12 = (pic_step11[0] + 80, pic_step11[1] + 30)

    json5 = to_point[0] + '-大线环1'
    json6 = to_point[0] + '(' + to_point[1] + ',' + to_point[2] + ')'

    # 7. 往上插入端口
    distance_step_7 = (len(to_slot_rows) - int(to_point[1]) + 1) * 35
    print('往上插入端口:' + str(distance_step_7))
    # log[7]
    log7 = '最后往上将线插入' + to_name + '96芯设备单元H' + to_point[0] + '端口(' + format_radio_96(to_point[1],to_point[2]) + ')中。'
    used_distance = distance_step_1 + distance_step_2 + distance_step_3 + distance_step_4 + distance_step_5 + distance_step_6 + distance_step_7 + 200
    print('总共需要线长：' + str(used_distance))
    cable_list = []
    for cable in CABLE_LENGTH:
        if cable > used_distance:
            cable_list.append(cable)
    cable_list.sort()
    shengyu_xianchang = cable_list[0] - used_distance
    print('剩余线长：' + str(shengyu_xianchang))

    # # 调整上下挂纤轮

    log0 = '此次跳纤计算的长度为' + str(round(used_distance / 1000, 1)) + '米，请选择一根长度为' + \
           str(int(cable_list[0] / 1000)) + '米的光纤跳线。'
    #
    # json4 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
    # # json_list[5] = '挂纤轮-13'  # json[5]
    # # json_list[6] = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0]) + 1)  # json[6]

    pic_step8_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[to_point[0]]) - 1) * 220)  # to_point对应左挂纤轮
    if int(to_point[0]) == 9:
        pic_step8_1 = (0,0)

    log_list = [log0, log1, log2, log3, log4, log5, log6, log7]
    step_list = [pic_step1, pic_step2, pic_step3, pic_step4, pic_step5, pic_step6, pic_step8, \
                 pic_step9, pic_step10, pic_step11, pic_step12, pic_step5_1, pic_step8_1]
    json_list = [1, log_list, json1, json2, json3, json4, json5, json6]

    print(step_list)
    print(log_list)
    print('used_distance:', used_distance)
    return step_list, log_list, json_list, int(cable_list[0] / 1000)


# 计算不同设备、不同side、背面-正面，跳纤方式
def calculate_two_back_front(jiechushebei_radio,jierushebei_radio, \
                             jiechushebei_slot_rows,jiechushebei_slot_cols, \
                             jierushebei_slot_rows,jierushebei_slot_cols, \
                             jiechushebei,jierushebei,\
                             shebei_count,CABLE_LENGTH):
    # step_list = []
    # json0 ='不同机架的72芯配线单元与96芯设备单元跳纤'
    from_point = jiechushebei_radio
    to_point = jierushebei_radio
    from_slot_rows = jiechushebei_slot_rows
    from_slot_cols = jiechushebei_slot_cols
    to_slot_rows = jierushebei_slot_rows
    to_slot_cols = jierushebei_slot_cols
    from_name = jiechushebei
    to_name = jierushebei
    right_to_left = 0
    if re.findall('\d+', from_name)[0] < re.findall('\d+', to_name)[0]:
        right_to_left = 1
    print('from_point'+str(from_point))
    print('to_point'+str(to_point))
    # 1. 先从第几排托盘往左出来
    distance_step_1 = 84 + 20.5 * (int(from_point[2])-1)
    log1 = '先从'+from_name+'的72芯配线单元L'+PEIXIAN_DANYUAN[from_point[0]]+'端口('+str(from_point[1])+','+str(from_point[2])+')出来。'
    if int(from_point[0]) <= 4:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25)
    elif int(from_point[0]) > 4 and int(from_point[0]) <= 8:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25 +335)
    elif int(from_point[0]) > 8 and int(from_point[0]) <= 12:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25 +335 * 2)
    pic_step2 = (250, pic_step1[1])

    json1 =PEIXIAN_DANYUAN[from_point[0]]+'('+from_point[1]+','+from_point[2]+')'

    # 2. 进入组合线环#XX中的小孔
    distance_step_2 = 34 + 26 * (6 - int(from_point[1]))
    # log[2] 一
    log2 = '进入'+from_name+'的72芯配线单元L'+PEIXIAN_DANYUAN[from_point[0]]+'组合线环的小孔。'
    if int(from_point[0]) <= 4:
        pic_step3 = (250, 360 + 160 * (int(from_point[0])-1))
    elif int(from_point[0]) > 4 and int(from_point[0]) <= 8:
        pic_step3 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340)
    elif int(from_point[0]) > 8 and int(from_point[0]) <= 12:
        pic_step3 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340 * 2)

    json2 = PEIXIAN_DANYUAN[from_point[0]]+'-小孔'

    # 3. 进入组合线环#XX+1的大孔
    if int(from_point[0]) < 12:
        if from_point[0] == '4' or from_point[0] == '8':
            distance_step_3 = 527  # 每四个之间相距527mm
        else:
            distance_step_3 = 169  # 组合线环之间相距169mm
        log3 = '进入'+from_name+'的72芯配线单元L'+PEIXIAN_DANYUAN[str(int(from_point[0])+1)]+'组合线环的大孔。'
        if int(from_point[0]) + 1 <= 4:
            pic_step4 = (250, 360 + 160 * int(from_point[0]))  # 背-大孔
            pic_step5 = (1080, 340 + 160 * int(from_point[0]))  # 侧-大孔
        elif int(from_point[0]) + 1 > 4 and int(from_point[0]) + 1 <= 8:
            pic_step4 = (250, 360 + 160 * int(from_point[0]) + 340)
            pic_step5 = (1080, 340 + 160 * int(from_point[0]) + 340)
        elif int(from_point[0]) + 1 > 8 and int(from_point[0]) + 1 <= 12:
            pic_step4 = (250, 360 + 160 * int(from_point[0]) + 340 * 2)
            pic_step5 = (1080, 340 + 160 * int(from_point[0]) + 340 * 2)
        pic_step5_1 = (785, 360 + (int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) - 1) * 220)  # from_point对应右挂纤轮
        json3 = PEIXIAN_DANYUAN[str(int(from_point[0])+1)]+'-大孔'

    elif int(from_point[0]) == 12:
        distance_step_3 = 0
        # log3 = '进入' + from_name + '的72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]))] + '组合线环的大孔。'
        log3 = '从组合线环穿出至侧面挂纤轮。'
        if int(from_point[0]) <= 4:
            pic_step4 = (250, 360 + 160 * (int(from_point[0]) - 1))  # 背-大孔
            pic_step5 = (1080, 340 + 160 * (int(from_point[0]) - 1))  # 侧-大孔
        elif int(from_point[0]) + 1 > 4 and int(from_point[0]) <= 8:
            pic_step4 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340)
            pic_step5 = (1080, 340 + 160 * (int(from_point[0]) - 1) + 340)
        elif int(from_point[0]) + 1 > 8 and int(from_point[0]) <= 12:
            pic_step4 = (250, 360 + 160 * (int(from_point[0]) - 1) + 340 * 2)
            pic_step5 = (1080, 340 + 160 * (int(from_point[0]) - 1) + 340 * 2)
        pic_step5_1 = (785, 360 + (int(BACK_RIGHT_WHEEL[from_point[0]]) - 1) * 220)  # from_point对应右挂纤轮
        json3 = PEIXIAN_DANYUAN[str(int(from_point[0]))] + '-大孔'


    if right_to_left:
        # 4. 往上至高于from_point的挂纤轮，水平走线槽，大线环2，wheel_above,wheel_bottom再调头向上走
        wheel_above = []
        wheel_bottom = []
        if COMBINATION_RING[from_point[0]] > BIGLINE_DISTANCE[to_point[0]]:
            if int(from_point[0]) < 12:
                compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) - 1 - 1]
            elif int(from_point[0]) == 12:
                compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1 - 1]
        else:
            compare_num = WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1 - 1]
        for wheel_d in WHEEL_DISTANCE:
            if (wheel_d + WHEEL_D) > (compare_num):
                wheel_above.append(wheel_d)
        wheel_above.sort()

        if int(from_point[0]) < 12:
            distance_step_4_1 = distance_sqrt(450, COMBINATION_RING[str(int(from_point[0])+1)] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0])+1)])-1])
            distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0])+1)])-1])
            distance_step_4_2 = distance_sqrt(450, BIGLINE2_DISTANCE[to_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1])
            distance_step_4_2 = distance_step_4_2 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1]))
            # distance_step_4_0 = wheel_above[0]+WHEEL - COMBINATION_RING[str(int(from_point[0])+1)]
            # print(distance_step_4_0)
            log4 = '从72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]) + 1)] + '的大孔穿出后，至右挂纤轮'+ str(13-int(BACK_RIGHT_WHEEL[str(int(from_point[0])+1)])+1)+\
                   '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + '，再至左挂纤轮' + str(13-int(FRONT_LEFT_WHEEL[to_point[0]])+1)
        elif int(from_point[0]) == 12:
            distance_step_4_1 = distance_sqrt(450, COMBINATION_RING[str(int(from_point[0]))] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1])
            distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1])
            distance_step_4_2 = distance_sqrt(450, BIGLINE2_DISTANCE[to_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1])
            distance_step_4_2 = distance_step_4_2 + distance_sqrt(200, (
            wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1]))
            # distance_step_4 = wheel_above[0] + WHEEL - COMBINATION_RING[str(int(from_point[0]))]
            log4 = '从72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]))] + '的大孔穿出后，至右挂纤轮'+ str(13-int(BACK_RIGHT_WHEEL[from_point[0]])+1)+\
                   '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + '，再至左挂纤轮' + str(13-int(FRONT_LEFT_WHEEL[to_point[0]])+1)

        # 高挂纤轮到from_point大线环2
        # distance_step_4_2 = wheel_above[0]+WHEEL - (BIGLINE2_DISTANCE[to_point[0]]+LINE)
        # 大线环2到水平走线槽边缘42mm，经过几个走线槽到from_point大线环2
        distance_step_4_3 = (shebei_count-1) * 748 + 42
        if right_to_left:
            distance_step_4_3 = (shebei_count - 1) * 748 + 200
        # 大线环2到机架2高挂纤轮
        # distance_step_4_4 = wheel_above[0]+WHEEL - (BIGLINE2_DISTANCE[to_point[0]]+LINE)
        distance_step_4_4 = 0
        distance_step_4 = distance_step_4_1 + distance_step_4_2 + distance_step_4_3 + distance_step_4_4

        distance_step_5 = 0

        log5 = '往下到'+from_name+'96芯设备单元H'+to_point[0]+'的大线环2。'
        # log[6] 三
        log6 = '从'+from_name+'96芯设备单元H'+to_point[0]+'的大线环2出来后，沿水平走线槽经过'+str(shebei_count-1)+'个机架。'
        # log[7] 三
        log7 = '到'+to_name+'96芯设备单元H'+to_point[0]+'的中线环。'
        log8 = ''
        pic_step6 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0])+1-1) * 215)  # wheel_above 水平走线钱
        # pic_step7 = (590, 230 + (WHEEL_DISTANCE.index(wheel_bottom[0])+1-1) * 215)  # wheel_bottom
        pic_step8_1 = (750, 535 + (int(to_point[0])-1) * 320)  # 2正-大线环2
        if right_to_left:
            pic_step8_1 = (750+930, 535 + (int(to_point[0]) - 1) * 320)  # 2正-大线环2
        # pic_step14 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0]) + 1 - 1) * 215)  # wheel_above1

        json4 ='挂纤轮-'+str(WHEEL_DISTANCE.index(wheel_above[0])+1)
        json5 = from_point[0] + '-大线环2'
        json6 = '水平走线槽'
        json7 = from_point[0] + '-大线环2'
        json8 ='挂纤轮-'+str(WHEEL_DISTANCE.index(wheel_above[0])+1)
        json9 ='挂纤轮-13'
        # json10 ='挂纤轮-'+str(WHEEL_DISTANCE.index(wheel_bottom[0])+1)

        # 5. 进入to_point大线环1
        # distance_step_6 = wheel_above[0] + WHEEL - (BIGLINE_DISTANCE[to_point[0]] + LINE)
        distance_step_6 = 0
        # log[9] 四
        # log9 = '往下进入' + to_name + '的96芯设备单元H' + to_point[0] + '的大线环1。'
        log9 = ''
        pic_step8 = (255, 470 + (int(to_point[0]) - 1) * 320)  # 侧-大线环1

        # 6. 往左进入slot的中线环，进入该端口邻近的8位小线环
        if int(to_point[2]) < 12:
            distance_step_7 = (len(to_slot_cols) - int(to_point[2])) * 18 + 12 + 26 + 140
        else:
            distance_step_7 = (len(to_slot_cols) - int(to_point[2])) * 18 + 26 + 140
        # log[10] 五
        log10 = '从' + to_name + '的96芯设备单元H' + to_point[0] + '的中线环出来后，将线嵌入邻近的小线环中。'
        pic_step9 = (230 + (int(to_point[2]) - 1) * 18, 315 + (int(to_point[0]) - 1) * 320 + (int(to_point[1]) - 1) * 35)
        pic_step10 = (pic_step9[0], pic_step9[1] + 35 * (5 - int(to_point[1])))
        pic_step11 = (pic_step10[0] + distance_step_7 - 140, pic_step10[1])
        pic_step12 = (pic_step11[0] + 80, pic_step11[1] + 30)

        json11 = to_point[0] + '-大线环1'
        json12 = to_point[0] + '(' + to_point[1] + ',' + to_point[2] + ')'

        # 7. 往上插入端口
        distance_step_7 = (len(to_slot_rows) - int(to_point[1]) + 1) * 35
        print('往上插入端口:' + str(distance_step_7))
        # log[11] 五
        log11 = '最后往上将线插入' + to_name + '96芯设备单元H' + to_point[0] + '端口(' + format_radio_96(to_point[1],to_point[2]) + ')中。'

        if int(from_point[0]) == 2 and int(to_point[0]) == 6:
            increase = 400
        elif int(from_point[0]) == 3 and int(to_point[0]) == 4:
            increase = 525
        elif int(from_point[0]) == 6 and int(to_point[0]) == 5:
            increase = 100
        else:
            increase = 0
        used_distance = distance_step_1 + distance_step_2 + distance_step_3 + distance_step_4 + \
                        distance_step_5 + distance_step_6 + distance_step_7 + increase + 200
        print('总共需要线长：' + str(used_distance))
        cable_list = []
        for cable in CABLE_LENGTH:
            if cable > used_distance:
                cable_list.append(cable)
        cable_list.sort()
        shengyu_xianchang = cable_list[0] - used_distance
        print('剩余线长：' + str(shengyu_xianchang))

        # # 调整上下挂纤轮
        pic_step7 = (590 , 230)
        log0 = '此次跳纤计算的长度为' + str(round(used_distance / 1000, 1)) + '米，请选择一根长度为' + \
               str(int(cable_list[0] / 1000)) + '米的光纤跳线。'
        # json8 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
        # # json10 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0]) + 1)
        json10 = ''

        pic_step13 = (235,570+(int(to_point[0])-1)*320)  # 侧-大线环2（第二步）
        pic_step13_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[to_point[0]]) - 1) * 220)  # to_point对应左挂纤轮
        if int(to_point[0]) == 9:
            pic_step13_1 = (0, 0)

        pic_step6_6 = (0, 0)
        pic_step7_7 = (0, 0)
        pic_step7_8 = (0, 0)

        log_list = [log0,log1,log2,log3,log4,log5,log6,log7,log8,log9,log10,log11]
        step_list = [pic_step1,pic_step2,pic_step3,pic_step4,pic_step5,pic_step6,pic_step7,pic_step8_1,pic_step8,\
                     pic_step9,pic_step10,pic_step11,pic_step12,pic_step13, pic_step5_1, pic_step13_1, \
                     pic_step6_6, pic_step7_7, pic_step7_8]
        json_list = [shebei_count, log_list, '1-'+json1, '1-'+json2, '1-'+json3, '1-'+json4, '1-'+json5, json6, str(shebei_count)+'-'+json7, str(shebei_count)+'-'+json8, str(shebei_count)+'-'+json9, str(shebei_count)+'-'+json10, str(shebei_count)+'-'+json11, str(shebei_count)+'-'+json12]

    elif not right_to_left:
        # right, 右挂纤轮-中挂纤轮-左挂纤轮
        # 4. 往上至高于from_point的挂纤轮，水平走线槽，大线环2，wheel_above,wheel_bottom再调头向上走
        wheel_above = []
        # wheel_bottom = []
        # wheel_above[0] = 高于from_point的中挂纤轮
        # if COMBINATION_RING[from_point[0]] > BIGLINE_DISTANCE[to_point[0]]:
        if int(from_point[0]) < 12:
            compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) - 1 - 1]
        elif int(from_point[0]) == 12:
            compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1 - 1]
        for wheel_d in WHEEL_DISTANCE:
            if (wheel_d + WHEEL_D) > (compare_num):
                wheel_above.append(wheel_d)
        wheel_above.sort()

        if int(from_point[0]) < 12:
            distance_step_4_1 = distance_sqrt(450, COMBINATION_RING[str(int(from_point[0]) + 1)] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) - 1])
            distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) - 1])
            distance_step_4_2 = distance_sqrt(450, BIGLINE2_DISTANCE[COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)]]) - 1])
            distance_step_4_2 = distance_step_4_2 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)]]) - 1]))
            print(COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)])
            log4 = '从72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]) + 1)] + '的大孔穿出后，至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[str(int(from_point[0]) + 1)]) + 1) + \
                   '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + '，再至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)]]) + 1)
        elif int(from_point[0]) == 12:
            distance_step_4_1 = distance_sqrt(450, COMBINATION_RING[str(int(from_point[0]))] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1])
            distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[from_point[0]]) - 1])
            distance_step_4_2 = distance_sqrt(450, BIGLINE2_DISTANCE[COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]]) - 1])
            distance_step_4_2 = distance_step_4_2 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]]) - 1]))
            # distance_step_4 = wheel_above[0] + WHEEL - COMBINATION_RING[str(int(from_point[0]))]
            log4 = '从72芯配线单元L' + PEIXIAN_DANYUAN[str(int(from_point[0]))] + '的大孔穿出后，至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[from_point[0]]) + 1) + \
                   '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + '，再至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]]) + 1)

        # 左挂纤轮到from_point组合线环对应大线环2
        # distance_step_4_2 = wheel_above[0]+WHEEL - (BIGLINE2_DISTANCE[to_point[0]]+LINE)
        # 大线环2到水平走线槽边缘42mm，经过几个走线槽到大线环2
        distance_step_4_3 = (shebei_count - 1) * 748 + 42
        if right_to_left:
            distance_step_4_3 = (shebei_count - 1) * 748 + 200
        # 大线环2到机架2高挂纤轮
        # distance_step_4_4 = wheel_above[0]+WHEEL - (BIGLINE2_DISTANCE[to_point[0]]+LINE)
        distance_step_4_4 = 0
        distance_step_4 = distance_step_4_1 + distance_step_4_2 + distance_step_4_3 + distance_step_4_4

        if int(from_point[0]) < 12:
            log5 = '往上到' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)] + '的大线环2。'
            log6 = '从' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)] + '的大线环2出来后，沿水平走线槽经过' + str(shebei_count - 1) + '个机架。'
            log7 = '到' + to_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)] + '的大线环2。'
        elif int(from_point[0]) == 12:
            log5 = '往上到' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(from_point[0]))] + '的大线环2。'
            log6 = '从' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(from_point[0]))] + '的大线环2出来后，沿水平走线槽经过' + str(shebei_count - 1) + '个机架。'
            log7 = '到' + to_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(from_point[0]))] + '的大线环2。'

        wheel_above2 = []
        wheel_bottom = []
        if int(from_point[0]) < 12:
            compare_num = WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)]]) - 1 - 1]
        elif int(from_point[0]) == 12:
            compare_num = WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]]) - 1 - 1]
        for wheel_d in WHEEL_DISTANCE:
            if (wheel_d + WHEEL_D) > (compare_num):
                wheel_above2.append(wheel_d)
        wheel_above2.sort()

        # 1#from_point对应大线环2到from_ponit下面左挂纤轮+左挂纤轮到wheel_above2
        if int(from_point[0]) < 12:
            distance_step_5_1 = distance_sqrt(430, BIGLINE2_DISTANCE[COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)]]) - 1])
            distance_step_5_1 = distance_step_5_1 + distance_sqrt(200, (wheel_above2[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)]]) - 1]))
        elif int(from_point[0]) == 12:
            distance_step_5_1 = distance_sqrt(430, BIGLINE2_DISTANCE[COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]]) - 1])
            distance_step_5_1 = distance_step_5_1 + distance_sqrt(200, (wheel_above2[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]]) - 1]))

        # 高挂纤轮wheel_above2到最下面的挂纤轮
        distance_step_5_2 = wheel_above2[0] + WHEEL - WHEEL_DISTANCE[-1]

        # 调头向上到高于to_point的挂纤轮
        if int(to_point[0]) == 9:
            wheel_bottom.append(WHEEL_DISTANCE[-2])
        else:
            for wheel_d in WHEEL_DISTANCE:
                if wheel_d + WHEEL_D > (WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1 - 1]):
                    wheel_bottom.append(wheel_d)
            wheel_bottom.sort()
        distance_step_5_3 = wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[-1]

        distance_step_5 = distance_step_5_1 + distance_step_5_2 + distance_step_5_3

        if int(from_point[0]) < 12:
            log8 = '从设备单元H' + COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)] + '大线环2穿出后，经过' + to_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above2[0]) + 1) + \
                   '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[to_point[0]]) + 1)
        elif int(from_point[0]) == 12:
            log8 = '从设备单元H' + COMBINATION_VS_BIGLINE2[str(int(from_point[0]))] + '大线环2穿出后，经过' + to_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above2[0]) + 1) + \
                   '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[to_point[0]]) + 1)


        pic_step6_6 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above2[0]) + 1 - 1) * 215)  # wheel_above2
        pic_step7_7 = (590, 230 + (WHEEL_DISTANCE.index(wheel_bottom[0]) + 1 - 1) * 215)  # wheel_bottom
        pic_step7_8 = (405, 360 + (int(FRONT_LEFT_WHEEL[to_point[0]]) - 1) * 220)  # to_point对应左挂纤轮
        if int(to_point[0]) == 9:
            pic_step7_8 = (0, 0)

        json3 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
        json4 = '挂纤轮-13'
        json5 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0]) + 1)

        # 4. wheel_bottom到to_point下面左挂纤轮+to_point下面做挂纤轮到to_point大线环2
        distance_step_6 = distance_sqrt(430, BIGLINE2_DISTANCE[to_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1])
        distance_step_6 = distance_step_6 + distance_sqrt(200, (wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[to_point[0]]) - 1]))



        pic_step6 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0]) + 1 - 1) * 215)  # wheel_above 水平走线
        # pic_step7 = (590, 230 + (WHEEL_DISTANCE.index(wheel_bottom[0])+1-1) * 215)  # wheel_bottom
        # pic_step8_1 = (750, 535 + (int(to_point[0]) - 1) * 320)  # 2正-大线环2
        if int(from_point[0]) < 12:
            pic_step8_1 = (750, 535 + (int(COMBINATION_VS_BIGLINE2[str(int(from_point[0])+1)]) - 1) * 320)  # 2正-from_point组合线环对应大线环2
        elif int(from_point[0]) == 12:
            pic_step8_1 = (750, 535 + (int(COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]) - 1) * 320)  # 2正-from_point组合线环对应大线环2
        if right_to_left:
            pic_step8_1 = (750 + 930, 535 + (int(to_point[0]) - 1) * 320)  # 2正-大线环2
        # pic_step14 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0]) + 1 - 1) * 215)  # wheel_above1

        json4 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
        json5 = from_point[0] + '-大线环2'
        json6 = '水平走线槽'
        json7 = from_point[0] + '-大线环2'
        json8 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
        json9 = '挂纤轮-13'
        # json10 ='挂纤轮-'+str(WHEEL_DISTANCE.index(wheel_bottom[0])+1)

        # 5. 进入to_point大线环1
        # distance_step_6 = wheel_above[0] + WHEEL - (BIGLINE_DISTANCE[to_point[0]] + LINE)

        # log[9] 四
        log9 = '往上进入' + to_name + '的96芯设备单元H' + to_point[0] + '的大线环1。'
        pic_step8 = (255, 470 + (int(to_point[0]) - 1) * 320)  # 侧-大线环1

        # 6. 往左进入slot的中线环，进入该端口邻近的8位小线环
        if int(to_point[2]) < 12:
            distance_step_7 = (len(to_slot_cols) - int(to_point[2])) * 18 + 12 + 26 + 140
        else:
            distance_step_7 = (len(to_slot_cols) - int(to_point[2])) * 18 + 26 + 140
        # log[10] 五
        log10 = '从' + to_name + '的96芯设备单元H' + to_point[0] + '的大线环1出来后，穿过中线环，将线嵌入邻近的小线环中。'
        pic_step9 = (230 + (int(to_point[2]) - 1) * 18, 315 + (int(to_point[0]) - 1) * 320 + (int(to_point[1]) - 1) * 35)
        pic_step10 = (pic_step9[0], pic_step9[1] + 35 * (5 - int(to_point[1])))
        pic_step11 = (pic_step10[0] + distance_step_7 - 140, pic_step10[1])
        pic_step12 = (pic_step11[0] + 80, pic_step11[1] + 30)

        json11 = to_point[0] + '-大线环1'
        json12 = to_point[0] + '(' + to_point[1] + ',' + to_point[2] + ')'

        # 7. 往上插入端口
        distance_step_7 = (len(to_slot_rows) - int(to_point[1]) + 1) * 35

        # log[11] 五
        log11 = '最后往上将线插入' + to_name + '96芯设备单元H' + to_point[0] + '端口(' + format_radio_96(to_point[1],
                                                                                          to_point[2]) + ')中。'

        if int(from_point[0]) == 2 and int(to_point[0]) == 6:
            increase = 400
        elif int(from_point[0]) == 3 and int(to_point[0]) == 4:
            increase = 525
        elif int(from_point[0]) == 6 and int(to_point[0]) == 5:
            increase = 100
        else:
            increase = 0
        used_distance = distance_step_1 + distance_step_2 + distance_step_3 + distance_step_4 + \
                        distance_step_5 + distance_step_6 + distance_step_7 + increase + 200
        print('总共需要线长：' + str(used_distance))
        cable_list = []
        for cable in CABLE_LENGTH:
            if cable > used_distance:
                cable_list.append(cable)
        cable_list.sort()
        shengyu_xianchang = cable_list[0] - used_distance
        print('剩余线长：' + str(shengyu_xianchang))

        # # 调整上下挂纤轮
        pic_step7 = (590, 230)
        log0 = '此次跳纤计算的长度为' + str(round(used_distance / 1000, 1)) + '米，请选择一根长度为' + \
               str(int(cable_list[0] / 1000)) + '米的光纤跳线。'
        # json8 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
        # # json10 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0]) + 1)
        json10 = ''

        # pic_step13 = (235, 570 + (int(to_point[0]) - 1) * 320)  # 侧-大线环2（第二步）
        # pic_step13_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[to_point[0]]) - 1) * 220)  # to_point对应左挂纤轮
        if int(from_point[0]) == 12 and int(to_point[0]) == 9:
            pic_step13 = (235, 570 + (int(COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]) - 1) * 320)  # 侧-from_point组合线环对应大线环2（第二步）
            pic_step13_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]]) - 1) * 220)  # from_point组合线环对应大线环2对应左挂纤轮
        elif int(from_point[0]) == 12 and int(to_point[0]) < 9 :
            pic_step13 = (235, 570 + (int(COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]) - 1) * 320)  # 侧-from_point组合线环对应大线环2（第二步）
            pic_step13_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0]))]]) - 1) * 220)  # from_point组合线环对应大线环2对应左挂纤轮
        elif int(to_point[0]) == 9 and int(from_point[0]) < 12:
            pic_step13 = (235, 570 + (int(COMBINATION_VS_BIGLINE2[str(int(from_point[0]) + 1)]) - 1) * 320)  # 侧-from_point组合线环对应大线环2（第二步）
            # pic_step13_1 = (0, 0)
            pic_step13_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0]) + 1)]]) - 1) * 220)  # from_point组合线环对应大线环2对应左挂纤轮
        elif int(from_point[0]) < 12:
            pic_step13 = (235, 570 + (int(COMBINATION_VS_BIGLINE2[str(int(from_point[0]) + 1)]) - 1) * 320)  # 侧-from_point组合线环对应大线环2（第二步）
            pic_step13_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(from_point[0]) + 1)]]) - 1) * 220)  # from_point组合线环对应大线环2对应左挂纤轮


        log_list = [log0, log1, log2, log3, log4, log5, log6, log7, log8, log9, log10, log11]
        step_list = [pic_step1, pic_step2, pic_step3, pic_step4, pic_step5, pic_step6, pic_step7, pic_step8_1,
                     pic_step8, \
                     pic_step9, pic_step10, pic_step11, pic_step12, pic_step13, pic_step5_1, pic_step13_1,\
                     pic_step6_6, pic_step7_7, pic_step7_8]
        json_list = [shebei_count, log_list, '1-' + json1, '1-' + json2, '1-' + json3, '1-' + json4, '1-' + json5,
                     json6, str(shebei_count) + '-' + json7, str(shebei_count) + '-' + json8,
                     str(shebei_count) + '-' + json9, str(shebei_count) + '-' + json10,
                     str(shebei_count) + '-' + json11, str(shebei_count) + '-' + json12]

    print(step_list)
    print(log_list)
    print('used_distance:', used_distance)
    return step_list, log_list, json_list, int(cable_list[0] / 1000), right_to_left


# 计算同一设备、不同side、正面-背面，跳纤方式
def calculate_one_front_back(jiechushebei_radio,jierushebei_radio, \
                              jiechushebei_slot_rows,jiechushebei_slot_cols, \
                              jierushebei_slot_rows,jierushebei_slot_cols, \
                              jiechushebei,jierushebei,CABLE_LENGTH):
    # json0 = ['相同机架的96芯设备单元与96芯设备单元跳纤']
    from_point = jiechushebei_radio
    to_point = jierushebei_radio
    from_slot_rows = jiechushebei_slot_rows
    from_slot_cols = jiechushebei_slot_cols
    to_slot_rows = jierushebei_slot_rows
    to_slot_cols = jierushebei_slot_cols
    from_name = jiechushebei
    to_name = jierushebei
    print('from_point'+str(from_point))
    print('to_point'+str(to_point))
    # 1. 先往下走到小线环
    distance_step_1 = (len(from_slot_rows) - int(from_point[1]) + 1) * 35

    log1 = '先从'+from_name+'的96芯设备单元H'+from_point[0]+'端口('+format_radio_96(from_point[1],from_point[2])+')'+'出来往下经过下方邻近的8位小线环。'
    pic_step1 = (230+(int(from_point[2])-1)*18, 315+(int(from_point[0])-1)*320+(int(from_point[1])-1)*35)
    pic_step2 = (pic_step1[0], pic_step1[1]+35*(5-int(from_point[1])))

    json1 = from_point[0]+'('+from_point[1]+','+from_point[2]+')'

    # 2. 往右穿过中线环，最后一个端口到slot边框/中线环是26mm，（到大线环1左边框是99mm，）,从中线环顶边到大线环2底边是190mm
    if int(from_point[2]) < 12 :
        distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 12 + 26 + 140
    else:
        distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 26 + 140
    print('2. 再经过中线环到大线环1:' + str(distance_step_2))

    log2 = '往右穿过中线环再到设备单元H'+from_point[0]+'的大线环1。'
    pic_step3 = (pic_step2[0]+distance_step_2-140,pic_step2[1])
    pic_step4 = (pic_step3[0]+80,pic_step3[1]+30)

    json2 = from_point[0]+'-大线环1'

    # 3. 往上走先到高于from_pront的挂纤轮，再往下走直到侧面最下面那个挂纤轮调头向上走
    # 大线环1到高于其的挂纤轮
    wheel_above = []
    # wheel_bottom = []
    if BIGLINE_DISTANCE[from_point[0]] > COMBINATION_RING[to_point[0]]:
        compare_num = WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]])-1-1]
    else:
        if int(to_point[0]) < 12:
            compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0]) + 1)]) - 1 - 1]
        elif int(to_point[0]) == 12:
            compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1 - 1]
    for wheel_d in WHEEL_DISTANCE:
        if wheel_d + WHEEL_D > (compare_num):
            wheel_above.append(wheel_d)
    wheel_above.sort()

    # from_point大线环1到做挂纤轮，左挂纤轮到wheel_above
    distance_step_3 =        distance_sqrt(430, BIGLINE_DISTANCE[from_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]]) - 1])
    distance_step_3 = distance_step_3 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]]) - 1]))
    # distance_step_3 = wheel_above[0]+WHEEL - (BIGLINE_DISTANCE[from_point[0]]+LINE)

    if int(to_point[0]) < 12:
        log3 = '穿过设备单元H' + from_point[0] + '大线环1后，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
               '，再至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[str(int(to_point[0]) + 1)]) + 1)
    elif int(to_point[0]) == 12:
        log3 = '穿过设备单元H' + from_point[0] + '大线环1后，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
               '，再至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[to_point[0]]) + 1)
    pic_step5 = (255,470+(int(from_point[0])-1)*320)  # 侧-大线环1
    pic_step6 = (590,230+(WHEEL_DISTANCE.index(wheel_above[0])+1-1)*215)  # wheel_above
    # pic_step7 = (590,230+(WHEEL_DISTANCE.index(wheel_bottom[0])+1-1)*215)  # wheel_bottom
    pic_step5_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[from_point[0]]) - 1) * 220)  # from_point对应左挂纤轮
    if int(from_point[0]) == 9:
        pic_step5_1 = (0, 0)

    json3 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0])+1)

    # 4. 往下进入to_point组合线环#XX+1的大孔
    if int(to_point[0]) < 12:
        distance_step_4 = distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)]) - 1])
        distance_step_4 = distance_step_4 +        distance_sqrt(430, COMBINATION_RING[str(int(to_point[0])+1)] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)])-1])

        log4 = '进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]) + 1)] + '组合线环的大孔。'
        json4 = PEIXIAN_DANYUAN[str(int(to_point[0]) + 1)] + '-大孔'
        if int(to_point[0]) + 1 <= 4:
            pic_step8 = (1080, 340 + 160 * int(to_point[0]))  # 侧-组合线环大孔
        elif int(to_point[0]) + 1 > 4 and int(to_point[0]) + 1 <= 8:
            pic_step8 = (1080, 340 + 160 * int(to_point[0]) + 340)
        elif int(to_point[0]) + 1 > 8 and int(to_point[0]) + 1 <= 12:
            pic_step8 = (1080, 340 + 160 * int(to_point[0]) + 340 * 2)
    elif int(to_point[0]) == 12:
        distance_step_4 = distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1])
        distance_step_4 = distance_step_4 +        distance_sqrt(430, COMBINATION_RING[to_point[0]] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1])

        log4 = '进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]))] + '组合线环。'
        json4 = PEIXIAN_DANYUAN[str(int(to_point[0]))] + '-大孔'
        if int(to_point[0]) <= 4:
            pic_step8 = (1080, 340 + 160 * (int(to_point[0]) - 1))
        elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
            pic_step8 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340)
        elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
            pic_step8 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340 * 2)

    # 5. 再向上进入to_point组合线环#XX的小孔
    if int(to_point[0]) < 12:
        distance_step_5 = COMBINATION_RING[to_point[0]] - COMBINATION_RING[str(int(to_point[0]) + 1)]
        if int(to_point[0]) <= 4:
            pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1))  # 侧-组合线环小孔
        elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
            pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340)
        elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
            pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340 * 2)
    elif int(to_point[0]) == 12:
        distance_step_5 = 0
        pic_step9 = (pic_step8[0], pic_step8[1])
    print('3. 再进入' + to_name + '72芯配线单元' + PEIXIAN_DANYUAN[str(int(to_point[0]))] + '组合线环的小孔。')

    log5 = '再进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]))] + '组合线环的小孔。'

    json5 = PEIXIAN_DANYUAN[str(int(to_point[0]))] + '-小孔'

    # 6. 往右进入指定托盘
    distance_step_6 = 34 + 26 * (6 - int(to_point[1])) + 84 + 20.5 * (int(to_point[2]) - 1)

    log6 = '从' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[to_point[0]] + '组合线环的小孔出穿出。'
    log7 = '往右进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(to_point[0])] + '端口(' + str(to_point[1]) + ',' + str(to_point[2]) + ')中。'

    if int(to_point[0]) <= 4:
        pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1))
        pic_step12 = (
        325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25)
    elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
        pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1) + 340)
        pic_step12 = (
        325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335)
    elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
        pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1) + 340 * 2)
        pic_step12 = (
        325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335 * 2)
    pic_step11 = (250, pic_step12[1])

    json6 = PEIXIAN_DANYUAN[to_point[0]] + '(' + to_point[1] + ',' + to_point[2] + ')'

    used_distance = distance_step_1 + distance_step_2 + distance_step_3 + distance_step_4 + \
                    distance_step_5 + distance_step_6 + 200
    print('总共需要线长：' + str(used_distance))
    cable_list = []
    for cable in CABLE_LENGTH:
        if cable > used_distance:
            cable_list.append(cable)
    cable_list.sort()
    shengyu_xianchang = cable_list[0] - used_distance
    print('剩余线长：' + str(shengyu_xianchang))

    # # 调整上下挂纤轮

    log0 = '此次跳纤计算的长度为' + str(round(used_distance / 1000, 1)) + '米，请选择一根长度为' + \
           str(int(cable_list[0] / 1000)) + '米的光纤跳线。'
    # json3 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)

    if int(to_point[0]) < 12:
        pic_step8_1 = (405, 360 + (int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)]) - 1) * 220)  # to_point对应左挂纤轮
    elif int(to_point[0]) == 12:
        pic_step8_1 = (405, 360 + (int(BACK_RIGHT_WHEEL[to_point[0]]) - 1) * 220)  # to_point对应左挂纤轮

    log_list = [log0, log1, log2, log3, log4, log5, log6, log7]
    step_list = [pic_step1, pic_step2, pic_step3, pic_step4, pic_step5, pic_step6, pic_step8, \
                 pic_step9, pic_step10, pic_step11, pic_step12, pic_step5_1, pic_step8_1]
    json_list = [1, log_list, json1, json2, json3, json4, json5, json6]

    print(step_list)
    print(log_list)
    print('used_distance:', used_distance)
    return step_list, log_list, json_list, int(cable_list[0] / 1000)


# 计算不同设备、不同side、正面-背面，跳纤方式
def calculate_two_front_back(jiechushebei_radio,jierushebei_radio, \
                              jiechushebei_slot_rows,jiechushebei_slot_cols, \
                              jierushebei_slot_rows,jierushebei_slot_cols, \
                              jiechushebei,jierushebei,\
                              shebei_count,CABLE_LENGTH):
    # json0 = ['不同机架的96芯设备单元与96芯设备单元跳纤']
    from_point = jiechushebei_radio
    to_point = jierushebei_radio
    from_slot_rows = jiechushebei_slot_rows
    from_slot_cols = jiechushebei_slot_cols
    to_slot_rows = jierushebei_slot_rows
    to_slot_cols = jierushebei_slot_cols
    from_name = jiechushebei
    to_name = jierushebei
    right_to_left = 0
    if re.findall('\d+', from_name)[0] < re.findall('\d+', to_name)[0]:
        right_to_left = 1
    print('from_point'+str(from_point))
    print('to_point'+str(to_point))

    if not right_to_left:
        # 1. 先往下走到小线环
        distance_step_1 = (len(from_slot_rows) - int(from_point[1]) + 1) * 35
        # log[0]
        log1 = '先从' + from_name + '的96芯设备单元H' + from_point[0] + '端口(' + format_radio_96(from_point[1], from_point[
            2]) + ')' + '出来往下经过下方邻近的8位小线环。'
        pic_step1 = (230 + (int(from_point[2]) - 1) * 18, 315 + (int(from_point[0]) - 1) * 320 + (int(from_point[1]) - 1) * 35)
        if right_to_left:
            pic_step1 = (230 + 930 + (int(from_point[2]) - 1) * 18,315 + (int(from_point[0]) - 1) * 320 + (int(from_point[1]) - 1) * 35)
        pic_step2 = (pic_step1[0], pic_step1[1] + 35 * (5 - int(from_point[1])))

        json1 = from_point[0] + '(' + from_point[1] + ',' + from_point[2] + ')'

        # 2. 往右穿过中线环，最后一个端口到slot边框/中线环是26mm，（到大线环1左边框是99mm，）,从中线环顶边到大线环2底边是190mm/到大线环1的底边是130mm
        # 从中线环到水平走线槽边是230
        if int(from_point[2]) < 12:
            distance_step_2_1 = (len(from_slot_cols) - int(from_point[2])) * 18 + 12 + 26 + 230
        else:
            distance_step_2_1 = (len(from_slot_cols) - int(from_point[2])) * 18 + 26 + 230
        # 经过N个机架到to_point的大线环2
        distance_step_2_2 = (shebei_count-1) * 748 + 70
        distance_step_2 = distance_step_2_1 + distance_step_2_2

        log2 = '往右穿过'+from_name+'96芯设备单元H'+from_point[0]+'的中线环，再到水平走线槽，沿着水平走线槽经过'+str(shebei_count-1)+'个机架到'+to_name+'96芯设备单元'+from_point[0]+'的大线环2。'
        pic_step3 = (pic_step2[0]+distance_step_2_1-230,pic_step2[1])
        pic_step4 = (pic_step3[0]+80,pic_step3[1]+130)

        json2 = from_point[0]+'-大线环2'

        # 3. 往上走先到高于from_pront的挂纤轮，再往下走直到侧面最下面那个挂纤轮调头向上走
        # 大线环1到高于其的挂纤轮
        wheel_above = []
        wheel_bottom = []
        if BIGLINE_DISTANCE[from_point[0]] > COMBINATION_RING[to_point[0]]:
            compare_num = WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]])-1-1]
        else:
            if int(to_point[0]) < 12:
                compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0]) + 1)]) - 1 - 1]
            elif int(to_point[0]) == 12:
                compare_num = WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1 - 1]
        for wheel_d in WHEEL_DISTANCE:
            if (wheel_d + WHEEL_D) > (compare_num):
                wheel_above.append(wheel_d)
        wheel_above.sort()

        # from_point大线环2到做挂纤轮，左挂纤轮到wheel_above
        distance_step_3_1 =        distance_sqrt(430, BIGLINE2_DISTANCE[from_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]]) - 1])
        distance_step_3_1 = distance_step_3_1 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]]) - 1]))
        # distance_step_3_1 = wheel_above[0]+WHEEL - (BIGLINE2_DISTANCE[from_point[0]]+LINE)
        # # 高挂纤轮到最下面的挂纤轮
        distance_step_3 = distance_step_3_1

        if int(to_point[0]) < 12:
            log3 = '穿过设备单元H' + from_point[0] + '大线环2后，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                   '，再至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[str(int(to_point[0]) + 1)]) + 1)
        elif int(to_point[0]) == 12:
            log3 = '穿过设备单元H' + from_point[0] + '大线环2后，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                   '，再至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[to_point[0]]) + 1)
        pic_step5 = (235,550+(int(from_point[0])-1)*320)  # 侧-大线环2
        pic_step6 = (590,230+(WHEEL_DISTANCE.index(wheel_above[0])+1-1)*215)  # wheel_above
        # pic_step7 = (590,230+(WHEEL_DISTANCE.index(wheel_bottom[0])+1-1)*215)  # wheel_bottom
        pic_step5_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[from_point[0]]) - 1) * 220)  # from_point对应左挂纤轮
        if int(from_point[0]) == 9:
            pic_step5_1 = (0, 0)

        json3= '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0])+1)
        json4 = '挂纤轮-13'
        # json5 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0])+1)

        # 4. 往下进入to_point组合线环#XX+1的大孔
        if int(to_point[0]) < 12:
            distance_step_4 = distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)]) - 1])
            distance_step_4 = distance_step_4 +        distance_sqrt(430, COMBINATION_RING[str(int(to_point[0])+1)] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)])-1])

            log4 = '进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]) + 1)] + '组合线环的大孔。'
            json6 = PEIXIAN_DANYUAN[str(int(to_point[0]) + 1)] + '-大孔'
            if int(to_point[0]) + 1 <= 4:
                pic_step8 = (1080, 340 + 160 * int(to_point[0]))  # 侧-组合线环大孔
            elif int(to_point[0]) + 1 > 4 and int(to_point[0]) + 1 <= 8:
                pic_step8 = (1080, 340 + 160 * int(to_point[0]) + 340)
            elif int(to_point[0]) + 1 > 8 and int(to_point[0]) + 1 <= 12:
                pic_step8 = (1080, 340 + 160 * int(to_point[0]) + 340 * 2)
        elif int(to_point[0]) == 12:
            distance_step_4 = distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1])
            distance_step_4 = distance_step_4 +        distance_sqrt(430, COMBINATION_RING[to_point[0]] - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[to_point[0]]) - 1])

            log4 = '进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]))] + '组合线环。'
            json6 = PEIXIAN_DANYUAN[str(int(to_point[0]))] + '-大孔'
            if int(to_point[0]) <= 4:
                pic_step8 = (1080, 340 + 160 * (int(to_point[0]) - 1))
            elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
                pic_step8 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340)
            elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
                pic_step8 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340 * 2)

        # 5. 再向上进入to_point组合线环#XX的小孔
        if int(to_point[0]) < 12:
            distance_step_5 = COMBINATION_RING[to_point[0]] - COMBINATION_RING[str(int(to_point[0]) + 1)]
            if int(to_point[0]) <= 4:
                pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1))  # 侧-组合线环小孔
            elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
                pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340)
            elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
                pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340 * 2)
        elif int(to_point[0]) == 12:
            distance_step_5 = 0
            pic_step9 = (pic_step8[0], pic_step8[1])

        log5 = '再进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]))] + '组合线环的小孔。'

        json7 = PEIXIAN_DANYUAN[str(int(to_point[0]))] + '-小孔'

        # 6. 往右进入指定托盘
        distance_step_6 = 34 + 26 * (6 - int(to_point[1])) + 84 + 20.5 * (int(to_point[2]) - 1)

        log6 = '从' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[to_point[0]] + '组合线环的小孔出穿出。'
        log7 = '往右进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(to_point[0])] + '端口(' + str(to_point[1]) + ',' + str(to_point[2]) + ')中。'

        if int(to_point[0]) <= 4:
            pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1))
            pic_step12 = (
            325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25)
        elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
            pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1) + 340)
            pic_step12 = (
            325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335)
        elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
            pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1) + 340 * 2)
            pic_step12 = (
            325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335 * 2)
        pic_step11 = (250, pic_step12[1])

        json8 = PEIXIAN_DANYUAN[to_point[0]] + '(' + to_point[1] + ',' + to_point[2] + ')'

        used_distance = distance_step_1 + distance_step_2 + distance_step_3 + distance_step_4 + \
                        distance_step_5 + distance_step_6 + 200
        print('总共需要线长：' + str(used_distance))
        cable_list = []
        for cable in CABLE_LENGTH:
            if cable > used_distance:
                cable_list.append(cable)
        cable_list.sort()
        shengyu_xianchang = cable_list[0] - used_distance
        print('剩余线长：' + str(shengyu_xianchang))

        # # 调整上下挂纤轮
        pic_step7 = (590, 230)

        if int(to_point[0]) < 12:
            pic_step8_1 = (405, 360 + (int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)]) - 1) * 220)  # to_point对应左挂纤轮
        elif int(to_point[0]) == 12:
            pic_step8_1 = (405, 360 + (int(BACK_RIGHT_WHEEL[to_point[0]]) - 1) * 220)  # to_point对应左挂纤轮

        log0 = '此次跳纤计算的长度为' + str(round(used_distance / 1000, 1)) + '米，请选择一根长度为' + \
               str(int(cable_list[0] / 1000)) + '米的光纤跳线。'
        # json3 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
        json5 = ''
        pic_step7_1 = (0, 0)
        pic_step8_8 = (0, 0)
        pic_step8_9 = (0, 0)
        pic_step13_1 = (0, 0)
        log4_1, log4_2, log4_3, log4_4, log4_5, log4_6 = '', '', '', '', '', ''

    elif right_to_left:
        # 1. 先往下走到小线环
        distance_step_1 = (len(from_slot_rows) - int(from_point[1]) + 1) * 35

        log1 = '先从' + from_name + '的96芯设备单元H' + from_point[0] + '端口(' + format_radio_96(from_point[1], from_point[2]) + ')' + '出来往下经过下方邻近的8位小线环。'
        pic_step1 = (230 + (int(from_point[2]) - 1) * 18, 315 + (int(from_point[0]) - 1) * 320 + (int(from_point[1]) - 1) * 35)
        pic_step2 = (pic_step1[0], pic_step1[1] + 35 * (5 - int(from_point[1])))

        json1 = from_point[0] + '(' + from_point[1] + ',' + from_point[2] + ')'

        # 2. 往右穿过中线环，最后一个端口到slot边框/中线环是26mm，（到大线环1左边框是99mm，）,从中线环顶边到大线环2底边是190mm
        if int(from_point[2]) < 12:
            distance_step_2_1 = (len(from_slot_cols) - int(from_point[2])) * 18 + 12 + 26 + 140
        else:
            distance_step_2_1 = (len(from_slot_cols) - int(from_point[2])) * 18 + 26 + 140

        # 到大线环1的距离
        distance_step_2_2 = 0
        distance_step_2 = distance_step_2_1 + distance_step_2_2

        log2 = '往右穿过中线环再到设备单元H' + from_point[0] + '的大线环1。'
        pic_step3 = (pic_step2[0] + distance_step_2_1 - 140, pic_step2[1])
        pic_step4 = (pic_step3[0] + 80, pic_step3[1] + 30)

        json2 = from_point[0] + '-大线环2'

        # 3. 往上走先到高于from_pront的挂纤轮，再往下走直到侧面最下面那个挂纤轮调头向上走
        # 大线环1到高于其的挂纤轮
        wheel_above = []
        wheel_bottom = []
        for wheel_d in WHEEL_DISTANCE:
            if wheel_d + WHEEL_D > (WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]]) - 1 - 1]):
                wheel_above.append(wheel_d)
        wheel_above.sort()
        # from_point大线环1到from_ponit下面左挂纤轮+左挂纤轮到wheel_above
        distance_step_3_1 = distance_sqrt(430, BIGLINE_DISTANCE[from_point[0]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]]) - 1])
        distance_step_3_1 = distance_step_3_1 + distance_sqrt(200, (wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[from_point[0]]) - 1]))

        # 高挂纤轮wheel_above到最下面的挂纤轮
        distance_step_3_2 = wheel_above[0] + WHEEL - WHEEL_DISTANCE[-1]

        # 调头向上到高于to_point的挂纤轮
        if int(to_point[0]) == 12:
            wheel_bottom.append(WHEEL_DISTANCE[-2])
        else:
            if int(to_point[0]) < 12:
                compare_num = WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]]) - 1 - 1]
            elif int(to_point[0]) == 12:
                compare_num = WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) - 1 - 1]
            for wheel_d in WHEEL_DISTANCE:
                if wheel_d + WHEEL_D > compare_num:
                    wheel_bottom.append(wheel_d)
            wheel_bottom.sort()
        distance_step_3_3 = wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[-1]
        distance_step_3 = distance_step_3_1 + distance_step_3_2 + distance_step_3_3

        log3 = '从设备单元H' + from_point[0] + '大线环1穿出后，经过' + from_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
               '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) + 1)
        if int(to_point[0]) == 12 and int(from_point[0]) == 9:
            log3 = '从设备单元H' + from_point[0] + '大线环1穿出后，经过' + from_name + '中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                   '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
        elif int(from_point[0]) == 9 and int(to_point[0]) < 12:
            log3 = '从设备单元H' + from_point[0] + '大线环1穿出后，经过' + from_name + '中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                   '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]]) + 1)
        elif int(to_point[0]) == 12:
            log3 = '从设备单元H' + from_point[0] + '大线环1穿出后，经过' + from_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                   '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '。'
        elif int(to_point[0]) < 12:
            log3 = '从设备单元H' + from_point[0] + '大线环1穿出后，经过' + from_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[from_point[0]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_above[0]) + 1) + \
                   '。再到最下面的中挂纤轮1' + '，再至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '，至左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]]) + 1)

        pic_step5 = (255, 470 + (int(from_point[0]) - 1) * 320)  # 侧-大线环1
        pic_step5_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[from_point[0]]) - 1) * 220)  # from_point对应左挂纤轮
        if int(from_point[0]) == 9:
            pic_step5_1 = (0, 0)
        pic_step6 = (590, 230 + (WHEEL_DISTANCE.index(wheel_above[0]) + 1 - 1) * 215)  # wheel_above
        pic_step7 = (590, 230 + (WHEEL_DISTANCE.index(wheel_bottom[0]) + 1 - 1) * 215)  # wheel_bottom
        if int(to_point[0]) < 12:
            pic_step7_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]]) - 1) * 220)  # to_point对应做挂纤轮
        elif int(to_point[0]) == 12:
            pic_step7_1 = (0, 0)


        json3 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
        json4 = '挂纤轮-13'
        # json5 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_bottom[0])+1)


        if int(to_point[0]) < 12:
            # 4. wheel_bottom到大线环2
            distance_step_4_1 = distance_sqrt(430, BIGLINE2_DISTANCE[COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]]) - 1])
            distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, (wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]]) - 1]))
            # 大线环2到水平走线槽边缘42mm，经过几个走线槽到to_point大线环1
            distance_step_4_2 = (shebei_count - 1) * 748 + 200  # 42
            distance_step_4 = distance_step_4_1 + distance_step_4_2

            log4_1 = '进入' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)] + '的大线环2。'
            log4_2 = '从' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)] + '的大线环2出来后，沿水平走线槽经过' + str(shebei_count - 1) + '个机架。'
            log4_3 = '到' + to_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)] + '的大线环2。'
            log4_4 = '从大线环2穿出后，经过' + to_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + '再至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[str(int(to_point[0])+1)]) + 1)
        elif int(to_point[0]) == 12:
            # 4. wheel_bottom到大线环2
            distance_step_4_1 = distance_sqrt(430, BIGLINE2_DISTANCE[COMBINATION_VS_BIGLINE2[str(int(to_point[0]))]] + LINE - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) - 1])
            distance_step_4_1 = distance_step_4_1 + distance_sqrt(200, (wheel_bottom[0] + WHEEL - WHEEL_DISTANCE[int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0]))]]) - 1]))
            # 大线环2到水平走线槽边缘42mm，经过几个走线槽到to_point大线环1
            distance_step_4_2 = (shebei_count - 1) * 748 + 200  # 42
            distance_step_4 = distance_step_4_1 + distance_step_4_2

            log4_1 = '进入' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(to_point[0]))] + '的大线环2。'
            log4_2 = '从' + from_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(to_point[0]))] + '的大线环2出来后，沿水平走线槽经过' + str(shebei_count - 1) + '个机架。'
            log4_3 = '到' + to_name + '96芯设备单元H' + COMBINATION_VS_BIGLINE2[str(int(to_point[0]))] + '的大线环2。'
            log4_4 = '从大线环2穿出后，经过' + to_name + '左挂纤轮' + str(13 - int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0]))]]) + 1) + '，至中挂纤轮' + str(12 - WHEEL_DISTANCE.index(wheel_bottom[0]) + 1) + \
                     '至右挂纤轮' + str(13 - int(BACK_RIGHT_WHEEL[str(int(to_point[0]))]) + 1)

        log4_5 = '进入'+to_name+'72芯配线单元L'+PEIXIAN_DANYUAN[str(int(to_point[0]))]+'组合线环。'
        log4_6 = '再进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]))] + '组合线环的小孔。'
        if int(to_point[0]) < 12:
            pic_step8_8 = (235, 570 + (int(COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]) - 1) * 320)  # 侧-大线环2
        elif int(to_point[0]) == 12:
            pic_step8_8 = (235, 570 + (int(COMBINATION_VS_BIGLINE2[str(int(to_point[0]))]) - 1) * 320)  # 侧-大线环2



        # 4. 往下进入to_point组合线环#XX+1的大孔
        if int(to_point[0]) < 12:
            distance_step_4 = distance_step_4 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[int(BACK_RIGHT_WHEEL[str(int(to_point[0]) + 1)]) - 1])
            distance_step_4 = distance_step_4 + distance_sqrt(430, COMBINATION_RING[str(int(to_point[0]) + 1)] -
                                                              WHEEL_DISTANCE[
                                                                  int(BACK_RIGHT_WHEEL[str(int(to_point[0]) + 1)]) - 1])

            log4 = '进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]) + 1)] + '组合线环的大孔。'
            json6 = PEIXIAN_DANYUAN[str(int(to_point[0]) + 1)] + '-大孔'
            if int(to_point[0]) + 1 <= 4:
                pic_step8 = (1080, 340 + 160 * int(to_point[0]))  # 侧-组合线环大孔
            elif int(to_point[0]) + 1 > 4 and int(to_point[0]) + 1 <= 8:
                pic_step8 = (1080, 340 + 160 * int(to_point[0]) + 340)
            elif int(to_point[0]) + 1 > 8 and int(to_point[0]) + 1 <= 12:
                pic_step8 = (1080, 340 + 160 * int(to_point[0]) + 340 * 2)
        elif int(to_point[0]) == 12:
            distance_step_4 = distance_step_4 + distance_sqrt(200, wheel_above[0] + WHEEL - WHEEL_DISTANCE[
                int(BACK_RIGHT_WHEEL[to_point[0]]) - 1])
            distance_step_4 = distance_step_4 + distance_sqrt(430, COMBINATION_RING[to_point[0]] - WHEEL_DISTANCE[
                int(BACK_RIGHT_WHEEL[to_point[0]]) - 1])

            log4 = '进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]))] + '组合线环的大孔。'
            json6 = PEIXIAN_DANYUAN[str(int(to_point[0]))] + '-大孔'
            if int(to_point[0]) <= 4:
                pic_step8 = (1080, 340 + 160 * (int(to_point[0]) - 1))
            elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
                pic_step8 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340)
            elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
                pic_step8 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340 * 2)

        # 5. 再向上进入to_point组合线环#XX的小孔
        if int(to_point[0]) < 12:
            distance_step_5 = COMBINATION_RING[to_point[0]] - COMBINATION_RING[str(int(to_point[0]) + 1)]
            if int(to_point[0]) <= 4:
                pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1))  # 侧-组合线环小孔
            elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
                pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340)
            elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
                pic_step9 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340 * 2)
        elif int(to_point[0]) == 12:
            distance_step_5 = 0
            pic_step9 = (pic_step8[0], pic_step8[1])

        log5 = '再进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(int(to_point[0]))] + '组合线环的小孔。'

        json7 = PEIXIAN_DANYUAN[str(int(to_point[0]))] + '-小孔'

        # 6. 往右进入指定托盘
        distance_step_6 = 34 + 26 * (6 - int(to_point[1])) + 84 + 20.5 * (int(to_point[2]) - 1)

        log6 = '从' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[to_point[0]] + '组合线环的小孔出穿出。'
        log7 = '往右进入' + to_name + '72芯配线单元L' + PEIXIAN_DANYUAN[str(to_point[0])] + '端口(' + str(to_point[1]) + ',' + str(
            to_point[2]) + ')中。'

        if int(to_point[0]) <= 4:
            pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1))
            pic_step12 = (
                325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25)
        elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
            pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1) + 340)
            pic_step12 = (
                325 + (int(to_point[2]) - 1) * 20,
                205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335)
        elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
            pic_step10 = (250, 360 + 160 * (int(to_point[0]) - 1) + 340 * 2)
            pic_step12 = (
                325 + (int(to_point[2]) - 1) * 20,
                205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335 * 2)
        pic_step11 = (250, pic_step12[1])

        json8 = PEIXIAN_DANYUAN[to_point[0]] + '(' + to_point[1] + ',' + to_point[2] + ')'

        used_distance = distance_step_1 + distance_step_2 + distance_step_3 + distance_step_4 + \
                        distance_step_5 + distance_step_6 + 200
        print('总共需要线长：' + str(used_distance))
        cable_list = []
        for cable in CABLE_LENGTH:
            if cable > used_distance:
                cable_list.append(cable)
        cable_list.sort()
        shengyu_xianchang = cable_list[0] - used_distance
        print('剩余线长：' + str(shengyu_xianchang))

        # # 调整上下挂纤轮
        # pic_step7 = (590, 230)

        if int(to_point[0]) < 12:
            pic_step8_1 = (405, 360 + (int(BACK_RIGHT_WHEEL[str(int(to_point[0]) + 1)]) - 1) * 220)  # to_point对应右挂纤轮
        elif int(to_point[0]) == 12:
            pic_step8_1 = (405, 360 + (int(BACK_RIGHT_WHEEL[to_point[0]]) - 1) * 220)  # to_point对应右挂纤轮

        log0 = '此次跳纤计算的长度为' + str(round(used_distance / 1000, 1)) + '米，请选择一根长度为' + \
               str(int(cable_list[0] / 1000)) + '米的光纤跳线。'
        # json3 = '挂纤轮-' + str(WHEEL_DISTANCE.index(wheel_above[0]) + 1)
        json5 = ''
        if int(to_point[0]) < 12:
            pic_step8_9 = (750 + 930, 535 + (int(COMBINATION_VS_BIGLINE2[str(int(to_point[0])+1)]) - 1) * 320)  # 2正-大线环2
        elif int(to_point[0]) == 12:
            pic_step8_9 = (750 + 930, 535 + (int(COMBINATION_VS_BIGLINE2[str(int(to_point[0]))]) - 1) * 320)  # 2正-大线环2

        if int(to_point[0]) < 12:
            pic_step13_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[str(int(to_point[0]) + 1)]]) - 1) * 220)  # to_point对应大线环2对应左挂纤轮
        elif int(to_point[0]) == 12:
            pic_step13_1 = (405, 360 + (int(FRONT_LEFT_WHEEL[COMBINATION_VS_BIGLINE2[to_point[0]]]) - 1) * 220)  # to_point对应大线环2对应左挂纤轮
        if int(COMBINATION_VS_BIGLINE2[to_point[0]]) == 9:
            pic_step13_1 = (0, 0)

    log_list = [log0, log1, log2, log3, log4, log5, log6, log7, log4_1, log4_2, log4_3, log4_4, log4_5, log4_6]
    step_list = [pic_step1, pic_step2, pic_step3, pic_step4, pic_step5, pic_step6, pic_step7, pic_step8, \
                 pic_step9, pic_step10, pic_step11, pic_step12, pic_step5_1, pic_step8_1, pic_step7_1, pic_step8_8, pic_step8_9, pic_step13_1]
    json_list = [shebei_count, log_list, '1'+json1, str(shebei_count)+'-'+json2, str(shebei_count)+'-'+json3, str(shebei_count)+'-'+json4, str(shebei_count)+'-'+json5, str(shebei_count)+'-'+json6, str(shebei_count)+'-'+json7, str(shebei_count)+'-'+json8]

    print(step_list)
    print(log_list)
    print('used_distance:', used_distance)
    return step_list, log_list, json_list, int(cable_list[0] / 1000), right_to_left