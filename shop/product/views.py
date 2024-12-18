from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from product.forms import CreateProductForm, EditProductForm
from product.models import Product
from store.models import Store


class ProductListView(LoginRequiredMixin, TemplateView):
    template_name = "product/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        context["title"] = "Products"
        return context


class DetailProductView(LoginRequiredMixin, TemplateView):
    def get(self, request, *arg, **kwargs):
        product = get_object_or_404(Product, id=kwargs["product_id"])
        return render(request, "product/product_detail.html", {"product": product})


class CreateProductView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateProductForm()
        return render(request, "product/create_product.html", {"form": form})

    def post(self, request):
        store = get_object_or_404(
            Store, id=request.GET.get("store_id"), owner=self.request.user.id
        )  # Or however you identify the shop
        form = CreateProductForm(request.POST, request.FILES)
        print(form.is_valid(), vars(form))
        if form.is_valid():
            form.save(store=store.id)
            return redirect("products")

        return render(request, "product/create_product.html", {"form": form})


class EditProductView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        product = get_object_or_404(Product, id=kwargs["product_id"])
        if request.user.id != product.store.owner_id:
            return redirect("products")

        form = CreateProductForm(instance=product)
        return render(request, "product/product_edit.html", {"form": form})

    def post(self, request, **kwargs):
        product = get_object_or_404(Product, id=kwargs["product_id"])
        if request.user.id != product.store.owner_id:
            return redirect("products")
        if "delete" in request.POST:
            return self.delete(request, **kwargs)

        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return render(request, "product/product_detail.html", {"product": product})
        return render(request, "product/product_edit.html", {"form": form})

    def delete(self, request, **kwargs):
        product = get_object_or_404(Product, id=kwargs["product_id"])
        if request.user.id != product.store.owner_id:
            return render(request, "product/product_detail.html", {"product": product})

        product.delete()
        return redirect("products")
