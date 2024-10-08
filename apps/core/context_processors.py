from apps.kids.models import Child
from apps.users.models import User


def session_child(request):
    child_id = request.session.get("child")
    if child_id:
        session_child = Child.objects.filter(id=child_id).last()
        return {"session_child": session_child}
    else:
        return {}


def children_count(request):
    if request.user.is_authenticated and request.user.type == User.Types.PARENT:
        children_count = Child.objects.filter(parent=request.user).count()
        return {"children_count": children_count}
    else:
        return {}
