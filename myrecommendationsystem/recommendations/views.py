from .forms import UserUpdateForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from .forms import UserCreationForm
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
import json
from recommend_service.RNN_recommend.recommend import get_RNN_recommend
from django.http import JsonResponse

def index(request):
    # 你可以在这里添加任何你需要传递给模板的上下文变量
    context = {}
    return render(request, 'index.html', context)

class UserRegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'get':
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('index')  # 或者你想要重定向的地方

    def get_object(self):
        return self.request.user

@csrf_exempt
def generate_recommendations(request):
    if request.method == 'POST':
        print(request.body)
        # 从请求中获取用户的历史歌曲
        song_history = json.loads(request.body)['song_history']
        print(song_history)

        # 假设 get_recommended_songs 是你的推荐算法函数
        recommended_songs = get_RNN_recommend(user_sequence=[int(song) for song in song_history], num_recommendations=5)
        print(recommended_songs)

        # 将推荐歌曲转换为JSON格式的数据
        recommended_songs_data = [
            {'title': song['title'], 'artist': song['artist'], 'rating': song['rating'], 'url': song['url']}
            for song in recommended_songs
        ]

        return JsonResponse({'recommended_songs': recommended_songs_data})

    return JsonResponse({'error': 'Invalid request'}, status=400)