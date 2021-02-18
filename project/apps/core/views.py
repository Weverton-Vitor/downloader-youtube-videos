from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from project.apps.core.forms import DownloaderYoutubeForm
from pytube import YouTube
import math


# Create your views here.


class DownloaderYoutube:
    """Classe para baixar videos do YouTube"""

    def __init__(self, link=''):
        self.title = None
        self.thumbnail = None
        self.link = link
        self.resolution = None
        self.streams = None

        self.search()

    def search(self, link=''):
        """ Faz a busca de um videos pelo link, usando a propriedade link do objeto ou o parâmetro do método"""
        video_link = self.link if self.link else link
        if not video_link:
            raise Exception('No link to search')

        yt = YouTube(video_link, on_progress_callback=self.progress, on_complete_callback=self.downloaded)

        self.title = yt.title
        self.thumbnail = yt.thumbnail_url
        self.streams = yt.streams

    def download(self, resolution):
        """ Executa o download do video"""
        stream = self.streams.filter(res=resolution).first()
        download_info = stream.download('./')

        if download_info:
            return download_info

        return False

    def get_all_resolutions(self):
        """ Retorna todas a resoluções que estão disponíveis """

        def sort_resolutions(resolutions):
            """ Ordena as resoluções em ordem crescente e remove itens repetidos """

            # Removendo o último caractere e convertento para inteiro cada item da lista
            sorted_resolutions = [int(resolution[:len(resolution) - 1]) for resolution in resolutions]

            # Removendo itens repetidos e ordenando
            sorted_resolutions = set(sorted_resolutions)
            sorted_resolutions = list(sorted_resolutions)
            sorted_resolutions.sort()

            # Adicionando o último caractere e convertente para string
            sorted_resolutions = [str(resolution) + 'p' for resolution in sorted_resolutions]

            return sorted_resolutions

        resolutions = [stream.resolution for stream in self.streams if stream.resolution != None]

        return sort_resolutions(resolutions)

    @staticmethod
    def progress(stream, chunk, bytes_remaining):
        print(math.ceil((stream.filesize - bytes_remaining) / (1024 * 1024)),
              stream.filesize / (1024 * 1024))  # 100Mb - 80Mb = 20Mb

    @staticmethod
    def downloaded(stream, file_path):
        print('completo')

    def __str__(self):
        return f'{self.title}'

class YoutubeForm(FormView):
    form_class = DownloaderYoutubeForm
    template_name = 'index.html'    
    success_url = reverse_lazy('core:index')
    video = None
    
    def form_valid(self, form):
        self.video = DownloaderYoutube(form.cleaned_data['link'])                    
        return render(self.request, self.template_name, context=self.get_context_data())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.video:
            context['title'] = self.video.title
            context['thumbnail_link'] = self.video.thumbnail
            context['resolutions'] = self.video.get_all_resolutions()
            
        
        return context
        
        
        


# 'https://www.youtube.com/watch?v=1szfg-VovbM&list=PLJbfCnxJZt8YKoBC_wigw0BZOlDw_vFKS&index=2'
