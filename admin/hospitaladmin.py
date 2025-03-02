from flask_admin.contrib.sqla import ModelView

class HospitalAdmin(ModelView):
    column_list = ('_id', 'jurisdiction', 'board', 'name')
    form_columns = ('jurisdiction', 'board', 'name')