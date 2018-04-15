# coding:utf-8

def pagination(current_page, total_num, single_page_num=10, show_page_num=5):

    total_page = total_num // single_page_num
    if total_num % single_page_num:
        total_page += 1

    current_page=int(current_page)

    start = single_page_num * (current_page - 1)
    end = start + single_page_num

    tmp_page = current_page - 1
    page_li = []

    # 往前找
    while tmp_page > 0:
        if tmp_page % show_page_num:
            page_li.append(tmp_page)
        else:
            # 遇到能被显示页页面数整除的直接退出循环
            break
        tmp_page -= 1


    tmp_page = current_page
    # 往后找
    while tmp_page <= total_page:
        # 后面能被整除的也要加进列表
        # 直接先加进列表，不管判断是否反正都要加进去的
        page_li.append(tmp_page)
        if tmp_page % show_page_num:
            tmp_page += 1
        else:
            break

    page_li.sort()

    show_end_num=total_page-(total_page%single_page_num)

    return (total_page,start,end,page_li,show_end_num)

