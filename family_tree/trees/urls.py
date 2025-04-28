from django.urls import path

from .views import (
    MyTreeList,
    TreeCreate,
    TreeDelete,
    TreeDetail,
    PersonCreate,
    PersonDelete,
    PersonDetail,
    PersonUpdate,
    TreeStructure,
    TreeUpdate,
)

app_name = 'trees'

# пути родословной
urlpatterns = [
    path('list/', MyTreeList.as_view(), name='tree_list'),
    path('create/', TreeCreate.as_view(), name='tree_create'),
    path('<str:slug>/', TreeDetail.as_view(), name='tree_detail'),
    path('<str:slug>/delete/', TreeDelete.as_view(), name='tree_delete'),
    path('<str:slug>/edit/', TreeUpdate.as_view(), name='tree_edit'),
    path('<str:slug>/structure/', TreeStructure.as_view(), name='tree_structure'),

]

# пути членов родословной
urlpatterns += [
    path('<str:slug>/person/<int:id>/', PersonDetail.as_view(), name='person'),
    path('<str:slug>/person/<int:id>/edit/', PersonUpdate.as_view(), name='person_edit'),
    path('<str:slug>/person/<int:id>/delete/', PersonDelete.as_view(), name='person_delete'),
    path('<str:slug>/person/create/', PersonCreate.as_view(), name='person_create'),
]
