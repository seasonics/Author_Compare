from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaulttags import csrf_token
import prepare
import cPickle as pickle
import logging

logger = logging.getLogger(__name__)
from author_compare.models import Author

# Create your views here.


def run_calulations(a1,a2,user_text):
    total = float(0)
    i = 0
    while i < 8:
        if i == 0:
            a1_dic = pickle.load( open( a1.dic_stopwords.path, "rb" ) )
            a2_dic = pickle.load( open( a2.dic_stopwords.path, "rb" ) )
            total += float(prepare.runUnknown(a1_dic, a2_dic,user_text, i))
        if i == 1:
            a1_dic = pickle.load( open( a1.dic_clean.path, "rb" ) )
            a2_dic = pickle.load( open( a2.dic_clean.path, "rb" ) )
            total += float(prepare.runUnknown(a1_dic, a2_dic,user_text, i))
        if i == 2:
            a1_dic = pickle.load( open( a1.avg_words.path, "rb" ) )
            a2_dic = pickle.load( open( a2.avg_words.path, "rb" ) )
            total += float(prepare.runUnknown(a1_dic, a2_dic,user_text, i))
        if i == 3:
            a1_dic = pickle.load( open( a1.var_words.path, "rb" ) )
            a2_dic = pickle.load( open( a2.var_words.path, "rb" ) )
            total += float(prepare.runUnknown(a1_dic, a2_dic,user_text, i))
        if i == 4:
            a1_dic = pickle.load( open( a1.var_sen.path, "rb" ) )
            a2_dic = pickle.load( open( a2.var_sen.path, "rb" ) )
            total += float(prepare.runUnknown(a1_dic, a2_dic,user_text, i))
        if i == 5:
            a1_dic = pickle.load( open( a1.bigram.path, "rb" ) )
            a2_dic = pickle.load( open( a2.bigram.path, "rb" ) )
            total += float(prepare.runUnknown(a1_dic, a2_dic,user_text, i))
        if i == 6:
            a1_dic = pickle.load( open( a1.bigram_clean.path, "rb" ) )
            a2_dic = pickle.load( open( a2.bigram_clean.path, "rb" ) )
            total += float(prepare.runUnknown(a1_dic, a2_dic,user_text, i))
        if i == 7:
            a1_dic = pickle.load( open( a1.trigram_clean.path, "rb" ) )
            a2_dic = pickle.load( open( a2.trigram_clean.path, "rb" ) )
            total += float(prepare.runUnknown(a1_dic, a2_dic,user_text, i))
        i +=1
    return total


def index(request):
    author_list = Author.objects.all()
    if request.method == 'POST':
        if request.POST.get('all'):
            user_text = request.POST.get('user_text')
            highest = author_list[0]
            for x in range(1,len(author_list)):
                total = run_calulations(author_list[0],author_list[x],user_text)
                if total >= 8:
                    continue
                else:
                    highest = author_list[x]
            result_author = highest.author
        else:
            author_1 = request.POST.get('author_1')
            author_2 = request.POST.get('author_2')
            user_text = request.POST.get('user_text')
            a1 = Author.objects.get(author=author_1)
            a2 = Author.objects.get(author=author_2)
            total = run_calulations(a1,a2,user_text)
            if total >= 8:
                result_author = author_1
            else:
                result_author = author_2
        context = {'author_list': author_list,'result_author': result_author}
    else:
        context = {'author_list': author_list}
    return render(request, 'author_compare/index.html', context)
def results(request):
    return HttpResponse("You're looking at the results of")
