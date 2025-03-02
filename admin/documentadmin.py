from flask_admin.contrib.sqla import ModelView

class DocumentAdmin(ModelView):
    column_list = ('id', 'title', 'description', 'hospital')
    form_columns = ('title', 'description', 'hospital')