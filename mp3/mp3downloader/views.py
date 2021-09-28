from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.contrib import messages
import pytube
import os


# Create your views here.
def home(request):
    return render(request, 'mp3_home.html')


def about(request):
    return render(request, 'about.html')


def copy(request):
    return render(request, 'copyright.html')


def dmca(request):
    return render(request, 'dmca.html')


def faqs(request):
    return render(request, 'faqs.html')


def contact(request):
    return render(request, 'contactus.html')


def privacy(request):
    return render(request, 'privacypolicy.html')


def terms(request):
    return render(request, 'termsofservice.html')


def msg(request, message):
    return render(request, 'download.html', {'msg': message})


def mp3_download(request):
    global link
    link = str(request.POST.get('link'))
    # print(link)
    yt = pytube.YouTube(link)
    dis = {}
    ls = []

    audio = yt.streams.filter(only_audio="True")

    for j in audio:
        dis['res'] = j.abr
        dis['frm'] = 'mp3'
        dis['size'] = str(round((j.filesize) / 1048576, 2)) + 'MB'

        ls.append(dis.copy())

    embed_link = link.replace("watch?v=", "embed/")

    title = yt.title + '  mp3 Download Here'
    data = {
        'title': title,
        'obj': ls
    }
    dump = json.dumps(data)
    # return render(request, 'mp3_video.html', {'embd': embed_link, 'obj': ls})
    return HttpResponse(dump, content_type='application/json')


def mp3_upload(request):
    global link
    url = link

    obj = pytube.YouTube(url)
    res = str(request.GET.get('resolution'))

    # f = str(request.POST.get('format')).split("/")

    # fromate = f[0]
    # frm = f[1]

    audio = './download/audio'
    msg = ''

    # if fromate == 'audio':
    if obj:
        da = obj.streams.filter(abr=res).first()
        # out_file = da.download(output_path=audio)
        out_file = da.download()
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        msg = obj.title + '  Convert into mp3 Audio Download Successfully'
        # print(msg)
        data = {
            'status': 'audio',
            'msg': msg
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')

    else:
        msg = 'Check your Internet connection or Enter Valid Link '
        # print(msg)
        # data = 'fail'
        # return 'fail'

        data = {
            'status': 'Fail',
            'msg': msg
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')
