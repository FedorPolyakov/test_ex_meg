from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import PostNumber
from django.urls import reverse
from .forms import PostNumberForm
from algorithm import algo, join_string_to_nums


def post_number(request):
    if request.method == "POST":
        form = PostNumberForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.number_str = algo(post.number_int)
            post.save()
            return HttpResponseRedirect(reverse('post_number'))
    else:
        form = PostNumberForm()
    # текущие данные поля ввода
    try:
        int_numb = list(PostNumber.objects.all().order_by('-created')[:1].values_list('number_int', flat=True))[0].replace(',','.')
        check_nds = list(PostNumber.objects.all().order_by('-created')[:1].values_list('nds', flat=True))[0]
        nds_percent = list(PostNumber.objects.all().order_by('-created')[:1].values_list('nds_percent', flat=True))[0]
    except IndexError:
        int_numb = ''
        check_nds = False
        nds_percent = 0

    if check_nds and nds_percent != 0:
        int_nds = str(algo(float(int_numb.replace(' ', '')) / (100 / nds_percent)))

        string_numb = f'{list(PostNumber.objects.all().order_by("-created")[:1].values_list("number_str", flat=True))[0]}' \
                      f', включая НДС {nds_percent}% в сумме {int_nds}'
    else:
        try:
            string_numb = list(PostNumber.objects.all().order_by('-created')[:1].values_list('number_str', flat=True))[0]
        except IndexError:
            string_numb = ''
    # история ввода. списки атрибутов
    history = list(PostNumber.objects.all().order_by('-created')[1:4].values_list('number_str', flat=True))
    history_int = list(PostNumber.objects.all().order_by('-created')[1:4].values_list('number_int', flat=True))
    history_nds = list(PostNumber.objects.all().order_by('-created')[1:4].values_list('nds_percent', flat=True))
    history_check_nds = list(PostNumber.objects.all().order_by('-created')[1:4].values_list('nds', flat=True))
    for i in range(3):
        try:
            if history_nds[i] != 0 and history_check_nds[i] == True:
                history_int[i] = history_int[i].replace(",", ".")
                history_int[i] = history_int[i].replace(" ", "")
                print(history_int[i])
                history[i] = "".join([history[i], f', включая НДС {history_nds[i]}% в сумме '
                                                  f'{str(algo(float(history_int[i]) / (100 / history_nds[i])))}'])
        except IndexError:
            pass
    content = {
        'form': form,
        'string_numb': string_numb,
        'history': history,
    }

    return render(request, 'mainapp/index.html', content)
