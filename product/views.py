
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs4s
from rest_framework.decorators import (api_view,permission_classes)
from django.views.decorators.http import require_GET
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as RR
from rest_framework.status import (HTTP_200_OK,HTTP_400_BAD_REQUEST)
from json import loads
from django.http import JsonResponse
from uuid import uuid4
import os
import threading

#@require_GET
def index(request):
    #rt = get_link(request)
    return render(request,'product/index.html',get_link(request))

#@api_view(['POST'])
#@permission_classes([AllowAny])




def get_link(request) :
    if request.method == 'POST':
        #url = request.POST.get('url')
        link = request.POST.get('textfield',None)
        result = scrapper(link)
        #scrapper(url)
        return result
        
        

def scrapper(link):
    response = requests.get(link)
    raise_error(response)
    soup = bs4s(response.text)
    images_link = []

    product_name = soup.select('h1')[0].getText()


    image_soup = soup.select('#imgs.sldr._img._prod.-rad4.-oh.-mbs a.itm')

    product_price_soup = soup.select('div.-hr.-pvs.-mtxs span.-b.-ltr.-tal.-fs24')

    for i in range(0, len(image_soup)):
        images_link.append(image_soup[i].get('href'))

    product_description = soup.select('div.markup.-mhm.-pvl.-oxa.-sc ')[0].getText()


    product_price = [i.strip() for i in product_price_soup[0].getText().split('¦')]

    #parse_json(list)
    result = [product_name, product_price, product_description, images_link]
    [print (i) for i in result]
    return {'result':result}
    





def raise_error(response):
    try:
        response.raise_for_status()
    except Exception as exc:
        return 'There was a problem %s' % (exc)



    
