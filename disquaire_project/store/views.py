# from django.shortcuts import render
from django.http import HttpResponse

from .models import Album, Artist, Contact, Booking

def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    return HttpResponse(message)

def listing(request):
    albums = Album.objects.filter(available=True)
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    message = """<ul>{}</ul>""".format("\n".join(formatted_albums))

    return HttpResponse(message)

def detail(request, album_id):
    album = Album.objects.get(pk=album_id)
    artists = " ".join([artist.name for artist in album.artists.all()])
    message = "Le nom de l'album est {} et a été écrit par {}".format(album.title, artists)

    return HttpResponse(message)

def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query) #query contained in title

        if not albums.exists(): # True if elt in the query set
            albums = Album.objects.filter(artists__name__icontains=query)

        if not albums.exists():
            message = "misère rien trouvé !"
        else:
            albums = ["<li>{}</li>".format(album.title) for album in albums]
            message = """
                Nous avons trouvé les albums correspondant à votre requête ! Les voici :
                <ul>
                    {}
                </ul>
            """.format("</li><li>".join(albums))

    return HttpResponse(message)
