from django.shortcuts import render
from django.http import HttpResponse
from .forms import TextForm
from cryptography.fernet import Fernet
from .models import Note
import random


def index(request):
    form = TextForm()
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            key = Fernet.generate_key()
            str_key = key.decode('ascii')
            f = Fernet(key)
            bin_string = form.cleaned_data['text'].encode('utf-8')
            cipher_text = f.encrypt(bin_string)
            str_cipher_text = cipher_text.decode('ascii')
            rnumber = random.randint(1000000, 9999999)
            while True:
                n = Note.objects.filter(number=rnumber).first()
                if n:
                    rnumber = random.randint(1000000, 9999999)
                    continue
                break
            cipher_note = Note(number=rnumber, text=str_cipher_text)
            link = f'{request.scheme}://{request.get_host()}/{rnumber}/{str_key}'
            cipher_note.save()
            return render(request, 'complete.html', {'link': link})
    return render(request, 'structure/index.html', {'form': form})

