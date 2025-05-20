from rest_framework import generics, permissions

from user import serializers


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        The get_object function is used to retrieve the object that this view will
        operate upon. Typically, it uses self.kwargs, which is a dictionary of values
        that are captured from the URLconf and made available to this view.

        :param self: Refer to the current object
        :return: The user object
        :doc-author: Trelent
        """
        return self.request.user
