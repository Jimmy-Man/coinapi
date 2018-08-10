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
    #return HttpResponse('Hello world')

    ## check login
    admin_id = request.session.get('admin_id',default=0)
    if admin_id <1:
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