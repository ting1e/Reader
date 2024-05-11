from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import os

def handle_local_book(request,url):
    if str(url)[-4:]!='.txt':
        return
    file_name = os.path.basename(url)
    book = Book(book_url = url)
    book.name = file_name
    if request.user.is_authenticated:
        book.uploader = request.user.id
    book.save()

    charset = 'utf-8'
    with open(url,'rb') as f:
        charset = chardet.detect(f.read()[:5000])["encoding"] 
    book.charset = charset

    with open(url,'r',conding=charset) as f:
        data = f.read()
        conding = chardet.detect(data)["encoding"] 
        #     pat = u'第[一二三四五六七八九十零百千0123456789]+[集章节卷]'
        pat = u'(?<=[　\s])(?:序章|序言|卷首语|扉页|楔子|正文(?!完|结)|终章|后记|尾声|番外|第?\s{0,4}[\d〇零一二两三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟]+?\s{0,4}(?:章|节(?!课)|卷|集(?![合和])|部(?![分赛游])|篇(?!张))).{0,30}$'
        pattern = re.compile(pat)
        match = pattern.findall(file)
        # print(file[:200])
        # print(match)
        st = file.find(match[0],0)
        
        intro = '介绍' if st > 5000 else '正文'
        content = Content(content = file[0:st])
        content.save()
        chapter = Chapter(title=intro,book_id = book.id,content_id = content.id,words = st)
        chapter.save()
        book.first_chapter = chapter.id
        book.save()
        for i in range(1,len(match)):
            en = file.find(match[i],st)       
            content = Content(content = file[st:en])
            content.save()
            tt = file[st:file.find('\n',st)] if file.find('\n',st) < st + 20 else match[i-1]
            chapter = Chapter(title=tt, book_id = book.id, content_id = content.id, words = en - st)
            chapter.save()
            st = en

            if i == len(match) -1 :
                content = Content(content = file[en:])
                content.save()
                tt = file[st:file.find('\n',st)] if file.find('\n',st) < st + 20 else match[i]
                chapter = Chapter(title=tt, book_id = book.id, content_id = content.id, words = len(file) - en)
                chapter.save()
 
    f = open(url,r)
    data = f.read()
    print(chardet.detect(data))


# def handle_uploaded_file(request):
#     f = request.FILES['file']
#     if str(f)[-4:]!='.txt':
#         return
#     file = ''
    
#     for chunk in f.chunks():
#         if 'conding' not in locals().keys():
#             conding = chardet.detect(chunk)["encoding"] 
#         file += chunk.decode(conding,'ignore')

#     book = Book(title = str(f)[:-4])
#     if request.user.is_authenticated:
#         book.uploader = request.user.id
#     book.save()

#     pat = u'第[一二三四五六七八九十零百千0123456789]+[集章节卷]'
#     # pat = u'(?<=[　\s])(?:序章|序言|卷首语|扉页|楔子|正文(?!完|结)|终章|后记|尾声|番外|第?\s{0,4}[\d〇零一二两三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟]+?\s{0,4}(?:章|节(?!课)|卷|集(?![合和])|部(?![分赛游])|篇(?!张))).{0,30}$'
#     pattern = re.compile(pat)
#     match = pattern.findall(file)
#     # print(file[:200])
#     # print(match)
#     st = file.find(match[0],0)
    
#     intro = '介绍' if st > 5000 else '正文'
#     content = Content(content = file[0:st])
#     content.save()
#     chapter = Chapter(title=intro,book_id = book.id,content_id = content.id,words = st)
#     chapter.save()
#     book.first_chapter = chapter.id
#     book.save()
#     for i in range(1,len(match)):
#         en = file.find(match[i],st)       
#         content = Content(content = file[st:en])
#         content.save()
#         tt = file[st:file.find('\n',st)] if file.find('\n',st) < st + 20 else match[i-1]
#         chapter = Chapter(title=tt, book_id = book.id, content_id = content.id, words = en - st)
#         chapter.save()
#         st = en

#         if i == len(match) -1 :
#             content = Content(content = file[en:])
#             content.save()
#             tt = file[st:file.find('\n',st)] if file.find('\n',st) < st + 20 else match[i]
#             chapter = Chapter(title=tt, book_id = book.id, content_id = content.id, words = len(file) - en)
#             chapter.save()