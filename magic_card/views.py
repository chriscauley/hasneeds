from django.http import HttpResponse

from metadata_parser import MetadataParser
import requests

def get_url(url):
  if not url.startswith("http"):
    url = "http://" + url
  headers = {'User-Agent':"Mozilla/5.0 (X11; CrOS x86_64 8872.73.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36"}
  head = requests.head(url,headers=headers,verify=False)
  if head.status_code/100 == 3: # 301,302
    return get_url(head.headers['Location'])
  response = requests.get(url,headers=headers,verify=False)
  return MetadataParser(html=response.text).metadata, url

def load_meta_data(request):
  url = request.GET.get("url",None)
  if not url:
    # nothing, shouldn't have been submitted here.
    return JsonResponse({})
  try:  
    metadata,url = get_url(url)
  except Exception, e:
    return JsonResponse({'error': "Unable to find that url. Exception given: \"%s\""%e},status=400)
  return JsonResponse({"result": metadata})
