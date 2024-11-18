from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from store.forms import CreateStoreForm
from store.models import Store


class CreateStoreView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateStoreForm()
        return render(request, "store/create_store.html", {"form": form})

    def post(self, request):
        form = CreateStoreForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("stores")

        return render(request, "store/create_store.html", {"form": form})


class StoreView(LoginRequiredMixin, TemplateView):
    template_name = "store/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stores"] = Store.objects.all()
        context["title"] = "Stores"
        return context
    
class UserStoresView(LoginRequiredMixin, TemplateView):
    template_name = "store/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stores"] = Store.objects.filter(owner=self.request.user)
        context["title"] = "My stores"
        return context

class StoreDetailView(LoginRequiredMixin, TemplateView):
    template_name = "store/store_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["store"] = Store.objects.get(id=self.kwargs.get("store_id"))
        return context
