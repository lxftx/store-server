class TitleMixin(object):
    """
    Миксин который собирает информацию о заголовках на страницах
    """
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
