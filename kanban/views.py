from django.shortcuts import render
from kanban.models import TrelloUser, Board, BoardMember, List, Card, Attachment
from users.models import CustomUser
from kanban.serializers import TrelloUserSerializer, BoardSerializer, BoardMemberSerializer, ListSerializer, CardSerializer, AttachmentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

from kanban.helper import update_board_count, get_user_details
from kanban.constants import MAX_FREE_BOARDS

# Create your views here.


class TrelloUserView(APIView):

    def get_object(self, pk):
        try:
            return TrelloUser.objects.get(pk=pk)
        except TrelloUser.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        TrelloUsers = TrelloUser.objects.all()
        serializer = TrelloUserSerializer(TrelloUsers, many=True)

        for key in serializer.data:
            user_id = key["UserID"]
            user = get_user_details(None, user_id)
            key["user"] = user
        return Response(serializer.data)

    def put(self, request, format=None):
        try: 
            pk = request.data["id"]
        except:
            return Response({"error_message": "id is required to update"}, status=status.HTTP_400_BAD_REQUEST)
        trello_user = self.get_object(pk)
        serializer = TrelloUserSerializer(trello_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardView(APIView):

    def get(self, request, format=None):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    # on create board, also create board member mapping and update board count of user who created board

    def post(self, request, format=None):
        user_details = get_user_details(request)
        user_id = user_details["id"]
        try:
            trello_user = TrelloUser.objects.get(UserID__exact=user_id)
            trello_user_serializer = TrelloUserSerializer(trello_user)
            if trello_user_serializer.data["BoardCount"] == MAX_FREE_BOARDS and trello_user_serializer.data["IsPremium"] == False:
                return Response({
                    "error_message": "max board count reached, upgrade to premium for unlimited boards"
                    }, status = 403)

        except TrelloUser.DoesNotExist:
                
            request.data["CreatedBy"] = user_id
            request.data["UserID"] = user_id
            board_serializer = BoardSerializer(data = request.data)

            if board_serializer.is_valid():
                board_serializer.save()
                
                board_member = {
                    "BoardID": board_serializer.data["id"],
                    "UserID": board_serializer.data["CreatedBy"]
                }

                board_member_serializer = BoardMemberSerializer(data = board_member)

                if board_member_serializer.is_valid():
                    board_member_serializer.save()

                    board_count_serializer = update_board_count(request)

                    if board_count_serializer.errors:
                        return Response(board_count_serializer.errors)

                    return Response(board_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(board_member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            return Response(board_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardMemberView(APIView):

    def get(self, request, format=None):
        user_details = get_user_details(request)
        user_id = user_details["id"]
        board_members = BoardMember.objects.filter(UserID=user_id)
        serializer = BoardMemberSerializer(
            board_members, many=True)
        for key in serializer.data:
            board_id = key["BoardID"]
            board = BoardSerializer(Board.objects.get(pk=board_id))
            key["board"] = board.data

        return Response(serializer.data)

class ListView(APIView):
    def get(self, request, format=None):
        board_id = request.query_params.get("BoardID", None)
        lists = List.objects.filter(BoardID=board_id)
        lists_serializer = ListSerializer(lists, many=True)
        for listObj in lists_serializer.data:
            list_id = listObj["id"]
            cards = Card.objects.filter(ListID=list_id)
            cards_serializer = CardSerializer(cards, many=True)
            listObj["cards"] = cards_serializer.data
            
            for card in cards_serializer.data:
                card_id = card["id"]
                attachments = Attachment.objects.filter(CardID=card_id)
                attachments_serializer = AttachmentSerializer(attachments, many=True)
                card["attachments"] = attachments_serializer.data

        return Response(lists_serializer.data)


    def post(self, request, format=None):
        list_serializer = ListSerializer(data=request.data)

        if list_serializer.is_valid():
            list_serializer.save()
            return Response(list_serializer.data, status=status.HTTP_201_CREATED)
        return Response(list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CardView(APIView):

    def get_object(self, pk):
        try:
            return Card.objects.get(pk=pk)
        except Card.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        card_serializer = CardSerializer(data=request.data)

        if card_serializer.is_valid():
            card_serializer.save()
            return Response(card_serializer.data, status=status.HTTP_201_CREATED)
        return Response(card_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            pk = request.data["id"]
        except:
            return Response({"error_message": "id is required to update"}, status=status.HTTP_400_BAD_REQUEST)
        card = self.get_object(pk)
        card_serializer = CardSerializer(
            card, data=request.data, partial=True)
        if card_serializer.is_valid():
            card_serializer.save()
            return Response(card_serializer.data)
        return Response(card_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CardDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            card_serializer = CardSerializer(Card.objects.get(pk=pk))
            return Response(card_serializer.data, status=200)
        except Card.DoesNotExist:
            return Response(status=404)
        

class AttachmentView(APIView):
    def post(self, request, format=None):
        user_details = get_user_details(request)
        user_id = user_details["id"]
        request.data["UploadedBy"] = user_id
        attachment_serializer = AttachmentSerializer(data=request.data)

        if attachment_serializer.is_valid():
            attachment_serializer.save()
            return Response(attachment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(attachment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
