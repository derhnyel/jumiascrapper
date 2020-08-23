
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs4s
from rest_framework.decorators import (api_view, permission_classes)
from django.views.decorators.http import require_GET
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as RR
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST)
from json import loads
from django.http import JsonResponse
from uuid import uuid4
import os
import threading


@require_GET
def index(request):
    return render(request, 'product/index.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def get_link(request):
    try:
        urls = request.POST.get('url')
        url = load_url(urls) 
        if url != None:
            p = scrapper(url)
            return RR(data={'Results': p, 'message': 'SuccessFul'})
        else:
            raise Exception('Invalid URL!')
    except Exception as e:
        return RR(data={'success': False, 'message': str(e)}, status=HTTP_400_BAD_REQUEST)


def load_url(url):
    url = loads(url)
    return url


def scrapper(link):
    response = requests.get(link)
    soup = bs4s(response.text)
    images_link = []
    product_name = soup.select('h1')[0].getText()
    image_soup = soup.select('#imgs.sldr._img._prod.-rad4.-oh.-mbs a.itm')
    product_price_soup = soup.select(
        'div.-hr.-pvs.-mtxs span.-b.-ltr.-tal.-fs24')
    for i in range(0, len(image_soup)):
        images_link.append(image_soup[i].get('href'))
    product_description = soup.select(
        'div.markup.-mhm.-pvl.-oxa.-sc ')[0].getText()
    product_price = [i.strip()
                     for i in product_price_soup[0].getText().split('¦')]               
    result = {'product_name': product_name, 'product_price': product_price,
              'product_description': product_description, 'images_link': images_link}
    return result
