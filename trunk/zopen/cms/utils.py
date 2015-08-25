# -*- encoding: utf-8 -*-

import sys
import time
import pytz
from datetime import datetime
from DateTime import DateTime
from interfaces import IFRSFolder, IFRSDocument


def getDisplayTime(input_time, show_mode='localdate'):
    """ 人性化的时间显示: (支持时区转换)

    time 是datetime类型，或者timestampe的服点数，
    最后的show_mode是如下:

    - localdate: 直接转换为本地时间显示，到天
    - localdatetime: 直接转换为本地时间显示，到 年月日时分
    - localtime: 直接转换为本地时间显示，到 时分
    - deadline: 期限，和当前时间的比较天数差别，这个时候返回2个值的 ('late', '12天前')
    - humandate: 人可阅读的天，今天、明天、后天、昨天、前天，或者具体年月日 ('today', '今天')
    """
    if not input_time:
        return ''
    
    utc = pytz.utc
    localzone = pytz.timezone('Asia/Hong_Kong')
    input_time = input_time.replace(tzinfo=utc)
    input_time = input_time.astimezone(localzone)

    today = DateTime()
    time_date = DateTime(input_time.year, input_time.month, input_time.day)
    year,month,day = today.year(), today.month(), today.day()
    today_start = DateTime(year, month, day)

    to_date = today_start - time_date

    # 期限任务的期限
    if show_mode == 'localdate':
        return input_time.strftime('%Y-%m-%d')
    elif show_mode == 'localdatetime':
        return input_time.strftime('%Y-%m-%d %H:%M')
    elif show_mode == 'localtime':
        return input_time.strftime('%H:%M')
    elif show_mode == 'deadline':
        if to_date == 0:
            return ('Today', '今天')
        elif to_date < 0:
            if to_date == -1:
                return (None, '明天')
            elif to_date == -2:
                return (None, '后天')
            else:
                return (None, str(int(-to_date))+'天')
        elif to_date > 0:
            if to_date == 1:
                return ('late', '昨天')
            elif to_date == 2:
                return ('late', '前天')
            else:
                return ('late', str(int(to_date))+'天前')
    elif show_mode == 'humandate':
        if to_date == 0:
            return ('Today', '今天')
        elif to_date < 0:
            if to_date == -1:
                return (None, '明天')
            elif to_date == -2:
                return (None, '后天')
            else:
                return (None, input_time.strftime('%Y-%m-%d'))
        elif to_date > 0:
            if to_date == 1:
                return ('late', '昨天')
            elif to_date == 2:
                return ('late', '前天')
            else:
                return ('late', input_time.strftime('%Y-%m-%d'))

def get_sub_time_paths(folder, root_vpath):
    """ 迭代查找整个子目录，找出所有的子路径 """
    result = []
    for obj in folder.values(True, False):
        dc = obj.metadata.get('dublin', {})
        if IFRSFolder.providedBy(obj):
            result.extend(get_sub_time_paths(obj, root_vpath))
        elif IFRSDocument.providedBy(obj):
            result.append((dc.get('created', ''),
                           obj.vpath.replace(root_vpath + '/', ''),
                          ))
    return result

