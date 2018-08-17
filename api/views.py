from django.shortcuts import render
##
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse

from api.models import domain

#from configuration import *

## auth user
from django.contrib.auth import authenticate

##
from django.utils.translation import gettext

from data_api.houbiapi.huobiapi import huobiapi
import datetime
import time

# Create your views here.

#PLATFORM_API_LIAT = ['HUOBI','BTN','']
PLATFORM_API_LIAT = {'HUOBI':'火币','BTN':'币安'}
TIME_STATE = ['15min','30min','1day','5day']

COIN_LIST = {}
COIN_LIST['HUOBI'] = {'USDT':['BTC/USDT','BCH/USDT','ECH/USDT','ETC/USDT','LTC/USDT','EOS/USDT','ADA/USDT','XRP/USDT','OMG/USDT','IOTA/USDT','ZEC/USDT','DASH/USDT','STEEM/USDT','HB1O/USDT','PAI/USDT','HT/USDT','IOST/USDT','ONT/USDT','ZIL/USDT','BTM/USDT','TRX/USDT','ELF/USDT','DTA/USDT','SOC/USDT','ELA/USDT','VEN/USDT','RUFF/USDT','THETA/USDT','NAS/USDT','CVC/USDT','QTU/USDT','ACT/USDT','BIX/USDT','LET/USDT','WICC/USDT','NEO/USDT','ITC/USDT','HSR/USDT','CTXC/USDT','BTS/USDT','OCN/USDT','CMT/USDT','MDS/USDT','STORJ/USDT','SNT/USDT','SMT/USDT','GNT/USDT','XEM/USDT'],
                      'BTC':['BCH/BTC','ETH/BTC','LTC/BTC','ETC/BTC','EOS/BTC','XRP/BTC','ADA/BTC','IOTA/BTC','OMG/BTC','ZEC/BTC','DASH/BTC','STEEM/BTC','XMR/BTC','PAI/BTC','HIT/BTC','BOX/BTC','HT/BTC','ELA/BTC','IOST/BTC','ONT/BTC','EDU/BTC','BFT/BTC','TRX/BTC','DTA/BTC','PAY/BTC','ZIL/BTC','ACT/BTC','POLY/BTC','GAS/BTC','CVC/BTC','OCN/BTC','GNX/BTC','MTN/BTC','BLZ/BTC','GXS/BTC','SOC/BTC','NAS/BTC','THETA/BTC','BTM/BTC','VEN/BTC','LBA/BTC','BIX/BTC','ELF/BTC','XVG/BTC','NEO/BTC','YEE/BTC','MANA/BTC','MEET/BTC','ABT/BTC','SWFTC/BTC','KAN/BTC','QTUM/BTC','STK/BTC','ITC/BTC','RUFF/BTC','WAX/BTC','WICC/BTC','LET/BTC','EKO/BTC','HSR/BTC','ICX/BTC','XLM/BTC','ZRX/BTC','TNB/BTC','LINK/BTC','MTX/BTC','CMT/BTC','CTXC/BTC','AIDOC/BTC','DBC/BTC','WAN/BTC','PROPY/BTC','MDS/BTC','ZLA/BTC','BTS/BTC','CHAT/BTC','STORJ/BTC','BAT/BTC','DCR/BTC','DGB/BTC','TOPC/BTC','QASH/BTC','XEM/BTC','SNT/BTC','MCO/BTC','SRN/BTC','SMT/BTC','APPC/BTC','WPR/BTC','GNT/BTC','KNC/BTC','WTC/BTC','RCN/BTC','QUN/BTC','UTK/BTC','SALT/BTC','AST/BTC','SNC/BTC','ENG/BTC','TNT/BTC','POWR/BTC','LUN/BTC','DGD/BTC','DAT/BTC','RDN/BTC','ADX/BTC','REQ/BTC','QSP/BTC','RPX/BTC','WAVES/BTC','LSK/BTC','OST/BTC','MTL/BTC','EVX/BTC','BCD/BTC','BCX/BTC','SBTC/BTC','BIFI/BTC','BTG/BTC'],
                      'ETH':['EOS/ETH','ADA/ETH','IOTA/ETH','OMG/ETH','STEEM/ETH','XMR/ETH','PAI/ETH','HIT/ETH','HT/ETH','BOX/ETH','ONT/ETH','IOST/ETH','ELA/ETH','EDU/ETH','ZIL/ETH','TRX/ETH','GXS/ETH','LBA/ETH','BLZ/ETH','BIX/ETH','NAS/ETH','BTM/ETH','DTA/ETH','ACT/ETH','POLY/ETH','VEN/ETH','PAY/ETH','RUFF/ETH','ELF/ETH','GNX/ETH','SOC/ETH','ABT/ETH','OCN/ETH','CVC/ETH','MTN/ETH','THETA/ETH','BFT/ETH','CTXC/ETH','HSR/ETH','YEE/ETH','CMT/ETH','LET/ETH','ITC/ETH','GAS/ETH','KAN/ETH','QTUM/ETH','WICC/ETH','DBC/ETH','XVG/ETH','SWFTC/ETH','EKO/ETH','TNB/ETH','LINK/ETH','MANA/ETH','STK/ETH','ZLA/ETH','MTX/ETH','AIDOC/ETH','ICX/ETH','ZRX/ETH','WAX/ETH','BTS/ETH','WAN/ETH','MEET/ETH','SRN/ETH','TOPC/ETH','MDS/ETH','QASH/ETH','SMT/ETH','XLM/ETH','CHAT/ETH','KNC/ETH','RCN/ETH','PROPY/ETH','APPC/ETH','QUN/ETH','BAT/ETH','DCR/ETH','DGB/ETH','AST/ETH','GNT/ETH','WTC/ETH','WPR/ETH','ADX/ETH','SALT/ETH','DAT/ETH','ENG/ETH','UTK/ETH','QSP/ETH','TNT/ETH','RDN/ETH','SNC/ETH','POWR/ETH','OST/ETH','MCO/ETH','DGD/ETH','REQ/ETH','LUN/ETH','LSK/ETH','WAVES/ETH','EVX/ETH'],
                      'HT':['EOS/HT','ETC/HT','XRP/HT','BCH/HT','LTC/HT','DASH/HT','IOST/HT']
                    }
COIN_LIST['BTN']   = {}


def index(request):
    ## check login
    admin_id = request.session.get('admin_id',default=0)
    if admin_id < 1:
        return HttpResponseRedirect('/api/login')

    content = {}
    text = {}
    text['title'] = gettext('行情分析')
    text['subtitle'] = gettext('周期统计')
    content['user_name'] = 'Jimmy'
    content['api_list']  = PLATFORM_API_LIAT;
    content['time_state'] = TIME_STATE;
    content['text'] = text
    return render(request,'api/index.html',content)

def ajax(request):
    var_return = {'status':0}
    get_type = request.GET['type']
    if get_type == 'get_coin':
        exchange_type = request.GET['exchange_type']
        var_list = COIN_LIST[exchange_type]
        var_return['data'] = var_list
        var_return['status'] = 1;
    elif get_type == 'get_symbol':
        exchange_type = request.GET['exchange_type']
        coin_name     = request.GET['coin_name']
        var_list = COIN_LIST[exchange_type][coin_name]
        var_return['data'] = var_list
        var_return['status'] = 1;
    elif get_type == 'analysis':
        cycle = request.GET['cycle']
        exchange_type = request.GET['exchange_type']
        coin_name     = request.GET['coin_name']
        symbol        = request.GET['symbol']
        start         = request.GET['start']
        #end           = request.GET['end']
        end           = time.localtime(time.time())
        symbol = symbol.lower().replace('/','')

        ## math times
        start_time = datetime.datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
        #end_time   = datetime.datetime.strptime(datetime.time(),"%Y-%m-%d %H:%M:%S")
        #timeArray = time.localtime(time.time())
        end        = time.strftime('%Y-%m-%d %H:%M:%S',end)
        end_time   = datetime.datetime.strptime(end,"%Y-%m-%d %H:%M:%S")
        #return HttpResponse(end_time)
        middle = end_time - start_time
        #return HttpResponse(middle.days)
        limit = 150
        if cycle == '15min':
            limit = middle.seconds%900
        elif cycle == '1day':
            limit =  int(middle.days)
            #return HttpResponse(limit)
        if limit < 2:limit =2
            
        coin_api =  huobiapi('06e39fd5-290a27b3-c5bb0ff0-40e2c','67f2faa5-9507f01e-b14aa6c3-ca24a')
        ## get kline
        kline = coin_api.get_kline(symbol,cycle,limit)
        if kline['status'] =='ok':
            kl = kline['data']
            for item in kline['data']:
                # K线id  
                var_id      = item['id']
                # 开盘价
                var_open    = item['open']
                # 收盘价,当K线为最晚的一根时，是最新成交价
                var_close   = item['close']
                # 最低价
                var_low     = item['low']
                # 最高价
                var_high    = item['high']
                # 成交量
                var_amount  = item['amount']
                # 成交笔数
                var_count   = item['count']
                # 成交额, 即 sum(每一笔成交价 * 该笔的成交量)
                var_vol     = item['vol']
            return JsonResponse(kline)
            ai = (kl[0]['close'] - kl[len(kline)-1]['close'])/kl[0]['close']
                
            #return HttpResponse(ret)
            var_return['status'] = 1;
            var_return['data'] = {'ai':ai}
            #var_return['data']['bb'] = ai
        else:
            var_return['error'] = '获取数据失败'
        return JsonResponse(var_return)
                
    return JsonResponse(var_return)
    

def login(request):
    # save data
    #domain1 =  domain(domain_name = 'baidu.com',domain_address='baidu.com',data_add=1382205588)
    #domain1.save()
    ## end save data

    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['password']
        var_result = {}
        var_result['status'] = 0
        auth =  authenticate(username=username, password=password)
        if not auth is None:
            var_result['status'] = 1
            request.session['admin_id'] = 1
        else:
            var_result['error'] = 'username or password is wrong!'    
        return JsonResponse(var_result)
        #return JsonResponse(var_result,safe=False)
    else:        
        content = {}        
        return render(request,'api/login.html',content)


    # domain_list = domain.objects.all()
    # domain_info = domain.objects.get(pk=1)

    # #print(var_list)
    # content = {}
    # content['domain_list'] = domain_list
    # content['domain_info'] = domain_info
    # return render(request,'api/login.html',content)

def logout(request):
    try:
        del request.session['admin_id']
    except KeyError:
        pass
    return HttpResponseRedirect('/api/login')