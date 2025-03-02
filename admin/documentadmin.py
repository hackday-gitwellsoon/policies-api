from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField
from wtforms.widgets import TextArea

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class DocumentAdmin(ModelView):
    column_list = ('id', 'title', 'description', 'hospital')
    form_columns = ('title', 'description', 'hospital')

    extra_js = ['//cdn.ckeditor.com/4.22.1/standard/ckeditor.js']
    form_overrides={
        'description':CKTextAreaField
    }
