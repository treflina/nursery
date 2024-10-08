from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()


def get_parent_context(function):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect(f"/konto/login/?next={request.path}")

        selected_child = None
        children = None

        if request.user.type == User.Types.PARENT:
            children = request.user.child_set.all()
            selected_child = request.session.get("child")
            if children and not selected_child:
                request.session["child"] = children.first().id
                selected_child = children.first().id

        return function(request, selected_child, children, *args, **kwargs)

    return wrapper
