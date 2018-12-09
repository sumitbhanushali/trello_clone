from kanban.serializers import TrelloUserSerializer
from kanban.models import TrelloUser
from users.models import CustomUser
from users.serializers import UserSerializer

def user_exist(user_id):
        try:
            return TrelloUser.objects.get(UserID__exact=user_id)
        except TrelloUser.DoesNotExist:
            return False

def update_board_count(request):
    trello_user = user_exist(request.data["UserID"])
    if trello_user:
        trello_user.BoardCount = trello_user.BoardCount + 1
        serializer = TrelloUserSerializer(
            trello_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

        return serializer
    else:
        request.data["BoardCount"] = 1
        serializer = TrelloUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        return serializer

def get_user_details(request, UserID = None):
    if UserID:
        user = CustomUser.objects.get(pk=UserID)
    else:
        user = CustomUser.objects.get(username__exact=request.user)
    return UserSerializer(user).data
