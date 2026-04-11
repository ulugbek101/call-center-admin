from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

def leaders_list(request):
    staffs = User.objects.filter(is_active=True, is_activation_code_used=True, is_superuser=False)

    staffs = sorted(staffs, key=lambda staff: staff.current_score, reverse=True)

    context = {
        "staffs": staffs[:10]
    }
    return render(request, "leaders_list.html", context)
