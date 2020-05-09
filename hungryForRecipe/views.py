from django.views.generic import TemplateView

class TestPage(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['loggedInUser'] = self.request.user
        return context

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name='index.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['loggedInUser'] = self.request.user
        return context
