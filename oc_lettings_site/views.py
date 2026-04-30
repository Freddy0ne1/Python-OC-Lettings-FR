from django.shortcuts import render


def index(request):
    """ Vue de la page d'accueil """
    return render(request, 'index.html')

# def lettings_index(request):
#     """ Vue de la liste des locations """
#     lettings_list = Letting.objects.all()
#     context = {'lettings_list': lettings_list}
#     return render(request, 'lettings_index.html', context)


# def letting(request, letting_id):
#     """ Vue de la page d'une location """
#     letting = Letting.objects.get(id=letting_id)
#     context = {
#         'title': letting.title,
#         'address': letting.address,
#     }
#     return render(request, 'letting.html', context)

# def profiles_index(request):
#     """ Vue de la liste des profils """
#     profiles_list = Profile.objects.all()
#     context = {'profiles_list': profiles_list}
#     return render(request, 'profiles_index.html', context)

# def profile(request, username):
#     """ Vue de la page d'un profil """
#     profile = Profile.objects.get(user__username=username)
#     context = {'profile': profile}
#     return render(request, 'profile.html', context)
